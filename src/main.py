from nodes.textnode import TextNode, TextType
from replace_public import replace_public
from gencontent import generate_pages_recursive
import sys

def main():
    replace_public()
    generate_pages_recursive('content', 'template.html', 'public')

if __name__ == "__main__":
    main()