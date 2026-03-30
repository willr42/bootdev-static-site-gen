import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.Bold)
        node2 = TextNode("This is a text node", TextType.Bold)
        self.assertEqual(node, node2)

    def test_unequal_string(self):
        node = TextNode("This is a text node", TextType.Bold)
        node2 = TextNode("This is another", TextType.Bold)
        self.assertNotEqual(node, node2)

    def test_unmatching_url(self):
        node = TextNode("This is a text node", TextType.Bold, "https://example.com")
        node2 = TextNode("This is a text node", TextType.Bold)
        self.assertNotEqual(node, node2)

    def test_unmatching_texttype(self):
        node = TextNode("This is a text node", TextType.Bold)
        node2 = TextNode("This is a text node", TextType.Italic)
        self.assertNotEqual(node, node2)

    def test_all_unmatching(self):
        node = TextNode("This is a text node", TextType.Bold, "https://example.com")
        node2 = TextNode("This is another", TextType.Italic, None)
        self.assertNotEqual(node, node2)


class TestTextToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.Text)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.Bold)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.to_html(), "<b>This is a bold node</b>")
