from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common import exceptions
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.action_chains import ActionChains

from pyvirtualdisplay import Display

import csv
import time
import urllib.parse

chrome_driver = None
user_agent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0"


def setupChromedriver():
    chrome_options = Options()

    try:
        pass
        # display = Display(visible=0, size=(1920, 1080))
        # display.start()
    except:
        print("production: Something went wrong while display setup")

    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("window-size=1920x1080")
    chrome_options.add_argument(f"user-agent={user_agent}")

    chrome_options.add_argument("disable-notifications")
    chrome_options.add_experimental_option("detach", True)
    service = Service(ChromeDriverManager().install())
    chrome_driver = webdriver.Chrome(service=service, options=chrome_options)
    chrome_driver.maximize_window()
    chrome_driver.implicitly_wait(35)

    return chrome_driver


def testSetup():
    chrome_options = Options()

    try:
        pass
        # display = Display(visible=0, size=(1920, 1080))
        # display.start()
    except:
        print("production: Something went wrong while display setup")

    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("window-size=1920x1080")
    chrome_options.add_argument(f"user-agent={user_agent}")

    chrome_options.add_argument("disable-notifications")
    # chrome_options.add_experimental_option("detach", True)

    chrome_options.add_experimental_option(
        "debuggerAddress", "localhost:6565")

    service = Service(ChromeDriverManager().install())
    chrome_driver = webdriver.Chrome(service=service, options=chrome_options)
    chrome_driver.maximize_window()
    chrome_driver.implicitly_wait(35)

    return chrome_driver


def readContacts(file_name):
    contacts = set()

    with open(file_name) as contacts_csv:
        temp_contacts = csv.reader(contacts_csv)
        for contact in temp_contacts:
            contacts.add(contact[0])

    return list(contacts)


def sendMessage(chrome_driver, phone_number, message):

    chrome_driver.get(
        f"https://api.whatsapp.com/send?phone=91{phone_number}&text={urllib.parse.quote(message)}")

    continue_btn = chrome_driver.find_element(
        by=By.ID, value='action-button')
    continue_btn.click()

    whatsapp_web = chrome_driver.find_element(
        by=By.XPATH, value='//div[@id="fallback_block"]/div/div/a')
    whatsapp_web.click()

    wait = WebDriverWait(driver=chrome_driver, timeout=35, poll_frequency=3, ignored_exceptions=[
        exceptions.NoSuchElementException
    ])

    send = wait.until(method=expected_conditions.element_to_be_clickable(
        (By.XPATH, '//div[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button[not(@disabled)]')))

    print(send)

    js = 'document.querySelector("#main > footer > div._2BU3P.tm2tP.copyable-area > div > span:nth-child(2) > div > div._2lMWa > div._3HQNh._1Ae7k > button").click()'
    chrome_driver.execute_script(js)
    time.sleep(1)


def makeMessage():
    return "testing"


def main():

    contacts = readContacts("contacts.csv")
    print(contacts)
    # quit()

    chrome_driver = testSetup()

    message = makeMessage()
    for contact in contacts:
        print(f"\n\nsending - {contact}\n")
        sendMessage(chrome_driver, contact, message)

    # chrome_driver.quit()


if __name__ == "__main__":
    main()

