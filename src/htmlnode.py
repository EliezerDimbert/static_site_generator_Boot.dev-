from __future__ import annotations
from dataclasses import dataclass
from typing import Any

@dataclass
class HTMLNode():
    tag:str|None=None
    value:str|None=None
    children: list[HTMLNode]|None=None
    props:dict[str, str]|None=None

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self) -> str:
        res = ''
        if not self.props: return ''
        for prop in self.props:
            res += f' {prop}="{self.props[prop]}"'
        return res

class LeafNode(HTMLNode):
    def __init__(self, tag:str|None, value:str, props:dict[str, str]|None=None) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None: raise ValueError
        if self.tag is None: return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
    
class ParentNode(HTMLNode):
    def __init__(self, tag:str, children:list[HTMLNode], props:dict[str, str]|None = None):
        super().__init__(tag, None, children, props)
    
    def to_html(self) -> str:
        if self.tag is None: raise ValueError('no tag')
        if self.children is None: raise ValueError('no children')
        res = f'<{self.tag}>'
        for child in self.children:
            res += child.to_html()
        res += f'</{self.tag}>'
        return res