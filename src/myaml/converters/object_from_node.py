from functools import singledispatch

from myaml.core.nodes import (
    MappingNode,
    ScalarNode,
    SequenceNode
)


@singledispatch
def object_from_node(node):
    raise Exception(f'unknown node: {node}')


@object_from_node.register(ScalarNode)
def _(node):
    return node.value


@object_from_node.register(MappingNode)
def _(node):
    res = {}
    for keyNode, valueNode in node.map_.items():
        key = object_from_node(keyNode)
        value = object_from_node(valueNode)
        res[key] = value
    return res


@object_from_node.register(SequenceNode)
def _(node):
    res = []
    for node in node.items:
        res.append(object_from_node(node))
    return res
