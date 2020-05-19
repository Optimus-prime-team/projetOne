import os
import time
import random
import json, csv
import pandas as pd
from selenium import webdriver
from selenium.webdriver import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from termcolor import colored
from pathlib import PureWindowsPath, PurePath, Path


confFile = pd.read_json(PurePath(os.getcwd()+"/config/config.json"))

ELEMENTS = confFile['conf']

USR = ELEMENTS['username']
PWD = ELEMENTS['password']

URL = ELEMENTS['urls']

LOGINPAGE = URL['login']
JOBSPAGE = URL['jobs']



def random_time():
    return random.randrange(1, 5)


def check_exists_by_element(driver, _type, element):
    try:
        if _type == 'css':
            target = driver.find_element_by_css_selector(element)
        elif _type == 'id':
            target = driver.find_element_by_id(element)
        return target.text
    except NoSuchElementException:
        return ""


def login(driver, loginpage):
    driver.get(loginpage)
    time.sleep(random_time())
    driver.find_element_by_id("username").send_keys(USR)
    time.sleep(random_time())
    driver.find_element_by_id("password").send_keys(PWD)
    driver.find_element_by_css_selector(".btn__primary--large").click()
    #driver.find_element_by_css_selector(".secondary-action").click()


def search(driver, jobspage):
    time.sleep(random_time())
    driver.get(jobspage)
    time.sleep(random_time())
    driver.find_element_by_css_selector("[id^='jobs-search-box-keyword-id-ember']").send_keys(ELEMENTS['search']['jobsname'][1])
    time.sleep(random_time())
    driver.find_element_by_css_selector("[id^='jobs-search-box-location-id-ember']").send_keys(ELEMENTS['location']['cityname'][0])
    time.sleep(random_time())
    driver.find_element_by_css_selector(".jobs-search-box__submit-button").click()

def scroll(driver):
    time.sleep(random_time())
    driver.find_element_by_css_selector(".jobs-search-results--is-two-pane").send_keys(Keys.END)
    time.sleep(random_time())

def click_list(driver, jobspage):
    scroll(driver)
    _listLi = driver.find_elements_by_css_selector("ul[itemtype*='schem'] li[id^='ember']") #TODO correct this selector, because it's click on the link when li has a link(s)
    i = 0
    for li in _listLi:
        li.click()
        print(colored(li.text, 'green', attrs=['bold', 'reverse']))
        i += 1
        print(colored("scrap num : {}".format(i), 'red', attrs=['bold', 'reverse', 'blink']))
        time.sleep(random_time())
        generalInfos = check_exists_by_element(driver, "css", ".jobs-details-top-card__content-container")
        print("\n"+generalInfos)
        title = check_exists_by_element(driver, "css", ".jobs-details-top-card__job-title")
        print("\n"+title)
        compagnyName = check_exists_by_element(driver, 'css', ".jobs-details-top-card__company-url")
        print("\n"+compagnyName)
        compagnyLocation = check_exists_by_element(driver, "css", ".jobs-details-top-card__bullet")
        print("\n"+compagnyLocation)
        description = check_exists_by_element(driver, "css", ".jobs-description-content__text")
        #print("\n"+description)
        put_in_csv(generalInfos, title, compagnyName, compagnyLocation, description)


def click_paginate(driver, jobspage):
    scroll(driver)
    time.sleep(random_time())
    pages = driver.find_elements_by_css_selector("li button[aria-label^='Page']")
    totalPages = int(pages[-1].text)
    for i in range(1, totalPages):
        click_list(driver, jobspage)
        time.sleep(random_time())
        li = driver.find_element_by_css_selector("ul li button[aria-label='Page "+str(i+1)+"']")
        scroll(driver)
        time.sleep(random_time())
        hover = ActionChains(driver).move_to_element(li)
        hover.perform()
        print("hover page {}".format(i+1))
        time.sleep(random_time())
        print("click page {}".format(i+1))
        li.click()


def put_in_csv(generalInfos, title, compagnyName, compagnyLocation, description):
    with open(PurePath(os.getcwd()+"/dbscrap/linkedin.csv") , 'a', newline='') as f:
        generalInfos = str(generalInfos)
        title = str(title)
        description = str(description)
        compagnyName = str(compagnyName)
        compagnyLocation = str(compagnyLocation)
        writer = csv.writer(f)
        writer.writerow([generalInfos, title, compagnyName, compagnyLocation, description])


def put_in_json(data):
    with open(PurePath(os.getcwd()+"/dbscrap/linkedin.json"), 'w') as outfile:
        json.dump(data, outfile)


def all_process(driver, loginpage, jobspage):
    login(driver, loginpage)
    search(driver, jobspage)
    #click_list(driver, jobspage)
    click_paginate(driver, jobspage)


start = time.time()
driver = webdriver.Chrome(ChromeDriverManager().install())
all_process(driver, LOGINPAGE, JOBSPAGE)
end = time.time()
print(end-start)



#jobs-search-results--is-two-panel
#driver.execute_script("window.scrollTo(0,document..scrollHeight)")
#element = driver.find_element_by_id("compactfooter-get_app_footer")
#hover = ActionChains(driver).move_to_element(element)
#hover.perform()

#target = driver.find_element_by_css_selector(".jobs-search-results__list")
#driver.execute_script('arguments[0].scrollIntoView(true);', target)


#element = driver.find_element_by_id("compactfooter-get_app_footer")
#hover = ActionChains(driver).move_to_element(element)
#hover.perform()
