import unittest

from .nodes import ScalarNode


class ScalarNodeTestCase(unittest.TestCase):
    pass


class TestFromString(ScalarNodeTestCase):

    def test_from_string_string(self):
        value = 'value string'
        expectedNode = ScalarNode(value=value)
        self.assertEqual(
            ScalarNode.from_string(string=value),
            expectedNode
        )


class TestToObject(ScalarNodeTestCase):

    def test_to_object(self):
        value = 'value string'
        node = ScalarNode(value=value)
        expectedObject = value
        self.assertEqual(
            node.to_object(),
            expectedObject
        )
