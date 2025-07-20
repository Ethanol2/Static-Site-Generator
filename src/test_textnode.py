import unittest

from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        
    def test_neq(self):
        node = TextNode("This is one sentence", TextType.ITALIC)
        node2 = TextNode("This is another sentence", TextType.ITALIC)
        self.assertNotEqual(node, node2)
        
    def test_url(self):
        node = TextNode("This node has a URL", TextType.URL, "https://google.ca")
        node2 = TextNode("This node doesn't have a URL", TextType.PLAIN)
        self.assertIsNotNone(node.url)
        self.assertIsNone(node2.url)
        
    def test_text(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        
    def test_code_delimiter_split(self):
        node = TextNode("This is text with a `code block` word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        correct_result = [
            TextNode("This is text with a ", TextType.PLAIN),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.PLAIN),
        ]
        
        # for node in new_nodes:
        #     print("\n")
        #     print(node)
        
        self.assertEqual(correct_result, new_nodes)
        
    def test_bold_delimiter_split(self):
        node = TextNode("This is text with a **bold block** word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", TextType.CODE)
        
        correct_result = [
            TextNode("This is text with a ", TextType.PLAIN),
            TextNode("bold block", TextType.CODE),
            TextNode(" word", TextType.PLAIN),
        ]
        
        # for node in new_nodes:
        #     print("\n")
        #     print(node)
        
        self.assertEqual(correct_result, new_nodes)
        
    def test_bad_bold_delimiter_split(self):
        node = TextNode("This is text with a **bold block word", TextType.PLAIN)
        
        with self.assertRaises(Exception): split_nodes_delimiter([node], "**", TextType.CODE)
        
if __name__ == "__main__":
    unittest.main()