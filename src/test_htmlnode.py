import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("a", "This is a link value", [], {"href": "http://example.com"})
        node2 = HTMLNode(
            "a", "This is a link value", [], {"href": "http://example.com"}
        )
        self.assertEqual(node, node2)

    def test_unequal_tags(self):
        node = HTMLNode("a", "This is a link value", [], {"href": "http://example.com"})
        node2 = HTMLNode(
            "b", "This is a link value", [], {"href": "http://example.com"}
        )
        self.assertNotEqual(node, node2)

    def test_props_to_html(self):
        node = HTMLNode("a", "This is a link value", [], {"href": "http://example.com"})
        self.assertEqual(node.props_to_html(), "href=http://example.com")


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_p_with_props(self):
        node = LeafNode("p", "Hello, world!", {"test": "value"})
        self.assertEqual(node.to_html(), "<p test=value>Hello, world!</p>")

    def test_leaf_to_raw_value(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_props(self):
        child_node = LeafNode("span", "child", {"style": "'color:black;'"})
        parent_node = ParentNode("div", [child_node], {"title": "parent"})
        self.assertEqual(
            parent_node.to_html(),
            "<div title=parent><span style='color:black;'>child</span></div>",
        )
