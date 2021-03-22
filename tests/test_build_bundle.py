from datetime import datetime, timedelta
from unittest.mock import MagicMock

from translator import build_bundle

TEST_FILE = 'test_file.xml'

EXPECTED_RESULT = {
    'external_ids': [
        'ctim-bundle-builder-bundle-6278ac188151f76261bae1'
        '40f463ef7168804b3035c28a46969b1df55e753591'
    ],
    'indicators': [
        {
            'confidence': 'High',
            'external_ids': [
                'ctim-bundle-builder-indicator-88a4ad9e43757ec'
                '70f338dfc953aeefdb23f64c57967f47405d31bb0932fd462'
            ],
            'producer': 'CTIM-STIX Translator',
            'schema_version': '1.0.17',
            'source': 'Threat Response CTIM Bundle Builder',
            'source_uri':
                'https://github.com/CiscoSecurity/tr-05-ctim-bundle-builder',
            'title': 'Found in test_file.xml',
            'type': 'indicator'
        }
    ],
    'relationships': [
        {
            'external_ids': [
                'ctim-bundle-builder-relationship-cef20b4addbbc18a7385a0b3ffb9'
                '848805efc0d8294dc064485221efc7fef668'
            ],
            'relationship_type': 'member-of',
            'schema_version': '1.0.17',
            'short_description': 'Sighting is member-of Indicator',
            'source': 'Threat Response CTIM Bundle Builder',
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
                'ctim-bundle-builder-sighting-1291694389eba6e71a9874cce1d9a01'
                '86dff9288b4a62042027c4073c41c4164',
                'ctim-bundle-builder-sighting-f9cce66af5669180a88d8277e58b'
                'b58103d2a49e618e34ce49bdbf570fa0ddf3'
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
            'source': 'Threat Response CTIM Bundle Builder',
            'source_uri':
                'https://github.com/CiscoSecurity/tr-05-ctim-bundle-builder',
            'title': 'Found in test_file.xml',
            'type': 'sighting'
        }
    ],
    'source': 'Threat Response CTIM Bundle Builder',
    'source_uri': 'https://github.com/CiscoSecurity/tr-05-ctim-bundle-builder',
    'type': 'bundle'
}


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
            {'value': '1.1.1.1', 'type': 'ip'}
        ],
        TEST_FILE, session_
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

    assert result == EXPECTED_RESULT
