from functools import singledispatch
import re
from myaml.core.nodes import (
    MappingNode,
    ScalarNode,
    SequenceNode
)
from myaml.constants import NUM_SPACES_IN_INDENT


@singledispatch
def string_from_node(node: 'Node', indentLevel=0) -> str:
    pass


@string_from_node.register(ScalarNode)
def _(node, indentLevel=0):
    return f'{" "*NUM_SPACES_IN_INDENT*indentLevel}{node.value}'


@string_from_node.register(MappingNode)
def _(node, indentLevel=0):
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
def _(node, indentLevel=0):
    string = ''
    for elementNode in node.items:
        elementString = string_from_node(elementNode,indentLevel=indentLevel+1)
        string += (
            re.sub(
                string=elementString,
                pattern=r'^(\s*)    ', repl=r'\g<1>-   ').strip('\n') + "\n")
    return string
