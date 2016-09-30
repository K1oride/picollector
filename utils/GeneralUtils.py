'''
Created on Aug 19, 2016

@author: Charlie
'''

import requests
import sys
import string
import exceptions

from utils.style import use_style

def getPage(url):
    return requests.get(url).content

def setRshow(value, set_, show):
    if value == "":
        show()
    else:
        set_(value)
        
def setDownloadPath(path):
    with open("config/path.txt", "w") as f:
        f.write(path)

def showDownloadPath():
    print getDownloadPath()
        
def getDownloadPath():
    with open("config/path.txt", "r") as f:
        return f.readline()

def setDBConfig(string):
    confirm()
    with open("config/db.txt", "w") as f:
        f.write(string)

def showDBConfig():
    with open("config/db.txt", "r") as f:
        print f.read()
                
def confirm():
    c = raw_input("confirm your action(y/n): ")
    c = c.lower()
    if c == 'y':
        return
    else:
        sys.exit(0)
    
def num2bool(bool):
    if bool == 0:
        return False
    else:
        return True

def safeExec(func, *args):
    try:
        return func(*args)
        
    except Exception, e:
        printError(e.message)

def selectByNum(prompt, process, *args):
    r = raw_input(prompt)
    try:
        return process(string.atoi(r), *args)
    except exceptions.ValueError:
        print "invalid input!"
        
def selectRange(prompt1, prompt2, process, *args):
    s = raw_input(prompt1)
    e = raw_input(prompt2)
    try:
        return process(string.atoi(s), string.atoi(e), *args)
    except exceptions.ValueError:
        print "invalid input!"
  
def printWarning(string):
    print use_style(string, fore='red')
    
def printSuccess(string):
    print use_style(string, fore='green')    
    
def printError(string):
    if type(string) == type("string"):
        print use_style("ERROR-" + string, fore='red', back='purple')
    else:
        print use_style("ERROR-" + str(type(string)) , mode='invert', fore='red', back='cyan')
