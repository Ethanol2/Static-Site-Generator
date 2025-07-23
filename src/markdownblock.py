import re
from enum import Enum
from htmlnode import ParentNode, LeafNode
from textnode import TextNode, TextType, text_to_textnodes, text_node_to_html_node

class BlockType(Enum):    
    PARAGRAPH = "paragraph"
    HEADING1 = "heading 1"
    HEADING2 = "heading 2"
    HEADING3 = "heading 3"
    HEADING4 = "heading 4"
    HEADING5 = "heading 5"
    HEADING6 = "heading 6"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

HTML_BLOCK_TAGS = {
    BlockType.PARAGRAPH: "p",
    BlockType.CODE: "pre",
    BlockType.ORDERED_LIST: "ol",
    BlockType.UNORDERED_LIST: "ul",
    BlockType.QUOTE: "blockquote",
    BlockType.HEADING1: "h1",
    BlockType.HEADING2: "h2",
    BlockType.HEADING3: "h3",
    BlockType.HEADING4: "h4",
    BlockType.HEADING5: "h5",
    BlockType.HEADING6: "h6",    
}
    
def markdown_to_blocks(markdown: str) -> list[str]:
    
    blocks = markdown.split("\n\n")
    
    for i in range(len(blocks) - 1, -1, -1):
        blocks[i] = blocks[i].strip()
        if len(blocks[i]) == 0:
            blocks.pop(i)
    
    return blocks

def block_to_block_type(block: str) -> BlockType:
    
    block = block.strip()
    
    if len(block) < 3:
        return BlockType.PARAGRAPH
    
    match block[0]:
        
        case '#':
            tag = block[:7]
            for i in range(len(tag)):
                if tag[i] == '#': continue
                if tag[i] == ' ': 
                    match i:
                        case 1:
                            return BlockType.HEADING1
                        case 2:
                            return BlockType.HEADING2
                        case 3:
                            return BlockType.HEADING3
                        case 4:
                            return BlockType.HEADING4
                        case 5:
                            return BlockType.HEADING5
                        case 6:
                            return BlockType.HEADING6
                break
        
        case '`':
            if len(block) > 6 and block[:3] == "```" and block[-3:] == "```":
                return BlockType.CODE
        
        case '>':
            lines = block.split("\n")
            for line in lines:
                line = line.strip()
                if len(line) == 0 or line[0] != ">":
                    return BlockType.PARAGRAPH
            return BlockType.QUOTE
        
        case '-':
            lines = block.split("\n")
            for line in lines:
                line = line.strip()
                if len(line) == 0 or line[:2] != "- ":
                    return BlockType.PARAGRAPH
            return BlockType.UNORDERED_LIST
        
        case '1':
            lines = block.split("\n")
            for i in range(len(lines)):
                lines[i] = lines[i].strip()
                if len(lines[i]) == 0 or lines[i][:3] != f'{i + 1}. ':
                    return BlockType.PARAGRAPH
            return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH

def block_to_html_node(block: str, block_type: BlockType) -> ParentNode:
    
    match block_type:
        
        case BlockType.CODE:
            trimmed_block = block[3:-3]
            
            if trimmed_block[0] == '\n':
                trimmed_block = trimmed_block[1:]
            
            return ParentNode(HTML_BLOCK_TAGS[BlockType.CODE], [text_node_to_html_node(TextNode(trimmed_block, TextType.CODE))])
        
        case BlockType.HEADING1:
            text_nodes = text_to_textnodes(block[1:].strip())
            children_nodes = [text_node_to_html_node(node) for node in text_nodes]
            return ParentNode(HTML_BLOCK_TAGS[BlockType.HEADING1], children_nodes)
        
        case BlockType.HEADING2:
            text_nodes = text_to_textnodes(block[2:].strip())
            children_nodes = [text_node_to_html_node(node) for node in text_nodes]
            return ParentNode(HTML_BLOCK_TAGS[BlockType.HEADING2], children_nodes)
        
        case BlockType.HEADING3:
            text_nodes = text_to_textnodes(block[3:].strip())
            children_nodes = [text_node_to_html_node(node) for node in text_nodes]
            return ParentNode(HTML_BLOCK_TAGS[BlockType.HEADING3], children_nodes)
        
        case BlockType.HEADING4:
            text_nodes = text_to_textnodes(block[4:].strip())
            children_nodes = [text_node_to_html_node(node) for node in text_nodes]
            return ParentNode(HTML_BLOCK_TAGS[BlockType.HEADING4], children_nodes)
        
        case BlockType.HEADING5:
            text_nodes = text_to_textnodes(block[5:].strip())
            children_nodes = [text_node_to_html_node(node) for node in text_nodes]
            return ParentNode(HTML_BLOCK_TAGS[BlockType.HEADING5], children_nodes)
        
        case BlockType.HEADING6:
            text_nodes = text_to_textnodes(block[6:].strip())
            children_nodes = [text_node_to_html_node(node) for node in text_nodes]
            return ParentNode(HTML_BLOCK_TAGS[BlockType.HEADING6], children_nodes)
        
        case BlockType.QUOTE:
            trimmed_block = re.sub("\n> ", "\n", block[2:].strip())
            text_nodes = text_to_textnodes(trimmed_block)
            leaf_nodes = [text_node_to_html_node(node) for node in text_nodes]
            return ParentNode(HTML_BLOCK_TAGS[BlockType.QUOTE], leaf_nodes)
        
        case BlockType.ORDERED_LIST:
            lines = block.split("\n")
            text_nodes = [text_to_textnodes(line[3:].strip()) for line in lines]
            children_nodes = []
            
            for nodes in text_nodes:
                leafs = ParentNode("li", [text_node_to_html_node(node) for node in nodes])
                children_nodes.append(leafs)
            
            return ParentNode(HTML_BLOCK_TAGS[BlockType.ORDERED_LIST], children_nodes)
        
        case BlockType.UNORDERED_LIST:
            lines = block.split("\n")
            text_nodes = [text_to_textnodes(line[2:].strip()) for line in lines]
            children_nodes = []
            
            for nodes in text_nodes:
                leafs = ParentNode("li", [text_node_to_html_node(node) for node in nodes])
                children_nodes.append(leafs)
            
            return ParentNode(HTML_BLOCK_TAGS[BlockType.UNORDERED_LIST], children_nodes)            
        
        case BlockType.PARAGRAPH:
            text_nodes = text_to_textnodes(block.strip().replace('\n', ' '))
            children_nodes = [text_node_to_html_node(node) for node in text_nodes]
            return ParentNode(HTML_BLOCK_TAGS[BlockType.PARAGRAPH], children_nodes)
                
def markdown_to_html_node(markdown: str) -> ParentNode:
    
    blocks = markdown_to_blocks(markdown)
    
    parent_html_node = ParentNode("div", [])

    for block in blocks:
        
        block_type = block_to_block_type(block)
        
        parent_html_node.children.append(block_to_html_node(block, block_type))
    
    return parent_html_node