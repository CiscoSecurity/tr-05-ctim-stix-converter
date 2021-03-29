from io import StringIO
from collections import namedtuple
from unittest.mock import patch

from pytest import raises, mark

from translator import (
    get_arguments,
    DEFAULT_SOURCE, DEFAULT_SOURCE_URI, DEFAULT_EXTERNAL_ID_PREFIX
)


TEST_FILE = 'test_file.xml'
PYTHON_COMMAND = 'python'


@mark.parametrize(
    'input_,error',
    (
            ([], IndexError),
            (['python'], SystemExit)
    ),
    ids=str,
)
def test_get_arguments_fail(input_, error):
    with patch('argparse._sys.argv', input_), \
         patch('sys.stderr', new=StringIO()):
        with raises(error):
            get_arguments()


def get_arguments_success_test_set():
    input_default = [PYTHON_COMMAND, TEST_FILE]
    output_default = {
        'file': TEST_FILE,
        'source': DEFAULT_SOURCE,
        'source_uri': DEFAULT_SOURCE_URI,
        'external_id_prefix': DEFAULT_EXTERNAL_ID_PREFIX,
        'exclude': None,
    }
    TestData = namedtuple('TestData', 'input output')
    yield TestData(input_default, output_default)
    yield TestData(
        [*input_default, '-s', 's'], {**output_default, 'source': 's'}
    )
    yield TestData(
        [*input_default, '-e', 'a', '-e', 'b'],
        {**output_default, 'exclude': ['a', 'b']}
    )
    yield TestData(
        [
            *input_default,
            '-s', 's', '-u', 'u', '--external_id_prefix', 'p',
            '-e', 'a', '-e', 'b'
        ],
        {
            'file': TEST_FILE,
            'source': 's', 'source_uri': 'u', 'external_id_prefix': 'p',
            'exclude': ['a', 'b'],
        }
    )


@mark.parametrize(
    'test_input,expected',
    get_arguments_success_test_set(),
    ids=str,
)
def test_get_arguments_success(test_input, expected):
    with patch('argparse._sys.argv', test_input):
        result = get_arguments()
        assert vars(result) == expected
