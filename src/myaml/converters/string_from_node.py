import re
from functools import singledispatch

from myaml.core.nodes import MappingNode, Node, ScalarNode, SequenceNode

DEFAULT_INDENT_SIZE = 2


@singledispatch
def string_from_node(node: 'Node', indentLevel=0, indentSize=DEFAULT_INDENT_SIZE) -> str:
    pass


@string_from_node.register(ScalarNode)
def _1(node, indentLevel=0, indentSize=DEFAULT_INDENT_SIZE) -> str:
    return f'{" "*indentSize*indentLevel}{node.value}'


@string_from_node.register(MappingNode)
def _2(node, indentLevel=0, indentSize=DEFAULT_INDENT_SIZE) -> str:
    string = ''
    for keyNode, valueNode in node.map_.items():
        key = string_from_node(keyNode, indentLevel=indentLevel, indentSize=indentSize)
        if isinstance(valueNode, ScalarNode):
            value = string_from_node(valueNode, indentLevel=0, indentSize=indentSize)
            string += f'{key}: {value}\n'
        else:
            value = string_from_node(valueNode, indentLevel=indentLevel+1, indentSize=indentSize)
            string += (f'{key}:\n{value}'.rstrip('\n')+'\n')
    return string


@string_from_node.register(SequenceNode)
def _3(node, indentLevel=0, indentSize=DEFAULT_INDENT_SIZE) -> str:
    string = ''
    for elementNode in node.items:
        elementString = string_from_node(elementNode,indentLevel=indentLevel+1, indentSize=indentSize)
        elementString = re.sub(
            string=elementString,
            pattern=r'^(\s*)    ',
            repl=r'\g<1>-   '
        )
        string += (elementString.strip('\n') + "\n")
    return string
