import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        node3 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node3)
        node4 = TextNode("This is one text node", TextType.BOLD)
        self.assertNotEqual(node, node4)
        node5 = TextNode(
            "This is a link to my portfolio", TextType.LINK, "https://www.khooitran.com"
        )
        self.assertNotEqual(node, node5)


class TestHTMLNode(unittest.TestCase):
    def test_props(self):
        node = HTMLNode("p", "Hello World!")
        self.assertEqual(node.props_to_html(), "")

        node2 = HTMLNode(
            "a",
            "this link to my portfolio",
            props={"href": "https://www.khooitran.com", "target": "_blank"},
        )
        self.assertEqual(
            node2.props_to_html(), ' href="https://www.khooitran.com" target="_blank"'
        )

        node3 = HTMLNode("div", children=[node, node2])
        node4 = HTMLNode(value="This node doesn't have a tag")


class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        node = LeafNode("p", "Hello World!")
        self.assertEqual(node.to_html(), "<p>Hello World!</p>")

        node2 = LeafNode(None, "This one doesn't have a tag")
        self.assertEqual(node2.to_html(), "This one doesn't have a tag")

        node3 = LeafNode(
            "a",
            "Click here!",
            {"href": "https://www.khooitran.com", "target": "_blank"},
        )
        self.assertEqual(
            node3.to_html(),
            '<a href="https://www.khooitran.com" target="_blank">Click here!</a>',
        )


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )


if __name__ == "__main__":
    unittest.main()
