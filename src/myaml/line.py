from dataclasses import dataclass
import re

NUM_SPACES_IN_INDENT = 4


@dataclass
class Line:
    string: str
    indent: int

    @classmethod
    def _get_lines(cls, string):
        lines = []
        lineStrings = string.split("\n")
        for lineString in lineStrings:
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
