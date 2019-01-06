from .node import Node


def parse(string):
    node = Node.from_string(string=string)
    return node.to_native_object()
