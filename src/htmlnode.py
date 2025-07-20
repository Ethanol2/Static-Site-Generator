
class HTMLNode:
    def __init__(self, tag: str = "", value: str = "", childen: list = [], props: dict = {}) -> None:
        self.tag = tag if tag != "" else None
        self.value = value if value != "" else None 
        self.children = childen if len(childen) > 0 else None
        self.props = props if len(props) > 0 else None
    
    def to_html(self) -> str:
        raise NotImplementedError
    
    def props_to_html(self) -> str:
        html = ""
        
        if self.props is not None:
            for key in self.props:
                html += f' {key}=\"{self.props[key]}\"'
        
        return html
    
    def tag_to_html(self, close: bool = False) -> str:
        html = ""
        
        if self.tag is not None:
            if close:
                html = f'</{self.tag}>'
            else:
                html = f'<{self.tag}{self.props_to_html()}>'
            
        #print(f'\nTag: {self.tag}\nClose: {close}\nHTML: {html}')
            
        return html
        
    def __repr__(self) -> str:
        return f'HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})'

class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict = {}) -> None:
        super().__init__(tag, value, [], props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError
        if self.tag is None:
            return self.value
        
        return f'{self.tag_to_html()}{self.value}{self.tag_to_html(True)}'
    
class ParentNode(HTMLNode):
    def __init__(self, tag: str, childen: list, props: dict = {}) -> None:
        super().__init__(tag, "", childen, props)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("Parent node missing tag")
        if self.children is None:
            raise ValueError("Parent node's children list is None'")
        
        html = self.tag_to_html()
        for child in self.children:
            html += child.to_html()            
        html += self.tag_to_html(True)
        
        #print(f"\n{self}\nHTML: {html}")
        
        return html
            
        