import uuid
import json
from collections import defaultdict

from ws4py.websocket import WebSocket

from utils import head, enum, tail, inverse


MESSAGES = enum({
    # http://wamp.ws/spec
    "WELCOME": 0,
    "PREFIX": 1,
    "SUBSCRIBE": 5,
    "UNSUBSCRIBE": 6,
    "PUBLISH": 7,
    "EVENT": 8,
})

PROTOCOL_VERSION = 1
SERVER_IDENT = "twister"


class Channel(list):

    def publish(self, message, exclude=None):
        for client in self:
            if exclude is client:
                continue
            client.send(message)


class Twister(WebSocket):
    channels = defaultdict(Channel)

    def opened(self):
        self.welcome()

    def send(self, payload, binary=False):
        message = json.dumps(payload)
        super(Twister, self).send(message, binary)

    def received_message(self, message):
        message = json.loads(message.data)
        message_type = inverse(MESSAGES, head(message))
        method = getattr(self, message_type.lower(),
                         self.raise_not_implemented)
        method(*tail(message))

    def welcome(self):
        session_id = self.generate_session_id()
        self.send([MESSAGES.WELCOME,
                   session_id,
                   PROTOCOL_VERSION,
                   SERVER_IDENT])

    def publish(self, channel_name, message, exclude_me=False):
        channel = self.channels[channel_name]
        channel.publish([MESSAGES.EVENT, channel_name, message],
                        exclude=self if exclude_me else None)

    def subscribe(self, channel):
        self.channels[channel].append(self)

    def unsubscribe(self, channel):
        self.channels[channel].remove(self)

    def closed(self, code, reason=None):
        for channel in self.channels.itervalues():
            if self in channel:
                channel.remove(self)

    def generate_session_id(self):
        return str(uuid.uuid4())

    def raise_not_implemented(self):
        raise NotImplementedError("Twister supports only the pub/sub "
                                  "implementation of WAMP spec for now.")
