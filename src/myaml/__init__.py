from myaml.converters.node_from_string import node_from_string
from myaml.converters.node_from_object import node_from_object
from myaml.converters.object_from_node import object_from_node
from myaml.converters.string_from_node import string_from_node
from myaml.utils.preprocessing import format_to_canonical_form


# not sure main.py is the appropriate thing here since this is a library
def load(string):
    string = format_to_canonical_form(string=string)
    node = node_from_string(string=string)
    return object_from_node(node)


def dump(obj):
    node = node_from_object(obj)
    return string_from_node(node)
