import os, sys
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
  
  # get necessary variables from the object with leetcode question info
  date, link, question_dict = leetcode_dict["date"].split("-"), leetcode_dict["link"], leetcode_dict["question"]
  year, month, day = int(date[0]), int(date[1]), int(date[2])
  curr_date = datetime(year,month,day)
  question_name = question_dict["title"]
  
  # build out file path
  FILE_PATH = build_file_path(curr_date, question_name)

  

  # write out generated template
  rendered_template = generate_readme(README_PATH, curr_date, link, question_name, question_dict)
  with open(FILE_PATH, "w") as file_writer:
    file_writer.write(rendered_template)

  return rendered_template

def build_file_path(date, question_name):
  dir_name = 'Daily_Challenge/{}/{}/'.format(date.year,date.strftime("%B")) 
  base_filename = '{}.{}'.format(date.day, question_name).replace(" ", "_")
  suffix = '.md'
  return os.path.join(dir_name, base_filename + suffix)
  
if __name__ == '__main__':
  template = main()
  print(template)