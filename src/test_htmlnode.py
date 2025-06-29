import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode 
from textnode import TextNode, TextType
from helper_func import text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("Tag", "10", None, {"a": "aaaa", "b": "bbbb"})
        str = ' a="aaaa" b="bbbb"'
        self.assertEqual(node.props_to_html(), str)

    def test_props_to_html2(self):
        node = HTMLNode()
        self.assertNotEqual(node.props_to_html(), None)

    def test_props_to_html3(self):
        node = HTMLNode("Tag", "10", None, {"a": "aaaa"})
        str = ' a="aaaa"'
        self.assertEqual(node.props_to_html(), str)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_p2(self):
        node = LeafNode("p", "Hello, world!", {"a": "aaaa", "b": "bbbb"})
        self.assertEqual(node.to_html(), '<p a="aaaa" b="bbbb">Hello, world!</p>')

    def test_leaf_to_html_p3(self):
        node = LeafNode("p", "Hello, world!", {"a": "aaaa"})
        self.assertEqual(node.to_html(), '<p a="aaaa">Hello, world!</p>')

    def test_parent_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_parent_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_parent_to_html_with_grandchildren2(self):
        grandchild1_node = LeafNode("b", "grandchild1")
        grandchild2_node = LeafNode("b", "grandchild2")
        child_node = ParentNode("span", [grandchild1_node, grandchild2_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild1</b><b>grandchild2</b></span></div>",
        )
    
    def test_parent_to_html_tag_fail(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("", [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("Bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold node")

    def test_italic(self):
        node = TextNode("Italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic node")

    def test_code(self):
        node = TextNode("Code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "Code node")

    def test_link(self):
        node = TextNode("Link node", TextType.LINK, "http")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.props, {"href": "http"})
        self.assertEqual(html_node.value, "Link node")

    def test_split_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, 
                         [TextNode("This is text with a ", TextType.TEXT), 
                          TextNode("code block", TextType.CODE), 
                          TextNode(" word", TextType.TEXT)])

    def test_split_bold(self):
        node = TextNode("This is text with a **bold block** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, 
                         [TextNode("This is text with a ", TextType.TEXT), 
                          TextNode("bold block", TextType.BOLD), 
                          TextNode(" word", TextType.TEXT)])

    def test_split_italic(self):
        node = TextNode("This is text with a _italic block_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes, 
                         [TextNode("This is text with a ", TextType.TEXT), 
                          TextNode("italic block", TextType.ITALIC), 
                          TextNode(" word", TextType.TEXT)])

    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(extract_markdown_images(text), [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(extract_markdown_links(text), [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])

    def test_split_nodes_image(self):
        node = TextNode("This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT,)
        self.assertEqual(split_nodes_image([node]), 
                         [TextNode("This is text with a link ", TextType.TEXT), 
                          TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev"), 
                          TextNode(" and ", TextType.TEXT), 
                          TextNode("to youtube", TextType.IMAGE, "https://www.youtube.com/@bootdotdev")
                          ])
        
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_nodes_link(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",TextType.TEXT)
        self.assertEqual(split_nodes_link([node]), 
                         [TextNode("This is text with a link ", TextType.TEXT), 
                          TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                          TextNode(" and ", TextType.TEXT),
                          TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")
                          ])
    
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertEqual(text_to_textnodes(text), [TextNode("This is ", TextType.TEXT), 
                                                   TextNode("text", TextType.BOLD), 
                                                   TextNode(" with an ", TextType.TEXT), 
                                                   TextNode("italic", TextType.ITALIC),
                                                   TextNode(" word and a ", TextType.TEXT),
                                                   TextNode("code block", TextType.CODE),
                                                   TextNode(" and an ", TextType.TEXT),
                                                   TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                                                   TextNode(" and a ", TextType.TEXT),
                                                   TextNode("link", TextType.LINK, "https://boot.dev")])

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

    def test_block_to_block_type_paragraph(self):
        block = "This is just a paragraph"
        self.assertEqual(BlockType.P, block_to_block_type(block))

    def test_block_to_block_type_heading(self):
        block = "### This is just a heading"
        self.assertEqual(BlockType.H, block_to_block_type(block))

    def test_block_to_block_type_code(self):
        block = "```This is just a code```"
        self.assertEqual(BlockType.C, block_to_block_type(block))

    def test_block_to_block_type_quote(self):
        block = """
> This is 
> just a 
> quote
"""
        self.assertEqual(BlockType.Q, block_to_block_type(block))

    def test_block_to_block_type_ul(self):
        block = """
- This is 
- just an
- unordered list
"""
        self.assertEqual(BlockType.UL, block_to_block_type(block))

    def test_block_to_block_type_ol(self):
        block = """
. This is 
. just an
. ordered list
"""
        self.assertEqual(BlockType.OL, block_to_block_type(block))

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_header(self):
        md = """
### This is **bolded** paragraph

# This is a _header_
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h3>This is <b>bolded</b> paragraph</h3><h1>This is a <i>header</i></h1></div>",
        )

    def test_blockquote(self):
        md = """
> This is **bolded** paragraph
> This is a _header_
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is <b>bolded</b> paragraph This is a <i>header</i></blockquote></div>",
        )

    def test_ul(self):
        md = """
- This is **bolded** paragraph
- This is a _header_
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is <b>bolded</b> paragraph</li><li>This is a <i>header</i></li></ul></div>",
        )

    def test_ol(self):
        md = """
. This is **bolded** paragraph
. This is a _header_
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>This is <b>bolded</b> paragraph</li><li>This is a <i>header</i></li></ol></div>",
        )

if __name__ == "__main__":
    unittest.main()