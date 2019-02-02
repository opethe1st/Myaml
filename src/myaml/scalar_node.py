import re
import typing

from dataclasses import dataclass

from .constants import NUM_SPACES_IN_INDENT
from .node import Node


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
        return f'{" "*NUM_SPACES_IN_INDENT*indentLevel}{self.value}'
