import re

from myaml.exceptions import ParsingException
from myaml.core.nodes import (
    MappingNode,
    ScalarNode,
    SequenceNode
)
from .utils import (
    get_element_strings,
    get_key_value_strings,
)


def node_from_string(string: str) -> 'Node':
    # can turn this to a for loop or a table driven scheme and have a registration mechanism
    if is_mapping_string(string=string):
        return mapping_node_from_string(string=string)
    elif is_sequence_string(string=string):
        return sequence_node_from_string(string=string)
    elif is_scalar_string(string=string):
        return scalar_node_from_string(string=string)
    else:
        raise ParsingException()


def scalar_node_from_string(string: str) -> 'ScalarNode':
    return ScalarNode(value=string.strip())


def sequence_node_from_string(string) -> 'SequenceNode':
    items = []
    for elementString in get_element_strings(string=string):
        items.append(
            node_from_string(string=elementString)
        )
    return SequenceNode(items=items)


def mapping_node_from_string(string: str) -> 'MappingNode':
    map_ = {}
    for itemString in get_key_value_strings(string=string):
        keyNode = get_key_node(string=itemString)
        valueNode = get_value_node(string=itemString)
        map_[keyNode] = valueNode
    return MappingNode(map_=map_)


def get_key_node(string: str) -> 'ScalarNode':
    match = re.match(string=string, pattern=r'^\s*(\S(?<!-).*?):\s*')
    key = match.group(1)
    return ScalarNode(value=key)


def get_value_node(string: str) -> 'Node':
    match = re.match(string=string, pattern=r'^\s*\S(?<!-).*?: (\S.*)$', flags=re.MULTILINE)
    if match:
        value = match.group(1)
        return ScalarNode(value=value)
    match = re.match(string=string, pattern=r'^\s*\S(?<!-).*?:.*?\n(.*)$', flags=re.DOTALL)
    if match:
        value = match.group(1)
        return node_from_string(string=value)
    return ScalarNode(value='')


def is_scalar_string(string: str) -> bool:
    return bool(re.match(pattern=r'.*', string=string))


def is_mapping_string(string: str) -> bool:
    return bool(
        re.match(
            pattern=r'''
                (^\s*\S(?<!-).*?:\s+)  # if the string looks like 'key: '
                |   (^\s*\S(?<!-).*?:$) # if the string looks like '  key:' but not '- key: '
            ''',
            string=string,
            flags=re.VERBOSE,
        )
    )


def is_sequence_string(string):
    return re.match(pattern=r'^\s*-', string=string)
