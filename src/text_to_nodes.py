from split_nodes import split_nodes_delimiter, split_nodes_image, split_nodes_link
from textnode import TextNode, TextType, text_node_to_html_node


def text_to_textnodes(text: str):
    nodes_with_images = split_nodes_image([TextNode(text, TextType.TEXT)])
    nodes_with_links = split_nodes_link(nodes_with_images)
    nodes_with_html = split_all_elements(nodes_with_links)
    return nodes_with_html


def split_all_elements(text_nodes):
    resolved_code = split_nodes_delimiter(text_nodes, "`", TextType.CODE)
    resolved_bold = split_nodes_delimiter(resolved_code, "**", TextType.BOLD)
    resolved_italic = split_nodes_delimiter(resolved_bold, "_", TextType.ITALIC)

    return resolved_italic
