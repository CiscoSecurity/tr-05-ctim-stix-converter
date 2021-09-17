from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

from bundlebuilder.exceptions import ValidationError, SchemaError
from pytest import raises, mark
from requests.exceptions import (
    ConnectionError,
    Timeout as TimeoutError,
    HTTPError
)

from api.exceptions import BundleBuilderError
from api.exceptions import (
    NoObservablesFoundError
)
from api.converter import build_bulk, extract_observables, convert

CONTENT = 'data'


def test_convert():
    with patch('api.converter.extract_observables') as extract_mock, \
            patch('api.converter.Session') as session_mock, \
            patch('api.converter.build_bundle') as build_bundle_mock:
        args = {
            'content': CONTENT, 'source': 's', 'source_uri': 'su',
            'external_id_prefix': 'p', 'exclude': ['f.com'], 'title': 't'
        }
        tr_client_mock = MagicMock()
        extract_mock.return_value = [
            {'value': 'a.com', 'type': 'domain'},
            {'value': '1.1.1.1', 'type': 'ip'}
        ]
        build_bundle_mock.return_value = 'Bundle'

        result = convert(args, tr_client_mock)

        assert result == 'Bundle'
        extract_mock.assert_called_once_with(
            CONTENT, tr_client_mock, exclude=['f.com']
        )
        session_mock.assert_called_once_with(
            external_id_prefix='p', source='s', source_uri='su'
        )
        build_bundle_mock.assert_called_once_with(
            [{'value': 'a.com', 'type': 'domain'},
             {'value': '1.1.1.1', 'type': 'ip'}],
            session_mock(),
            {'title': 't', 'source': 's',
             'source_uri': 'su', 'external_id_prefix': 'p'}
        )


def test_extract_observables_success():
    tr_client_mock = MagicMock()
    tr_client_mock.inspect.inspect = MagicMock(
        return_value=[{'value': 'a', 'type': 't'}, {'value': 'b', 'type': 't'}]
    )

    result = extract_observables(CONTENT, tr_client_mock, exclude=['a'])

    tr_client_mock.inspect.inspect.assert_called_with({'content': CONTENT})
    assert result == [{'value': 'b', 'type': 't'}]


def test_extract_observables_no_observables_found():
    tr_client_mock = MagicMock()
    tr_client_mock.inspect.inspect = MagicMock(
        return_value=[{'value': 'a', 'type': 't'}]
    )

    with raises(NoObservablesFoundError):
        extract_observables(CONTENT, tr_client_mock, exclude=['a'])

    tr_client_mock.inspect.inspect.assert_called_with({'content': CONTENT})


@mark.parametrize(
    'error', (TimeoutError, ConnectionError, HTTPError), ids=str(),
)
def test_extract_observables_tr_communication_failed(error):
    tr_client_mock = MagicMock()
    tr_client_mock.inspect.inspect = MagicMock(side_effect=error())

    with raises(error):
        extract_observables(CONTENT, tr_client_mock)

    tr_client_mock.inspect.inspect.assert_called_with({'content': CONTENT})


EXPECTED_BUNDLE = {
    'external_ids': [
        'ctim-bundle-builder-bundle-6278ac188151f76261bae1'
        '40f463ef7168804b3035c28a46969b1df55e753591'
    ],
    'indicators': [
        {
            'confidence': 'High',
            'external_ids': [
                'ctim-bundle-builder-indicator-53f8288fd13e5c42a'
                'bea3ea45b8f6705109a68da402bbcd8b22bc32b45f82116'
            ],
            'producer': 'CTIM-STIX Converter',
            'schema_version': '1.0.17',
            'source': 'SecureX Threat Response CTIM Bundle Builder',
            'source_uri':
                'https://github.com/CiscoSecurity/tr-05-ctim-bundle-builder',
            'title': 'Generated with CTIM-STIX Converter',
            'type': 'indicator'
        }
    ],
    'relationships': [
        {
            'external_ids': [
                'ctim-bundle-builder-relationship-6b7c20ef47b2c7'
                '7fc6b8963384b437a1ace32fbb2e43f80ab49c36db9044f9b7'
            ],
            'relationship_type': 'member-of',
            'schema_version': '1.0.17',
            'short_description': 'Sighting is member-of Indicator',
            'source': 'SecureX Threat Response CTIM Bundle Builder',
            'source_uri':
                'https://github.com/CiscoSecurity/tr-05-ctim-bundle-builder',
            'type': 'relationship'
        }
    ],
    'schema_version': '1.0.17',
    'sightings': [
        {
            'confidence': 'High',
            'count': 1,
            'external_ids': [
                'ctim-bundle-builder-sighting-c517a944964dc8b926'
                '83bbff5343054fcdfa0e242d81bdf38efc7075513dcf3a',
                'ctim-bundle-builder-sighting-5856bf0654957d0df6'
                '7de631d39bfbc18c3086347d46b1bc9663d35dd4697ed7'
            ],
            'internal': False,
            'observables': [
                {
                    'type': 'domain',
                    'value': 'a.com'
                },
                {
                    'type': 'ip',
                    'value': '1.1.1.1'
                }
            ],
            'schema_version': '1.0.17',
            'source': 'SecureX Threat Response CTIM Bundle Builder',
            'source_uri':
                'https://github.com/CiscoSecurity/tr-05-ctim-bundle-builder',
            'title': 'Generated with CTIM-STIX Converter',
            'type': 'sighting'
        }
    ],
    'source': 'SecureX Threat Response CTIM Bundle Builder',
    'source_uri': 'https://github.com/CiscoSecurity/tr-05-ctim-bundle-builder',
    'type': 'bundle'
}

DEFAULT_ARGS = {
    'indicator': {'title': 'Generated with CTIM-STIX Converter',
                  'confidence': 'High', 'producer': 'CTIM-STIX Converter'},
    'source': 'CTIM-STIX Converter',
    'sighting': {'title': 'Generated with CTIM-STIX Converter',
                 'confidence': 'High', 'internal': False, 'count': 1},
    'source_uri':
        'https://github.com/CiscoSecurity/tr-05-ctim-stix-translator',
    'external_id_prefix': 'ctim-stix-converter'}


def check_and_pop_time(entity, time_field_name, start_time, end_time=None):
    if end_time is None:
        end_time = start_time
    assert entity[time_field_name]['start_time'].startswith(
        start_time.isoformat(timespec='minutes')
    )
    assert entity.pop(time_field_name)['end_time'].startswith(
        end_time.isoformat(timespec='minutes')
    )


def check_and_pop_id(entity):
    assert entity.pop('id').startswith(
        f'transient:ctim-bundle-builder-{entity["type"]}-')


def test_build_bundle():
    start_time = datetime.now()
    session_ = MagicMock()

    result = build_bundle(
        [
            {'value': 'a.com', 'type': 'domain'},
            {'value': '1.1.1.1', 'type': 'ip'},
        ],
        session_,
        args=DEFAULT_ARGS
    )
    result = result.json

    check_and_pop_id(result)
    check_and_pop_id(result['relationships'][0])
    assert result['sightings'][0]['id'] == result['relationships'][0].pop(
        'source_ref')
    assert result['indicators'][0]['id'] == result['relationships'][0].pop(
        'target_ref')
    check_and_pop_id(result['sightings'][0])
    check_and_pop_time(result['sightings'][0], 'observed_time', start_time)
    check_and_pop_id(result['indicators'][0])
    check_and_pop_time(
        result['indicators'][0], 'valid_time',
        start_time, start_time + timedelta(30)
    )
    assert result == EXPECTED_BUNDLE


@mark.parametrize(
    'error', (ValidationError, SchemaError), ids=str(),
)
def test_build_bundle_failed(error):
    session_ = MagicMock()
    with patch('api.converter.Sighting') as sighting_mock:
        sighting_mock.side_effect = error()

        with raises(BundleBuilderError):
            build_bundle([{'value': 'a.com', 'type': 'domain'}], session_)
