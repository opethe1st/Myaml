import unittest

from myaml.converters.node_from_lines import node_from_lines
from myaml.converters.utils.line import Line
from myaml.converters.utils.tokenizer import (
    Indent,
    Separator,
    SequenceIndent,
    Value
)
from myaml.core.nodes import MappingNode, Node, ScalarNode, SequenceNode


class TestNodeFromLines(unittest.TestCase):

    def test_mapping_node(self):
        node = node_from_lines(lines=[Line(indent=0, tokens=[Value(data='key'), Separator(), Value(data='value')])])
        self.assertEqual(
            node,
            MappingNode(map_={ScalarNode(value='key'): ScalarNode(value='value')})
        )

    def test_mapping_node_2(self):
        node = node_from_lines(
            lines=[
                Line(
                    indent=0,
                    tokens=[
                        Value(data='key'),
                        Separator(),
                        Value(data='value')
                    ]
                ),
                Line(
                    indent=0,
                    tokens=[
                        Value(data='key1'),
                        Separator(),
                    ]
                ),
                Line(
                    indent=1,
                    tokens=[
                        Value(data='key2'),
                        Separator(),
                        Value(data='value')
                    ]
                ),
            ]
        )
        self.assertEqual(
            node,
            MappingNode(
                map_={
                    ScalarNode(value='key'): ScalarNode(value='value'),
                    ScalarNode(value='key1'): MappingNode(map_={ScalarNode(value='key2'): ScalarNode(value='value')}),
                }
            )
        )

    def test_sequence_node(self):
        node = node_from_lines(
            lines=[
                Line(indent=1, tokens=[SequenceIndent(), Value(data='value')])
            ]
        )
        self.assertEqual(
            node,
            SequenceNode(items=[ScalarNode(value='value')])
        )

    def test_sequence_node_2(self):
        node = node_from_lines(
            lines=[
                Line(indent=1, tokens=[SequenceIndent(), Value(data='value')]),
                Line(indent=1, tokens=[SequenceIndent(), Value(data='value')])
            ]
        )
        self.assertEqual(
            node,
            SequenceNode(items=[ScalarNode(value='value'), ScalarNode(value='value')])
        )

    def test_scalar_node(self):
        node = node_from_lines(
            lines=[
                Line(indent=0, tokens=[Value(data='value')])
            ]
        )
        self.assertEqual(
            node,
            ScalarNode(value='value')
        )
