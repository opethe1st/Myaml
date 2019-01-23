import re

from ._line import Line
from .constants import NUM_SPACES_IN_INDENT


def get_key_value_strings(string):
    if not string:
        return []
    lines = Line.get_lines(string=string)
    cursor = 0
    indentLevel = lines[cursor].indent
    res = []
    while cursor < len(lines) and lines[cursor].indent >= indentLevel:
        if lines[cursor].indent == indentLevel:
            currentLines = [lines[cursor]]
            cursor += 1
            while cursor < len(lines) and lines[cursor].indent > indentLevel:
                currentLines.append(lines[cursor])
                cursor += 1
            res.append(Line._get_string_from_lines(lines=currentLines))
    return res


def get_element_strings(string):
    return [
        re.sub(pattern=r'(\s*?)-(.*)', repl=r'\g<1> \g<2>', string=part)
                for part in get_key_value_strings(string=string
        )
    ]


def convert_to_string_with_desired_indent(string):
    currentIndentSize = _detect_indentation(string=string)
    return _replace_indent_size(string=string, oldIndentSize=currentIndentSize, newIndentSize=NUM_SPACES_IN_INDENT)


def _detect_indentation(string):
    for line in string.split('\n'):
        if line:
            indentSize = _get_indent_size(line=line)
            if indentSize:
                return indentSize
    return 4


def _get_indent_size(line):
    match = re.match(string=line, pattern=r'(\s*)\S')
    if match:
        return len(match.group(1))
    return 0


def _replace_indent_size(string, oldIndentSize, newIndentSize):
    lines = string.split('\n')
    lines = [re.sub(string=line, pattern=r'-'+' '*(oldIndentSize-1), repl='!') for line in lines]
    lines = [re.sub(string=line, pattern=r' '*oldIndentSize, repl='$') for line in lines]
    lines = [re.sub(string=line, pattern=r'\$', repl=' '*newIndentSize) for line in lines]
    lines = [re.sub(string=line, pattern=r'\!', repl='-'+' '*(newIndentSize-1)) for line in lines]
    return "\n".join(lines)
