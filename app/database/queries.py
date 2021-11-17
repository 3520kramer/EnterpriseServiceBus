from . import db_connection
# import db_connection

import uuid
from datetime import datetime
import json


def insert(msg):
    query = '''
      INSERT INTO queue_log (uuid, is_consumed, topic, published_time, content_format, content)
      VALUES(%s, %s, %s, %s, %s, %s)
    '''

    msg['content'] = json.dumps(msg['content'])

    query_params = list(msg.values())
    print("query_params", query_params)
    db_connection.query_db(query, query_params)


def update(uuid):  # uuid
    query = '''
      UPDATE queue_log
      SET is_consumed = %s, consumed_time = %s
      WHERE uuid = %s
    '''

    query_params = [1,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    uuid]

    db_connection.query_db(query, query_params)


def get_all():
    query = "SELECT uuid, topic, content_format, content FROM queue_log WHERE is_consumed = 0"

    result = db_connection.query_db(query, None, is_select_query=True)

    return result


def create_publish_message(topic, content_format, content):
    return {
        'uuid':  uuid.uuid4().hex,
        'is_consumed': False,
        'topic': topic,
        'published_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        # 'consumed_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'content_format': content_format,
        'content': 'content'
    }
