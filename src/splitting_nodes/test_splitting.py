import unittest
from src.splitting_nodes.splitting import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link
from nodes.textnode import TextNode, TextType

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code_block(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
                                    TextNode("This is text with a ", TextType.TEXT),
                                    TextNode("code block", TextType.CODE),
                                    TextNode(" word", TextType.TEXT),
                                    ])

    def test_bold_delimiter(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ])

    def test_italic_delimiter(self):
        node = TextNode("This is _italic_ text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ])

    def test_multiple_delimiters(self):
        node = TextNode("**bold1** and **bold2**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("bold1", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("bold2", TextType.BOLD),
        ])

    def test_no_delimiter(self):
        node = TextNode("This is plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [node])

    def test_non_text_node_unchanged(self):
        node = TextNode("This is **bold**", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [node])

    def test_empty_delimiter_content(self):
        # Empty delimiter content creates a split but the empty node is skipped
        node = TextNode("This is `` empty code", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is ", TextType.TEXT),
            TextNode(" empty code", TextType.TEXT),
        ])

    def test_multiple_nodes(self):
        nodes = [
            TextNode("This is **bold** text", TextType.TEXT),
            TextNode("Already bold", TextType.BOLD),
        ]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
            TextNode("Already bold", TextType.BOLD),
        ])

    def test_uneven_delimiters_raises_error(self):
        node = TextNode("This is unclosed **bold", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_consecutive_delimiters(self):
        node = TextNode("Start **bold** **bold2** end", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("Start ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" ", TextType.TEXT),
            TextNode("bold2", TextType.BOLD),
            TextNode(" end", TextType.TEXT),
        ])


class TestExtractImages(unittest.TestCase):
    def test_extract_single_image(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_multiple_images(self):
        matches = extract_markdown_images(
            "![first](url1.png) and ![second](url2.png)"
        )
        self.assertListEqual([("first", "url1.png"), ("second", "url2.png")], matches)

    def test_extract_no_images(self):
        matches = extract_markdown_images("Just plain text here")
        self.assertListEqual([], matches)

    def test_extract_image_with_complex_alt(self):
        matches = extract_markdown_images("![alt text with spaces](https://example.com/image.png)")
        self.assertListEqual([("alt text with spaces", "https://example.com/image.png")], matches)

    def test_extract_image_empty_alt(self):
        matches = extract_markdown_images("![](https://example.com/image.png)")
        self.assertListEqual([("", "https://example.com/image.png")], matches)


class TestExtractLinks(unittest.TestCase):
    def test_extract_single_link(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://example.com)"
        )
        self.assertListEqual([("link", "https://example.com")], matches)

    def test_extract_multiple_links(self):
        matches = extract_markdown_links(
            "[first link](url1) and [second link](url2)"
        )
        self.assertListEqual([("first link", "url1"), ("second link", "url2")], matches)

    def test_extract_no_links(self):
        matches = extract_markdown_links("Just plain text here")
        self.assertListEqual([], matches)

    def test_extract_link_with_complex_text(self):
        matches = extract_markdown_links("[click here for more info](https://example.com/page)")
        self.assertListEqual([("click here for more info", "https://example.com/page")], matches)

    def test_extract_link_empty_text(self):
        matches = extract_markdown_links("[](https://example.com)")
        self.assertListEqual([("", "https://example.com")], matches)

    def test_extract_mixed_with_images(self):
        text = "![image](img.png) and [link](url.com)"
        links = extract_markdown_links(text)
        images = extract_markdown_images(text)
        # Note: extract_markdown_links extracts all [...] patterns, including image alt text
        self.assertListEqual([("image", "img.png"), ("link", "url.com")], links)
        self.assertListEqual([("image", "img.png")], images)


class TestSplitNodesImage(unittest.TestCase):
    def test_split_single_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_multiple_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_no_images(self):
        node = TextNode("This is plain text with no images", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_image_at_start(self):
        node = TextNode("![image](url.png) followed by text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "url.png"),
                TextNode(" followed by text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_image_at_end(self):
        node = TextNode("Text followed by ![image](url.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Text followed by ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "url.png"),
            ],
            new_nodes,
        )

    def test_split_non_text_node_unchanged(self):
        node = TextNode("![image](url.png)", TextType.BOLD)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_mixed_nodes(self):
        nodes = [
            TextNode("Text with ![image](url.png)", TextType.TEXT),
            TextNode("Already formatted", TextType.BOLD),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "url.png"),
                TextNode("Already formatted", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_split_consecutive_images(self):
        node = TextNode("![img1](url1.png)![img2](url2.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("img1", TextType.IMAGE, "url1.png"),
                TextNode("img2", TextType.IMAGE, "url2.png"),
            ],
            new_nodes,
        )


class TestSplitNodesLink(unittest.TestCase):
    def test_split_single_link(self):
        node = TextNode(
            "This is text with a [link](https://example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
            ],
            new_nodes,
        )

    def test_split_multiple_links(self):
        node = TextNode(
            "Check [link1](url1) and [link2](url2)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Check ", TextType.TEXT),
                TextNode("link1", TextType.LINK, "url1"),
                TextNode(" and ", TextType.TEXT),
                TextNode("link2", TextType.LINK, "url2"),
            ],
            new_nodes,
        )

    def test_split_no_links(self):
        node = TextNode("This is plain text with no links", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_link_at_start(self):
        node = TextNode("[link](url) followed by text", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "url"),
                TextNode(" followed by text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_link_at_end(self):
        node = TextNode("Text followed by [link](url)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Text followed by ", TextType.TEXT),
                TextNode("link", TextType.LINK, "url"),
            ],
            new_nodes,
        )

    def test_split_non_text_node_unchanged(self):
        node = TextNode("[link](url)", TextType.BOLD)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_consecutive_links(self):
        node = TextNode("[link1](url1)[link2](url2)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link1", TextType.LINK, "url1"),
                TextNode("link2", TextType.LINK, "url2"),
            ],
            new_nodes,
        )

    def test_split_mixed_nodes(self):
        nodes = [
            TextNode("Text with [link](url)", TextType.TEXT),
            TextNode("Already bold", TextType.BOLD),
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("link", TextType.LINK, "url"),
                TextNode("Already bold", TextType.BOLD),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()