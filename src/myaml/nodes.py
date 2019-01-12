import re
import typing


from dataclasses import dataclass

from .node import Node
from ._utils import get_element_strings
from ._utils import get_key_value_strings


# All the nodes are here because they are tightly coupled - by the parse method - I will figure out how to move them out later


@dataclass(unsafe_hash=True)
class ScalarNode(Node):

    value: str

    regex: typing.ClassVar = re.compile(pattern=r'.*', flags=re.DOTALL)

    @classmethod
    def from_string(cls, string: str) -> 'ScalarNode':
        return cls(value=string)

    def to_object(self) -> str:
        return self.value  # later this will be used to convert to primitive types


@dataclass
class MappingNode(Node):

    elementsMap: typing.Dict[ScalarNode, Node]

    regex = re.compile(pattern=r'(^\s*(\S(?<!-).*?):\s)|^(^\s*(\S(?<!-).*?):$)', flags=re.MULTILINE)

    @classmethod
    def from_string(cls, string: str) -> 'MappingNode':
        elementsMap = {}
        for elementString in cls._get_element_strings(string=string):
            print('elementString', elementString, string)
            keyNode = cls._get_key_node(string=elementString)
            valueNode = cls._get_value_node(string=elementString)
            elementsMap[keyNode] = valueNode
        return cls(elementsMap=elementsMap)

    def to_object(self) -> dict:
        res = {}
        for keyNode, valueNode in self.elementsMap.items():
            res[keyNode.to_object()] = valueNode.to_object()
        return res

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
            return from_string_to_node(string=value)
        return None


@dataclass
class SequenceNode(Node):

    elements: typing.List[Node]

    regex = re.compile(pattern=r'^\s*-', flags=re.MULTILINE)

    @classmethod
    def from_string(cls, string: str) -> 'SequenceNode':
        elements = []
        for elementString in cls._get_element_string(string=string):
            elements.append(from_string_to_node(string=elementString))
        return cls(elements=elements)

    def to_object(self) -> list:
        res = []
        for node in self.elements:
            res.append(node.to_object())
        return res

    @staticmethod
    def _get_element_string(string: str) -> typing.List[str]:
        return get_element_strings(string=string)


class NodeRegistry:

    _items = []

    @classmethod
    def register(cls, nodeCls: 'Node'):
        cls._items.append(nodeCls)

    @staticmethod
    def get_node_classes() -> list:
        return NodeRegistry._items


NodeRegistry.register(nodeCls=MappingNode)
NodeRegistry.register(nodeCls=SequenceNode)
NodeRegistry.register(nodeCls=ScalarNode)


def from_string_to_node(string):
    for nodeCls in NodeRegistry.get_node_classes():
        if nodeCls.match(string=string):
            return nodeCls.from_string(string=string)
    raise Exception('unknown node type')