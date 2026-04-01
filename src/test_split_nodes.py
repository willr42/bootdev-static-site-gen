import unittest

from split_nodes import split_nodes_delimiter, split_nodes_image, split_nodes_link
from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code_node(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        nodelist = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(nodelist, new_nodes)

    def test_bold_node(self):
        node = TextNode("This is text with a **bold block** word", TextType.TEXT)
        nodelist = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold block", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(nodelist, new_nodes)


class TestSplitNodesLink(unittest.TestCase):
    def test_code_node(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        nodelist = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
        ]
        new_nodes = split_nodes_link([node])
        self.assertListEqual(nodelist, new_nodes)


class TestSplitNodesImage(unittest.TestCase):
    def test_image_node(self):
        node = TextNode(
            "This is text with an image ![to boot dev](https://www.boot.dev/img/logo.png) and ![to youtube](https://www.youtube.com/img/logo.png)",
            TextType.TEXT,
        )
        nodelist = [
            TextNode("This is text with an image ", TextType.TEXT),
            TextNode(
                "to boot dev", TextType.IMAGE, "https://www.boot.dev/img/logo.png"
            ),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.IMAGE, "https://www.youtube.com/img/logo.png"
            ),
        ]
        new_nodes = split_nodes_image([node])
        self.assertListEqual(nodelist, new_nodes)
