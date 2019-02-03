import re

from .mapping import (
    get_key_value_strings,
)


def get_element_strings(string):
    return [
        re.sub(
            pattern=r'(\s*?)-(.*)',
            repl=r'\g<1> \g<2>',
            string=part
        )   for part in get_key_value_strings(string=string)
    ]
