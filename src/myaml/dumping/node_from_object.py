from functools import singledispatch

from myaml.core import (
    MappingNode,
    ScalarNode,
    SequenceNode,
)

@singledispatch
def node_from_object(obj):
    pass


@node_from_object.register(str)
def _1(obj) -> 'ScalarNode':
    return ScalarNode(data=obj)


@node_from_object.register(dict)
def _2(obj) -> 'MappingNode':
    mapping = {}
    for key, value in obj.items():
        keyNode = node_from_object(key)
        valueNode = node_from_object(value)
        mapping[keyNode] = valueNode
    return MappingNode(mapping=mapping)


@node_from_object.register(list)
def _3(obj) -> 'SequenceNode':
    items = []
    for element in obj:
        elementNode = node_from_object(element)
        items.append(elementNode)
    return SequenceNode(items=items)
