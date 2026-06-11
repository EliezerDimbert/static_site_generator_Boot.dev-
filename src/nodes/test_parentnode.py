from nodes.htmlnode import ParentNode, LeafNode
import unittest

class TestParentNode(unittest.TestCase):
    def test_to_html_with_child(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_childen(self):
        child_node_1 = LeafNode("span", "child_1")
        child_node_2 = LeafNode("bold", "child_2")
        parent_node = ParentNode("div", [child_node_1, child_node_2])
        self.assertEqual(parent_node.to_html(), "<div><span>child_1</span><bold>child_2</bold></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

if __name__ == "__main__":
    unittest.main()