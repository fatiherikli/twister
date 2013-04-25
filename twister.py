from gevent import monkey
monkey.patch_all()

import uuid
import json
import argparse
import collections

from ws4py.server.geventserver import WebSocketWSGIApplication, WSGIServer
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


class Channel(object):
    def __init__(self):
        self.clients = []

    def subscribe(self, client):
        self.clients.append(client)

    def unsubscribe(self, client):
        self.clients.remove(client)

    def publish(self, message):
        for client in self.clients:
            client.send(message)


class Twister(WebSocket):
    channels = collections.defaultdict(Channel)

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

    def publish(self, channel_name, message):
        channel = self.channels[channel_name]
        channel.publish([MESSAGES.EVENT, channel_name, message])

    def subscribe(self, channel):
        self.channels[channel].subscribe(self)

    def unsubscribe(self, channel):
        self.channels[channel].unsubscribe(self)

    def closed(self, code, reason=None):
        for channel in self.channels.itervalues():
            if self in channel.clients:
                channel.unsubscribe(self)

    def generate_session_id(self):
        return str(uuid.uuid4())

    def raise_not_implemented(self):
        raise NotImplementedError("Twister supports only the pub/sub "
                                  "implementation of WAMP spec for now.")

if __name__ == '__main__':
    from ws4py import configure_logger
    configure_logger()

    parser = argparse.ArgumentParser(description='Twister Server')
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('-p', '--port', default=9000, type=int)
    args = parser.parse_args()

    server = WSGIServer((args.host, args.port),
                        WebSocketWSGIApplication(handler_cls=Twister))
    server.serve_forever()
