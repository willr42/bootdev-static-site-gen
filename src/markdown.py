import re

from enum import Enum

from htmlnode import LeafNode, ParentNode
from text_to_nodes import text_to_textnodes
from textnode import text_nodes_to_html_nodes


class BlockType(Enum):
    HEADING = "heading"
    PARAGRAPH = "paragraph"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown: str):
    blocks = list(
        filter(lambda x: x != "", map(lambda x: x.strip(), markdown.split("\n\n")))
    )
    return blocks


def block_to_block_type(block: str):
    if re.match(r"#{1,6} ", block):
        return BlockType.HEADING
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE

    valid_quote = True
    valid_unordered_list = True
    valid_ordered_list = True
    i = 1
    for line in block.split("\n"):
        if not line.startswith(">"):
            valid_quote = False
        if not line.startswith("- "):
            valid_unordered_list = False
        if not line.startswith(f"{i}. ") or int(line[0]) < i:
            valid_ordered_list = False
        i += 1

    if valid_quote:
        return BlockType.QUOTE
    if valid_unordered_list:
        return BlockType.UNORDERED_LIST
    if valid_ordered_list:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown: str):
    blocks = markdown_to_blocks(markdown)
    node_list: list[ParentNode] = []
    for block in blocks:
        type = block_to_block_type(block)
        tag = type_to_tag_string(type, block)
        if type != BlockType.CODE:
            child_text_nodes = text_to_children(
                " ".join(line.strip() for line in block.split("\n"))
            )
            children = text_nodes_to_html_nodes(child_text_nodes)
            node = ParentNode(tag, children)
            node_list.append(node)
        else:
            text = "\n".join(
                # get inner code, split on \n, strip whitespace
                line.strip()
                for line in block.split("```")[1].split("\n")
                # left-strip leading newline on ``` codeblock
            ).lstrip("\n")
            inner = LeafNode("code", text)
            outer = ParentNode("pre", [inner])
            node_list.append(outer)

    return ParentNode("div", node_list)


def type_to_tag_string(type: BlockType, block: str):
    match type:
        case BlockType.HEADING:
            leading_hashes = block.split(" ", 1)
            h_level = leading_hashes[0].count("#")
            return f"h{h_level}"
        case BlockType.PARAGRAPH:
            return "p"
        case BlockType.CODE:
            return "code"
        case BlockType.QUOTE:
            return "blockquote"
        case BlockType.UNORDERED_LIST:
            return "ul"
        case BlockType.ORDERED_LIST:
            return "ol"
        case _:
            raise Exception("somehow unsupported BlockType")


def text_to_children(inp: str):
    return text_to_textnodes(inp)
