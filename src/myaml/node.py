import abc
import typing

from .node_registry import nodeRegistry


class Node(abc.ABC):

    @property
    @abc.abstractproperty
    def regex(self):
        pass

    @property
    @abc.abstractproperty
    def nativeType(self):
        pass

    @abc.abstractclassmethod
    def from_string(cls, string: str) -> 'Node':
        for nodeCls in nodeRegistry.get_node_classes():
            if nodeCls.match(string=string):
                return nodeCls.from_string(string=string)
        raise Exception('unknown node type')

    @abc.abstractmethod
    def to_object(self) -> typing.Union[str, dict, list]:
        pass

    @abc.abstractclassmethod
    def from_object(cls, obj: typing.Union[str, dict, list]) -> 'Node':
        for nodeCls in nodeRegistry.get_node_classes():
            if nodeCls.match_object(obj=obj):
                return nodeCls.from_object(obj=obj)
        raise Exception('unknown node type')

    @abc.abstractmethod
    def to_string(self) -> str:  # this should be the same as the __repr__  or __str__?
        pass

    @classmethod
    def match_object(cls, obj):
        return isinstance(obj, cls.nativeType)

    @classmethod
    def match(cls, string) -> bool:
        if cls.regex.match(string=string):
            return True
        return False
