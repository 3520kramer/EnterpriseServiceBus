from database.db import Database
from utilities import helpers
from models.message_queue import MessageQueue
from models.subscriber import Subscriber
import socketio


class MessageQueueCollection:

    def __init__(self, socket) -> None:
        self.queues: dict[str, MessageQueue] = dict()
        self.socket: socketio.AsyncServer = socket
        self.db_connection: Database = Database()

    def __str__(self):
        return str(self.queues)

    def __repr__(self):
        return str(self.queues)

    def create_and_populate_queues(self):
        messages = self.db_connection.get_all()
        
        for message in messages:
            topic = message['topic']

            self.create_queue_if_not_exists(message['topic'])

            self.queues[topic].queue.put_nowait(message)

    def create_queue_if_not_exists(self, topic):
        do_queue_exist = self.queues.get(topic)

        if(not do_queue_exist):
            self.queues[topic] = MessageQueue(
                socket=self.socket, 
                db_connection=self.db_connection
                )

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
        
        # Creates the log message and inserts it in the database
        log_msg = helpers.create_log_message(msg)
        self.db_connection.insert(log_msg)

    async def publish_topic(self, topic):
        queue = self.queues.get(topic)
        await queue.push_messages()
