import re
import typing


from dataclasses import dataclass

from .node import Node
from ._utils import get_element_strings
from ._utils import get_key_value_strings


# All the nodes are here because they are tightly coupled
# - the parse method uses the Node registry to know about the 3 classes.
# Right now, the NodeRegistry is a singleton - it can't be instantiated
# I could make this work by moving it to its own class. then importing in each file that defines a node
# then register the node - will need to make sure the files with the nodes get imported so that the registration happens
# I will figure out how to move them out later
# Another thing, maybe use less regex going forward?? good idea?


@dataclass(unsafe_hash=True)
class ScalarNode(Node):

    value: str

    regex: typing.ClassVar = re.compile(pattern=r'.*', flags=re.DOTALL)
    nativeType: typing.ClassVar = str

    @classmethod
    def from_string(cls, string: str) -> 'ScalarNode':
        return cls(value=string.strip())

    def to_object(self) -> str:
        return self.value.strip()  # later this will be used to convert to primitive types - if this matches a pattern

    @classmethod
    def from_object(cls, obj):
        return cls(value=obj)

    def to_string(self, indentLevel=0):
        return f'{" "*4*indentLevel}{self.value}'


@dataclass
class MappingNode(Node):

    elementsMap: typing.Dict[ScalarNode, Node]

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
            keyNode = from_object_to_node(obj=key)
            valueNode = from_object_to_node(obj=value)
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
                string += f'{key}:\n{value}\n'
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
            return from_string_to_node(string=value)
        return ScalarNode(value='')


@dataclass
class SequenceNode(Node):

    elements: typing.List[Node]

    regex = re.compile(pattern=r'^\s*-', flags=re.MULTILINE)
    nativeType: typing.ClassVar = list

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

    @classmethod
    def from_object(cls, obj):
        elements = []
        for element in obj:
            elementNode = from_object_to_node(obj=element)
            elements.append(elementNode)
        return cls(elements=elements)


    def to_string(self, indentLevel=0):
        string = ''
        for elementNode in self.elements:
            string = string + re.sub(string=elementNode.to_string(indentLevel=indentLevel+1), pattern=r'^(\s*)    ', repl=r'\g<1>-   ') + "\n"
        return string

    @staticmethod
    def _get_element_string(string: str) -> typing.List[str]:
        return get_element_strings(string=string)


class NodeRegistry:

    _items = []

    def __init__(self):
        raise NotImplementedError

    @classmethod
    def register(cls, nodeCls: 'Node'):
        cls._items.append(nodeCls)

    @staticmethod
    def get_node_classes() -> list:
        return NodeRegistry._items


# The order matters here in case
NodeRegistry.register(nodeCls=MappingNode)
NodeRegistry.register(nodeCls=SequenceNode)
NodeRegistry.register(nodeCls=ScalarNode)


def from_string_to_node(string):
    for nodeCls in NodeRegistry.get_node_classes():
        if nodeCls.match(string=string):
            return nodeCls.from_string(string=string)
    raise Exception('unknown node type')


def from_object_to_node(obj):
    for nodeCls in NodeRegistry.get_node_classes():
        if nodeCls.match_object(obj=obj):
            return nodeCls.from_object(obj=obj)
    raise Exception('unknown node type')
