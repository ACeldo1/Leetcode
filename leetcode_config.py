import os, sys, yaml

CONFIG_PATH = os.getenv("LC_CONFIG", "config.yml")
YAML_KEY_LEETCODE = "leetcode"
YAML_KEY_LC_USERNAME = "username"
YAML_KEY_LC_PASSWORD = "leetcode"

def get_config():

  def check_config_file():
    if not os.path.isfile(CONFIG_PATH):
      sys.exit("Config file is missing!")
    print("Using config file: " + CONFIG_PATH)

  def load_config_object():
    with open(CONFIG_PATH, 'r') as config_yaml:
      config = None
      try:
        config = yaml.safe_load(config_yaml)
      except yaml.YAMLError as exc:
        sys.exit("Invalid config file: config file could not be parsed")
      
      if not config:
        sys.exit("Invalid config: empty file")

    return config
  
  def validate_config(config):
    if YAML_KEY_LEETCODE not in config or not isinstance(YAML_KEY_LEETCODE, dict):
      sys.exit("Invalid config: missing leetcode key")
      
    leetcode = config["leetcode"]
    
    if YAML_KEY_LC_USERNAME not in leetcode or not isinstance(YAML_KEY_LC_USERNAME, str):
      sys.exit("Invalid config: missing leetcode -> username key")

    if YAML_KEY_LC_PASSWORD not in leetcode or not isinstance(YAML_KEY_LC_PASSWORD, str):
      sys.exit("Invalid config: missing leetcode -> password key")

    return config
  
  check_config_file()
  config = load_config_object()
  return validate_config(config)