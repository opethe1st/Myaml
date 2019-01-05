import unittest

from parameterized import parameterized

from .parser import Node
from .parser import NodeTypes


class NodeTestCase(unittest.TestCase):
    pass


class TestFromString(NodeTestCase):

    def test_scalar(self):
        pass

    def test_sequence(self):

        pass

    def test_mapping(self):
        pass

    @parameterized.expand([
        ('''''', {})
    ])
    def test_complex_mapping(self, string, expected):
        self.assertEqual(Node.from_string(string=string), Node(nodeType=NodeTypes.MAPPING, value=string))


class TestToNativeObject(NodeTestCase):
    pass


class TestgetNodeType(NodeTestCase):

    @parameterized.expand([
        ('''this is a value''', NodeTypes.SCALAR),
        ('''key: ''', NodeTypes.MAPPING),
        ('''key:''', NodeTypes.MAPPING),
        ('''    key: ''', NodeTypes.MAPPING),
        ('''key: value''', NodeTypes.MAPPING),
        ('''key:
    key2: value''', NodeTypes.MAPPING),
        ('''- value
- value2
- value4''', NodeTypes.SEQUENCE),
        ('''- value
- key: value2
- value4''', NodeTypes.SEQUENCE),
    ])
    def test__get_node_type(self, string, expected):
        self.assertEqual(Node._get_node_type(string=string), expected)


class TestGetKey(NodeTestCase):
    @parameterized.expand([
        ('''key: value''', 'key'),
        ('''key:
    key2: value''', 'key'),
        ('''key:
''', 'key')
    ])
    def test_get_key(self, string, expected):
        self.assertEqual(Node.from_string(string=string).get_key(), expected)


class TestGetValue(NodeTestCase):
    @parameterized.expand([
        ('''key: value''', 'value'),
        ('''key:
    key2: value''', 'key2: value'),
        ('''key:
''', {})
    ])
    def test_get_value(self, string, expected):
        self.assertEqual(Node.from_string(string=string).get_key(), expected)


class TestgetKeyValueStrings(NodeTestCase):
    pass


class TestgetElementStrings(NodeTestCase):
    pass
