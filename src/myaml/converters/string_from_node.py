import re
from functools import singledispatch

from myaml.constants import NUM_SPACES_IN_INDENT
from myaml.core.nodes import MappingNode, Node, ScalarNode, SequenceNode


@singledispatch
def string_from_node(node: 'Node', indentLevel=0) -> str:
    pass


@string_from_node.register(ScalarNode)
def _1(node, indentLevel=0) -> str:
    return f'{" "*NUM_SPACES_IN_INDENT*indentLevel}{node.value}'


@string_from_node.register(MappingNode)
def _2(node, indentLevel=0) -> str:
    string = ''
    for keyNode, valueNode in node.map_.items():
        key = string_from_node(keyNode, indentLevel=indentLevel)
        if isinstance(valueNode, ScalarNode):
            value = string_from_node(valueNode, indentLevel=0)
            string += f'{key}: {value}\n'
        else:
            value = string_from_node(valueNode, indentLevel=indentLevel+1)
            string += (f'{key}:\n{value}'.rstrip('\n')+'\n')
    return string


@string_from_node.register(SequenceNode)
def _3(node, indentLevel=0) -> str:
    string = ''
    for elementNode in node.items:
        elementString = string_from_node(elementNode,indentLevel=indentLevel+1)
        elementString = re.sub(
            string=elementString,
            pattern=r'^(\s*)    ',
            repl=r'\g<1>-   '
        )
        string += (elementString.strip('\n') + "\n")
    return string
