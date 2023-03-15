import os, sys, re
from datetime import datetime, timezone
import jinja2
import shutil

from get_daily_challenge_dict import LeetcodeQueryExecutor as lc_executor
from generate_daily_challenge_template import generate_readme

CONFIG_PATH = os.getenv("RPN_CONFIG", "config.yaml")
README_PATH = os.getenv("README_PATH", "Daily_Challenge/README.md")
YAML_KEY_LEETCODE = "leetcode"

def main():
  # get leetcode information 
  leetcode_dict = lc_executor().get_leetcode_dict() 
  
  # get necessary variables
  date, link, question_dict = leetcode_dict["date"].split("-"), leetcode_dict["link"], leetcode_dict["question"]
  year, month, day = int(date[0]), int(date[1]), int(date[2])
  curr_date = datetime(year,month,day)
  question_name = question_dict["title"]
  
  # build out file path
  # FILE_PATH = r'{build_file_path(year, month, day, question_name)}'
  cloned_file_list = build_file_path(curr_date, question_name)
  FILE_DIR, FILE_PATH = cloned_file_list[0], cloned_file_list[1]
  
  # clone file now that we have both file paths
  shutil.copyfile(README_PATH,FILE_DIR)

  # rename cloned file
  os.rename(FILE_DIR+"/README.md",FILE_PATH)

  # write out generated template
  readme_file = generate_readme(FILE_PATH, curr_date, link, question_name, leetcode_dict)
  
  return readme_file

def build_file_path(date, question_name):
  dir_name = 'Daily_Challenge/{}/{}'.format(date.year,date.strftime("%B")) 
  base_filename = '{}.{}'.format(date.day, question_name).replace(" ", "_")
  suffix = '.md'
  return [dir_name, os.path.join(dir_name+'/', base_filename + suffix)]
  
if __name__ == '__main__':
  template = main()
  print(template)
  # leetcode_dict = lc_executor().get_leetcode_dict() # daily leetcode challenge dict
  
  # # get necessary variables
  # date_dict, link, question_dict = leetcode_dict["date"], leetcode_dict["link"], leetcode_dict["question"]
  # date_data = date_dict["date"].splitdate, year, month, day = date_data[0], date_data[1], date_data[2]
  # curr_date = datetime(year, month, day)
  # question_name = question_dict["title
  # FILE_PATH = build_file_path(year,date. month,date.strftime("%B"), question_name)

  # # write out date.generated template
  # readme_file = generate_readme(FILE_PATH, curr_date.day, link, question_name, leetcode_dict) 
  
  