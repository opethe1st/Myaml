from unittest import TestCase

from myaml.core.nodes import (
    MappingNode,
    ScalarNode,
    SequenceNode,
)
from myaml.converters.node_from_object import node_from_object


class TestScalarFromObject(TestCase):

    def test_from_object(self):
        obj = 'value'
        expectedNode = ScalarNode(value=obj)
        self.assertEqual(
            node_from_object(obj),
            expectedNode
        )


class TestMappingFromObject(TestCase):

    def test_from_object(self):
        obj = {'key': 'value'}
        expectedNode = MappingNode(
            map_={
                ScalarNode(value='key'): ScalarNode(value='value')
            }
        )
        self.assertEqual(
            node_from_object(obj),
            expectedNode
        )



class TestFromObject(TestCase):

    def test_from_object(self):
        obj = ['value', {'key': 'value'}]
        expectedNode = SequenceNode(
            items=[
                ScalarNode(value='value'),
                MappingNode(
                    map_={ScalarNode(value='key'): ScalarNode(value='value')}
                )
            ]
        )
        self.assertEqual(
            node_from_object(obj),
            expectedNode
        )
