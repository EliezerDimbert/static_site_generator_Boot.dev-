from blocking.md_to_html import markdown_to_html_node
import os
import shutil

def extract_title(markdown:str) -> str:
    print(f'reading from {markdown[:10]}')
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

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    directory_content:list[str] = os.listdir(dir_path_content)
    for item in directory_content:
        path_to_item = os.path.join(dir_path_content, item)
        path_to_dest = os.path.join(dest_dir_path, item)
        print(f'copying from {path_to_item} to {path_to_dest}')
        if os.path.isdir(path_to_item):
            print(f'{path_to_item} is a dir')
            os.makedirs(path_to_dest)
            generate_pages_recursive(path_to_item, template_path, path_to_dest)
        else:
            if item.endswith('.md'):
                print(f'{path_to_item} is a .md file')
                path_to_dest = path_to_dest.replace('.md', '.html')
                generate_page(path_to_item, template_path, path_to_dest)
            else:
                print(f'{path_to_item} is a file')
                shutil.copyfile(path_to_item, path_to_dest)