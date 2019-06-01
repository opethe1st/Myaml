from unittest import TestCase

from myaml.core import (
    MappingNode,
    ScalarNode,
    SequenceNode,
)
from myaml.loading.object_from_node import object_from_node


class TestObjectFromScalarNode(TestCase):

    def test_to_object(self):
        value = 'value string'
        node = ScalarNode(data=value)
        expectedObject = value
        self.assertEqual(
            object_from_node(node),  # sigh. I can't use keyword arguments with singledispatch functions
            expectedObject
        )


class TestObjectFromSequenceNode(TestCase):

    def test_to_object(self):
        items = [ScalarNode(data='value')]
        node = SequenceNode(items=items)
        expectedObject = ['value']
        self.assertEqual(
            object_from_node(node),
            expectedObject
        )


class TestObjectFromMappingNode(TestCase):

    def test_to_object(self):
        mapping = {ScalarNode(data='key'): ScalarNode(data='value')}
        node = MappingNode(mapping=mapping)
        expectedObject = {'key': 'value'}
        self.assertEqual(
            object_from_node(node),
            expectedObject
        )
