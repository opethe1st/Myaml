import abc
import typing


class Node(abc.ABC):

    regex = None

    @abc.abstractclassmethod
    def from_string(cls, string: str) -> 'Node':
        pass

    @abc.abstractmethod
    def to_object(self) -> typing.Any:
        pass

    @classmethod
    def match(cls, string) -> bool:
        if cls.regex.match(string=string):
            return True
        return False
