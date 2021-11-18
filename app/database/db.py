import mysql.connector
from utilities import helpers
import json
from datetime import datetime

class Database():
    def __init__(self):
        self.db_config = helpers.get_db_config()

    def insert(self, msg):
      query = '''
        INSERT INTO queue_log (uuid, is_consumed, topic, published_time, content_format, content)
        VALUES(%s, %s, %s, %s, %s, %s)
      '''

      msg['content'] = json.dumps(msg['content'])

      query_params = list(msg.values())
      print("query_params", query_params)
      self.__query_db(query, query_params)


    def update(self, uuid):  # uuid
        query = '''
          UPDATE queue_log
          SET is_consumed = %s, consumed_time = %s
          WHERE uuid = %s
        '''

        query_params = [1,
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        uuid]

        self.__query_db(query, query_params)


    def get_all(self):
        query = "SELECT uuid, topic, content_format, content FROM queue_log WHERE is_consumed = 0"

        result = self.__query_db(query, None, is_select_query=True)

        return result

    def __query_db(self, query: str, query_params, is_select_query=False):
        try:
            db = mysql.connector.connect(**self.db_config)

            if is_select_query:
                cursor = db.cursor(dictionary=True)
            else:
                cursor = db.cursor(prepared=True)

            cursor.execute(query, query_params)

            if(is_select_query):
                return cursor.fetchall()

            db.commit()
        except mysql.connector.Error as error:
            print(f'Query failed:\n{error}')
        finally:
            if db.is_connected():
                cursor.close()
                db.close()
