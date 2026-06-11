import unittest
from nodes.htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_empty_eq(self):
        node1 = HTMLNode()
        node2 = HTMLNode()
        self.assertEqual(node1, node2)
    def test_full_eq(self):
        node1 = HTMLNode('tag', 'val', [HTMLNode()], {'href': 'https://www.google.com'})
        node2 = HTMLNode('tag', 'val', [HTMLNode()], {'href': 'https://www.google.com'})
        self.assertEqual(node1, node2)
    def test_props_to_html(self):
        node = HTMLNode('tag', 'val', [HTMLNode()], {'href': 'https://www.google.com'})
        props_res = ' href="https://www.google.com"'
        self.assertEqual(node.props_to_html(), props_res)

if __name__ == "__main__":
    unittest.main()