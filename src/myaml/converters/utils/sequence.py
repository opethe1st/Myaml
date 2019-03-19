import re
from typing import List

from .mapping import get_key_value_strings


def get_element_strings(string: str) -> List[str]:
    return [
        re.sub(
            pattern=r'(\s*?)-(.*)',
            repl=r'\g<1> \g<2>',
            string=part
        )   for part in get_key_value_strings(string=string)
    ]
