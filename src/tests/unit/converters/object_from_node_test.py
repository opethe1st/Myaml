from unittest import TestCase

from myaml.core.nodes import (
    MappingNode,
    ScalarNode,
    SequenceNode,
)
from myaml.converters.object_from_node import object_from_node


class TestObjectFromScalarNode(TestCase):

    def test_to_object(self):
        value = 'value string'
        node = ScalarNode(value=value)
        expectedObject = value
        self.assertEqual(
            object_from_node(node),  # sigh. I can't use keyword arguments with singledispatch functions
            expectedObject
        )


class TestObjectFromSequenceNode(TestCase):

    def test_to_object(self):
        items = [ScalarNode(value='value')]
        node = SequenceNode(items=items)
        expectedObject = ['value']
        self.assertEqual(
            object_from_node(node),
            expectedObject
        )


class TestObjectFromMappingNode(TestCase):

    def test_to_object(self):
        map_ = {ScalarNode(value='key'): ScalarNode(value='value')}
        node = MappingNode(map_=map_)
        expectedObject = {'key': 'value'}
        self.assertEqual(
            object_from_node(node),
            expectedObject
        )
