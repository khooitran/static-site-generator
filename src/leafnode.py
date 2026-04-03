from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Leaf node has no value")

        if self.tag is None:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        str = []
        if self.tag:
            str.append(f"Tag: {self.tag}")
        if self.value is not None:
            str.append(f"value: {self.value}")
        if self.props:
            str.append(f"props: {self.props_to_html()}")

        return ", ".join(str)
