from xml.dom import minidom

from api.exceptions import (
    NoObservablesFoundError
)
from api.mappings import Indicator


def convert(args):
    indicators_data = extract_indicators(args['content'])

    return build_bulk(indicators_data)


def extract_observables(content, tr_client, exclude=None):
    exclude = exclude or []

    observables = tr_client.inspect.inspect({'content': content})
    observables = [
        ob for ob in observables if ob['value'] not in exclude
    ]

    if not observables:
        raise NoObservablesFoundError()

    return observables


def build_bulk(indicators_data):
    indicators = []

    for indicator_data in indicators_data:
        indicator = Indicator.map(indicator_data)
        indicators.append(indicator)

    return indicators


def extract_indicators(content):
    tree = minidom.parseString(content)

    indicators_data = []

    indicators = tree.getElementsByTagName('incident:Related_Indicator')

    for indicator in indicators:
        indicator_data = {}

        # get title
        title = indicator.getElementsByTagName('indicator:Title')
        title = title[0].firstChild.nodeValue
        indicator_data['title'] = title

        # get id and start_time
        indicator_object = indicator.getElementsByTagName('stixCommon:Indicator')
        id = indicator_object[0].getAttribute('id')
        start_time = indicator_object[0].getAttribute('timestamp')
        indicator_data['id'] = id
        indicator_data['start_time'] = f'{start_time}Z'

        # get producer
        producer = indicator.getElementsByTagName('stixCommon:Name')
        producer = producer[0].firstChild.nodeValue
        indicator_data['producer'] = producer

        # get description
        description = indicator.getElementsByTagName('indicator:Description')
        description = description[0].firstChild.nodeValue
        indicator_data['description'] = description

        # get confidence
        confidence = indicator.getElementsByTagName('stixCommon:Value')
        if confidence:
            confidence = confidence[0].firstChild.nodeValue
        indicator_data['confidence'] = confidence

        # get types
        indicator_types = indicator.getElementsByTagName('indicator:Type')
        types = []
        for type in indicator_types:
            types.append(type.firstChild.nodeValue)
        indicator_data['indicator_type'] = types

        indicators_data.append(indicator_data)

    return indicators_data
