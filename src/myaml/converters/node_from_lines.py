from typing import List

from myaml.converters.utils.line import Line
from myaml.converters.utils.tokenizer import Indent, Separator, Value
from myaml.core.nodes import MappingNode, Node, ScalarNode, SequenceNode
from myaml.exceptions import ParsingException


def node_from_lines(lines: List['Line']):
    if not lines:
        raise Exception('You need to pass in a non-empty list of Lines')
    if lines[0].is_mapping():
        return mapping_node_from_lines(lines=lines)
    elif lines[0].is_sequence():
        return sequence_node_from_lines(lines=lines)
    elif lines[0].is_scalar():
        return scalar_node_from_lines(lines=lines)
    raise Exception('Unknown token sequence') # currently a bullshit error message


def scalar_node_from_lines(lines):
    return ScalarNode(value=lines[0].tokens[0].data)


def mapping_node_from_lines(lines):
    map_ = {}
    for itemLines in get_item_lines(lines=lines):
        keyNode, valueNode = get_key_value_node(lines=itemLines)
        map_[keyNode] = valueNode
    return MappingNode(map_=map_)


# TODO(ope): return a list of bounds
def get_item_lines(lines: List['Line']) -> List[List['Line']]:
    firstLineIndentLevel = lines[0].indent
    itemLines = []
    position = 0
    while position < len(lines):
        if lines[position].indent == firstLineIndentLevel:
            currentLines = []
            currentLines.append(lines[position])
            position += 1
            while position < len(lines) and lines[position].indent > firstLineIndentLevel:
                currentLines.append(lines[position])
                position += 1
            itemLines.append(currentLines)
        elif lines[position].indent < firstLineIndentLevel:
            raise ParsingException('Unexpected indent level. What is you doing!')
    return itemLines


def get_key_value_node(lines):
    if not lines:
        raise Exception('Lines needs to be non-empty')
    if not lines[0].is_mapping():
        raise Exception(f'these lines are not a mapping {lines}')
    if len(lines) == 1:
        line = lines[0]
        keyNode = ScalarNode(value=line.tokens[0].data)
        data = line.tokens[2].data if len(line.tokens) > 2 else None
        valueNode = ScalarNode(value=data)
        return keyNode, valueNode
    else:
        keyNode = ScalarNode(value=lines[0].tokens[0].data)
        valueNode = node_from_lines(lines=lines[1:])
        return keyNode, valueNode


def sequence_node_from_lines(lines):
    items = []
    for valueLines in get_value_lines(lines=lines):
        items.append(node_from_lines(lines=valueLines))
    return SequenceNode(items=items)


def get_value_lines(lines):
    firstLineIndentLevel = lines[0].indent
    itemLines = []
    position = 0
    while position < len(lines):
        if lines[position].indent == firstLineIndentLevel and lines[position].is_sequence():
            currentLines = []
            line = lines[position]
            currentLines.append(Line(indent=line.indent, tokens=line.tokens[1:])) # tokens except the SequenceIndent token
            position += 1
            while position < len(lines) and lines[position].indent >= firstLineIndentLevel and not lines[position].is_sequence():
                currentLines.append(lines[position])
                position += 1
            itemLines.append(currentLines)
        elif lines[position].indent < firstLineIndentLevel:
            raise ParsingException('Unexpected indent level. What is you doing!')
    return itemLines
