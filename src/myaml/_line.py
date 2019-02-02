import re

from dataclasses import dataclass

from .constants import NUM_SPACES_IN_INDENT
from .exceptions import InconsistentIndentation


@dataclass
class Line:
    string: str
    indent: int

    @classmethod
    def get_lines(cls, string):
        lines = []
        lineStrings = string.split("\n")
        for lineString in lineStrings:
            if re.match(string=lineString, pattern=r'\s*\S.*'):
                lines.append(cls.from_string(string=lineString))
        return lines

    @classmethod
    def from_string(cls, string):
        indent = cls._get_indent(string=string)
        value = cls._get_string(string=string)
        return cls(string=value, indent=indent)

    @staticmethod
    def _get_indent(string):
        match = re.match(pattern=r'(\s*?)\S', string=string)
        numOfSpaces = len(match.group(1)) if match is not None else 0
        if numOfSpaces%NUM_SPACES_IN_INDENT:
            raise InconsistentIndentation(
                f'Got {numOfSpaces} spaces in the indentation, need a multiple of {NUM_SPACES_IN_INDENT}'
            )
        return numOfSpaces//NUM_SPACES_IN_INDENT

    @staticmethod
    def _get_string(string):
        match = re.match(pattern=r'\s*?(\S.*)$', string=string, flags=re.MULTILINE)
        return match.group(1) if match is not None else ''

    @staticmethod
    def _get_string_from_lines(lines):
        lineStrings = [
            "{indent}{string}".format(indent=' '*NUM_SPACES_IN_INDENT*line.indent, string=line.string)
            for line in lines
        ]
        return "\n".join(lineStrings)
