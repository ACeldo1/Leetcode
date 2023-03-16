from datetime import datetime
import jinja2

LEETCODE_BASE_URL = 'https://leetcode.com'

def color_helper(diff):
  if diff == "Easy": return "green"
  elif diff == "Medium": return "yellow"
  elif diff == "Hard": return "red"
  return "white"

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
  # related_topics = next(iter(leetcode_dict["topicTags"]))
  related_topics = leetcode_dict["topicTags"]
  difficulty = leetcode_dict["difficulty"]
  difficulty_color = color_helper(difficulty) 

  return template.render(
    date=curr_date.date().isoformat(),
    question_name=question_name,
    question_name_link=question_name.replace(" ","-"),
    link_to_problem=LEETCODE_BASE_URL+link,
    difficulty=difficulty,
    difficulty_color=difficulty_color,
    description=leetcode_dict["content"],
    related_topics=enumerate(related_topics),
    related_topics_len=len(related_topics),
    explanation="",
    code_block=""
  )