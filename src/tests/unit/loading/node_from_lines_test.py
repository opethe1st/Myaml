import unittest

from myaml.loading.node_from_lines import node_from_lines
from myaml.loading.line import Line
from myaml.loading.tokenizer import (
    Indent,
    Separator,
    SequenceIndent,
    Value
)
from myaml.core import MappingNode, Node, ScalarNode, SequenceNode


class TestNodeFromLines(unittest.TestCase):

    def test_mapping_node(self):
        node = node_from_lines(lines=[Line(indent=0, tokens=[Value(data='key'), Separator(), Value(data='value')])])
        self.assertEqual(
            node,
            MappingNode(mapping={ScalarNode(data='key'): ScalarNode(data='value')})
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
                mapping={
                    ScalarNode(data='key'): ScalarNode(data='value'),
                    ScalarNode(data='key1'): MappingNode(mapping={ScalarNode(data='key2'): ScalarNode(data='value')}),
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
            SequenceNode(items=[ScalarNode(data='value')])
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
            SequenceNode(items=[ScalarNode(data='value'), ScalarNode(data='value')])
        )

    def test_scalar_node(self):
        node = node_from_lines(
            lines=[
                Line(indent=0, tokens=[Value(data='value')])
            ]
        )
        self.assertEqual(
            node,
            ScalarNode(data='value')
        )
