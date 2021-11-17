import configparser

config_path = '/Users/kramer/Documents/DAT18b/7_semester/system_integration/mandatory_2/esb/config.ini'
config = configparser.ConfigParser()
config.read(config_path)

def get_offset_id():
  return config.get('options', 'offset_id')

def set_offset_id(new_id):
  return config.set('options', 'offset_id', new_id)

if __name__ == '__main__':
  print("MAIN")