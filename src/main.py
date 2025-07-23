import os
import shutil

from textnode import TextNode
from textnode import TextType

def main():
    node = TextNode("This is some anchor text", TextType.URL, "https://www.boot.dev")
    print(node)
    
def copy_static_to_public():
    public_path = "./public/"
    static_path = "./static/"
    
    if not os.path.exists(static_path):
        raise Exception("Error: The static folder doesn't exist")
    if not os.path.exists(public_path):
        os.mkdir(public_path)
        
    copy_dir_to_dir(static_path, public_path)

def copy_dir_to_dir(source: str, destination: str):
    
    for item in os.listdir(source):
        joined_path = os.path.join(source, item)
        
        #if os.pa
        
        #shutil.copy(os.path.join())
    
main()