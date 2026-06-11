from .blocking import markdown_to_blocks, block_to_block_type, BlockType
from nodes.htmlnode import HTMLNode, LeafNode, ParentNode
from nodes.textnode import text_node_to_html_node, TextNode, TextType
from splitting_nodes.txt_to_node import text_to_textnodes

def markdown_to_html_node(markdown) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    content: list[HTMLNode] = []
    for block in blocks:
        block_type = block_to_block_type(block)
        conversion_func = block_type_to_conversion_func[block_type]
        content.append(conversion_func(block))
    return ParentNode('div', children=content)

def find_children(block:str) -> list[HTMLNode]:
    block_cpy = block.replace('\n', ' ')
    text_node_children = text_to_textnodes(block_cpy)
    leaf_node_children: list[HTMLNode] = list(map(text_node_to_html_node, text_node_children))
    return leaf_node_children

def paragraph_block_to_HTMLNode(block:str) -> ParentNode:
    children = find_children(block)
    return ParentNode("p", children)

def heading_block_to_HTMLNode(block:str) -> ParentNode:
    heading_count = 0
    for char in block:
        if char == '#':
            heading_count += 1
            block = block[1:] # remove the '#'
        else:
            break
    block = block.lstrip()
    children = find_children(block)
    return ParentNode(f'h{heading_count}', children)

def quote_block_to_HTMLNode(block:str) -> ParentNode:
    lines = block.split('\n')
    stripped_lines = list(map(lambda l: l.lstrip('>').lstrip(), lines))
    stripped_block = ' '.join(stripped_lines)
    children = find_children(stripped_block)
    return ParentNode('blockquote', children)

def code_block_to_HTMLNode(block:str) -> ParentNode:
    block = block[4:-3]
    children: list[HTMLNode] = [LeafNode('code', block)]
    return ParentNode('pre', children)

def unordered_list_block_to_HTMLNode(block:str) -> ParentNode:
    lines = block.split('\n')
    stripped_lines = list(map(lambda l: l.lstrip('-').lstrip(), lines))
    line_nodes: list[HTMLNode] = list(map(lambda l: ParentNode('li', find_children(l)), stripped_lines))
    list_node = ParentNode('ul', line_nodes)
    return list_node

def ordered_list_block_to_HTMLNode(block:str) -> ParentNode:
    lines = block.split('\n')
    stripped_lines = list(map(lambda l: l.split('.', 1)[1].lstrip(), lines))
    line_nodes: list[HTMLNode] = list(map(lambda l: ParentNode('li', find_children(l)), stripped_lines))
    list_node = ParentNode('ol', line_nodes)
    return list_node

block_type_to_conversion_func = {
    BlockType.PARAGRAPH: paragraph_block_to_HTMLNode,
    BlockType.HEADING: heading_block_to_HTMLNode,
    BlockType.QUOTE: quote_block_to_HTMLNode,
    BlockType.CODE: code_block_to_HTMLNode,
    BlockType.UNORD_LIST: unordered_list_block_to_HTMLNode,
    BlockType.ORD_LIST: ordered_list_block_to_HTMLNode
}