from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Parent node does not have a tag")

        if not self.children:
            raise ValueError("Parent node does not have children")

        str = [f"<{self.tag}{self.props_to_html()}>"]

        for child in self.children:
            str.append(child.to_html())

        str.append(f"</{self.tag}>")

        return "".join(str)
