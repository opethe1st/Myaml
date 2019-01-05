import re
import typing

from .exceptions import ParsingException


def parse(string: str) -> typing.Union[typing.Dict, typing.List]:
    parser = Parser()
    return parser.parse(string=string)


class Parser:

    def __init__(self):
        # TODO(ope): add the option of detecting the indent level later or setting
        self._indent = 2
        # might need to move this to a parser that parses key value
        self._key_value_regex = re.compile(pattern=r'\W*(\w.*): (\w.*)$')
        self._key_regex = re.compile(pattern=r'\W*(\w.*):\W*$')
        self._get_indent_regex = re.compile(pattern=r'^(([ ]*)\w)|^')

    def parse(self, string: str):
        return self.get_mapping(lines=string.split('\n'))

    def get_mapping(self, lines: typing.List[str]):
        lines = [line for line in lines if line]
        res = {}
        current_line_index = 0
        current_indent_level = self._get_indent_level(line=lines[current_line_index])

        line_index = current_line_index

        while line_index < len(lines):
            if self._get_indent_level(line=lines[line_index]) == current_indent_level:
                if self._is_key_value(line=lines[line_index]):
                    key, value = self._get_key_value(line=lines[line_index])
                    res[key] = value
                    line_index += 1
                elif self._is_mapping_key(line=lines[line_index]):
                    key = self._get_key(line=lines[line_index])
                    next_line_index = line_index + 1
                    sublines = []
                    while next_line_index < len(lines) and self._get_indent_level(line=lines[next_line_index]) > current_indent_level:
                        sublines.append(lines[next_line_index])
                        next_line_index += 1
                    # this is recursive but what is the base case? - key-value
                    value = self.get_mapping(lines=sublines) if sublines else {}
                    res[key] = value
                    line_index = next_line_index
                else:
                    raise Exception('should never get here')
        return res

    def _get_key_value(self, line):
        if self._key_value_regex is None:
            self._key_value_regex = re.compile(pattern=r'\W*(\w.*): (\w.*)$')
        match = self._key_value_regex.search(string=line)
        return match.group(1), match.group(2)

    def _is_key_value(self, line):
        return bool(self._key_value_regex.search(string=line))

    def _is_mapping_key(self, line):
        return bool(re.search(pattern=r'\W*(\w.*):\W*$', string=line))

    def _get_indent_level(self, line: str):
        if self._get_indent_regex is None:
            self._get_indent_regex = re.compile(pattern=r'^(([ ]*)\w)|^')
        match = self._get_indent_regex.search(string=line)
        if match.group(2) is not None:
            number_of_spaces = len(match.group(2))
            indent_level = number_of_spaces / self._indent
            # might make this a function so my code is more self documenting - checks if a number is an integer
            if int(indent_level) != indent_level:
                raise ParsingException(f'Expected a multiple of {self._indent} as the indent but got {number_of_spaces}')
        else:
            raise ParsingException(rf'''The line didn't match the pattern. line: "{line}". pattern: "^(([ ]*)\w)|^"''')
        return indent_level

    def _get_key(self, line: str):
        # TODO(ope) - might compile this regex to make it faster
        if self._key_regex is None:
            self._key_regex = re.compile(pattern=r'\W*(\w.*):\W*$')
        match = self._key_regex.search(string=line)
        if match:
            return match.group(1)
        else:
            raise ParsingException(f'Expected the line to match this pattern, but it didn\'t. line: {line!r}')
