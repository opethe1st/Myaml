from .nodes import from_string_to_node
from .nodes import from_object_to_node


def parse(string):
    node = from_string_to_node(string=string)
    return node.to_object()


def dump(obj):
    node = from_object_to_node(obj=obj)
    return node.to_string()
