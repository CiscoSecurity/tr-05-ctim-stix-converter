import os
from unittest.mock import patch, MagicMock

from translator import main

TEST_FILE = 'test_file.xml'
CTR_CLIENT = 'CTR_CLIENT'
CTR_PASSWORD = 'CTR_PASSWORD'


@patch.dict(
    os.environ, {CTR_CLIENT: CTR_CLIENT, CTR_PASSWORD: CTR_PASSWORD}
)
def test_main_no_observables():
    with patch('translator.get_arguments') as get_arguments_mock, \
            patch('translator.ThreatResponse') as tr_mock, \
            patch('translator.extract_observables') as extract_mock, \
            patch('translator.print') as print_mock:
        get_arguments_mock.return_value = MagicMock(
            file='/path/' + TEST_FILE,
            source='s', source_uri='su', external_id_prefix='p',
            exclude=['f.com']
        )
        extract_mock.return_value = []

        main()

        get_arguments_mock.assert_called_once()
        tr_mock.assert_called_once_with(
            client_id=CTR_CLIENT, client_password=CTR_PASSWORD, region='us'
        )
        extract_mock.assert_called_once_with(
            TEST_FILE, tr_mock(), exclude=['f.com']
        )
        print_mock.assert_called_once_with(
            'Error occurred: ', f'No observables found in {TEST_FILE}'
        )


@patch.dict(
    os.environ, {CTR_CLIENT: CTR_CLIENT, CTR_PASSWORD: CTR_PASSWORD}
)
def test_main_success():
    with patch('translator.get_arguments') as get_arguments_mock, \
        patch('translator.ThreatResponse') as tr_mock, \
        patch('translator.extract_observables') as extract_mock, \
        patch('translator.Session') as session_mock, \
        patch('translator.build_bundle') as build_bundle_mock, \
        patch('translator.json.dumps') as json_dumps_mock, \
        patch('translator.print') as print_mock: \

        get_arguments_mock.return_value = MagicMock(
            file='/path/' + TEST_FILE,
            source='s', source_uri='su', external_id_prefix='p',
            exclude=['f.com']
        )
        extract_mock.return_value = [
            {'value': 'a.com', 'type': 'domain'},
            {'value': '1.1.1.1', 'type': 'ip'}
        ]

        build_bundle_mock.return_value = MagicMock()
        json_dumps_mock.return_value = 'Expected result'

        main()

        get_arguments_mock.assert_called_once()
        tr_mock.assert_called_once_with(
            client_id=CTR_CLIENT, client_password=CTR_PASSWORD, region='us'
        )
        extract_mock.assert_called_once_with(
            TEST_FILE, tr_mock(), exclude=['f.com']
        )
        session_mock.assert_called_once_with(
            external_id_prefix='p', source='s', source_uri='su'
        )
        build_bundle_mock.assert_called_once_with(
            [{'value': 'a.com', 'type': 'domain'},
             {'value': '1.1.1.1', 'type': 'ip'}],
            'test_file.xml',
            session_mock()
        )
        print_mock.assert_called_once_with('Expected result')
