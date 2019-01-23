from .exceptions import ParsingException
from .node import Node

from .mapping_node import MappingNode
from .node_registry import nodeRegistry
from .scalar_node import ScalarNode
from .sequence_node import SequenceNode
from ._utils import convert_to_string_with_desired_indent


nodeRegistry.register(MappingNode)
nodeRegistry.register(SequenceNode)
nodeRegistry.register(ScalarNode)


def parse(string):
    string = convert_to_string_with_desired_indent(string=string)
    node = Node.from_string(string=string)
    return node.to_object()


def dump(obj):
    node = Node.from_object(obj=obj)
    return node.to_string()
