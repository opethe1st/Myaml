import re

from ._line import Line


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
    return [re.sub(pattern=r'(\s*?)-', repl=r'\g<1> ', string=part) for part in get_key_value_strings(string=string)]
