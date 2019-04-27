from myaml.converters.node_from_lines import node_from_lines
from myaml.converters.node_from_object import node_from_object
from myaml.converters.object_from_node import object_from_node
from myaml.converters.string_from_node import string_from_node
from myaml.converters.utils.line import lines_from_tokens
from myaml.converters.utils.tokenizer import tokenize


# not sure main.py is the appropriate thing here since this is a library
def load(string):
    tokens = tokenize(string=string)
    lines = lines_from_tokens(tokens=tokens)
    node = node_from_lines(lines=lines)
    return object_from_node(node)


def dump(obj, indentSize=4):
    node = node_from_object(obj)
    return string_from_node(node, indentSize=indentSize)
