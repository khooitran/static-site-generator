class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if self.props is None:
            return ""
        str = ""
        for key in self.props:
            str += f' {key}="{self.props[key]}"'

        return str

    def __repr__(self):
        str = []
        if self.tag:
            str.append(f"Tag: {self.tag}")
        if self.value is not None:
            str.append(f"value: {self.value}")
        if self.children:
            tag_list = [child.tag for child in self.children]
            str.append(f"children: {tag_list}")
        if self.props:
            str.append(f"props:{self.props_to_html()}")

        return ", ".join(str)
