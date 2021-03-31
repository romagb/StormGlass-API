from pprint import pformat
import sys
from twisted.internet import reactor
from twisted.internet.defer import Deferred
from twisted.internet.protocol import Protocol
from twisted.web.client import Agent, readBody
from twisted.web.http_headers import Headers

import urlparse
from urllib import urlencode

DEFAULT_LOCATIONS = {
    'Kyiv': {
        'lat': 50.45466,
        'lng': 30.5238,
        'params': ','.join(sys.argv[1:])
    },
    'Lviv': {
        'lat': 49.842957,
        'lng': 24.031111,
        'params': ','.join(sys.argv[1:])
    },
    'Austin': {
        'lat': 30.26666,
        'lng': -97.73333,
        'params': ','.join(sys.argv[1:])
    },
    'New York': {
        'lat': 40.73061,
        'lng': -73.935242,
        'params': ','.join(sys.argv[1:])
    },
    'Paris': {
        'lat': 48.86471,
        'lng': 2.34901,
        'params': ','.join(sys.argv[1:])
    }
}


class BeginningPrinter(Protocol):
    def __init__(self, finished):
        self.finished = finished
        self.remaining = 1024 * 10

    def dataReceived(self, bytes):
        if self.remaining:
            display = bytes[:self.remaining]
            print 'Some data received:'
            print display
            self.remaining -= len(display)

    def connectionLost(self, reason):
        print 'Finished receiving body:', reason.getErrorMessage()
        self.finished.callback(None)


def cbRequest(response):
    print 'Response version:', response.version
    print 'Response code:', response.code
    print 'Response phrase:', response.phrase
    print 'Response headers:'
    print pformat(list(response.headers.getAllRawHeaders()))
    finished = Deferred()
    response.deliverBody(BeginningPrinter(finished))
    return finished


def link_generator(default_link, dictionary):
    url_parts = list(urlparse.urlparse(default_link))
    query = dict(urlparse.parse_qsl(url_parts[3]))
    query.update(dictionary)
    url_parts[4] = urlencode(query)
    url = urlparse.urlunparse(url_parts)
    return url


start_url = 'https://api.stormglass.io/v2/weather/point'
url_list = []
for key in DEFAULT_LOCATIONS:
    url_list.append(link_generator(start_url, DEFAULT_LOCATIONS[key]))

agent = Agent(reactor)
for link in url_list:
    d = agent.request(
        'GET',
        link,
        Headers({'Authorization': ['a14f509c-9211-11eb-a242-0242ac130002-a14f511e-9211-11eb-a242-0242ac130002']}),
        None)
    d.addCallback(cbRequest)

reactor.run()
