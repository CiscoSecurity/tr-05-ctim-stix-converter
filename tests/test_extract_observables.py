from unittest.mock import patch, mock_open, MagicMock

from pytest import raises, mark

from exceptions import NoObservablesFoundError, FailedToReadFileError, TRError
from translator import extract_observables
from requests.exceptions import (
    ConnectionError,
    Timeout as TimeoutError,
    HTTPError
)

TEST_FILE = 'test_file.xml'


def test_extract_observables():
    tr_client_mock = MagicMock()
    tr_client_mock.inspect.inspect = MagicMock(
        return_value=[{'value': 'a', 'type': 't'}, {'value': 'b', 'type': 't'}]
    )

    with patch('builtins.open', mock_open(read_data='data')) as file_mock:
        result = extract_observables(TEST_FILE, tr_client_mock, exclude=['a'])

    file_mock.assert_called_with(TEST_FILE)
    tr_client_mock.inspect.inspect.assert_called_with({'content': 'data'})
    assert result == [{'value': 'b', 'type': 't'}]


def test_extract_observables_no_observables_found():
    tr_client_mock = MagicMock()
    tr_client_mock.inspect.inspect = MagicMock(
        return_value=[{'value': 'a', 'type': 't'}]
    )

    with raises(NoObservablesFoundError):
        with patch('builtins.open', mock_open(read_data='data')) as file_mock:
            extract_observables(TEST_FILE, tr_client_mock, exclude=['a'])

    file_mock.assert_called_with(TEST_FILE)
    tr_client_mock.inspect.inspect.assert_called_with({'content': 'data'})


@mark.parametrize(
    'error', (FileNotFoundError, IsADirectoryError, IOError), ids=str(),
)
def test_extract_observables_failed_to_read_file(error):
    tr_client_mock = MagicMock()
    with patch('builtins.open') as file_mock:
        file_mock.side_effect = error()

        with raises(FailedToReadFileError):
            extract_observables(TEST_FILE, tr_client_mock)

    file_mock.assert_called_with(TEST_FILE)


@mark.parametrize(
    'error', (TimeoutError, ConnectionError, HTTPError), ids=str(),
)
def test_extract_observables_tr_communication_failed(error):
    tr_client_mock = MagicMock()
    tr_client_mock.inspect.inspect = MagicMock(side_effect=error())
    with patch('builtins.open', mock_open(read_data='data')) as file_mock:

        with raises(TRError):
            extract_observables(TEST_FILE, tr_client_mock)

    file_mock.assert_called_with(TEST_FILE)
    tr_client_mock.inspect.inspect.assert_called_with({'content': 'data'})
