from textnode import TextNode, TextType, extract_markdown_links


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


def split_nodes_link(old_nodes: list[TextNode]):
    new_nodes: list[TextNode] = []
    for n in old_nodes:
        if n.text_type != TextType.TEXT:
            new_nodes.append(n)
            continue
        links = extract_markdown_links(n.text)

        remaining = n.text
        if len(links) == 0:
            continue

        for link in links:
            image_alt = link[0]
            image_link = link[1]

            sections = remaining.split(f"[{image_alt}]({image_link})", 1)

            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], n.text_type))

            new_nodes.append(TextNode(image_alt, TextType.LINK, image_link))

            remaining = sections[1]

        if len(remaining) > 0:
            new_nodes.append(TextNode(remaining, n.text_type))

    return new_nodes


#
def split_nodes_image(old_nodes: list[TextNode]):
    new_nodes: list[TextNode] = []
    pass
