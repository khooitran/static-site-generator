import unittest
from textnode import TextType, TextNode
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
from texttohtml import text_node_to_html_node


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

        node3 = HTMLNode("a", props={"href": "https://www.boot.dev"})
        self.assertEqual(node3.props_to_html(), ' href="https://www.boot.dev"')


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

    def test_to_html_with_multiple_children(self):
        child_node1 = LeafNode("p", "This link")
        child_node2 = LeafNode(
            "a", "Click here", {"href": "https://www.khooitran.com", "target": "_blank"}
        )
        parent_node = ParentNode("div", [child_node1, child_node2])
        grandparent_node = ParentNode("section", [parent_node])

        self.assertEqual(
            grandparent_node.to_html(),
            '<section><div><p>This link</p><a href="https://www.khooitran.com" target="_blank">Click here</a></div></section>',
        )

    def test_errors(self):
        parent_node = ParentNode("div", [])
        with self.assertRaises(ValueError):
            parent_node.to_html()


class TestTextToHTML(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_to_html(self):
        node = TextNode("This is some bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "<b>This is some bold text</b>")

    def test_image(self):
        node = TextNode(
            "This is the alt description",
            TextType.IMAGE,
            "https://www.img.com/some_image",
        )
        html_node = text_node_to_html_node(node)
        self.assertEqual(
            html_node.to_html(),
            '<img src="https://www.img.com/some_image" alt="This is the alt description"></img>',
        )

    def test_error(self):
        node = TextNode("This is not a text type", TextType.TEXT)
        node.text_type = "not_a_valid_type"
        with self.assertRaises(Exception):
            text_node_to_html_node(node)


if __name__ == "__main__":
    unittest.main()
