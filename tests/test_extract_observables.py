from unittest.mock import patch, mock_open, MagicMock

from translator import extract_observables

TEST_FILE = 'test_file.xml'


def test_extract_observables():
    tr_client_mock = MagicMock()
    tr_client_mock.inspect.inspect = MagicMock(
        return_value=[{'value': 'a', 'type': 't'}, {'value': 'b', 'type': 't'}]
    )

    with patch("builtins.open", mock_open(read_data="data")) as file_mock:
        result = extract_observables(TEST_FILE, tr_client_mock, exclude=['a'])

    file_mock.assert_called_with(TEST_FILE)
    tr_client_mock.inspect.inspect.assert_called_with({'content': 'data'})
    assert result == [{'value': 'b', 'type': 't'}]
