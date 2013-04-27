from gevent import monkey
monkey.patch_all()

from ws4py.server.geventserver import WebSocketWSGIApplication, WSGIServer
from twister import Twister


def main():
    import argparse
    from ws4py import configure_logger

    configure_logger()

    parser = argparse.ArgumentParser(description='Twister Server')
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('-p', '--port', default=9000, type=int)
    args = parser.parse_args()

    server = WSGIServer((args.host, args.port),
                        WebSocketWSGIApplication(handler_cls=Twister))

    print "Twister running on %s:%s" % (args.host, args.port)

    server.serve_forever()


main()