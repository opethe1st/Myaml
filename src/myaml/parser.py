import re
import typing

from dataclasses import dataclass
from dataclasses import field

from .exceptions import ParsingException


class NodeTypes:
    MAPPING = 'MAPPING'
    SCALAR = 'SCALAR'
    SEQUENCE = 'SEQUENCE'


@dataclass
class Node:
    nodeType: str
    value: str
    innerNodes: typing.List['Node'] = field(default_factory=list)

    @classmethod
    def from_string(cls, string):
        nodeType = cls._get_node_type(string=string)
        if nodeType == NodeTypes.SCALAR:
            return Node(value=string, nodeType=NodeTypes.SCALAR)
        elif nodeType == NodeTypes.MAPPING:
            innerNodes = []
            for keyValueString in cls._get_key_value_strings(string=string):
                innerNodes.append(Node.from_string(string=keyValueString))
            return Node(value=string, nodeType=NodeTypes.MAPPING, innerNodes=innerNodes)
        elif nodeType == NodeTypes.SEQUENCE:
            innerNodes = []
            for elementString in cls._get_element_strings(string=string):
                innerNodes.append(Node.from_string(string=elementString))
            return Node(value=string, nodeType=NodeTypes.SEQUENCE, innerNodes=innerNodes)
        else:
            raise Exception('Unknown Nod type')

    def to_native_object(self):
        if self.nodeType == NodeTypes.MAPPING:
            res = {}
            for innerNode in self.innerNodes:
                res[innerNode.get_key().to_native_object()] = innerNode.get_value().to_native_object()
            return res
        if self.nodeType == NodeTypes.SEQUENCE:
            res = []
            for innerNode in self.innerNodes:
                res.append(innerNode.to_native_object())
            return res
        if self.nodeType == NodeTypes.SCALAR:
            return self.value
        raise Exception('Unknown NodeTypes')

    def get_key(self):
        if self.nodeType == NodeTypes.MAPPING:
            match = re.match(string=self.value, pattern=r'^\s*(\S(?<!-).*?):\s')
            return match.group(1)
        raise Exception('get key cannot get keys for non-mapping nodes')

    def get_value(self):
        if self.nodeType == NodeTypes.MAPPING:
            match = re.match(string=self.value, pattern=r'^\s*(\S(?<!-).*?):\s')
            return match.group(1)
        raise Exception('Unknown NodeType')

    @staticmethod
    def _get_node_type(string):
        if re.match(pattern=r'(^\s*(\S(?<!-).*?):\s)|^(^\s*(\S(?<!-).*?):$)', string=string, flags=re.MULTILINE):
            return NodeTypes.MAPPING
        if re.match(pattern=r'^\s*-', string=string, flags=re.MULTILINE):
            return NodeTypes.SEQUENCE
        return NodeTypes.SCALAR

    @staticmethod
    def _get_key_value_strings(string):
        return []

    @staticmethod
    def _get_element_strings(string):
        return []


def parse(string):
    node = Node.from_string(string=string)
    return node.to_native_object()
