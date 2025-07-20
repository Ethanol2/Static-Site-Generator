from enum import Enum
from htmlnode import HTMLNode, LeafNode, ParentNode

class TextType(Enum):
    PLAIN = "plain"
    BOLD = "bolt"
    ITALIC = "italic"
    CODE = "code"
    URL = "url"
    IMAGE = "image"

class TextNode:
    def __init__(self, text: str, text_type: TextType, url = None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url
        
    def __eq__(self, value) -> bool:
        if not isinstance(value, TextNode):
            return False
        return self.text == value.text and self.text_type == value.text_type and self.url == value.url
    
    def __repr__(self) -> str:
        return f'TextNode({self.text}, {self.text_type}, {self.url})'
    
def text_node_to_html_node(text_node: TextNode) -> HTMLNode:
    
    match text_node.text_type:
        
        case TextType.PLAIN:
            return LeafNode(tag="", value=text_node.text)
        
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        
        case TextType.URL:
            return LeafNode(tag="a", value=text_node.text, props={"href":text_node.url})
        
        case TextType.IMAGE:
            return LeafNode(tag="img", value="", props={
                "src":text_node.url,
                "alt":text_node.text
            })
    
    raise NotImplementedError

def split_nodes_delimiter(old_nodes: list, delimiter: str, text_type: TextType):
    new_nodes = []
    
    for node in old_nodes:
        if not isinstance(node, TextNode):
            continue
        
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        
        delim_len = len(delimiter)
        i = 0
        marker = 0
        while i + delim_len < len(node.text):
            i += delim_len
            
            if node.text[i:i+delim_len] == delimiter:
                
                new_nodes.append(TextNode(node.text[marker:i], TextType.PLAIN))
                
                k = i + delim_len
                while node.text[k:k+delim_len] != delimiter:
                    if k + delim_len >= len(node.text):
                        raise Exception(f"Error: Markdown tag \"{delimiter}\" not closed")                    
                    k += 1
                    
                new_nodes.append(TextNode(node.text[i + delim_len:k], text_type))
                i = k + delim_len + 1
                marker = i - 1
        
        if marker < len(node.text):
            new_nodes.append(TextNode(node.text[marker:len(node.text)], TextType.PLAIN))
    
    return new_nodes