import os, re
import time, datetime
import random
import json, csv
import numpy as np
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

URL = ELEMENTS['urls']['indeed']

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
    driver.find_element_by_css_selector("[id='text-input-what']").send_keys(ELEMENTS['search']['jobsname'][1]) #JOBS NAME
    time.sleep(random_time())
    driver.find_element_by_id("text-input-where").send_keys(Keys.CONTROL + "a")
    driver.find_element_by_css_selector("[id='text-input-where']").send_keys(ELEMENTS['location']['region'][-1]) #CITY
    time.sleep(random_time())
    driver.find_element_by_css_selector(".icl-WhatWhere-button").click()

def scroll(driver):
    time.sleep(random_time())
    driver.find_element_by_css_selector(".jobs-search-results--is-two-pane").send_keys(Keys.END)
    time.sleep(random_time())


def _formatNumbers(element):
    elem = re.findall("\d+", element.replace(" ", ""))
    elem = list(map(int, elem))
    return elem

def elem2Mean(elem):
    elem = _formatNumbers(elem)
    return np.mean(elem)


def click_list(driver, jobspage):
    time.sleep(5)
    _listLi = driver.find_elements_by_css_selector("td[id='resultsCol'] [id^='p']") 
    i = 0
    for li in _listLi:
        li.click()
        time.sleep(random_time())
        print(colored(li.text, 'green', attrs=['bold', 'reverse']))
        i += 1
        print(colored("scrap num : {}".format(i), 'red', attrs=['bold', 'reverse', 'blink']))

        city = check_exists_by_element(driver, "css", ".jobMetadataHeader > div:first-child")
        contrat = check_exists_by_element(driver, "css", ".jobMetadataHeader > div:nth-child(2)")
        salary = check_exists_by_element(driver, "css", ".jobMetadataHeader > div:nth-child(3)")
        postdate = check_exists_by_element(driver, "css", ".date")
        print(colored("city : "+city, 'blue'))
        print(colored("contrat : "+contrat, 'cyan'))
        print(colored("salary : "+salary, 'yellow'))
        print(colored("post data : "+postdate, 'magenta'))
        #time.sleep(random_time())
        title = check_exists_by_element(driver, "id", "vjs-jobtitle")
        print("\n"+title)
        compagnyName = check_exists_by_element(driver, 'id', "vjs-cn")
        print("\n"+compagnyName)
        compagnyLocation = check_exists_by_element(driver, "id", "vjs-loc")
        print("\n"+compagnyLocation)
        description = check_exists_by_element(driver, "id", "vjs-desc")
        print("\n"+description)
        salary = salary if salary == "" else elem2Mean(salary)
        postdate = postdate if postdate == "" else elem2Mean(postdate)
        x = datetime.datetime.now()
        scrapdate = x.strftime("%x")+"-"+x.strftime("%X")
    
        all_inf = [city, contrat, salary,title, compagnyName, compagnyLocation, description, postdate, scrapdate]
        put_in_csv(all_inf)



def detect_paginate(driver, jobspage):
    pagination = check_exists_by_element(driver, "css", ".pagination")
    if pagination != "":
        click_paginate(driver, jobspage)
    else:
        click_list(driver, jobspage)


def click_paginate(driver, jobspage):
    time.sleep(random_time())
    popup = check_exists_by_element(driver, "id", "popover-background")
    i = 0
    while True:
        i += 1
        print(i)
        if i == 2:
            print("COUCOU")
            time.sleep(random_time())
            print("click popup")
            driver.find_element_by_css_selector(".popover-x-button-close").click()
        click_list(driver, jobspage)
        time.sleep(random_time())
        li = check_exists_by_element(driver, "css", "a[aria-label='Suivant']")
        #scroll(driver)
        time.sleep(random_time())
        hover = ActionChains(driver).move_to_element(li)
        hover.perform()
        print(colored("hover page {}".format(i+1), "cyan", attrs=["bold", "reverse"]))
        time.sleep(random_time())
        print(colored("click page {}".format(i+1), "cyan", attrs=["bold", "reverse"]))
        li.click()


def put_in_csv(all_inf):
    inf = [str(i) for i in all_inf]
    with open(PurePath(os.getcwd()+"/dbscrap/indeed3.csv") , 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(inf)


def put_in_json(data):
    with open(PurePath(os.getcwd()+"/dbscrap/indeed.json"), 'w') as outfile:
        json.dump(data, outfile)


def all_process(driver, loginpage, jobspage):
    #login(driver, loginpage)
    search(driver, jobspage)
    detect_paginate(driver, jobspage)
    #click_paginate(driver, jobspage)


start = time.time()
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.maximize_window()
all_process(driver, LOGINPAGE, JOBSPAGE)
end = time.time()
print("\ntook {:.2f}s".format(end-start))



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
