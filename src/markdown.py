def markdown_to_blocks(markdown: str):
    blocks = list(
        filter(lambda x: x != "", map(lambda x: x.strip(), markdown.split("\n\n")))
    )
    return blocks
