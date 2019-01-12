from .nodes import from_string_to_node


def parse(string):
    node = from_string_to_node(string=string)
    return node.to_object()
