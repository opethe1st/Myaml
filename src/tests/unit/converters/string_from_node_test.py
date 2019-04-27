import unittest
from functools import singledispatch

from myaml.core import (
    MappingNode,
    ScalarNode,
)
from myaml.converters.string_from_node import string_from_node



class TestStringFromNode(unittest.TestCase):

    def test_to_object(self):
        node = MappingNode(
            map_={
                ScalarNode(value='key'): ScalarNode(value='value')
            }
        )
        expectedString = 'key: value\n'
        self.assertEqual(
            string_from_node(node, indentLevel=0),
            expectedString
        )

    def test_to_object_complex(self):
        node = MappingNode(
            map_={
                ScalarNode(value='key1'): ScalarNode(value='value'),
                ScalarNode(value='key'): MappingNode(
                    map_={
                        ScalarNode(value='key1'): ScalarNode(value='value'),
                        ScalarNode(value='key'): MappingNode(
                            map_={
                                ScalarNode(value='key'): ScalarNode(value='value')
                            }
                        )
                    }
                )
            }
        )
        expectedString = '''key1: value
key:
  key1: value
  key:
    key: value
'''
        self.assertEqual(
            string_from_node(node, indentLevel=0),
            expectedString
        )

    def test_to_object_complex_specify_indent_size(self):
        node = MappingNode(
            map_={
                ScalarNode(value='key1'): ScalarNode(value='value'),
                ScalarNode(value='key'): MappingNode(
                    map_={
                        ScalarNode(value='key1'): ScalarNode(value='value'),
                        ScalarNode(value='key'): MappingNode(
                            map_={
                                ScalarNode(value='key'): ScalarNode(value='value')
                            }
                        )
                    }
                )
            }
        )
        expectedString = '''key1: value
key:
    key1: value
    key:
        key: value
'''
        self.assertEqual(
            string_from_node(node, indentLevel=0, indentSize=4),
            expectedString
        )
