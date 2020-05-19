import os, re
import time, datetime
import random
import json, csv
import numpy as np
import pandas as pd
from datetime import timedelta
from selenium import webdriver
from selenium.webdriver import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from termcolor import colored
from pathlib import PureWindowsPath, PurePath, Path


confFile = pd.read_json(PurePath(os.getcwd()+"/config/config.json"))

ELEMENTS = confFile['conf']

URL = ELEMENTS['urls']['indeed']

LOGINPAGE = URL['login']
JOBSPAGE = URL['jobs']


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""
return random int between 1 to 5
"""
def random_time():
    return random.randrange(1, 5)


"""
param element = str element

return array with only digits in element and concat numbers
"""
def checkNumbers(element):
    elem = re.findall("\d+", element.replace(" ", ""))
    return elem


"""
param element = arr element

return array of int
"""
def _formatNumbers(element):
    elem = checkNumbers(element)
    elem = list(map(int, elem))
    return elem



"""
param elem = arr elem

return mean of elem
"""
def elem2Mean(elem):
    elem = _formatNumbers(elem)
    return np.mean(elem)



"""
param salary = int salary

convert day's/mounth's salary to year salary
"""

def _salary(salary):
    salary = str(int(salary))
    
    if len(salary) == 5: # 40000
        return int(salary) #euro
    if len(salary) == 4: # 4000
        return int(salary)*12 #euro *30
    if len(salary) == 3: # 400
        return int(salary)*30*12 #euro * 30 * 12


"""
param el = element in post datetime

return string element | int element
"""
def getPostDate(el):
    
    if "Publiée à l'instant".find(str(el)) != -1 or "Aujourd'hui".find(str(el)) != -1:
        return el
    else:
        return int(re.findall("\d+",el)[0])



"""
param days     = datetime()
param position = 1 is actual date, 2 is the post date

return date format 05/12/20-11:31:19

"""
def dateformat(days, position):
    now = datetime.datetime.now()
    if "Publiée à l'instant".find(str(days)) != -1 or "Aujourd'hui".find(str(days)) != -1:
        return now.strftime("%x")+"-"+now.strftime("%X")
    if position == 1:
        return now.strftime("%x")+"-"+now.strftime("%X")
    elif position == 2:
        postdate = now - timedelta(days=days)
        return postdate.strftime("%x")




"""
param driver   = driver
param _type    = "id" | "css"
param element  = element selected


return text element or empty string
"""

def check_exists_by_element(driver, _type, element):
    try:
        if _type == 'css':
            target = driver.find_element_by_css_selector(element)
        elif _type == 'id':
            target = driver.find_element_by_id(element)
        return target.text
    except NoSuchElementException:
        return ""



""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#############################SELENIUM CODE####################################


""" #uncomment if u want to log to u'r accout #feature not done
def login(driver, loginpage):
    driver.get(loginpage)
    time.sleep(random_time())
    driver.find_element_by_id("username").send_keys(USR)
    time.sleep(random_time())
    driver.find_element_by_id("password").send_keys(PWD)
    driver.find_element_by_css_selector(".btn__primary--large").click()
    #driver.find_element_by_css_selector(".secondary-action").click()
"""

def search(driver, jobspage):
    time.sleep(random_time())
    driver.get(jobspage)
    time.sleep(random_time())
    driver.find_element_by_css_selector("[id='text-input-what']").send_keys(ELEMENTS['search']['jobsname'][1]) #JOBS NAME
    time.sleep(random_time())
    driver.find_element_by_id("text-input-where").send_keys(Keys.CONTROL + "a")
    driver.find_element_by_css_selector("[id='text-input-where']").send_keys(ELEMENTS['location']['region'][0]) #CITY
    time.sleep(random_time())
    driver.find_element_by_css_selector(".icl-WhatWhere-button").click()


def click_list(driver, jobspage):
    time.sleep(5)
    _listLi = driver.find_elements_by_css_selector("td[id='resultsCol'] [id^='p']") #TODO change this variable's name 
    i = 0
    for li in _listLi:
        li.click()
        time.sleep(random_time())
        print(colored(li.text, 'green', attrs=['bold', 'reverse']))
        i += 1
        print(colored("scrap num : {}".format(i), 'red', attrs=['bold', 'reverse', 'blink']))
        city = check_exists_by_element(driver, "css", ".jobMetadataHeader > div:first-child")
        contrat = check_exists_by_element(driver, "css", ".jobMetadataHeader > div:nth-child(2)")
        contrat = "" if len(checkNumbers(contrat)) > 0 else contrat
        salary = check_exists_by_element(driver, "css", ".jobMetadataHeader > div:nth-child(3)")
        postdate = check_exists_by_element(driver, "css", "div[id='vjs-footer'] > div:first-child .date")
        print(colored("city : "+city, 'blue'))
        print(colored("contrat : "+contrat, 'cyan'))
        print(colored("salary : "+salary, 'yellow'))
        print(colored("post data : "+postdate, 'magenta'))
        time.sleep(random_time())
        
        
        title = check_exists_by_element(driver, "id", "vjs-jobtitle")
        print("\n"+title)
        compagnyName = check_exists_by_element(driver, 'id', "vjs-cn")
        print("\n"+compagnyName)
        description = check_exists_by_element(driver, "id", "vjs-desc")
        print("\n"+description)
        salary = salary if salary == "" else _salary(elem2Mean(salary))
        print(colored(salary, 'red'))
        overOneMounth = 1 if str(postdate).find("plus de") != -1 else 0
        postDate = getPostDate(postdate)
        scrapDate = dateformat(postDate, 1)
        postDate = dateformat(postDate, 2)
        all_inf = [city, contrat, salary, title, compagnyName, description, postDate, scrapDate, overOneMounth]
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
        if i == 2: #Dans le cas ou une popup pop
            print("COUCOU")
            time.sleep(random_time())
            print("click close popup")
            driver.find_element_by_css_selector(".popover-x-button-close").click()
        click_list(driver, jobspage)
        time.sleep(random_time())
        li = driver.find_element_by_css_selector("a[aria-label='Suivant']")
        #scroll(driver)
        time.sleep(random_time())
        hover = ActionChains(driver).move_to_element(li)
        hover.perform()
        print(colored("hover page {}".format(i+1), "cyan", attrs=["bold", "reverse"]))
        time.sleep(random_time())
        print(colored("click page {}".format(i+1), "cyan", attrs=["bold", "reverse"]))
        li.click()


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""



def put_in_csv(all_inf):
    inf = [str(i) for i in all_inf]
    with open(PurePath(os.getcwd()+"/dbscrap/indeed.csv") , 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(inf)


def put_in_json(data):
    with open(PurePath(os.getcwd()+"/dbscrap/indeed.json"), 'w') as outfile:
        json.dump(data, outfile)



def all_process(driver, loginpage, jobspage):
    #login(driver, loginpage)
    search(driver, jobspage)
    detect_paginate(driver, jobspage)


start = time.time()
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.maximize_window() #full size window (we won't open a new browser tab on each click)
all_process(driver, LOGINPAGE, JOBSPAGE)
end = time.time()
print("\ntook {:.2f}s".format(end-start))
