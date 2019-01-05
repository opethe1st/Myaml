import re

from .exceptions import ParsingException


class NodeTypes:
    MAPPING = 'MAPPING'
    SCALAR = 'SCALAR'
    SEQUENCE = 'SEQUENCE'


def parse(string):
    # node = Node.from_string(string=string)
    # v
    nodeType = get_node_type(string=string)
    if nodeType == NodeTypes.MAPPING:
        res = {}
        keyValueStrings = get_key_value_strings(string=string)
        for keyValueString in keyValueStrings:
            key = parse(string=get_key_string(keyValueString))
            value = parse(string=get_value_string(keyValueString))
            res[key] = value
        return res
    elif nodeType == NodeTypes.SEQUENCE:
        res = []
        valueStrings = get_value_strings(string=string)
        for valueString in valueStrings:
            res.append(parse(string=get_sequence_element_string(string=valueString)))
        return res
    elif nodeType == NodeTypes.SCALAR:
        return get_scalar(string=string)
    else:
        raise ParsingException('')


KEY_REGEX = re.compile(pattern=r'\W*(\w.*?):\W*$', flags=re.MULTILINE)
VALUE_REGEX = re.compile(pattern=r'.*$\n([\w\W\n]*)', flags=re.MULTILINE)


def get_node_type(string):
    if KEY_REGEX.match(string=string):
        return NodeTypes
    return NodeTypes.SCALAR


def get_key_string(string):
    if KEY_REGEX.match(string):
        return KEY_REGEX.search(string=string).group(1)
    return None


def get_value_string(string):
    if KEY_REGEX.match(string):
        return KEY_REGEX.search(string=string).group(1)
    return None


def get_sequence_element_string(string):
    return 'key'


def get_scalar(string):
    return string


def get_key_value_strings(string):
    return []


def get_value_strings(string):
    return []
