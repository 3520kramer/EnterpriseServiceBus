from models.message_queue import MessageQueue
from models.subscriber import Subscriber
import socketio


class MessageQueueCollection:

    def __init__(self, socket) -> None:
        self.queues: dict[str, MessageQueue] = dict()
        self.socket: socketio.AsyncServer = socket

    def __str__(self):
        return str(self.queues)

    def __repr__(self):
        return str(self.queues)

    def create_and_populate_queues(self, messages):
        for message in messages:
            topic = message['topic']

            self.create_queue_if_not_exists(message['topic'])

            self.queues[topic].queue.put_nowait(message)

    def create_queue_if_not_exists(self, topic):
        do_queue_exist = self.queues.get(topic)

        if(not do_queue_exist):
            self.queues[topic] = MessageQueue(socket=self.socket)

    def add_subscriber(self, subscriber: Subscriber):
        self.create_queue_if_not_exists(subscriber.topic)

        queue = self.queues.get(subscriber.topic)

        queue.add_subscriber(subscriber)

    # Removes the subscriber from the queue(s)
    def remove_subscriber(self, sid: str):
        for queue in self.queues.values():
            queue.remove_subscriber(sid)

    async def add_message(self, msg):
        topic = msg['topic']
        await self.queues[topic].add_message(msg)

    async def publish_topic(self, topic):
        queue = self.queues.get(topic)
        await queue.push_messages()
