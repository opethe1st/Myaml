from functools import singledispatch

from myaml.core.nodes import (
    MappingNode,
    ScalarNode,
    SequenceNode,
)

@singledispatch
def node_from_object(obj):
    pass


@node_from_object.register(str)
def _1(obj) -> 'ScalarNode':
    return ScalarNode(value=obj)


@node_from_object.register(dict)
def _2(obj) -> 'MappingNode':
    map_ = {}
    for key, value in obj.items():
        keyNode = node_from_object(key)
        valueNode = node_from_object(value)
        map_[keyNode] = valueNode
    return MappingNode(map_=map_)


@node_from_object.register(list)
def _3(obj) -> 'SequenceNode':
    items = []
    for element in obj:
        elementNode = node_from_object(element)
        items.append(elementNode)
    return SequenceNode(items=items)
