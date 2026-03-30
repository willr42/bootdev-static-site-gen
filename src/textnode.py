from enum import Enum

from htmlnode import LeafNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str | None = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, value):
        if (
            self.text == value.text
            and self.text_type == value.text_type
            and self.url == value.url
        ):
            return True
        return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def text_node_to_html_node(text_node: TextNode):
    """Turns a given TextNode to a LeafNode"""
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("somehow unsupported TextType")


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
):
    """Splits up a TEXT TextNode into new TextNodes based on a delimiter"""
    new_nodes: list[TextNode] = []
    for n in old_nodes:
        if n.text_type != TextType.TEXT:
            new_nodes.append(n)
            continue
        parts = n.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise Exception("non-valid Markdown syntax")
        for i, part in enumerate(parts):
            if i % 2 != 0:
                new_nodes.append(TextNode(part, text_type))
            else:
                new_nodes.append(TextNode(part, n.text_type))

    return new_nodes
