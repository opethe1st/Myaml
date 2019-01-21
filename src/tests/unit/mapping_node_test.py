import unittest

from myaml.mapping_node import MappingNode
from myaml.scalar_node import ScalarNode


class MappingNodeTestCase(unittest.TestCase):
    pass


class TestFromString(MappingNodeTestCase):

    def test_from_string_string(self):
        string = 'key1: value'
        expectedNode = MappingNode(
            elementsMap={
                ScalarNode(value='key1'): ScalarNode(value='value')
            }
        )
        self.assertEqual(
            MappingNode.from_string(string=string),
            expectedNode
        )


class TestToObject(MappingNodeTestCase):

    def test_to_object(self):
        elementsMap = {ScalarNode(value='key'): ScalarNode(value='value')}
        node = MappingNode(elementsMap=elementsMap)
        expectedObject = {'key': 'value'}
        self.assertEqual(
            node.to_object(),
            expectedObject
        )


class TestFromObject(MappingNodeTestCase):

    def test_from_object(self):
        obj = {'key': 'value'}
        expectedNode = MappingNode(
            elementsMap={
                ScalarNode(value='key'): ScalarNode(value='value')
            }
        )
        self.assertEqual(
            MappingNode.from_object(obj=obj),
            expectedNode
        )


class TestToString(MappingNodeTestCase):

    def test_to_object(self):
        node = MappingNode(
            elementsMap={
                ScalarNode(value='key'): ScalarNode(value='value')
            }
        )
        expectedString = 'key: value\n'
        self.assertEqual(
            node.to_string(),
            expectedString
        )

    def test_to_object_complex(self):
        node = MappingNode(
            elementsMap={
                ScalarNode(value='key1'): ScalarNode(value='value'),
                ScalarNode(value='key'): MappingNode(
                    elementsMap={
                        ScalarNode(value='key1'): ScalarNode(value='value'),
                        ScalarNode(value='key'): MappingNode(
                            elementsMap={
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
            node.to_string(),
            expectedString
        )