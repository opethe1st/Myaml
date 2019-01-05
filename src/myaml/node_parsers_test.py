import pytest

from .node_parsers import KeyParser
from .node_parsers import KeyValueParser


@pytest.fixture
def key_parser():
    return KeyParser()


@pytest.mark.parametrize(
    ('test_input', 'expected_output'),
    [
        ('key: ', 'key'),
        ('key:', 'key'),
    ]
)
def test_consume_returns_the_expected_key(key_parser, test_input, expected_output):
    assert key_parser.consume(line=test_input) == expected_output


@pytest.fixture
def key_value_parser():
    return KeyValueParser()


@pytest.mark.parametrize(
    ('test_input', 'expected_output'),
    [
        ('key: value', ('key', 'value')),
        (' key: value', ('key', 'value')),
        ('   key: value', ('key', 'value')),
    ]
)
def test_consume_returns_the_expected_key_value(key_value_parser, test_input, expected_output):
    assert key_value_parser.consume(line=test_input) == expected_output
