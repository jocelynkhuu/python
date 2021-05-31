# Script was created to allow auto-launch of chrome browser and auto-login to a website. 
# Will need to create a login.yml

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import yaml

# Create login.yml file and edit the fields as needed
conf = yaml.load(open('/path/to/login.yml'), Loader=yaml.BaseLoader)
mylogin = conf['login_user']['login']
mypassword = conf['login_user']['password']

browser = webdriver.Chrome(executable_path='/path/to/chromedriver')
browser.get(('https://www.websitehere.com'))

# Fill in username and password and hit next button
# Grab element ID by inspecting field 
username = browser.find_element_by_id('username')
username.send_keys(mylogin)
password = browser.find_element_by_id('password')
password.send_keys(mypassword)

signInButton = browser.find_element_by_id('login')
signInButton.click()
