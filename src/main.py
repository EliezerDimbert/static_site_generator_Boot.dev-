from nodes.textnode import TextNode, TextType
from replace_public import replace_docs
from gencontent import generate_pages_recursive
import sys

def main():
    replace_docs()
    try:
        basepath = sys.argv[1]
    except IndexError:
        basepath = '/'
    generate_pages_recursive('content', 'template.html', 'docs', basepath)

if __name__ == "__main__":
    main()