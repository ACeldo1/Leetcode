import os
from datetime import datetime
from pathlib import Path
import jinja2

from backend.utils.url_constants import LEETCODE
# import utils.url_constants as LEETCODE

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
    self,
    README_PATH,
    curr_date,
    link,
    question_name,
    leetcode_dict,
    code_block = "",
    notes = " "
  ):
    template = None
    with open(README_PATH, "r", encoding="utf-8") as file:
      template = jinja2.Template(file.read())
    
    # get more indepth information about the question
    related_topics = leetcode_dict["topicTags"]
    difficulty = leetcode_dict["difficulty"]

    final_template = template.render(
      date=curr_date.date().isoformat(),
      question_name=question_name,
      question_name_link=question_name.replace(" ","-"),
      link_to_problem=LEETCODE+link,
      difficulty=difficulty,
      description=leetcode_dict["content"],
      related_topics=enumerate(related_topics),
      related_topics_len=len(related_topics),
      code_block=code_block,
      notes=notes
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
    daily_challenge_path = Path(__file__).parent.parent.resolve().parent.__str__()
    dir_name = '\\'.join([daily_challenge_path,'Daily_Challenge',year])
    
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
      