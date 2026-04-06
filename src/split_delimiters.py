from textnode import TextType, TextNode


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
