import re

from enum import Enum


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
