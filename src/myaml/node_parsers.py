import re


class KeyParser:

    def __init__(self):
        self.regex = re.compile(pattern=r'\W*(\w.*):\W*$')

    def is_type(self, line):
        return bool(self.regex.match(line))

    def parse(self, line):
        if self.regex.match(line):
            return self.regex.search(string=line).group(1)
        return None


class KeyValueParser:

    def __init__(self):
        self.regex = re.compile(pattern=r'\W*(\w.*): (\w.*)$')

    def is_type(self, line):
        return bool(self.regex.match(line))

    def parse(self, line):
        if self.regex.match(line):
            match = self.regex.search(string=line)
            return match.group(1), match.group(2)
        return None


class ArrayElementParser:

    def __init__(self):
        self.regex = re.compile(pattern=r'\W*-(\w.*)$')

    def is_type(self, line):
        return bool(self.regex.match(line))

    def parse(self, text):
        return 'key'
