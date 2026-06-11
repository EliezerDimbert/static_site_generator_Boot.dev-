from blocking.md_to_html import markdown_to_html_node
import os

def extract_title(markdown:str) -> str:
    lines = markdown.split('\n')
    for line in lines:
        if line.startswith('# '):
            return line.lstrip('#').lstrip()
    raise Exception('no title found')

def generate_page(from_path:str, template_path:str, dest_path:str):
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')
    with open(from_path, 'r') as from_file, open(template_path, 'r') as template_file:
        template_copy = template_file.read()
        markdown_text = from_file.read()
        html_node = markdown_to_html_node(markdown_text)
        html_content = html_node.to_html()
        title = extract_title(markdown_text)
        new_page = template_copy.replace('{{ Title }}', title).replace('{{ Content }}', html_content)
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        with open(dest_path, 'w') as dest_file:
            dest_file.write(new_page)