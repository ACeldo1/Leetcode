# import from official python libraries 
import requests
from requests import PreparedRequest

from abc import ABC, abstractmethod

from cgitb import grey
from pprint import pprint

import json

# third party imports
from bs4 import BeautifulSoup

from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from graphql import DocumentNode

# import classes created in this workspace
from load_queries import GraphQLQueries

# hard coded / final path variables needed locally
# GRAPHQL_PATH = "graphql/{}"
GRAPHQL_PATH = "graphql/{}.graphql"
LANG = "java"

# hard coded / final url variable needed for query execution
LEETCODE_URL = "https://leetcode.com/"
generate_url = lambda url: ''.join([LEETCODE_URL,url])
LEETCODE_GRAPHQL_URL = generate_url("graphql/")
PROBLEMS_URL = generate_url("problems/")
LOGIN_URL = generate_url("accounts/login/")

class LeetBot(ABC):
  """ Abstract class for leetcode scripts / bots, with necessary info for graphql queries
  :param username: Leetcode username
  :type username: str
  :param password: Leetcode password
  :type password: str
  :param gql_query: query as gql object
  :type gql_query: Document
  :param str_query: query as String object
  :type str_query: String
  """
  def __init__(self, str_query: str, gql_query: DocumentNode = None, **kwargs):
    # for gql queries
    # Select your transport with a defined url endpoint
    # transport = AIOHTTPTransport(LEETCODE_GRAPHQL_URL)
    # # Create a GraphQL client using the defined transport
    # self.client = Client(transport=transport,fetch_schema_from_transport=False)
    
    # needed for child bots to execute queries
    self.str_query, self.gql_query = str_query, gql_query

    # come back to mangle attributes into private rather than public, (ex: passwords)
    for key, val in kwargs.items():
      setattr(self, key, val)

  @abstractmethod 
  def run(self):
    pass
    
  def _build_request_data(self, query: str, operation_name: str, variables: dict[str: any]=None):
    return {
      "query": query,
      "variables": variables,
      "operationName": operation_name
    }
  
  def _get_response(self, data: dict[str:any] = None, cookies: dict[str,any] = None):
    session = requests.Session()
    
    request = requests.Request(method="POST", url=LEETCODE_GRAPHQL_URL, json=data, cookies=cookies)
    prep_request = session.prepare_request(request=request)
    
    result = None
    with session.send(prep_request, verify=False) as response:
      result = response.content
    
    session.close()
    return self.__format_byte_response_to_dict(result)

  def __format_byte_response_to_dict(self, response: bytes):
    str_response = response.decode('utf-8')
    json_str_response = json.loads(str_response)
    return json_str_response["data"]
  
  def format_prepped_request(self, request: PreparedRequest, encoding: str =None):
    encoding = encoding or request.utils.get_encoding_from_headers(request.headers)
    body = request.body.decode(encoding) if encoding else '<binary data>'
    headers = '\n'.join(['{}; {}'.format(*hv) for hv in request.headers.items()])
    return f"""\
      {request.method} {request.path_url} HTTP/1.1
      {headers}
      {body}
      """

  # def execute_query_with_gql(self, variables=None):
  #   """same purpose as run() method, but uses the GQL library to execute graphql queries with gql objects.
  #   May not work with all child class / bots as this is experimental
  #   Will not work with graphql queries that require login (session tokens)"""
  #   try: 
  #     result_dict = self.client.execute(document=self.gql_query, variable_values=variables)
  #   except RuntimeError:
  #     print("Failed to execute gql query: {}".format(self.gql_query), RuntimeError)
  #   return result_dict  

class SyncedCodeBot(LeetBot):
  """ Will retrieve synced code from leetcode user session
  :param leetcode_session: Leetcode session token
  :type leetcode_session: string
  """
  def __init__(self, str_query: str, gql_query: DocumentNode=None, leetcode_session=None, **kwargs):
    if leetcode_session is None or not isinstance(leetcode_session, str):
      raise ValueError("leetcode_session must be valid string!")
    
    super().__init__(str_query=str_query, gql_query=gql_query, **kwargs)
    self.cookies = {'LEETCODE_SESSION': leetcode_session}

  def run(self, question_id: int = None, lang: int = None):
    """Execute query to get synced code"""
    if question_id is None or lang is None:
      raise ValueError('Missing one or more parameters for query!')
    if not isinstance(question_id, int) or not isinstance(lang, int):
      raise TypeError('Incorrect type for one or more parameters!')

    variables = {"lang":lang, "questionId":question_id}
    data = self._build_request_data(query=self.str_query, operation_name="syncedCode", variables=variables)
    response = self._get_response(data=data, cookies=self.cookies)
    return response

class QuestionDataBot(LeetBot):
  """Will retrieve question data from leetcode, does not require authentication, sessions, etc.
  :param str_query: graphql query
  :type str_query: str
  :gql_query: graphql query
  :type gql_query: DocumentNode
  """
  def __init__(self, str_query: str, gql_query: DocumentNode = None, **kwargs):
    super().__init__(str_query=str_query, gql_query=gql_query, **kwargs)
  
  def run(self, title_slug: str = None):
    if title_slug is None:
      raise ValueError("Title slug can not be empty!")
    if not isinstance(title_slug, str):
      raise TypeError("Title slug must be a string!")
    
    variables = {"titleSlug":title_slug}
    data = self._build_request_data(query=self.str_query, operation_name="questionData", variables=variables)
    response = self._get_response(data=data)
    return response

# unfinished / untested
class RecentAcSubmissionBot(LeetBot):
  """Will retrieve accepted submissions from question, does not require authentication, sessions, etc.
  :param str_query: graphql query
  :type str_query: str
  :gql_query: graphql query
  :type gql_query: DocumentNode
  """
  def __init__(self, str_query: str, gql_query: DocumentNode, **kwargs):
    super().__init__(str_query, gql_query, **kwargs)
    
  def run(self, username: str = None, limit: int = None):
    if username is None or limit is None:
      raise ValueError("Missing one or more parameters!")
    if not isinstance(username, str) or not isinstance(limit, int):
      raise TypeError("Invalid username or limit parameter!") 
    
    variables = {
      "username": username,
      "limit": limit
    }
    data = self._build_request_data(query=self.str_query, variables=variables, operation_name="recentAcSubmissions")
    response = self._get_response(data=data)
    return response

class QuestionOfTodayBot(LeetBot):
  """ Bot to retrieve daily challenge question and related info."""
  def run(self):
    data = self._build_request_data(query=self.str_query, operation_name="questionOfToday")
    response = self._get_response(data=data)
    return response

# unfinished / untested
class SubmissionBot(LeetBot):
  """Will retrieve submission data from leetcode for a specific question.
  :param str_query: graphql query
  :type str_query: str
  :gql_query: graphql query
  :type gql_query: DocumentNode
  """
  def __init__(self, str_query: str, gql_query: DocumentNode, **kwargs):
    super().__init__(str_query, gql_query, **kwargs)
    
  def run(self, offset: int = None, limit: int = None, last_key: str = None, question_slug: str = None):
    if offset is None or limit is None or last_key is None or question_slug is None:
      raise ValueError("Missing one or more parameters!")
    if not isinstance(offset, int) or not isinstance(limit, int) or not isinstance(last_key, str) or not isinstance(question_slug, str):
      raise TypeError("Incorrect types for one or more parameters")
    
    variables = {
      "offset": offset,
      "limit": limit,
      "lastKey": last_key,
      "questionsSlug": question_slug
    }
    data = self._build_request_data(query=self.str_query, variables=variables, operation_name="Submission")
    response = self._get_response(data=data)
    return response

if __name__ == '__main__':
  username = 'andyceldo1'
  password = 'xxxxxxxxx'
  lc_session = ' '
  graphql_queries = GraphQLQueries()
  # str_q = graphql_queries.get_query_as_str("syncedCode")
  # gql_q = graphql_queries.get_query_as_gql("syncedCode")

  # synced_code_bot = SyncedCodeBot(LEETCODE_SESSION=lc_session, str_query=str_q, gql_query=gql_q, username=username, password=password)
  # synced_code_bot.run(question_id=2403,lang=1)
  
  str_q = graphql_queries.get_query_as_str("questionOfToday")
  question_of_today_bot = QuestionOfTodayBot(str_query=str_q)
  q_daily_data = question_of_today_bot.run()
  print(q_daily_data)


  str_q = graphql_queries.get_query_as_str("questionData")
  title_slug = q_daily_data["activeDailyCodingChallengeQuestion"]["question"]["titleSlug"]  
  question_data_bot = QuestionDataBot(str_query=str_q)
  q_data = question_data_bot.run(title_slug=title_slug)
  print(q_data)