import uuid
from datetime import datetime


def create_log_message(msg):
    return {
        'uuid':  uuid.uuid4().hex,
        'is_consumed': False,
        'topic': msg['topic'],
        'published_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'content_format': msg['content_format'],
        'content': msg['content']
    }


def create_publish_message(msg):
    return {
        'uuid':  uuid.uuid4().hex,
        'topic': msg['topic'],
        'content': msg['content']
    }


def get_connect_headers(sid, environ):
    return {
        'topic': environ['HTTP_TOPIC'],
        'output_format': environ['HTTP_OUTPUT_FORMAT'],
        'sid': sid
    }
