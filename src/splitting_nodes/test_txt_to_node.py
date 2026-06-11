import unittest
from src.splitting_nodes.txt_to_node import text_to_textnodes
from nodes.textnode import TextNode, TextType


class TestTextToTextNodes(unittest.TestCase):
    def test_plain_text(self):
        result = text_to_textnodes("Just plain text")
        self.assertListEqual(
            [TextNode("Just plain text", TextType.TEXT)],
            result,
        )

    def test_single_bold(self):
        result = text_to_textnodes("This is **bold** text")
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
            result,
        )

    def test_single_italic(self):
        result = text_to_textnodes("This is _italic_ text")
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.TEXT),
            ],
            result,
        )

    def test_single_code(self):
        result = text_to_textnodes("This is `code` text")
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" text", TextType.TEXT),
            ],
            result,
        )

    def test_multiple_bold(self):
        result = text_to_textnodes("**bold1** and **bold2**")
        self.assertListEqual(
            [
                TextNode("bold1", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("bold2", TextType.BOLD),
            ],
            result,
        )

    def test_multiple_italic(self):
        result = text_to_textnodes("_italic1_ and _italic2_")
        self.assertListEqual(
            [
                TextNode("italic1", TextType.ITALIC),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic2", TextType.ITALIC),
            ],
            result,
        )

    def test_bold_and_italic(self):
        result = text_to_textnodes("**bold** and _italic_")
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            result,
        )

    def test_bold_and_code(self):
        result = text_to_textnodes("**bold** and `code`")
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("code", TextType.CODE),
            ],
            result,
        )

    def test_italic_and_code(self):
        result = text_to_textnodes("_italic_ and `code`")
        self.assertListEqual(
            [
                TextNode("italic", TextType.ITALIC),
                TextNode(" and ", TextType.TEXT),
                TextNode("code", TextType.CODE),
            ],
            result,
        )

    def test_all_formatting_types(self):
        result = text_to_textnodes("**bold** _italic_ `code` all together")
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" all together", TextType.TEXT),
            ],
            result,
        )

    def test_single_image(self):
        result = text_to_textnodes("This has an ![image](https://example.com/img.png)")
        self.assertListEqual(
            [
                TextNode("This has an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://example.com/img.png"),
            ],
            result,
        )

    def test_multiple_images(self):
        result = text_to_textnodes("![img1](url1.png) and ![img2](url2.png)")
        self.assertListEqual(
            [
                TextNode("img1", TextType.IMAGE, "url1.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode("img2", TextType.IMAGE, "url2.png"),
            ],
            result,
        )

    def test_single_link(self):
        result = text_to_textnodes("This is a [link](https://example.com)")
        self.assertListEqual(
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
            ],
            result,
        )

    def test_multiple_links(self):
        result = text_to_textnodes("[link1](url1) and [link2](url2)")
        self.assertListEqual(
            [
                TextNode("link1", TextType.LINK, "url1"),
                TextNode(" and ", TextType.TEXT),
                TextNode("link2", TextType.LINK, "url2"),
            ],
            result,
        )

    def test_image_and_link(self):
        result = text_to_textnodes("![image](img.png) and [link](url.com)")
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "img.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode("link", TextType.LINK, "url.com"),
            ],
            result,
        )

    def test_formatting_with_images(self):
        result = text_to_textnodes("**bold** text with ![image](url.png)")
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" text with ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "url.png"),
            ],
            result,
        )

    def test_formatting_with_links(self):
        result = text_to_textnodes("**bold** text with [link](url)")
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" text with ", TextType.TEXT),
                TextNode("link", TextType.LINK, "url"),
            ],
            result,
        )

    def test_all_types_combined(self):
        result = text_to_textnodes("**bold** _italic_ `code` ![image](img.png) [link](url)")
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "img.png"),
                TextNode(" ", TextType.TEXT),
                TextNode("link", TextType.LINK, "url"),
            ],
            result,
        )

    def test_nested_formatting_not_parsed(self):
        # Formatting delimiters are only processed on TEXT nodes
        # Once text is marked as BOLD, inner delimiters are NOT processed
        result = text_to_textnodes("**bold with `code` inside**")
        self.assertListEqual(
            [
                TextNode("bold with `code` inside", TextType.BOLD),
            ],
            result,
        )

    def test_text_starting_with_bold(self):
        result = text_to_textnodes("**bold** at start")
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" at start", TextType.TEXT),
            ],
            result,
        )

    def test_text_ending_with_bold(self):
        result = text_to_textnodes("Ending with **bold**")
        self.assertListEqual(
            [
                TextNode("Ending with ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
            ],
            result,
        )

    def test_text_starting_with_image(self):
        result = text_to_textnodes("![image](url.png) at start")
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "url.png"),
                TextNode(" at start", TextType.TEXT),
            ],
            result,
        )

    def test_text_ending_with_image(self):
        result = text_to_textnodes("Ending with ![image](url.png)")
        self.assertListEqual(
            [
                TextNode("Ending with ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "url.png"),
            ],
            result,
        )

    def test_text_starting_with_link(self):
        result = text_to_textnodes("[link](url) at start")
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "url"),
                TextNode(" at start", TextType.TEXT),
            ],
            result,
        )

    def test_text_ending_with_link(self):
        result = text_to_textnodes("Ending with [link](url)")
        self.assertListEqual(
            [
                TextNode("Ending with ", TextType.TEXT),
                TextNode("link", TextType.LINK, "url"),
            ],
            result,
        )

    def test_consecutive_bold(self):
        result = text_to_textnodes("**bold1** **bold2**")
        self.assertListEqual(
            [
                TextNode("bold1", TextType.BOLD),
                TextNode(" ", TextType.TEXT),
                TextNode("bold2", TextType.BOLD),
            ],
            result,
        )

    def test_consecutive_images(self):
        result = text_to_textnodes("![img1](url1)![img2](url2)")
        self.assertListEqual(
            [
                TextNode("img1", TextType.IMAGE, "url1"),
                TextNode("img2", TextType.IMAGE, "url2"),
            ],
            result,
        )

    def test_consecutive_links(self):
        result = text_to_textnodes("[link1](url1)[link2](url2)")
        self.assertListEqual(
            [
                TextNode("link1", TextType.LINK, "url1"),
                TextNode("link2", TextType.LINK, "url2"),
            ],
            result,
        )

    def test_empty_string(self):
        result = text_to_textnodes("")
        # Empty string results in empty list (empty text segments are skipped)
        self.assertListEqual(
            [],
            result,
        )

    def test_only_bold(self):
        result = text_to_textnodes("**bold**")
        self.assertListEqual(
            [TextNode("bold", TextType.BOLD)],
            result,
        )

    def test_only_italic(self):
        result = text_to_textnodes("_italic_")
        self.assertListEqual(
            [TextNode("italic", TextType.ITALIC)],
            result,
        )

    def test_only_code(self):
        result = text_to_textnodes("`code`")
        self.assertListEqual(
            [TextNode("code", TextType.CODE)],
            result,
        )

    def test_only_image(self):
        result = text_to_textnodes("![alt](url)")
        self.assertListEqual(
            [TextNode("alt", TextType.IMAGE, "url")],
            result,
        )

    def test_only_link(self):
        result = text_to_textnodes("[text](url)")
        self.assertListEqual(
            [TextNode("text", TextType.LINK, "url")],
            result,
        )

    def test_complex_real_world_example(self):
        text = "Check out **bold text** with _italics_ and `code blocks`. Also see ![example image](https://example.com/img.png) and this [helpful link](https://example.com)!"
        result = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("Check out ", TextType.TEXT),
                TextNode("bold text", TextType.BOLD),
                TextNode(" with ", TextType.TEXT),
                TextNode("italics", TextType.ITALIC),
                TextNode(" and ", TextType.TEXT),
                TextNode("code blocks", TextType.CODE),
                TextNode(". Also see ", TextType.TEXT),
                TextNode("example image", TextType.IMAGE, "https://example.com/img.png"),
                TextNode(" and this ", TextType.TEXT),
                TextNode("helpful link", TextType.LINK, "https://example.com"),
                TextNode("!", TextType.TEXT),
            ],
            result,
        )

    def test_whitespace_preservation(self):
        result = text_to_textnodes("  spaces  **bold**  more spaces  ")
        self.assertListEqual(
            [
                TextNode("  spaces  ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode("  more spaces  ", TextType.TEXT),
            ],
            result,
        )


if __name__ == "__main__":
    unittest.main()
