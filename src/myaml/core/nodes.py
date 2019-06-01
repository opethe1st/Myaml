import typing

from dataclasses import dataclass


class Node:
    pass


@dataclass(unsafe_hash=True)
class ScalarNode(Node):
    data: str # this is a string to start with


@dataclass
class MappingNode(Node):
    mapping: typing.Dict['ScalarNode', 'Node']


@dataclass
class SequenceNode(Node):
    items: typing.List['Node']
