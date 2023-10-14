from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from datetime import datetime
import pickle

from backend.leetcode_config import get_config
from backend.utils.url_constants import LEETCODE, LEETCODE_LOGIN

class LeetcodeSession(object):
  
  def __init__(self):
    try:
      with open("src/backend/pickles/leetcode_session.p", "rb") as cookie:
        self.__leetcode_session = pickle.load(cookie)
    except:
      self.__leetcode_session = None

  def get_leetcode_session_token(self):
    def generate_leetcode_session():
      leetcode_config = get_config()["leetcode"]
      lc_username, lc_password = leetcode_config["username"], leetcode_config["password"]
      
      options = webdriver.ChromeOptions()
      # options.add_experimental_option("detach", True)
      service = ChromeService(executable_path="src/drivers/chromedriver.exe")
      driver = webdriver.Chrome(service=service, options=options)

      driver.get(LEETCODE_LOGIN)
      wait = WebDriverWait(driver, 20)
      
      username_login = wait.until(EC.presence_of_element_located((By.ID, "id_login")))
      username_login.send_keys(lc_username)

      password_login = wait.until(EC.presence_of_element_located((By.ID, "id_password")))
      password_login.send_keys(lc_password)
      
      wait.until(lambda driver: username_login.get_attribute('value') == lc_username and password_login.get_attribute('value') == lc_password)
      signin_button = driver.find_element(By.ID, "signin_btn")
      driver.execute_script("arguments[0].click()", signin_button)

      wait.until(EC.url_changes(LEETCODE) and EC.presence_of_element_located((By.TAG_NAME, 'body')))
      self.__wait_for_cookie(driver, 'LEETCODE_SESSION')
      self.__leetcode_session = driver.get_cookie('LEETCODE_SESSION')
      
      with open("src/backend/pickles/leetcode_session.p", "wb") as writer:
        pickle.dump(self.__leetcode_session, writer)
      
      driver.quit()

    if self.__leetcode_session is None: # we have yet to obtain a cookie
      generate_leetcode_session()
    elif datetime.now().timestamp() > self.__leetcode_session['expiry']: # cookie has expired!
      generate_leetcode_session()
      
    return self.__leetcode_session['value']

  def __wait_for_cookie(self, driver, cookie_name, timeout = 30):
    wait = WebDriverWait(driver, timeout)
    def is_cookie_loaded(driver):
      cookies = driver.get_cookies()
      for cookie in cookies:
        if cookie['name'] == cookie_name:
          return True
      return False
    return wait.until(is_cookie_loaded)

if __name__ == '__main__':
  lc_session_class = LeetcodeSession()
  leetcode_session_token = lc_session_class.get_leetcode_session_token()
  print('leetcode_session: {}'.format(leetcode_session_token))