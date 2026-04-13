import unittest

from markdown import (
    BlockType,
    block_to_block_type,
    markdown_to_blocks,
    markdown_to_html_node,
)


class TestToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_with_heading_to_blocks(self):
        md = """
# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
            ],
        )


class TestBlockToBlockType(unittest.TestCase):
    def test_headings(self):
        parsed = block_to_block_type("# Heading")
        self.assertEqual(parsed, BlockType.HEADING)
        parsed = block_to_block_type("###### Heading 6")
        self.assertEqual(parsed, BlockType.HEADING)
        parsed = block_to_block_type("####### Heading 7 not a thing")
        self.assertEqual(parsed, BlockType.PARAGRAPH)

    def test_code_block(self):
        parsed = block_to_block_type("```\nprint(I'm fake python code)```")
        self.assertEqual(parsed, BlockType.CODE)

    def test_quote_block(self):
        parsed = block_to_block_type("> a fake quote\n> that spans\n> multiple lines")
        self.assertEqual(parsed, BlockType.QUOTE)
        parsed = block_to_block_type("> a fake quote\nthat's malformed")
        self.assertEqual(parsed, BlockType.PARAGRAPH)

    def test_unordered_list(self):
        parsed = block_to_block_type("- an unordered list\n- on multiple lines")
        self.assertEqual(parsed, BlockType.UNORDERED_LIST)
        parsed = block_to_block_type("- an unordered list\nthat's malformed")
        self.assertEqual(parsed, BlockType.PARAGRAPH)

    def test_ordered_list(self):
        parsed = block_to_block_type("1. an unordered list\n2. on multiple lines")
        self.assertEqual(parsed, BlockType.ORDERED_LIST)
        parsed = block_to_block_type("1. an unordered list\nthat's malformed")
        self.assertEqual(parsed, BlockType.PARAGRAPH)
        parsed = block_to_block_type(
            "1. an unordered list\n3. that counts wrongly\n2. oops"
        )
        self.assertEqual(parsed, BlockType.PARAGRAPH)

    def test_paragraph(self):
        parsed = block_to_block_type("just some random paragraph")
        self.assertEqual(parsed, BlockType.PARAGRAPH)


class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
