WORK IN PROGRESS.

### What is WAMP?

WAMP is an open WebSocket subprotocol that provides two asynchronous
messaging patterns: RPC and PubSub.

More information: <http://wamp.ws/spec>


Twister implements a subset (Pub/Sub) of WAMP.


### Running

    $ python -m twister
    Twister running on 127.0.0.1:9000


Now you can interact with twister with twister.js

<http://github.com/fatiherikli/twister.js>

### Example

```javascript

var twister = new Twister("ws://localhost:9000/ws");
twister.connect(function () {
    twister.subscribe('articles/23', function (channel, message) {
        console.log(message);
    });

    twister.publish('articles/23', "Hello!");
});
````