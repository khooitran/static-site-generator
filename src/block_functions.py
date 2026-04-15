from enum import Enum


def markdown_to_blocks(markdown):
    new_blocks = []
    blocks = markdown.split("\n\n")
    for block in blocks:
        if block.strip():
            new_blocks.append(block.strip())

    return new_blocks


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block):
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE

    lines = block.split("\n")
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    ordered = True
    for i in range(len(lines)):
        if not lines[i].startswith(f"{i + 1}. "):
            ordered = False
    if ordered:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
