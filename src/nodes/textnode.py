from enum import Enum
from nodes.htmlnode import LeafNode

class TextType(Enum):
	BOLD = "bold"
	ITALIC = "italic"
	CODE = "code"
	LINK = "link"
	IMAGE = "image"
	TEXT = "text"

class TextNode():
	def __init__(self, text:str, text_type:TextType, url: str | None = None) -> None:
		self.text = text
		self.text_type = text_type
		self.url = url
	def __eq__(self, other: object) -> bool:
		if isinstance(other, TextNode):
			return self.text == other.text and self.text_type == other.text_type and self.url == other.url
		return False
	def __repr__(self) -> str:
		return f'TextNode({self.text}, {self.text_type.value}, {self.url})'
	

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
	match(text_node.text_type):
		case TextType.TEXT:
			return LeafNode(None, text_node.text, None)
		case TextType.BOLD:
			return LeafNode('b', text_node.text, None)
		case TextType.ITALIC:
			return LeafNode('i', text_node.text, None)
		case TextType.CODE:
			return LeafNode('code', text_node.text, None)
		case TextType.LINK:
			return LeafNode('a', text_node.text, {'href': text_node.url}) #type: ignore
		case TextType.IMAGE:
			return LeafNode('img', '', {'src': text_node.url, 'alt': text_node.text}) #type: ignore
		case _:
			raise Exception('Invalid text type')