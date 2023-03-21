from selenium import webdriver
from leetcode_config import check_config

LOGIN_URL = "https://leetcode.com/accounts/login"

def leetcode_login(): 
  driver = webdriver.Chrome()
  leetcode_config = check_config()["leetcode"]
  lc_username, lc_password = leetcode_config["username"], lc_password = leetcode_config["password"]
  
  driver.get(LOGIN_URL)
  driver.find_element_by_id("id_login").send_keys(lc_username)
  driver.find_element_by_id("id_password").send_keys(lc_password)
  driver.find_element_by_id("signin_btn").click()
  
  driver.
  
  