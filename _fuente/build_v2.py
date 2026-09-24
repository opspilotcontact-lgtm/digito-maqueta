import os
S = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.expanduser('~/Documents/GitHub/digito-maqueta/index.html')
src = open(os.path.join(S, 'digito-v2.src.html'), encoding='utf-8').read()
logo = open(os.path.join(S, 'logo_defs.html'), encoding='utf-8').read()

# Titular en letras corpóreas: cada letra se monta sola; las palabras no se parten.
H1 = '¿Tu fachada ha perdido fuerza?'.upper()
i, words = 0, []
for w in H1.split(' '):
    ls = []
    for c in w:
        ls.append(f'<span class="l" style="--i:{i}">{c}</span>'); i += 1
    words.append('<span class="w">' + ''.join(ls) + '</span>')
h1 = '<span class="corporeo" aria-hidden="true">' + ' '.join(words) + '</span>'

html = src.replace('{{LOGO}}', logo).replace('{{H1}}', h1).replace('{{PIE_LINKS}}', globals().get('PIE_HOME', ''))
assert '{{' not in html
open(OUT, 'w', encoding='utf-8').write(html)
print('ok', len(html))
