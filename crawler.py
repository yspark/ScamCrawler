from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC  # available since 2.26.0

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from selenium import *
import sys, traceback
import random
import os
import time
from datetime import datetime
from datetime import timedelta

from pyvirtualdisplay import Display



accountList = []
passwdList = []

def loadAccount():
  file = open('BestRecovery Users.csv')
  
  for line in file.readlines():
    if not line: break
    
    ele = line.strip().split(',')
    
    if ele[1] == 'User': continue
    
    accountList.append(ele[1])
    passwdList.append(ele[2])
#enddef
  

def sendKeyToElement(inputType, category, targetCategory, inputText, flagOptional=False):
  xpath = "//%s[@%s='%s']" % (inputType, category, targetCategory)

  try:
      inputElement = WebDriverWait(driver, 10).until(lambda driver : driver.find_element_by_xpath(xpath))
  except TimeoutException:
      if flagOptional == False:
        traceback.print_exc(file=sys.stdout)
        sys.exit()
  else:
      inputElement.send_keys(inputText)
#enddef


def clickElement(inputType, category, categoryValue, flagOptional=False, flagContains=False):
  if flagContains == False:
    xpath = "//%s[@%s='%s']" % (inputType, category, categoryValue)
  else:
    xpath = "//%s[contains(@%s, '%s')]" % (inputType, category, categoryValue)

  try:
      inputElement = WebDriverWait(driver, 10).until(lambda driver : driver.find_element_by_xpath(xpath))
  except TimeoutException:
      if flagOptional == False:
        traceback.print_exc(file=sys.stdout)
        sys.exit()
  else:
      inputElement.click()
#enddef


def appendField(text, field):
  text = text + '\"' + field + '\", '
  
  return text
#enddef

def appendNewline(text):
  text = text + '\n'
  
  return text
#enddef



def outputTable(account, passwd):

  pageCount = 0 
  
  siteLogsLink = siteLogs + '?p=' + str(pageCount)
    
  outputText = ''
  counter = 0

  validCounter = 0    
        
  while True:  
 
    driver.get(siteLogsLink)

    time.sleep(3)

    tbodyList = driver.find_elements_by_xpath('//tbody')
           

    if len(tbodyList) <= 1:
      break

    print counter, len(tbodyList)
  
    # select tbody
    tbody = tbodyList[counter]
  
    # discard garbage tr
    if "DELETE" in tbody.text: 
      if validCounter > 0:
        validCounter = 0
        counter = 0
        pageCount += 1
        siteLogsLink = siteLogs + '?p=' + str(pageCount)
        continue
      else:
        break
      #endif
    #endif
    
    # extract td
    tds = tbody.find_elements_by_tag_name('td')    

    outputText = appendField(outputText, account)
    outputText = appendField(outputText, passwd)
        
    for td in tds:
      outputText = appendField(outputText, td.text)      
    #endfor
      
    # get contents
    contentLink = tbody.find_element_by_tag_name('a')
    if contentLink:                    
      driver.get(contentLink.get_attribute('href'))
     
      time.sleep(3)
 
      textarea = driver.find_element_by_tag_name('textarea')
      outputText = appendField(outputText, repr(textarea.get_attribute('value')))      
    #endif
         
    # newline 
    outputText = appendNewline(outputText)
    
    
    counter += 1
    validCounter += 1
  #endwhile
      
      
  return outputText
#enddef
  

  
####################################################################

display = Display(visible=0, size=(1024, 768))
display.start()


file = open('scamlog.csv', 'w')

siteMain = 'http://privaterecovery.net/br/Login.php'
siteLogs = 'http://privaterecovery.net/br/Check_Logs.php'


loadAccount()

file.write('"Account", "Passwd", "Serial", "PCNAME", "NOTE", "IP", "COUNTRY", "DATE", "TIME", "CONTENTS"\n')


for i in range(len(accountList)):
  account = accountList[i]
  passwd = passwdList[i]

  #account = 'golden22'
  #passwd = 'greatgod'

  if account == '': continue

  print i, account, passwd

  driver = webdriver.Firefox()

  # login
  driver.get(siteMain)
  
  sendKeyToElement("input", "name", "user", account) 
  sendKeyToElement("input", "name", "pass", passwd) 

  clickElement("input", "name", "Login")
  
  
  # check log
  driver.get(siteLogs)
  
  outputText = outputTable(account, passwd)

  file.write(outputText)
  
  # logout
  driver.quit()
    
#endfor


close(file)




      
