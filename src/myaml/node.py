import abc
import typing


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
        pass

    @abc.abstractmethod
    def to_object(self) -> typing.Union[str, dict, list]:
        pass

    @abc.abstractclassmethod
    def from_object(cls, obj: typing.Union[str, dict, list]) -> 'Node':
        pass

    @abc.abstractmethod
    def to_string(self) -> str:
        pass

    @classmethod
    def match_object(cls, obj):
        return isinstance(obj, cls.nativeType)

    @classmethod
    def match(cls, string) -> bool:
        if cls.regex.match(string=string):
            return True
        return False
