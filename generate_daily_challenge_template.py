from datetime import datetime
import jinja2

LEETCODE_BASE_URL = 'https://leetcode.com'

def generate_readme(
  FILE_PATH,
  curr_date,
  link,
  question_name,
  leetcode_dict
):
  with open(FILE_PATH, "r", encoding="utf-8") as file:
    template = jinja2.Template(file.read())
  
  # get more indepth information about the question
  
  return template.render(
    date=curr_date.date().isoformat(),
    question_name=question_name,
    question_name_link=question_name.replace(" ","-"),
    link_to_problem=LEETCODE_BASE_URL+link,
    difficulty=leetcode_dict["difficulty"],
    description=leetcode_dict["content"],
    test_cases=leetcode_dict["exampleTestcases"],
    explanation="",
    code_block=""
  )