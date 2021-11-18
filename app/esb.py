from aiohttp import web
import socketio
from models.subscriber import Subscriber
from models.message_queue_collection import MessageQueueCollection
from utilities import helpers

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

    # after the log entry has been created the topic will be published
    await message_queues.publish_topic(publish_msg['topic'])


def start(port: int):
    message_queues.create_and_populate_queues()
    print("Initiated queues: ", message_queues)
    web.run_app(app, port=port)


if __name__ == '__main__':
    start(port=10000)