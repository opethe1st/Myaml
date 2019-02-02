import re

from myaml.constants import NUM_SPACES_IN_INDENT

def format_to_canonical_form(string):
    string = _remove_comments(string=string)
    currentIndentSize = _detect_indentation(string=string)
    return _replace_indent_size(string=string, oldIndentSize=currentIndentSize, newIndentSize=NUM_SPACES_IN_INDENT)


def _detect_indentation(string):
    for line in string.split('\n'):
        if line:
            indentSize = _get_indent_size(line=line)
            if indentSize:
                return indentSize
    return NUM_SPACES_IN_INDENT


def _get_indent_size(line):
    match = re.match(string=line, pattern=r'(^-\s+)\S')
    if match:
        return len(match.group(1))
    match = re.match(string=line, pattern=r'(^\s+)\S')
    if match:
        return len(match.group(1))
    return None


def _remove_comments(string):
    lines = string.split('\n')
    lines = [re.sub(string=line, pattern=r'#.*?$', repl='') for line in lines]
    lines = [line for line in lines if not re.match(string=line, pattern=r'^\s*$')]
    return "\n".join(lines)


def _replace_indent_size(string, oldIndentSize, newIndentSize):
    lines = string.split('\n')
    # this means that if # or $ are present in my text, I am going to have problems
    lines = [re.sub(string=line, pattern=r'-'+' '*(oldIndentSize-1), repl='#') for line in lines]
    lines = [re.sub(string=line, pattern=r' '*oldIndentSize, repl='$') for line in lines]
    lines = [re.sub(string=line, pattern=r'\$', repl=' '*newIndentSize) for line in lines]
    lines = [re.sub(string=line, pattern=r'#', repl='-'+' '*(newIndentSize-1)) for line in lines]
    return "\n".join(lines)
