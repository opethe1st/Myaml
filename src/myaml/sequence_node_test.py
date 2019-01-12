import unittest

from .nodes import SequenceNode
from .nodes import ScalarNode


class SequenceNodeTestCase(unittest.TestCase):
    pass


class TestFromString(SequenceNodeTestCase):

    def test_from_string_string(self):
        string = '-   value'
        expectedNode = SequenceNode(
            elements=[
                ScalarNode(value='    value')
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
