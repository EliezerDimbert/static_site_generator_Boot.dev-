import os
import shutil

def replace_public():
    if not os.path.exists('public'):
        os.mkdir('public')
    shutil.rmtree('public')
    shutil.copytree(src='static', dst='public')
    
