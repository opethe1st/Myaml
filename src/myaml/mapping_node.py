import re
import typing

from dataclasses import dataclass

from ._utils import get_element_strings
from ._utils import get_key_value_strings
from .node import Node
from .scalar_node import ScalarNode


@dataclass
class MappingNode(Node):

    elementsMap: typing.Dict['ScalarNode', Node]

    regex: typing.ClassVar = re.compile(pattern=r'(^\s*(\S(?<!-).*?):\s)|^(^\s*(\S(?<!-).*?):$)', flags=re.MULTILINE)
    nativeType: typing.ClassVar = dict

    @classmethod
    def from_string(cls, string: str) -> 'MappingNode':
        elementsMap = {}
        for elementString in cls._get_element_strings(string=string):
            keyNode = cls._get_key_node(string=elementString)
            valueNode = cls._get_value_node(string=elementString)
            elementsMap[keyNode] = valueNode
        return cls(elementsMap=elementsMap)

    def to_object(self) -> dict:
        res = {}
        for keyNode, valueNode in self.elementsMap.items():
            res[keyNode.to_object()] = valueNode.to_object()
        return res

    @classmethod
    def from_object(cls, obj):
        elementsMap = {}
        for key, value in obj.items():
            keyNode = super().from_object(obj=key)
            valueNode = super().from_object(obj=value)
            elementsMap[keyNode] = valueNode
        return cls(elementsMap=elementsMap)

    def to_string(self, indentLevel=0):
        string = ''
        for keyNode, valueNode in self.elementsMap.items():
            key = keyNode.to_string(indentLevel=indentLevel)
            if isinstance(valueNode, ScalarNode):
                value = valueNode.to_string()
                string += f'{key}: {value}\n'
            else:
                value = valueNode.to_string(indentLevel=indentLevel+1)
                string += (f'{key}:\n{value}'.rstrip('\n')+'\n')
        return string


    @staticmethod
    def _get_element_strings(string: str) -> typing.List[str]:
        return get_key_value_strings(string=string)

    @staticmethod
    def _get_key_node(string: str) -> 'ScalarNode':
        match = re.match(string=string, pattern=r'^\s*(\S(?<!-).*?):\s*')
        key = match.group(1)
        return ScalarNode(value=key)

    @staticmethod
    def _get_value_node(string: str) -> 'Node':
        match = re.match(string=string, pattern=r'^\s*\S(?<!-).*?: (\S.*)$', flags=re.MULTILINE)
        if match:
            value = match.group(1)
            return ScalarNode(value=value)
        match = re.match(string=string, pattern=r'^\s*\S(?<!-).*?:.*?\n(.*)$', flags=re.DOTALL)
        if match:
            value = match.group(1)
            return super().from_string(string=value)
        return ScalarNode(value='')
