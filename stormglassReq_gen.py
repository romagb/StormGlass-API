import json
import sys
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks
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


def linkGenerator(default_link, dictionary):
    url_parts = list(urlparse.urlparse(default_link))
    query = dict(urlparse.parse_qsl(url_parts[3]))
    query.update(dictionary)
    url_parts[4] = urlencode(query)
    url = urlparse.urlunparse(url_parts)
    return url


@inlineCallbacks
def reply(tw_agent, urls_list):
    try:
        response = yield tw_agent.request(
            'GET',
            urls_list,
            Headers({'Authorization': ['a14f509c-9211-11eb-a242-0242ac130002-a14f511e-9211-11eb-a242-0242ac130002']}),
            None)
    except Exception, exc:
        print (exc)
    else:
        readReply(response)


@inlineCallbacks
def readReply(reply):
    try:
        reply_obj = yield readBody(reply)
    except Exception, exc:
        print (exc)
    else:
        convertData(reply_obj)


def convertData(body):
    parseData(json.loads(body))


def parseData(convertation_result):
    try:
        modeling_data = convertation_result.get('meta')
        monitoring_data = convertation_result.get('hours')
    except Exception, exc:
        print (exc)
    else:
        writeJson('modeling_data.json', modeling_data)
        writeJson('monitoring_data.json', monitoring_data)


def writeJson(f_name, data):
    with open(f_name, 'a') as data_file:
        json.dump(data, fp=data_file, indent=2, encoding='utf-8')


if __name__ == '__main__':
    start_url = 'https://api.stormglass.io/v2/weather/point'
    agent = Agent(reactor)
    url_list = []
    for key in DEFAULT_LOCATIONS:
        url_list.append(linkGenerator(start_url, DEFAULT_LOCATIONS[key]))

    for link in url_list:
        try:
            reply(agent, link)
        except Exception, exc:
            print (exc)

    reactor.run()
