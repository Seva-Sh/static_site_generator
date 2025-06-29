import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq2(self):
        node = TextNode("Text node", TextType.ITALIC)
        node2 = TextNode("Text node", TextType.ITALIC, "url")
        self.assertNotEqual(node, node2)

    def test_eq3(self):
        node = TextNode("Text node", TextType.ITALIC, "url")
        node2 = TextNode("Text node", TextType.ITALIC, "url")
        self.assertEqual(node, node2)

    def test_eq4(self):
        node = TextNode("Text nodes", TextType.ITALIC, "url")
        node2 = TextNode("Text node", TextType.ITALIC, "url")
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()