from unittest import TestCase

from myaml.converters.node_from_string import (
    node_from_string,
    mapping_node_from_string,
    scalar_node_from_string,
    sequence_node_from_string,
)
from myaml.core import (
    MappingNode,
    ScalarNode,
    SequenceNode,
)


class TestNodeFromString(TestCase):

    def test_mapping_from_string_string(self):
        string = 'key1: value'
        expectedNode = MappingNode(
            map_={
                ScalarNode(value='key1'): ScalarNode(value='value')
            }
        )
        self.assertEqual(
            node_from_string(string=string),
            expectedNode
        )

    def test_scalar_from_string_string(self):
        value = 'value string'
        expectedNode = ScalarNode(value=value)
        self.assertEqual(
            node_from_string(string=value),
            expectedNode
        )

    def test_sequence_from_string_string(self):
        string = '-   value'
        expectedNode = SequenceNode(
            items=[
                ScalarNode(value='value')
            ]
        )
        self.assertEqual(
            node_from_string(string=string),
            expectedNode
        )
