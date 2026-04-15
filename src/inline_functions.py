import re
from textnode import TextType, TextNode
from leafnode import LeafNode


def text_node_to_html_node(text_node):
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
            raise Exception("Text type not found")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            parts = node.text.split(delimiter)
            if len(parts) % 2 == 0:
                raise Exception("closing delimiter not found")
            for i in range(0, len(parts)):
                if i % 2 == 0:
                    if parts[i]:
                        new_nodes.append(TextNode(parts[i], TextType.TEXT))
                else:
                    if parts[i]:
                        new_nodes.append(TextNode(parts[i], text_type))

    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if not node.text:
            continue

        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        matches = extract_markdown_images(node.text)
        if not matches:
            new_nodes.append(node)

        else:
            node_to_split = node.text
            for match in matches:
                image_alt = match[0]
                image_link = match[1]
                sections = node_to_split.split(f"![{image_alt}]({image_link})", 1)
                if sections[0]:
                    new_nodes.append(TextNode(f"{sections[0]}", TextType.TEXT))
                new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
                node_to_split = sections[1]

            if node_to_split:
                new_nodes.append(TextNode(node_to_split, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if not node.text:
            continue

        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        matches = extract_markdown_links(node.text)
        if not matches:
            new_nodes.append(node)

        else:
            node_to_split = node.text
            for match in matches:
                alt = match[0]
                link = match[1]
                sections = node_to_split.split(f"[{alt}]({link})", 1)
                if sections[0]:
                    new_nodes.append(TextNode(f"{sections[0]}", TextType.TEXT))
                new_nodes.append(TextNode(alt, TextType.LINK, link))
                node_to_split = sections[1]

            if node_to_split:
                new_nodes.append(TextNode(node_to_split, TextType.TEXT))

    return new_nodes


def text_to_textnodes(text):
    text_node = TextNode(text, TextType.TEXT)
    return split_nodes_link(
        split_nodes_image(
            split_nodes_delimiter(
                split_nodes_delimiter(
                    split_nodes_delimiter([text_node], "**", TextType.BOLD),
                    "_",
                    TextType.ITALIC,
                ),
                "`",
                TextType.CODE,
            )
        )
    )
