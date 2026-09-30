"""Construye la v4 y la copia a la raíz del repo, que es lo que sirve GitHub Pages.

Uso (desde digito-maqueta/sitio):  python publicar.py
Luego: revisar `git status` en la raíz, commit y push.

Guarda en .publicado.txt lo que copió; en la siguiente vuelta borra primero esa lista,
así no quedan páginas viejas colgadas. Nunca toca v1/, v2/, sitio/, _fuente/ ni robots.txt.
"""
import shutil
import subprocess
import sys
from pathlib import Path

SITIO = Path(__file__).resolve().parent
RAIZ = SITIO.parent
DIST = SITIO / 'dist'
LISTA = SITIO / '.publicado.txt'
INTOCABLES = {'v1', 'v2', 'sitio', '_fuente', 'robots.txt', '.git', '.nojekyll', '.gitignore', 'README.md'}

subprocess.run('npm run build', cwd=SITIO, shell=True, check=True)

if LISTA.exists():
    for nombre in LISTA.read_text(encoding='utf-8').split():
        p = RAIZ / nombre
        if nombre in INTOCABLES:
            continue
        if p.is_dir():
            shutil.rmtree(p)
        elif p.exists():
            p.unlink()

copiados = []
for p in sorted(DIST.iterdir()):
    if p.name in INTOCABLES:
        sys.exit(f'dist/ trae {p.name}, que choca con algo que no se toca. Revisar.')
    destino = RAIZ / p.name
    if p.is_dir():
        shutil.copytree(p, destino)
    else:
        shutil.copy2(p, destino)
    copiados.append(p.name)

LISTA.write_text('\n'.join(copiados) + '\n', encoding='utf-8')
print('Publicado en la raíz:', ', '.join(copiados))
