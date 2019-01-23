import re
import typing


from dataclasses import dataclass

from .node import Node
from ._utils import get_element_strings
from ._utils import get_key_value_strings


@dataclass
class SequenceNode(Node):

    elements: typing.List[Node]

    regex = re.compile(pattern=r'^\s*-', flags=re.MULTILINE)
    nativeType: typing.ClassVar = list

    @classmethod
    def from_string(cls, string: str) -> 'SequenceNode':
        elements = []
        for elementString in cls._get_element_string(string=string):
            elements.append(super().from_string(string=elementString))
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
            elementNode = super().from_object(obj=element)
            elements.append(elementNode)
        return cls(elements=elements)


    def to_string(self, indentLevel=0):
        string = ''
        for elementNode in self.elements:
            # I should make the indent here configurable
            string = string + (re.sub(string=elementNode.to_string(indentLevel=indentLevel+1), pattern=r'^(\s*)    ', repl=r'\g<1>-   ').strip('\n') + "\n")
        return string

    @staticmethod
    def _get_element_string(string: str) -> typing.List[str]:
        return get_element_strings(string=string)
