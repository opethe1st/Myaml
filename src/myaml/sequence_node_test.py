import unittest

from .nodes import SequenceNode
from .nodes import ScalarNode
from .nodes import MappingNode


class SequenceNodeTestCase(unittest.TestCase):
    pass


class TestFromString(SequenceNodeTestCase):

    def test_from_string_string(self):
        string = '-   value'
        expectedNode = SequenceNode(
            elements=[
                ScalarNode(value='value')
            ]
        )
        self.assertEqual(
            SequenceNode.from_string(string=string),
            expectedNode
        )


class TestToObject(SequenceNodeTestCase):

    def test_to_object(self):
        elements = [ScalarNode(value='value')]
        node = SequenceNode(elements=elements)
        expectedObject = ['value']
        self.assertEqual(
            node.to_object(),
            expectedObject
        )


class TestFromObject(SequenceNodeTestCase):

    def test_from_object(self):
        obj = ['value', {'key': 'value'}]
        expectedNode = SequenceNode(
            elements=[
                ScalarNode(value='value'),
                MappingNode(
                    elementsMap={ScalarNode(value='key'): ScalarNode(value='value')}
                )
            ]
        )
        self.assertEqual(
            SequenceNode.from_object(obj=obj),
            expectedNode
        )


class TestToString(SequenceNodeTestCase):

    def test_to_string(self):
        node = SequenceNode(
            elements=[
                ScalarNode(value='value'),
                MappingNode(
                    elementsMap={ScalarNode(value='key'): ScalarNode(value='value')}
                )
            ]
        )
        expectedString = '''-   value
-   key: value
'''
        self.assertEqual(
            node.to_string(),
            expectedString
        )
