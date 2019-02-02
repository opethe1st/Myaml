import typing

from dataclasses import dataclass


class Node:
    pass


@dataclass(unsafe_hash=True)
class ScalarNode(Node):
    value: str # this is a string to start with


@dataclass
class MappingNode(Node):
    map_: typing.Dict['ScalarNode', 'Node']


@dataclass
class SequenceNode(Node):
    items: typing.List['Node']
