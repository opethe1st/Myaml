from functools import singledispatch
from typing import Dict, List

from myaml.core import MappingNode, Node, ScalarNode, SequenceNode


@singledispatch
def object_from_node(node: 'Node'):
    raise Exception(f'unknown node: {node}')


@object_from_node.register(ScalarNode)
def _1(node: 'ScalarNode') -> str:
    return node.data


@object_from_node.register(MappingNode)
def _2(node: 'MappingNode') -> Dict:
    res = {}
    for keyNode, valueNode in node.mapping.items():
        key = object_from_node(keyNode)
        value = object_from_node(valueNode)
        res[key] = value
    return res


@object_from_node.register(SequenceNode)
def _3(node: 'SequenceNode') -> List:
    res = []
    for itemNode in node.items:
        res.append(object_from_node(itemNode))
    return res
