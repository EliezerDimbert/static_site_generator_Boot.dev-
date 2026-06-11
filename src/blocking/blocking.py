from enum import Enum

def markdown_to_blocks(markdown:str) -> list[str]:
    blocks = markdown.split('\n\n')
    stripped_blocks = list(map(lambda s: s.strip(), blocks))
    filtered_blocks = list(filter(lambda s: len(s) != 0, stripped_blocks))
    return filtered_blocks

class BlockType(Enum):
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    UNORD_LIST = 'unordered_list'
    ORD_LIST = 'ordered_list'

def block_to_block_type(block:str) -> BlockType:
    heading_starts = tuple(['#' * i + ' ' for i in range(1, 7)])
    if block.startswith(heading_starts):
        return BlockType.HEADING
    elif block.startswith('```\n') and block.endswith('```'):
        return BlockType.CODE
    elif is_a_quote(block):
        return BlockType.QUOTE
    elif is_a_unordered_list(block):
        return BlockType.UNORD_LIST
    elif is_a_ordered_list(block):
        return BlockType.ORD_LIST
    return BlockType.PARAGRAPH
    
def is_a_ordered_list(block:str) -> bool:
    lines = block.split('\n')
    for i in range(len(lines)):
        if lines[i].startswith(f'{i+1}. '): continue
        return False
    return True

def is_a_quote(block:str) -> bool:
    lines = block.split('\n')
    for i in range(len(lines)):
        if lines[i].startswith((f'> ', '>')): continue
        return False
    return True

def is_a_unordered_list(block:str) -> bool:
    lines = block.split('\n')
    for i in range(len(lines)):
        if lines[i].startswith(f'- '): continue
        return False
    return True

