from cgitb import grey
from pprint import pprint

from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

from requests import session
from bs4 import BeautifulSoup

import sys

# from get_signedin_driver import get_signedin_driver

# hard coded / final path variables needed locally
GRAPHQL_PATH = "graphql/{}"
LANG = "java"

# hard coded / final url variable needed for query execution
LEETCODE_URL = "https://leetcode.com/"
generate_url = lambda url: ''.join([LEETCODE_URL,url])
LEETCODE_GRAPHQL_URL = generate_url("graphql/")
PROBLEMS_URL = generate_url("problems/")
LOGIN_URL = generate_url("accounts/login/")

class LeetcodeQueryExecutor(object):
  def __init__(self, **kwargs):
    def load_query(filename):
      with open(GRAPHQL_PATH.format(filename)) as f:
        return gql(f.read())
      
    # Select your transport with a defund url endpoint
    transport = AIOHTTPTransport(LEETCODE_GRAPHQL_URL)
    # transport = AIOHTTPTransport(url=LEETCODE_GRAPHQL_URL)
    # Create a GraphQL client using the defined transport
    self.client = Client(transport=transport,fetch_schema_from_transport=False)
    
    # load all queries
    # self.daily_challenge_query = load_query("daily_challenge_query.graphql")
    # self.leetcode_question_query = load_query("leetcode_question_query.graphql")
    # self.get_question_submissions = load_query("get_question_submissions.graphql")
    # self.get_synced_code_query = load_query("get_synced_code_query.graphql")

    # load all queries
    queries = ["daily_challenge_query.graphql", "leetcode_question_query.graphql", "get_question_submissions.graphql", "get_synced_code_query.graphql"]
    for q in queries:
      setattr(self, q.split(".", maxsplit=1)[0], load_query(q))

    # come back to mangle attributes into private rather than public for lc information
    for key, val in kwargs.items():
      setattr(self, key, val)

  def get_latest_submission(self, problem_id):
    pass

  # automate login to get synced code from asscoiated leetcode account
  def get_synced_code(self, titleSlug, question_id):
    # payload for request
    payload = {
      'action': 'login',
      'username': self.username,
      'password': self.password
    }
    
    # urls for requests
    login_url = LOGIN_URL
    # question_url = PROBLEMS_URL.join([titleSlug,'/'])

    synced_code = ""
    with session() as cookie:
      cookie.post(login_url, data=payload)
      try:
        synced_code_request = cookie.post(LEETCODE_GRAPHQL_URL, json={"query": self.get_synced_code_query})
        synced_code = synced_code_request["syncedCode"]["code"]
      except Exception as e:
        print("synced_code request failed -> {}".format(e))
        sys.exit()
    # synced_code = self.__execute_query(self.get_synced_code_query, {"lang" : LANG})
    return synced_code

  def get_leetcode_dict(self):
    # get daily question data
    daily_question_dict = self.__execute_query(self.daily_challenge_query)

    # get more info about daily challenge question
    title_slug = daily_question_dict["activeDailyCodingChallengeQuestion"]["question"]["titleSlug"]
    leetcode_question_variables = { "titleSlug": title_slug }
    question_dict = self.__execute_query(self.leetcode_question_query, leetcode_question_variables)
    
    return daily_question_dict["activeDailyCodingChallengeQuestion"] | question_dict
  
  # private helper methods

  # generate leetcode dictionary to fill in template
  def __execute_query(self, query, variables=None):
    result_dict = self.client.execute(document=query, variable_values=variables)
    return result_dict

if __name__ == "__main__":
  import leetcode_config
  lc = leetcode_config.get_config()["leetcode"]
  lc_exe = LeetcodeQueryExecutor(username=lc["username"], password=lc["password"]) 
  pprint(lc_exe.get_leetcode_dict())

  # test synced code method
  # pprint(lc_exe.get_synced_code(titleSlug="two-sum", question_id=1))
  pprint(lc_exe.get_synced_code(titleSlug="count-unreachable-pairs-of-nodes-in-an-undirected-graph", question_id=2403))