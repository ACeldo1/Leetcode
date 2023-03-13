import get_daily_challenge_dict as gdcd
import os, sys, re
from datetime import datetime
import jinja2

def generate_readme(
  README_PATH,
  FILE_PATH,
  curr_date,
  link,
  question_name,
  leetcode_dict
):
  with open(README_PATH, "r", encoding="utf-8") as file:
    template = jinja2.Template(file.read())
  
  # get more indepth information about the question
  

  return template.render(
    day=day,
    title=question_name,
    link_to_problem=link
    difficulty=leetcode_dict["difficulty"],
    description=leetcode_dict["content"],
    test_cases=leetcode_dict["exampleTestCases"],
    explanation="",
    code_block=""
  )