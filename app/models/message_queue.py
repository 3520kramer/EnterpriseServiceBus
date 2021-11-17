from asyncio import Queue
from models.subscriber import Subscriber
from utilities import transformer
from database import queries
import socketio

from utilities.transformer import transform

# https://www.geeksforgeeks.org/python-list-comprehensions-vs-generator-expressions/


class MessageQueue:
    def __init__(self, socket) -> None:
        self.subscribers: list[Subscriber] = []
        self.queue = Queue()
        self.socket: socketio.AsyncServer = socket

    def __str__(self):
        return str(self.subscribers)

    def __repr__(self):
        return str(self.subscribers)

    def find_subscriber_by_sid(self, sid: str):
        find_sub_generator = (
            sub for sub in self.subscribers if sub.sid == sid)
        return next(find_sub_generator, None)

    def add_subscriber(self, subscriber: Subscriber):
        self.subscribers.append(subscriber)

    def remove_subscriber(self, sid: str):
        subscriber = self.find_subscriber_by_sid(sid)
        if subscriber is not None:
            self.subscribers.remove(subscriber)

    async def add_message(self, msg):
        await self.queue.put(msg)

    async def push_messages(self):
        while not self.queue.empty():
            try:
                msg = await self.queue.get()
                output_format = self.subscribers[0].output_format

                transformed_msg = transformer.transform(msg, output_format)
                await self.socket.emit('msg_to_subscriber', transformed_msg['content'], room=self.subscribers[0].sid)
                
                self.queue.task_done()
                queries.update(msg['uuid'])

            except Exception as e:
                print("Subscribe ERROR:", e)