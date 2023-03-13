import os, sys, re
from datetime import datetime, timezone
import jinja2

from get_daily_challenge_dict import LeetcodeQueryExecutor as lc_executor
from generate_daily_challenge_template import generate_readme

CONFIG_PATH = os.getenv("RPN_CONFIG", "config.yaml")
README_PATH = os.getenv("README_PATH", "Daily Challenge/README.md")
YAML_KEY_LEETCODE = "leetcode"

def build_file_path(year, month, day, question_name):
  dir_name = 'Daily Challenge/{}/{}/'.format(year,month)
  base_filename = '{}. {}'.format(day, question_name) 
  suffix = '.md'
  return os.path.join(dir_name, base_filename + suffix)
  
if __name__ == '__main__':
  leetcode_dict = lc_executor().get_leetcode_dict() # daily leetcode challenge dict
  
  # get necessary variables
  date_dict, link, question_dict = leetcode_dict["date"], leetcode_dict["link"], leetcode_dict["question"]
  date_data = date_dict["date"].split("-")
  year, month, day = date_data[0], date_data[1], date_data[2]
  curr_date = datetime(year, month, day)
  question_name = question_dict["title"]
  
  # build out file path
  FILE_PATH = build_file_path(year, month, day, question_name)

  # write out generated template
  readme_file = generate_readme(README_PATH, FILE_PATH, curr_date.day, link, question_name, leetcode_dict) 
  
  