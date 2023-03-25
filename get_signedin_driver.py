from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from leetcode_config import get_config

LEETCODE_URL = "https://leetcode.com/problemset/all/"
LOGIN_URL = "https://leetcode.com/accounts/login"

def get_signedin_driver(lc_query_executor, question_id):
  driver = webdriver.Chrome()
  leetcode_config = get_config()["leetcode"]
  lc_username, lc_password = leetcode_config["username"], lc_password = leetcode_config["password"]
  
  driver.get(LOGIN_URL)
  driver.find_element(By.ID, "id_login").send_keys(lc_username)
  driver.find_element(By.ID, "id_password").send_keys(lc_password)
  driver.find_element(By.ID, "signin_btn").click() 
  
  driver.get(LEETCODE_URL)
  return driver