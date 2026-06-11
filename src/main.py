from nodes.textnode import TextNode, TextType
from replace_public import replace_public
from gencontent import generate_page

def main():
    replace_public()
    generate_page('content/index.md', 'template.html', 'public/index.html')

if __name__ == "__main__":
    main()