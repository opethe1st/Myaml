from .line import (
    get_lines,
    get_string_from_lines,
)


def get_key_value_strings(string):
    if not string:
        return []
    lines = get_lines(string=string)
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
            res.append(get_string_from_lines(lines=currentLines))
    return res
