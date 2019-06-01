from .node_from_lines import node_from_lines
from .object_from_node import object_from_node
from .line import lines_from_tokens
from .tokenizer import tokenize


def load(string):
    tokens = tokenize(string=string)
    lines = lines_from_tokens(tokens=tokens)
    node = node_from_lines(lines=lines)
    return object_from_node(node)
