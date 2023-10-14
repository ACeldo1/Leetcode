import os

from cgitb import grey
from pprint import pprint

from gql import gql

# hard coded / final path variables needed locally
GRAPHQL_DIR = "src/graphql/{}"
GQL_TEMPLATE, STR_TEMPLATE = "gql_{}", "str_{}"

# class will execute gql files located in graphql file directory
class GraphQLQueries(object):
  """ Responsible for converting .graphql files into usable formats to
  execute queries (for now, only gql and string objects)"""
  def __init__(self):
    def graphql_to_gql(filename: str): # helper method to for loading gql query
      with open(file=GRAPHQL_DIR.format(filename),mode='r',encoding="utf8") as f:
        return gql(f.read())
    def graphql_to_str(filename: str):
      with open(file=GRAPHQL_DIR.format(filename),mode='r',encoding="utf8") as f:
        return f.read()
      
    # load queries from graphql directory
    graphql_files = os.fsencode(GRAPHQL_DIR.format(""))
    for file in os.listdir(graphql_files):
      filename = os.fsdecode(file)
      if filename.endswith(".graphql"):
        # load queries for use with gql libarary
        query_name = filename[0:-8]
        setattr(self, GQL_TEMPLATE.format(query_name), graphql_to_gql(filename))
        # load queries as strings for use with python requsts library
        setattr(self, STR_TEMPLATE.format(query_name), graphql_to_str(filename))

  def get_query_as_str(self, query_name: str):
    """ return requested graphql query as gql object """
    return getattr(self, STR_TEMPLATE.format(query_name))

  def get_query_as_gql(self, query_name: str):
    """ return request graphql query as string """
    return getattr(self, GQL_TEMPLATE.format(query_name))
  
if __name__ == "__main__":
  test = GraphQLQueries()
  
  # print(type(test.get_query_as_str("syncedCode")), ": ", test.get_query_as_str("syncedCode"))
  # print(type(test.get_query_as_gql("syncedCode")), ": ", test.get_query_as_gql("syncedCode"))