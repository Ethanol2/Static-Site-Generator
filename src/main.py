from textnode import TextNode
from textnode import TextType

def main():
    node = TextNode("This is some anchor text", TextType.URL, "https://www.boot.dev")
    print(node)
    
main()