"""Revisión del sitio generado: frases prohibidas por las reglas de integridad y enlaces internos rotos."""
import glob, os, re
from urllib.parse import urljoin, urlparse, unquote

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
files = [f.replace(os.sep, '/') for f in glob.glob('**/index.html', recursive=True) if not f.startswith('v1')]
BAD = re.compile(r'(24 ?h\b|48 ?h\b|24-48|48 horas|24 horas|horas laborables|garant[ií]a por escrito|no subcontrat|'
                 r'pocos talleres|Hemos hecho de todo|Garrotal|WhatsApp 957|\{\{|\}\})', re.I)
issues, broken = [], {}
for f in files:
    s = open(f, encoding='utf-8').read()
    txt = re.sub(r'<script.*?</script>|<style.*?</style>', '', s, flags=re.S)
    for m in BAD.finditer(re.sub('<[^>]+>', ' ', txt)):
        issues.append((f, m.group(0)))
    base = 'http://x/' + f
    for h in re.findall(r'(?:href|src)="([^"]+)"', s):
        if h.startswith(('http', 'tel:', 'mailto:', '#', 'data:')): continue
        p = unquote(urlparse(urljoin(base, h)).path.lstrip('/'))
        if p == '' or p.endswith('/'): p += 'index.html'
        if not os.path.exists(p): broken.setdefault(h, []).append(f)
print(len(files), 'páginas revisadas')
print('frases prohibidas:', len(issues))
for i in issues[:20]: print('  ', i)
print('enlaces rotos:', len(broken))
for k, v in list(broken.items())[:20]: print('  ', k, '<-', v[:2])
