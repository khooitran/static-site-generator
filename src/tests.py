import unittest
from textnode import TextType, TextNode
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
from inline_functions import (
    text_node_to_html_node,
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from block_functions import markdown_to_blocks, block_to_block_type, BlockType


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


class TestSplitNodeDelimiter(unittest.TestCase):
    def test_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_beginning(self):
        node = TextNode("**This is bold** while this is not", TextType.TEXT)
        node2 = TextNode("_The whole thing is italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node, node2], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is bold", TextType.BOLD),
                TextNode(" while this is not", TextType.TEXT),
                TextNode("The whole thing is italic", TextType.ITALIC),
            ],
        )

    def test_error(self):
        node = TextNode("This **should not work", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter(node)


class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_error(self):
        matches = extract_markdown_images(
            "This is text with an ![image](this should not work"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is a link to [my portfolio](https://www.khooitran.com)."
        )
        self.assertEqual([("my portfolio", "https://www.khooitran.com")], matches)


class TextSplitImagesAndLinks(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )

        node2 = TextNode(
            "This is an ![image](https://i.imgur.com/khooi.png) and that's it!",
            TextType.TEXT,
        )

        node3 = TextNode(
            "![Image right away!](https://i.imgur.com/rightaway.jpeg)", TextType.TEXT
        )

        node4 = TextNode("[This](shouldn't work", TextType.TEXT)

        new_nodes = split_nodes_image([node, node2, node3, node4])

        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode("This is an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/khooi.png"),
                TextNode(" and that's it!", TextType.TEXT),
                TextNode(
                    "Image right away!",
                    TextType.IMAGE,
                    "https://i.imgur.com/rightaway.jpeg",
                ),
                TextNode("[This](shouldn't work", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode("[This is a link](https://www.khooitran.com)", TextType.TEXT)

        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [TextNode("This is a link", TextType.LINK, "https://www.khooitran.com")],
            new_nodes,
        )


class TextToTextNodes(unittest.TestCase):
    def test(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            text_to_textnodes(text),
        )


class MarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items


     
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

        self.assertEqual(block_to_block_type(blocks[0]), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(blocks[1]), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(blocks[2]), BlockType.UNORDERED_LIST)


class BlockToBlockType(unittest.TestCase):
    def test_block_to_block_type(self):
        text = """
```
// This is a code block
// With some comments in it
```

- Milk
- Cheese
- Spaghetti
- Bacon

This should just be a normal paragraph
With a line break in the middle. 

> As once says,
> This is a quote
> Something something

1. Do some programming
2. Learn Japanese
3. Teach Clusters
4. Do some housework

##### How to make spaghetti carbonara
"""
        blocks = markdown_to_blocks(text)

        self.assertListEqual(
            list(map(lambda block: block_to_block_type(block), blocks)),
            [
                BlockType.CODE,
                BlockType.UNORDERED_LIST,
                BlockType.PARAGRAPH,
                BlockType.QUOTE,
                BlockType.ORDERED_LIST,
                BlockType.HEADING,
            ],
        )


if __name__ == "__main__":
    unittest.main()
