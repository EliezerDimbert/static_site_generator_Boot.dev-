from nodes.htmlnode import LeafNode
import unittest

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        res = node.to_html()
        self.assertEqual(res, "<p>Hello, world!</p>")
    def test_no_value(self):
        with self.assertRaises(ValueError):
            node = LeafNode(None, None, None).to_html() # type: ignore
    def test_no_tag(self):
        node = LeafNode(None, 'Hello, world', None)
        res = node.to_html()
        self.assertEqual(res, 'Hello, world')

if __name__ == "__main__":
    unittest.main()