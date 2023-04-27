import os
from datetime import datetime

import jinja2

LEETCODE_BASE_URL = 'https://leetcode.com'

def color_helper(diff):
  if diff == "Easy": return "green"
  elif diff == "Medium": return "yellow"
  elif diff == "Hard": return "red"
  return "white"

class TemplateWriter:
  """Object will handle writing to file
  :param question_name: Name of leetcode (daily?) question
  :type question_name: str
  :param curr_date: current date
  :type curr_date: datetime
  """
  def __init__(
    self,
    question_name: str,
    curr_date: datetime = datetime.now()
  ):
    self.FILE_PATH = self.__build_file_path(question_name, curr_date)
    self.__build_directory(self.FILE_PATH, curr_date.strftime("%B"), curr_date.strftime("%Y")) # build directory if it doesn't exist

  def write_template(
  # def generate_readme(
    self,
    README_PATH,
    curr_date,
    link,
    question_name,
    leetcode_dict,
    explanation = "",
    code_block = ""
  ):
    template = None
    with open(README_PATH, "r", encoding="utf-8") as file:
      template = jinja2.Template(file.read())
    
    # get more indepth information about the question
    # related_topics = next(iter(leetcode_dict["topicTags"]))
    related_topics = leetcode_dict["topicTags"]
    difficulty = leetcode_dict["difficulty"]
    difficulty_color = color_helper(difficulty) 

    final_template = template.render(
      date=curr_date.date().isoformat(),
      question_name=question_name,
      question_name_link=question_name.replace(" ","-"),
      link_to_problem=LEETCODE_BASE_URL+link,
      difficulty=difficulty,
      description=leetcode_dict["content"],
      related_topics=enumerate(related_topics),
      related_topics_len=len(related_topics),
      explanation=explanation,
      code_block=code_block
    )

    with open(self.FILE_PATH, "w", encoding="utf8") as file_writer:
      file_writer.write(final_template)
  
  # build file directory/path
  def __build_file_path(self, question_name: str, date: datetime):
    dir_name = 'Daily_Challenge/{}/{}/'.format(date.year,date.strftime("%B")) 
    base_filename = '{}.{}'.format(date.day, question_name).replace(" ", "_")
    suffix = '.md'
    return os.path.join(dir_name, base_filename + suffix)

  # build directory to file if it does not exist
  def __build_directory(self, file_path: str, month: str, year: str):
    dir_name = ''.join(['Daily_Challenge/',year])
    
    if not os.path.isdir(dir_name): # if year folder doesn't exist, create it 
      os.mkdir(path=dir_name)
    dir_name = f'{dir_name}/{month}'
    
    if not os.path.isdir(dir_name): # if month folder doesn't exist create
      os.mkdir(path=dir_name)
    
    if os.path.isfile(file_path):
      return # file is already generated, exit early
    
    # file is not created, so create empty file
    with open(file_path, "w", encoding="utf8") as file_writer:
      file_writer.write("")
      