import pytest

from .yaml_parser import Parser
from .node_types import NodeTypes


class ParserTestCase:

    def setup_method(self, method):
        self.parser = Parser()


class TestConsume(ParserTestCase):
    pass


class TestGetNodeType(ParserTestCase):

    @pytest.mark.parametrize(
        'test_input, expected_output', [
            ('key: ', NodeTypes.KEY),
            ('key: value', NodeTypes.KEY_VALUE),
            # ('- key', NodeTypes.ARRAY_ELEMENT),
        ]
    )
    def test_that_the_correct_not_type(self, test_input, expected_output):
        assert self.parser._get_node_type(line=test_input) == expected_output
