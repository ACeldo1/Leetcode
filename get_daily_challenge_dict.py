from cgitb import grey
from pprint import pprint
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

GRAPHQL_PATH = "graphql/"

class LeetcodeQueryExecutor(object):
  def __init__(self):
    def load_query(path):
      with open(path) as f:
        return gql(f.read())
      
    # Select your transport with a defund url endpoint
    transport = AIOHTTPTransport(url="https://leetcode.com/graphql/")
    # Create a GraphQL client using the defined transport
    self.client = Client(transport=transport,fetch_schema_from_transport=False)
    
    # load all queries
    self.daily_challenge_query = load_query("daily_challenge_query.graphql")
    self.leetcode_question_query = load_query("leetcode_question_query.graphql")
    self.leetcode_question_query = load_query("get_question_submission.graphql")

  def get_latest_submission(self, problem_id):
    pass

  # generate leetcode dictionary to fill in template
  def __execute_query(self, query, variables=None):
    result_dict = self.client.execute(document=GRAPHQL_PATH+query, variable_values=variables)
    return result_dict

  def get_leetcode_dict(self):
    # get daily question data
    daily_question_dict = self.__execute_query(self.daily_challenge_query)

    # get more info about daily challenge question
    title_slug = daily_question_dict["activeDailyCodingChallengeQuestion"]["question"]["titleSlug"]
    leetcode_question_variables = { "titleSlug": title_slug }
    question_dict = self.__execute_query(self.leetcode_question_query, leetcode_question_variables)
    
    return daily_question_dict["activeDailyCodingChallengeQuestion"] | question_dict
  
if __name__ == "__main__":
  pprint(LeetcodeQueryExecutor().get_leetcode_dict())