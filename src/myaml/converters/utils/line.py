import re
from typing import List

from dataclasses import dataclass

from myaml.constants import NUM_SPACES_IN_INDENT
from myaml.exceptions import InconsistentIndentation


@dataclass
class Line:
    string: str
    indent: int


def get_lines(string: str) -> List[Line]:
    lines = []
    lineStrings = string.split("\n")
    for lineString in lineStrings:
        if re.match(string=lineString, pattern=r'\s*\S.*'):
            lines.append(line_from_string(string=lineString))
    return lines


def line_from_string(string: str) -> Line:
    indent = get_indent(string=string)
    value = get_string(string=string)
    return Line(string=value, indent=indent)


def get_indent(string: str) -> int:
    match = re.match(pattern=r'(\s*?)\S', string=string)
    numOfSpaces = len(match.group(1)) if match is not None else 0
    if numOfSpaces%NUM_SPACES_IN_INDENT:
        raise InconsistentIndentation(
            f'Got {numOfSpaces} spaces in the indentation, need a multiple of {NUM_SPACES_IN_INDENT}'
        )
    return numOfSpaces//NUM_SPACES_IN_INDENT


def get_string(string: str) -> str:
    match = re.match(pattern=r'\s*?(\S.*)$', string=string, flags=re.MULTILINE)
    return match.group(1) if match is not None else ''


def get_string_from_lines(lines: List[Line]) -> str:
    lineStrings = [
        "{indent}{string}".format(indent=' '*NUM_SPACES_IN_INDENT*line.indent, string=line.string)
        for line in lines
    ]
    return "\n".join(lineStrings)
