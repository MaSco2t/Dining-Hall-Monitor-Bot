# The Imports ------------------------------ 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import chrome 

import time
from datetime import datetime 

# Useful Functions ------------------------------ 
def clearPopUps(driver):
    pop_up_1_exit = driver.find_element(By.CSS_SELECTOR, ".sc-hmdomO button[aria-label='Close']")
    pop_up_1_exit.click()
    pop_up_2_exit = driver.find_element(By.CSS_SELECTOR, "#onetrust-accept-btn-handler")
    pop_up_2_exit.click()

def getMeal(meal,driver):
    select=""
    option=""
    match meal:
        case "breakfast":
            option="0"
            select="2"
        case "brunch":
            option="1"
            select="2"
        case "lunch":
            option="1"
            select="3"
        case "week-dinner":
            option="2"
            select="4"
        case "weekend-dinner":
            option="3"
            select="3"
    
    menu_selector = driver.find_element(By.CSS_SELECTOR,".DateMealFilterButton div")
    driver.execute_script("arguments[0].click();", menu_selector)

    menu_selector_toggle = driver.find_element(By.CSS_SELECTOR, ".css-geczwp-indicatorContainer")
    menu_selector_toggle.click()

    meal_button = driver.find_element(By.CSS_SELECTOR,"#react-select-"+select+"-option-"+option)
    meal_button.click()

    done_button = driver.find_element(By.CSS_SELECTOR,".Done");
    done_button.click()
    time.sleep(4)
    print(meal.upper()+" --------------------")
    print()
    print_meal_options(driver)
    time.sleep(1)

def print_meal_options(driver):
    menu_categories = driver.find_elements(By.CSS_SELECTOR, ".MenuStation_no-categories")
    for category in menu_categories:
        section_name = category.find_element(By.CSS_SELECTOR, ".StationHeader")
        print(section_name.text.title()+":")
        menu_item_names = category.find_elements(By.CSS_SELECTOR, ".HeaderItemName")
        for item_name in menu_item_names:
            if item_name.text != "":
                print("\t"+item_name.text)
    print()

# The Main Code ------------------------------ 
if __name__ == "__main__":

    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    driver.get("https://ucf.campusdish.com/en/locationsandmenus/63south//")
    driver.implicitly_wait(10)

    clearPopUps(driver)

    now = datetime.now()
    weekday = now.weekday()

    print("Good Morning! Here are today's meal plan options!\n")
    if (weekday!=5 and weekday!=6):
        #Sometimes the webpage refreshes after the first load when it has been interacted with, so this try...except statement baits that out.
        try:
            getMeal("breakfast",driver)
        except:
            getMeal("breakfast",driver)
        finally:
            getMeal("lunch",driver)
            getMeal("week-dinner",driver)   
    else:
        try:
            getMeal("brunch",driver)
        except:
            getMeal("brunch",driver)
        finally:
            getMeal("weekend-dinner",driver)