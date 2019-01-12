import unittest

from .nodes import MappingNode
from .nodes import ScalarNode


class MappingNodeTestCase(unittest.TestCase):
    pass


class TestFromString(MappingNodeTestCase):

    def test_from_string_string(self):
        string = 'key1: value'
        expectedNode = MappingNode(
            elementsMap={
                ScalarNode(value='key'): ScalarNode(value='value')
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
