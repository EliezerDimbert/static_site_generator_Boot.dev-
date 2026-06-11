from nodes.textnode import TextNode, TextType
import re
def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT: 
            new_nodes.append(node)
            continue
        if node.text.count(delimiter) % 2 != 0: raise ValueError(f'Uneven number of delimiters on node {node}')
        split_text = node.text.split(delimiter)
        for i in range(len(split_text)):
            text_segment = split_text[i]
            if text_segment == '': continue
            if i % 2 == 0:
                new_nodes.append(TextNode(text_segment, TextType.TEXT))
            else:
                new_nodes.append(TextNode(text_segment, text_type))
    return new_nodes

def extract_markdown_images(text:str) -> list[tuple[str, str]]:
    return re.findall(r'!\[([^\]]*)\]\(([^\)]*)', text)

def extract_markdown_links(text:str) -> list[tuple[str, str]]:
    return re.findall(r'\[([^\]]*)\]\(([^\)]*)\)', text)

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        remaining_text = node.text
        images = extract_markdown_images(remaining_text)
        if len(images) == 0:
            new_nodes.append(node)
            continue
        for image in images:
            alt_text, url = image
            split_text = remaining_text.split(f"![{alt_text}]({url})", 1)
            pre_text_node = TextNode(split_text[0], TextType.TEXT)
            link_node = TextNode(alt_text, TextType.IMAGE, url)
            remaining_text = split_text[1]
            if pre_text_node.text != '':
                new_nodes.append(pre_text_node)
            new_nodes.append(link_node)
        if remaining_text != '':
            final_text_node = TextNode(remaining_text, TextType.TEXT)
            new_nodes.append(final_text_node)
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        remaining_text = node.text
        links = extract_markdown_links(remaining_text)
        if len(links) == 0:
            new_nodes.append(node)
            continue
        for link in links:
            alt_text, url = link
            split_text = remaining_text.split(f"[{alt_text}]({url})", 1)
            pre_text_node = TextNode(split_text[0], TextType.TEXT)
            image_node = TextNode(alt_text, TextType.LINK, url)
            remaining_text = split_text[1]
            if pre_text_node.text != '':
                new_nodes.append(pre_text_node)
            new_nodes.append(image_node)
        if remaining_text != '':
            final_text_node = TextNode(remaining_text, TextType.TEXT)
            new_nodes.append(final_text_node)
    return new_nodes

