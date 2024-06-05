import express from "express"
import {spawn} from "child_process"
import cron from "node-cron"
import mailer from "nodemailer"
import dotenv from "dotenv"

const app = express();
dotenv.config();

function sendMail(body){
    console.log("Sending Email")
    const transporter = mailer.createTransport({
        service: "Gmail",
        auth: {
            user: process.env.USER,
            pass: process.env.PASS
        }
    });
    const mail = {
        from: "UCF Dining Hall Monitor",
        to: process.env.RECIPIENT,
        subject: "Daily Meal",
        text: body
    }
    transporter.sendMail(mail, (error, response)=>{
        if(error){
            console.log(error);
        }
        transporter.close();
    });
}


const executePython = async (script) => {
    const py = spawn("python", [script]);

    const result = await new Promise((resolve,reject)=>{
        let output ="";
        py.stdout.on('data',(data)=>{
            output+=data.toString();
        })
        py.stderr.on('data',(data)=>{
            console.error(`Python error occured ${data}`);
            reject(`Error occured in ${script}`)
        })
        py.on("exit",()=>{
            resolve(output);
        })
    })
    return result;

};

app.listen(3000,(req,res)=>{
    cron.schedule('0 0 7 * * *', async () => {
        try {
            const result = await executePython('scrapper.py');
            sendMail(result);
        }catch(error){
            console.log(error);
        }
      });
});