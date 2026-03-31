import unittest

from textnode import (
    TextNode,
    TextType,
    extract_markdown_images,
    extract_markdown_links,
    text_node_to_html_node,
)


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_unequal_string(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is another", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_unmatching_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://example.com")
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_unmatching_texttype(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_all_unmatching(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://example.com")
        node2 = TextNode("This is another", TextType.ITALIC, None)
        self.assertNotEqual(node, node2)


class TestTextToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.to_html(), "<b>This is a bold node</b>")


class TestExtractImages(unittest.TestCase):
    def test_image_extract(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)


class TextExtractLinks(unittest.TestCase):
    def test_link_extract(self):
        matches = extract_markdown_links(
            "This is text with a [link](http://example.com)"
        )
        self.assertListEqual([("link", "http://example.com")], matches)

    def test_multiple_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            matches,
        )
