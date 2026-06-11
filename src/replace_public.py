import os
import shutil

def replace_docs():
    print('clearing docs')
    if not os.path.exists('docs'):
        os.mkdir('docs')
    shutil.rmtree('docs')
    shutil.copytree(src='static', dst='docs')
    
