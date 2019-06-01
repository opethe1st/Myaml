from unittest import TestCase

from myaml.core import MappingNode, ScalarNode, SequenceNode
from myaml.dumping.node_from_object import node_from_object


class TestScalarFromObject(TestCase):

    def test_from_object(self):
        obj = 'value'
        expectedNode = ScalarNode(data=obj)
        self.assertEqual(
            node_from_object(obj),
            expectedNode
        )


class TestMappingFromObject(TestCase):

    def test_from_object(self):
        obj = {'key': 'value'}
        expectedNode = MappingNode(
            mapping={
                ScalarNode(data='key'): ScalarNode(data='value')
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
                ScalarNode(data='value'),
                MappingNode(
                    mapping={ScalarNode(data='key'): ScalarNode(data='value')}
                )
            ]
        )
        self.assertEqual(
            node_from_object(obj),
            expectedNode
        )
