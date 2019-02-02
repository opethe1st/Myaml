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
def _(obj):
    return ScalarNode(value=obj)


@node_from_object.register(dict)
def _(obj):
    map_ = {}
    for key, value in obj.items():
        keyNode = node_from_object(key)
        valueNode = node_from_object(value)
        map_[keyNode] = valueNode
    return MappingNode(map_=map_)


@node_from_object.register(list)
def _(obj):
    items = []
    for element in obj:
        elementNode = node_from_object(element)
        items.append(elementNode)
    return SequenceNode(items=items)
