import os
from datetime import datetime

from backend.leetcode_config import get_config
from backend.generate_daily_challenge_template import TemplateWriter
from backend.load_queries import GraphQLQueries
import backend.bots as bots
from graphql import DocumentNode

from backend.get_leetcode_session import LeetcodeSession

CONFIG_PATH = os.getenv("LC_CONFIG", "config.yaml")
README_PATH = os.getenv("README_PATH", "Daily_Challenge/README.md")

# all functions will be using the requests import, although 
# bots will have functionality with the gql library

# return data of daily leetcode challenge
def get_daily_question_data(q_today_query: str, q_data_query: str):
  q_of_today_bot = bots.QuestionOfTodayBot(str_query=q_today_query)
  daily_question_data = q_of_today_bot.run()
  title_slug = daily_question_data["activeDailyCodingChallengeQuestion"]["question"]["titleSlug"]

  q_data_bot = bots.QuestionDataBot(str_query=q_data_query)
  more_question_data = q_data_bot.run(title_slug=title_slug)
  
  return daily_question_data["activeDailyCodingChallengeQuestion"] | more_question_data 

def get_synced_code(synced_code_query: str, lc_session: str, question_id: int, lang: int):
  synced_code_bot = bots.SyncedCodeBot(str_query=synced_code_query, leetcode_session=lc_session)
  synced_code_data = synced_code_bot.run(question_id=question_id, lang=lang)
  synced_code = ""
  try:
    synced_code = synced_code_data["syncedCode"]["code"]
  except TypeError:
    print("Have not attempted daily challenge yet!")
  return synced_code

def build_file_path(date: datetime, question_name: str):
  dir_name = 'Daily_Challenge/{}/{}/'.format(date.year,date.strftime("%B")) 
  base_filename = '{}.{}'.format(date.day, question_name).replace(" ", "_")
  suffix = '.md'
  return os.path.join(dir_name, base_filename + suffix)

def get_question_notes(synced_code_query: str, lc_session: str, title_slug: str):
  question_note_bot = bots.QuestionNoteBot(str_query=synced_code_query, leetcode_session=lc_session)
  question_note_data = question_note_bot.run(title_slug=title_slug)
  return question_note_data["question"]["note"]

def generate_daily_challenge_markdown():
  # check config files first
  lc_config = get_config()
  
  # create leetcode executor class
  lc = lc_config["leetcode"]
  language = int(lc["language"])

  # load queries to be executed
  graphql_queries = GraphQLQueries()
  
  # get dictionary filled with daily question data
  daily_question_data = get_daily_question_data(graphql_queries.get_query_as_str("questionOfToday"), graphql_queries.get_query_as_str("questionData"))
  
  # date based on retrieved data
  q_date = daily_question_data["date"].split("-")
  year, month, day = int(q_date[0]), int(q_date[1]), int(q_date[2])
  curr_date = datetime(year,month,day)
  
  # create variables for useful info to get synced code and more
  link, question_data = daily_question_data["link"], daily_question_data["question"]
  question_name = question_data["title"]
  question_id = int(question_data["questionId"])
  question_title_slug = question_data["titleSlug"]
  
  # get synced code for daily question
  lc_session = LeetcodeSession().get_leetcode_session_token()
  synced_code = get_synced_code(graphql_queries.get_query_as_str("syncedCode"), lc_session, question_id, language)
  question_notes = get_question_notes(graphql_queries.get_query_as_str("questionNote"), lc_session, question_title_slug)

  # build out file path to build template and write out generated template
  # FILE_PATH = build_file_path(curr_date, question_name)
  template_writer = TemplateWriter(question_name, curr_date)
  template_writer.write_template(
    README_PATH,
    curr_date,
    link,
    question_name,
    question_data,
    code_block=synced_code,
    notes = question_notes
  )

if __name__ == '__main__':
  generate_daily_challenge_markdown()