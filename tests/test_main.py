from unittest.mock import patch, MagicMock, mock_open

from requests import HTTPError

from exceptions import NoObservablesFoundError
from translator import main

TEST_FILE = 'test_file.xml'
CTR_CLIENT = 'CTR_CLIENT'
CTR_PASSWORD = 'CTR_PASSWORD'


def test_main_success():
    with patch('translator.get_arguments') as get_arguments_mock, \
            patch('translator.get_tr_client') as get_tr_client_mock, \
            patch('translator.extract_observables') as extract_mock, \
            patch('translator.Session') as session_mock, \
            patch('translator.build_bundle') as build_bundle_mock, \
            patch('translator.json.dumps') as json_dumps_mock, \
            patch('translator.print') as print_mock:
        get_arguments_mock.return_value = MagicMock(
            file='/path/' + TEST_FILE,
            source='s', source_uri='su', external_id_prefix='p',
            exclude=['f.com']
        )
        tr_client_mock = MagicMock()
        get_tr_client_mock.return_value = tr_client_mock
        extract_mock.return_value = [
            {'value': 'a.com', 'type': 'domain'},
            {'value': '1.1.1.1', 'type': 'ip'}
        ]
        build_bundle_mock.return_value = MagicMock()
        json_dumps_mock.return_value = 'Expected result'

        main()

        get_arguments_mock.assert_called_once()
        get_tr_client_mock.assert_called_once()
        extract_mock.assert_called_once_with(
            TEST_FILE, tr_client_mock, exclude=['f.com']
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


def test_main_failed_with_authorization_error():
    with patch('translator.get_arguments') as get_arguments_mock, \
            patch('translator.get_tr_client') as get_tr_client_mock, \
            patch('translator.print') as print_mock, \
            patch('builtins.open', mock_open(read_data='data')):
        get_arguments_mock.return_value = MagicMock()
        tr_client_mock = MagicMock()
        tr_client_mock.inspect.inspect = MagicMock(
            side_effect=HTTPError(
                response=MagicMock(
                    status_code=400,
                    json=lambda: {'error': 'invalid_client',
                                  'error_description': 'unknown client',
                                  'error_uri': 'uri'}
                )
            )
        )
        get_tr_client_mock.return_value = tr_client_mock

        main()

        get_arguments_mock.assert_called_once()
        assert print_mock.call_args.args[1].startswith(
            'Failed to connect to Cisco SecureX Threat Response.'
            ' Make sure that your API credentials'
            ' (CTR_CLIENT and CTR_PASSWORD) are valid.'
        )


def test_main_failed_with_no_observables():
    with patch('translator.get_arguments') as get_arguments_mock, \
            patch('translator.get_tr_client') as get_tr_client_mock, \
            patch('translator.extract_observables') as extract_mock, \
            patch('translator.print') as print_mock:
        get_arguments_mock.return_value = MagicMock(
            file='/path/' + TEST_FILE,
            source='s', source_uri='su', external_id_prefix='p',
            exclude=['f.com']
        )
        tr_client_mock = MagicMock()
        get_tr_client_mock.return_value = tr_client_mock
        extract_mock.side_effect = NoObservablesFoundError(TEST_FILE)

        main()

        get_arguments_mock.assert_called_once()
        get_tr_client_mock.assert_called_once()
        extract_mock.assert_called_once_with(
            TEST_FILE, tr_client_mock, exclude=['f.com']
        )
        print_mock.assert_called_once_with(
            'Error occurred: ', f'No observables found in {TEST_FILE}'
        )
