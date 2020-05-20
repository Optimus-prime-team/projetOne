"""
J'ai du commenter l'import l-16
et rajouter le try excepte l-24

Le reste du code est identique sauf le dernier bloc qui est variable
cf (IF NICO vs IF FAKHRE) l-296 - l-315

"""


import os, re
import time, datetime
import random
import json, csv
import numpy as np
import pandas as pd
from datetime import timedelta
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from termcolor import colored
from pathlib import PureWindowsPath, PurePath, Path
import mongo_indeed as bdd

try :
    confFile = pd.read_json(PurePath(os.getcwd()+"/config/config.json"))
except :
    confFile = pd.read_json("C:/Users/MonOrdiPro/Desktop/projetOne/config/config.json")


ELEMENTS = confFile['conf']

URL = ELEMENTS['urls']['indeed']

LOGINPAGE = URL['login']
JOBSPAGE = URL['jobs']

# 0-> developpeur | 1 -> data scientist | 2 -> data analyst | 3 -> business intelligence
job_querry = ELEMENTS['search']['jobsname'][-1]

# 0 -> Paris | 1 -> Lyon | 2 -> Toulouse | 3 -> Nantes | 4 -> Bordeaux
city_querry = ELEMENTS['location']['region'][-1]



""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""
return random int between 1 to 5
"""
def random_time():
    return 2


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
    elem = list(map(int, element))
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

def detectSalary(element, driver):
    element = element.replace(" ", "")
    salary = re.findall("\d+(?=€)", element)
    salaryInDom = check_exists_by_element(driver, "css", ".jobMetadataHeader > div:nth-child(3)") 
    return salary, salaryInDom

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
    driver.find_element_by_css_selector("[id='text-input-what']").send_keys(job_querry) #JOBS NAME
    time.sleep(random_time())
    driver.find_element_by_id("text-input-where").send_keys(Keys.CONTROL + "a")
    driver.find_element_by_css_selector("[id='text-input-where']").send_keys(city_querry) #CITY
    time.sleep(random_time())
    driver.find_element_by_css_selector(".icl-WhatWhere-button").click()


def click_list(driver, jobspage):
    cols = ['city', 'contrat', 'salary','title', 'compagnyName', 
        'description', 'postdate', 'overOneMounth', 'job_querry', 'city_querry']
    df = pd.DataFrame(columns = cols)
    time.sleep(2)
    _listLi = driver.find_elements_by_css_selector("td[id='resultsCol'] [id^='p']") #TODO change this variable's name 
    i = 0
    for li in _listLi:
        li.click()
        time.sleep(random_time())
        #print(colored(li.text, 'green', attrs=['bold', 'reverse']))
        i += 1
        #print(colored("scrap num : {}".format(i), 'red', attrs=['bold', 'reverse', 'blink']))
        metaDataHeader = check_exists_by_element(driver, "css", ".jobMetadataHeader") #ICI pour detecter le salaire dans cette div
        city = check_exists_by_element(driver, "css", ".jobMetadataHeader > div:first-child")
        contrat = check_exists_by_element(driver, "css", ".jobMetadataHeader > div:nth-child(2)") #ICI a corriger
        contrat = "" if len(checkNumbers(contrat)) > 0 else contrat
        salary, salaryInDom = detectSalary(metaDataHeader, driver)
        postdate = check_exists_by_element(driver, "css", "div[id='vjs-footer'] > div:first-child .date")
        #print(colored("city : "+city, 'blue'))
        #print(colored("contrat : "+contrat, 'cyan'))
        #print(colored("salary : "+salaryInDom, 'yellow'))
        #print(colored("post data : "+postdate, 'magenta'))
        time.sleep(random_time())
        
        
        title = check_exists_by_element(driver, "id", "vjs-jobtitle")
        #print("\n"+title)
        compagnyName = check_exists_by_element(driver, 'id', "vjs-cn")
        #print("\n"+compagnyName)
        description = check_exists_by_element(driver, "id", "vjs-desc")
        #print("\n"+description)
        salary = "" if salary == [] else _salary(elem2Mean(salary))

        #print(colored(salary, 'red'))
        overOneMounth = 1 if str(postdate).find("plus de") != -1 else 0
        postDate = getPostDate(postdate)
        scrapDate = dateformat(postDate, 1)
        postDate = dateformat(postDate, 2)
        #all_inf = [city, contrat, salary, title, compagnyName, description, postDate, scrapDate, overOneMounth]
        all_inf = pd.DataFrame([[city, contrat, salary,title, compagnyName, 
                             description, postdate, overOneMounth, job_querry, city_querry]], columns=cols)


        df = df.append(all_inf)
    bdd.save_offers(df)
        
        #put_in_csv(all_inf)
        #put_in_json(all_inf)


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
    with open(PurePath(os.getcwd()+"/dbscrap/indeed3.csv") , 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(inf)


def put_in_json(all_inf):
    dictOfWords = { i : 5 for i in all_inf } #TODO finish this funciton
    with open(PurePath(os.getcwd()+"/dbscrap/indeed.json"), 'w') as outfile:
        json.dump(all_inf, outfile)



def all_process(driver, loginpage, jobspage):
    #login(driver, loginpage)
    search(driver, jobspage)
    detect_paginate(driver, jobspage)




try:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    path = 'C:/Users/MonOrdiPro/Desktop/ScrapFinal-master/chromedriver.exe'

    driver = webdriver.Chrome(path, chrome_options=chrome_options)
except:
    from webdriver_manager.chrome import ChromeDriverManager
    driver = webdriver.Chrome(ChromeDriverManager().install())

start = time.time()
driver.maximize_window()
all_process(driver, LOGINPAGE, JOBSPAGE)
end = time.time()
print("\ntook {:.2f}s".format(end-start))
