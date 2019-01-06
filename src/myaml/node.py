import re
import typing

from dataclasses import dataclass
from dataclasses import field

from .line import Line
from .node_types import NodeTypes


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
            for innerNode in self.innerNodes:  # pylint: disable=E1133
                key = Node.from_string(string=innerNode.get_key_string()).to_native_object()
                value = Node.from_string(string=innerNode.get_value_string()).to_native_object()
                res[key] = value
            return res
        if self.nodeType == NodeTypes.SEQUENCE:
            res = []
            for innerNode in self.innerNodes:  # pylint: disable=E1133
                res.append(innerNode.to_native_object())
            return res
        if self.nodeType == NodeTypes.SCALAR:
            return self.value
        raise Exception('Unknown NodeTypes')

    @staticmethod
    def _get_node_type(string):
        if re.match(pattern=r'(^\s*(\S(?<!-).*?):\s)|^(^\s*(\S(?<!-).*?):$)', string=string, flags=re.MULTILINE):
            return NodeTypes.MAPPING
        if re.match(pattern=r'^\s*-', string=string, flags=re.MULTILINE):
            return NodeTypes.SEQUENCE
        return NodeTypes.SCALAR

    @staticmethod
    def _get_key_value_strings(string):
        lines = Line._get_lines(string=string)
        if not lines:
            return []
        cursor = 0
        indentLevel = lines[cursor].indent
        res = []
        while cursor < len(lines) and lines[cursor].indent >= indentLevel:
            if lines[cursor].indent == indentLevel:
                currentLines = [lines[cursor]]
                cursor += 1
                while cursor < len(lines) and lines[cursor].indent > indentLevel:
                    currentLines.append(lines[cursor])
                    cursor += 1
                res.append(Line._get_string_from_lines(lines=currentLines))
        return res

    def get_key_string(self):
        if self.nodeType == NodeTypes.MAPPING:
            match = re.match(string=self.value, pattern=r'^\s*(\S(?<!-).*?):\s')
            return match.group(1)
        raise Exception('get key cannot get keys for non-mapping nodes')

    def get_value_string(self):
        if self.nodeType == NodeTypes.MAPPING:
            match = re.match(string=self.value, pattern=r'^\s*\S(?<!-).*?:.*?\n(.*)$', flags=re.DOTALL)
            if match:
                return match.group(1)
            match = re.match(string=self.value, pattern=r'^\s*\S(?<!-).*?: (\S.*)$')
            if match:
                return match.group(1)
            match = re.match(string=self.value, pattern=r'^\s*\S(?<!-).*?:\s*$')
            if match:
                return ''
        raise Exception('Unknown NodeType')

    @classmethod
    def _get_element_strings(cls, string):
        return [re.sub(pattern=r'(\s*?)-', repl=r'\g<1> ', string=part) for part in cls._get_key_value_strings(string=string)]

