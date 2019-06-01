from .node_from_object import node_from_object
from .string_from_node import string_from_node


def dump(obj, indentSize=4):
    node = node_from_object(obj)
    return string_from_node(node, indentSize=indentSize)
