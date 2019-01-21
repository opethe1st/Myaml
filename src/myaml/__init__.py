from .exceptions import ParsingException

from .node import Node


def parse(string):
    node = Node.from_string(string=string)
    return node.to_object()


def dump(obj):
    node = Node.from_object(obj=obj)
    return node.to_string()
