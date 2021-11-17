from aiohttp import web
import asyncio
import socketio
from models.subscriber import Subscriber
from models.message_queue_collection import MessageQueueCollection
from utilities import helpers, transformer
from database import queries

# https://medium.com/@joel.barmettler/how-to-upload-your-python-package-to-pypi-65edc5fe9c56

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)

message_queues = MessageQueueCollection(socket=sio)


@sio.event
async def connect(sid, environ):
    print('connect ', sid)


@sio.event
def disconnect(sid):
    print('disconnect ', sid)
    message_queues.remove_subscriber(sid)
    print('Queues after disconnect', message_queues)


@sio.on('subscribe')
async def handle_subscription(sid, data):
    # Add the session id to the data dict
    data['sid'] = sid

    # Creates a subscriber and adds them to a queue
    subscriber = Subscriber(**data)
    message_queues.add_subscriber(subscriber)
    print('Queues after new subcriber', message_queues)

    # Publish the topic for the subscriber
    await message_queues.publish_topic(subscriber.topic)


@sio.on('publish')
async def handle_published_msg(sid, data):
    print('message ', data)

    # Map incoming data to a publish message
    publish_msg = helpers.create_publish_message(data)

    # Create the queue for the topic if it doesn't exist
    message_queues.create_queue_if_not_exists(publish_msg['topic'])

    # Place the message in the queue for the topic
    await message_queues.add_message(publish_msg)

    # Create the log message and insert it in the database
    log_msg = helpers.create_log_message(data)
    queries.insert(log_msg)

    # after the log entry has been created the topic will be published
    await message_queues.publish_topic(publish_msg['topic'])


def start():
    messages = queries.get_all()
    message_queues.create_and_populate_queues(messages)
    print("Initiated queues: ", message_queues)

    web.run_app(app, port=10000)


if __name__ == '__main__':
    start()


# @sio.event
# async def connect(sid, environ):
#     print('connect ', sid)

#     # If a subscriber connects
#     if environ.get('HTTP_TYPE') == 'subscriber':
#         # Gets the header information from the connect request
#         connect_headers = helpers.get_connect_headers(sid, environ)

#         # Creates a subscriber and adds them to a queue
#         subscriber = Subscriber(**connect_headers)
#         message_queues.add_subscriber(subscriber)

#         #
#         await message_queues.publish_topic(subscriber.topic)
#     print('Queues after connect', message_queues)


# @sio.on('subscribe')
# async def handle_subscribtion(sid, data):
#     print("data", data)
#     queue_name = data['queue']
#     # create_queue_if_not_exists(queue_name)

#     queue = message_queues[queue_name]

#     while True:
#         try:
#             print('Waiting for element in queue')
#             msg = await queue.get()
#             print('Found queued element - Sending....')

#             content = msg['content']
#             input_format = msg['content_format']  # json
#             output_format = data['output_format']

#             transformed = transformer.transform(
#                 content, input_format, output_format)

#             await sio.emit('msg_to_subscriber', transformed, room=sid)

#             print('Sent the element...')

#             queries.update(msg['uuid'])

#         except Exception as e:
#             print("Subscribe ERROR:", e)
#         finally:
#             queue.task_done()

#messages = log.get_messages_from_log()
#new_queues = queue.create_and_populate_queues(messages)
# message_queues.update(new_queues)


# msg['is_consumed'] = True
# msg['datetime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# log.append_to_log_file(msg)

# def create_queue_if_not_exists(queue_name):
#     do_queue_exist = message_queues.get(queue_name)
#     if(not do_queue_exist):
#         message_queues[queue_name] = asyncio.Queue()
#     return
