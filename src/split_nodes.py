from textnode import TextNode, TextType, extract_markdown_images, extract_markdown_links


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
        # non-text nodes pass through unchanged
        if n.text_type != TextType.TEXT:
            new_nodes.append(n)
            continue
        links = extract_markdown_links(n.text)

        # if none found, go to next node
        if len(links) == 0:
            continue

        remaining = n.text
        for link in links:
            link_text = link[0]
            link_url = link[1]

            # split on first occasion of link
            sections = remaining.split(f"[{link_text}]({link_url})", 1)

            # only add proceeding text if non-empty
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], n.text_type))

            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))

            # carry forward leftover text
            remaining = sections[1]

        # add trailing text from node
        if len(remaining) > 0:
            new_nodes.append(TextNode(remaining, n.text_type))

    return new_nodes


def split_nodes_image(old_nodes: list[TextNode]):
    new_nodes: list[TextNode] = []
    for n in old_nodes:
        # non-text nodes pass through unchanged
        if n.text_type != TextType.TEXT:
            new_nodes.append(n)
            continue
        images = extract_markdown_images(n.text)

        # if none found, go to next node
        if len(images) == 0:
            continue

        remaining = n.text
        for image in images:
            alt_text = image[0]
            image_url = image[1]

            # split on first occasion of image
            sections = remaining.split(f"![{alt_text}]({image_url})", 1)

            # only add proceeding text if non-empty
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], n.text_type))

            new_nodes.append(TextNode(alt_text, TextType.IMAGE, image_url))

            # carry forward leftover text
            remaining = sections[1]

        # add trailing text from node
        if len(remaining) > 0:
            new_nodes.append(TextNode(remaining, n.text_type))

    return new_nodes
