"""Genera la web de Dígito (v2) con su contenido SEO: servicios, subservicios, pueblos, guías y trabajos.

Fuente de los datos: el Astro de Digitorotulacion/web (services/localities/images/guides exportados a data.json)
y las guías renderizadas de su preview. Estrategia: doc de NotionPilot 6c12e340 (24-sep-2026).
Reglas de integridad aplicadas aquí (no a mano): fuera los compromisos sin confirmar (24/48 h, garantía por
escrito, «no subcontratamos»…), fuera las afirmaciones de trabajo en un pueblo sin foto que lo pruebe, precios
siempre «orientativos». Uso:  python _fuente/generar.py   (desde la raíz del repo)
"""
import html, json, os, re, shutil
from bs4 import BeautifulSoup

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = os.path.join(RAIZ, '_fuente')
ASTRO_IMG = os.path.expanduser('~/Documents/GitHub/Digitorotulacion/web/public/img')
DOM = 'https://digitorotulacion.com'
D = json.load(open(os.path.join(F, 'data.json'), encoding='utf-8'))
for _g in D['guides']:
    if _g['slug'] == 'licencia-rotulo-fachada-cordoba':
        _g['title'] = 'Permiso para un rótulo en la fachada en Córdoba: lo que dice la ordenanza, artículo por artículo'
        _g['desc'] = 'Licencia de obra menor, banderolas (altura y vuelo) y casco histórico (sin luminosos, murales de 50 cm): la Ordenanza de Publicidad Exterior de Córdoba, explicada.'
esc = lambda s: html.escape(s or '', quote=True)

# ───────────────────────── integridad ─────────────────────────
DROP = re.compile(r'(24 ?h\b|48 ?h\b|24-48|24 horas|48 horas|horas laborables|garant[ií]a por escrito|no subcontrat|pocos talleres|'
                  r'nunca (más de|tengas)|mismo día|lacamos siempre|como el primer día|Nosotros sí, siempre|sin «a partir de»)', re.I)
REPL = [
    (r'Somos de los pocos talleres de la provincia que seguimos trabajando el neón de cristal, así que te podemos dar las dos opciones con precio\.', ''),
    (r'Es el 70 % de lo que rotulamos: barato, duradero \(7-10 años\) y se lee perfectamente\.', 'Es lo más económico, dura de 7 a 10 años y se lee perfectamente.'),
    (r'\s*Nosotros sí\.', ''),
    (r'Muchos de los que ves en las calles de [^.]*salieron de nuestro taller\.', ''),
    (r'Y seguimos manteniendo rótulos que montamos hace veinte años\.', ''),
    (r'\s*\(el más pedido\)', ''),
    (r'Para el 95 % de los casos', 'En la mayoría de los casos'),
    (r'para el 95 % de los casos', 'en la mayoría de los casos'),
    (r'Para el 80 % de los comercios', 'Para la mayoría de los comercios'),
]
def limpia(t):
    if not t: return t
    for a, b in REPL: t = re.sub(a, b, t)
    partes = re.split(r'(?<=[.!?])\s+', t.strip())
    t = ' '.join(p for p in partes if p and not DROP.search(p))
    return re.sub(r'\s{2,}', ' ', t).strip()

PASOS = [
    ('Nos cuentas qué necesitas', 'Por WhatsApp, por teléfono o con el formulario: qué tipo de rótulo, medidas aproximadas, dónde va y una foto del sitio.'),
    ('Diseño y presupuesto', 'Te preparamos el diseño sobre la foto de tu fachada o tu vehículo y el presupuesto con materiales, medidas, plazo y montaje.'),
    ('Fabricación en el taller', 'Estructura, chapa, soldadura, luz, impresión y vinilo, en nuestra nave del Polígono Gallardo de La Carlota.'),
    ('Montaje', 'Lo llevamos y lo montamos con los medios que haga falta, y te lo dejamos funcionando.'),
]
NOTA_PRECIOS = 'Precios orientativos con IVA (septiembre de 2026), para que vayas con una idea. El precio real depende de las medidas, el material, la altura de montaje y la distancia: te lo damos cerrado con la foto y las medidas.'

# ───────────────────────── pueblos publicados (estrategia 6c12e340, por SERP medido) ─────────────────────────
P1 = ['la-carlota', 'fuente-palmera', 'palma-del-rio', 'la-rambla', 'santaella', 'la-victoria', 'guadalcazar', 'posadas',
      'almodovar-del-rio', 'fernan-nunez', 'montemayor', 'montalban', 'la-luisiana', 'fuentes-de-andalucia', 'hornachuelos']
P2 = ['ecija', 'montilla', 'aguilar-de-la-frontera', 'puente-genil', 'cordoba']
INE = {'la-carlota': 14503, 'fuente-palmera': 9883, 'palma-del-rio': 20438, 'montilla': 22305, 'puente-genil': 29963,
       'aguilar-de-la-frontera': 13130, 'fernan-nunez': 9670, 'almodovar-del-rio': 8040, 'la-rambla': 7412, 'posadas': 7273,
       'ecija': 39530, 'cordoba': 323262}   # padrón INE 1-1-2025 (doc 25ba2d4f)
ANGULO = {   # reescritos: solo hechos públicos y trabajos con foto en el archivo
    'la-carlota': 'Es nuestro pueblo: el taller está en el Polígono Gallardo, junto a la A-4. De aquí son muchos de los trabajos de nuestro archivo: la imagen de La Carloteña (el camión, el tótem de la fábrica, la placa y el corpóreo), la señal de la rotonda y las vallas de las promociones de viviendas. Es un pueblo de carretera, industria agroalimentaria y comercio, repartido entre el núcleo y sus aldeas (Aldea Quintana, La Chica Carlota, El Arrecife, Fuencubierta, Los Algarbes…).',
    'guadalcazar': 'Los paneles informativos turísticos del Ayuntamiento de Guadalcázar (Torre Mocha, el Abrevadero y el Lavadero) salieron de nuestro taller. Es un pueblo agrícola con comercio de proximidad y explotaciones que rotulan sus vehículos y sus naves.',
    'cordoba': 'La capital está a media hora por la A-4. En el casco histórico, la ordenanza de publicidad exterior prohíbe los rótulos luminosos y limita tamaños y materiales: te lo contamos, artículo por artículo, en la guía de permisos.',
}
CLAIM = re.compile(r'\b(hemos|hicimos|trabajamos|rotulamos|conocemos)\b', re.I)
def angulo(l):
    if l['slug'] in ANGULO: return ANGULO[l['slug']]
    partes = re.split(r'(?<=[.!?])\s+', l['angle'])
    return ' '.join(p for p in partes if not CLAIM.search(p))

LOC = {l['slug']: l for l in D['localities']}
PUB = [s for s in P1 + P2 if s in LOC]
SERV = {s['slug']: s for s in D['services']}
FOTOS = D['photos']

# ───────────────────────── fotos: copia las que se usan ─────────────────────────
usadas = set()
def foto(key):
    p = FOTOS.get(key)
    if not p: return None
    src = os.path.join(ASTRO_IMG, p['slug'] + '-800.webp')
    dst = os.path.join(RAIZ, 'img', p['slug'] + '.webp')
    if not os.path.exists(dst) and os.path.exists(src): shutil.copy(src, dst)
    usadas.add(p['slug'])
    return p

# ───────────────────────── plantilla ─────────────────────────
SRC = open(os.path.join(F, 'digito-v2.src.html'), encoding='utf-8').read()
CSS_BASE = re.search(r'<style>(.*?)</style>', SRC, re.S).group(1)
CSS_SUB = r'''
/* ===== Páginas interiores ===== */
.migas{font-size:.82rem;color:#B9C0CA;margin:0 0 1rem;display:flex;flex-wrap:wrap;gap:.2rem .5rem}
.migas a{color:#fff}.migas span[aria-hidden]{opacity:.6}
.sub-hero{position:relative;background:var(--grecada);color:#fff;overflow:hidden;padding:clamp(2rem,4vw,3.2rem) 0 clamp(2.4rem,5vw,3.6rem)}
.sub-hero::before{content:"";position:absolute;z-index:2;left:0;top:0;bottom:0;width:1.6rem;background:var(--damero-bg)}
.sub-hero::after{content:"";position:absolute;z-index:2;left:1.6rem;top:0;bottom:0;width:.4rem;background:var(--amarillo)}
.sub-hero .wrap{position:relative;padding-left:max(var(--gutter),3.2rem);display:grid;grid-template-columns:minmax(0,1.25fr) minmax(0,1fr);gap:1.5rem 3rem;align-items:center}
.sub-hero h1{font-size:clamp(2.3rem,5.4vw,4.4rem);font-weight:880;font-stretch:66%;text-transform:uppercase;line-height:.93;text-shadow:.02em .025em 0 var(--canto-osc),.04em .05em 0 var(--canto-osc)}
.sub-hero .lead{color:#E3E6EB;font-size:1.12rem;margin:1.1rem 0 1.4rem}
.sub-hero.guia h1{font-size:clamp(2rem,3.9vw,3.2rem);font-stretch:70%}
.prosa details{border-top:1px solid var(--hielo-2);padding:.8rem 0;max-width:62ch}
.prosa summary{cursor:pointer;font-weight:700}
.prosa details p{margin:.5rem 0 0}
.sub-hero .marca{color:var(--amarillo)}
.sub-hero figure{margin:0;border:.35rem solid var(--tinta);box-shadow:0 0 0 .35rem var(--amarillo)}
.sub-hero figure img{width:100%;aspect-ratio:4/3;object-fit:cover}
@media (max-width:52rem){.sub-hero .wrap{grid-template-columns:1fr;padding-left:2.4rem}.sub-hero::before{width:1rem}.sub-hero::after{left:1rem;width:.3rem}}
.bloque{padding:clamp(3rem,6vw,4.5rem) 0}
.bloque.claro{background:var(--hielo)}.bloque.gris{background:var(--hielo-2)}
.bloque.luz{background:var(--amarillo)}.bloque.noche{background:var(--damero);color:#fff}
.bloque h2{margin-bottom:1.2rem}
.dos-col{display:grid;grid-template-columns:minmax(0,1.2fr) minmax(0,1fr);gap:2rem 3.5rem;align-items:start}
@media (max-width:52rem){.dos-col{grid-template-columns:1fr}}
.prosa p{font-size:1.06rem}
.prosa h2{font-size:clamp(1.8rem,3.6vw,2.7rem);margin:2.4rem 0 1rem}
.prosa h3{font-size:1.45rem;font-weight:800;font-stretch:80%;text-transform:uppercase;margin:1.8rem 0 .6rem}
.prosa ul,.prosa ol{padding-left:1.2rem;max-width:62ch}.prosa li{margin:.35rem 0}
.prosa a{text-decoration-thickness:2px;text-underline-offset:2px}
.prosa .corto{background:var(--amarillo);padding:1rem 1.2rem;border-left:.45rem solid var(--tinta);max-width:62ch}
.checks{list-style:none;padding:0;margin:0;display:grid;gap:.55rem}
.checks li{display:flex;gap:.6rem;align-items:flex-start}
.checks li::before{content:"";flex:none;width:1.1rem;height:.55rem;margin-top:.5rem;border-radius:50%;background:var(--amarillo);box-shadow:0 0 0 .1rem var(--tinta);transform:rotate(-9deg)}
.tabla-wrap{overflow-x:auto;background:#fff;border:.3rem solid var(--tinta)}
table.precios{border-collapse:collapse;width:100%;font-size:.95rem;min-width:34rem}
table.precios th,table.precios td{padding:.7rem .9rem;text-align:left;border-bottom:1px solid var(--hielo-2);vertical-align:top}
table.precios th{font-family:var(--rotulo);text-transform:uppercase;font-stretch:90%;font-size:.8rem;letter-spacing:.06em;background:var(--tinta);color:#fff}
table.precios td.num{white-space:nowrap;font-weight:700;font-variant-numeric:tabular-nums}
table.precios small{display:block;color:var(--tinta-suave)}
.nota{font-size:.88rem;color:var(--tinta-suave);margin-top:.8rem}
.bloque.luz .nota{color:#3B3F2A}
.faq details{border-top:1px solid #3A4050;padding:.9rem 0}
.faq summary{cursor:pointer;font-weight:700;font-size:1.05rem;list-style:none;display:flex;justify-content:space-between;gap:1rem}
.faq summary::after{content:"+";font-family:var(--rotulo);color:var(--amarillo);font-size:1.4rem;line-height:1}
.faq details[open] summary::after{content:"–"}
.faq details p{color:#D5DAE1;margin:.6rem 0 0}
.fotos-3{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.4rem;background:var(--tinta);padding:.4rem}
.fotos-3 figure{margin:0;position:relative}.fotos-3 img{width:100%;height:clamp(10rem,18vw,14rem);object-fit:cover}
.fotos-3 figcaption{position:absolute;left:.4rem;bottom:.4rem;background:rgb(16 19 22/.84);color:#fff;font-size:.75rem;padding:.15rem .5rem;border-radius:.2rem}
@media (max-width:40rem){.fotos-3{grid-template-columns:1fr 1fr}.fotos-3 figure:first-child{grid-column:1 / -1}}
.tarjetas{display:grid;grid-template-columns:repeat(auto-fill,minmax(15rem,1fr));gap:.8rem}
.tarjeta{display:block;text-decoration:none;background:#fff;border-top:.4rem solid var(--amarillo);padding:1rem 1.1rem;transition:transform .25s var(--curva)}
.tarjeta:hover{transform:translateY(-3px)}
.tarjeta b{display:block;font-family:var(--rotulo);font-weight:850;font-stretch:66%;text-transform:uppercase;font-size:1.45rem;line-height:1;margin-bottom:.4rem}
.tarjeta span{font-size:.92rem;color:var(--tinta-suave)}
.chips-links{display:flex;flex-wrap:wrap;gap:.45rem}
.chips-links a{text-decoration:none;border:1.5px solid var(--tinta);border-radius:999px;padding:.35rem .85rem;font-weight:600;font-size:.92rem}
.chips-links a:hover{background:var(--tinta);color:var(--amarillo)}
.pasos-4{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:1rem;counter-reset:p}
.pasos-4 li{background:#fff;border-top:.4rem solid var(--canto);padding:1rem 1.1rem}
.pasos-4 h3{display:flex;gap:.6rem;align-items:center;font-size:1.35rem;font-weight:850;font-stretch:66%;text-transform:uppercase;margin-bottom:.4rem}
.pasos-4 h3::before{counter-increment:p;content:counter(p);display:grid;place-items:center;width:2.6rem;height:1.35rem;border-radius:50%;background:var(--amarillo);box-shadow:0 0 0 .1rem #fff,0 0 0 .24rem var(--canto);font-size:.85rem;font-stretch:100%;transform:rotate(-9deg);flex:none}
.pasos-4 p{margin:0;font-size:.95rem;color:var(--tinta-suave)}
@media (max-width:60rem){.pasos-4{grid-template-columns:1fr 1fr}}@media (max-width:36rem){.pasos-4{grid-template-columns:1fr}}
.galeria{display:grid;grid-template-columns:repeat(auto-fill,minmax(14rem,1fr));gap:.4rem}
.galeria figure{margin:0;position:relative;background:var(--tinta)}
.galeria img{width:100%;aspect-ratio:4/3;object-fit:cover}
.galeria figcaption{font-size:.8rem;padding:.35rem .5rem;color:#D5DAE1}
.pie-links{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:1.5rem 2rem;margin-top:2rem;padding-top:1.6rem;border-top:1px solid #2B3038}
.pie-links h3{margin-bottom:.6rem}.pie-links ul{list-style:none;margin:0;padding:0;display:grid;gap:.25rem;font-size:.88rem}
.pie-links a{color:#C9CED6;text-decoration:none}.pie-links a:hover{color:var(--amarillo)}
@media (max-width:52rem){.pie-links{grid-template-columns:1fr 1fr}}
.cab-logo img{width:7.6rem;height:auto}
.pie .pie-logo{width:8rem;height:auto;margin-bottom:.8rem}
'''

SPRITE = re.search(r'(<symbol id="i-tel".*?)</svg>\n<a class="salto"', SRC, re.S).group(1)
FORM = re.search(r'(<form class="pide".*?</form>)', SRC, re.S).group(1)
FORM_JS = re.search(r'(<script>\n// Presupuesto por WhatsApp.*?</script>)', SRC, re.S).group(1)

def rel(depth): return '../' * depth

def pie_links(r):
    s = ''.join(f'<li><a href="{r}rotulos/{x["slug"]}/">{esc(x["short"])}</a></li>' for x in D['services'])
    p = ''.join(f'<li><a href="{r}rotulos-en/{x}/">{esc(LOC[x]["name"])}</a></li>' for x in PUB[:9]) + f'<li><a href="{r}rotulos-en/">Todos los pueblos</a></li>'
    g = ''.join(f'<li><a href="{r}guias/{x["slug"]}/">{esc(x["short"])}</a></li>' for x in D['guides'][:5]) + f'<li><a href="{r}guias/">Todas las guías</a></li>'
    t = f'<li><a href="{r}trabajos/">Trabajos</a></li><li><a href="{r}#donde">Dónde estamos</a></li><li><a href="{r}#presupuesto">Presupuesto</a></li>'
    return f'<div class="pie-links"><div><h3>Qué hacemos</h3><ul>{s}</ul></div><div><h3>Dónde montamos</h3><ul>{p}</ul></div><div><h3>Guías</h3><ul>{g}</ul></div><div><h3>El taller</h3><ul>{t}</ul></div></div>'

def cierre(r, titulo='Mándanos una foto de tu fachada.'):
    f = FORM.replace('id="pide"', 'id="pide"')
    return f'''<section class="cierre" id="presupuesto" aria-labelledby="t-cierre">
  <div class="wrap">
    <div>
      <p class="marca">Presupuesto</p>
      <h2 id="t-cierre">{esc(titulo)}</h2>
      <p class="lead">Dinos qué necesitas y dónde. Te preparamos el mensaje de WhatsApp: tú solo adjuntas la foto y nos lo envías.</p>
      <div class="otros"><a href="tel:+34957301773">Llamar al taller: 957 30 17 73</a><a href="mailto:info@digitorotulacion.com">info@digitorotulacion.com</a></div>
    </div>
    {f}
  </div>
</section>'''

def pagina(path, title, meta, cuerpo, schema, migas):
    depth = path.strip('/').count('/') + 1 if path.strip('/') else 0
    r = rel(depth)
    ld = json.dumps({'@context': 'https://schema.org', '@graph': schema + [{
        '@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': i + 1, 'name': n, **({'item': DOM + u} if u else {})} for i, (n, u) in enumerate(migas)]}]},
        ensure_ascii=False)
    migas_html = '<nav class="migas" aria-label="Estás en">' + '<span aria-hidden="true">›</span>'.join(
        (f'<a href="{r}{u.strip("/") + "/" if u.strip("/") else ""}">{esc(n)}</a>' if u else f'<span aria-current="page">{esc(n)}</span>') for n, u in migas) + '</nav>'
    cuerpo = cuerpo.replace('{{R}}', r).replace('{{MIGAS}}', migas_html)
    out = f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(meta)}">
<link rel="canonical" href="{DOM}{path}">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#323846">
<link rel="icon" href="{r}img/logo-digito.svg" type="image/svg+xml">
<link rel="preload" href="{r}fonts/anybody-var-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{r}fonts/instrument-var-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{r}css/digito.css">
<script type="application/ld+json">{ld}</script>
</head>
<body>
<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false">{SPRITE}</svg>
<a class="salto" href="#contenido">Saltar al contenido</a>
<div class="propuesta">Propuesta de rediseño en revisión · la web oficial sigue en <a href="https://digitorotulacion.com/">digitorotulacion.com</a></div>
<header class="cab">
  <div class="wrap">
    <a class="cab-logo" href="{r or './'}" aria-label="Dígito Rotulación, inicio"><img src="{r}img/logo-digito.svg" alt="Dígito Rotulación" width="216" height="108"></a>
    <nav aria-label="Principal">
      <a href="{r}rotulos/">Qué hacemos</a><a href="{r}trabajos/">Trabajos</a><a href="{r}rotulos-en/">Pueblos</a><a href="{r}guias/">Guías</a><a href="{r}#donde">Dónde</a>
    </nav>
    <a class="btn btn-luz" href="#presupuesto" aria-label="Pide presupuesto por WhatsApp"><svg class="ico"><use href="#i-wa"/></svg><span>Presupuesto</span></a>
  </div>
</header>
<main id="contenido">
{cuerpo}
{cierre(r)}
</main>
<footer class="pie">
  <div class="wrap">
    <div class="pie-rejilla">
      <div><img class="pie-logo" src="{r}img/logo-digito.svg" alt="Dígito Rotulación" width="216" height="108" loading="lazy"><p>Taller de rótulos en La Carlota desde 1993.</p></div>
      <div><h3>El taller</h3><p>P.I. Gallardo, C/ Ingeniero Juan de la Cierva, 38</p><p>14100 La Carlota (Córdoba)</p><p>L-V 8:00-14:00 y 16:00-18:00</p></div>
      <div><h3>Contacto</h3><p><a href="tel:+34957301773">957 30 17 73</a></p><p><a href="https://wa.me/34696915689">696 915 689</a> (WhatsApp)</p><p><a href="mailto:info@digitorotulacion.com">info@digitorotulacion.com</a></p></div>
    </div>
    {pie_links(r)}
    <div class="legal"><span>© Dígito Rotulación</span><span>Aviso legal y privacidad (pendiente)</span></div>
  </div>
</footer>
{FORM_JS}
</body>
</html>
'''
    dst = os.path.join(RAIZ, path.strip('/'), 'index.html')
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    open(dst, 'w', encoding='utf-8').write(out)
    PAGINAS.append((path, title))

PAGINAS = []
NEGOCIO = {'@type': 'LocalBusiness', '@id': DOM + '/#taller', 'name': 'Dígito Rotulación', 'telephone': '+34957301773',
           'address': {'@type': 'PostalAddress', 'streetAddress': 'Polígono Industrial Gallardo, C/ Ingeniero Juan de la Cierva, 38',
                       'postalCode': '14100', 'addressLocality': 'La Carlota', 'addressRegion': 'Córdoba', 'addressCountry': 'ES'}}

def fig(key, cls=''):
    p = foto(key)
    if not p: return ''
    return f'<figure{cls}><img src="{{{{R}}}}img/{p["slug"]}.webp" alt="{esc(p["alt"])}" width="{p["w"]}" height="{p["h"]}" loading="lazy"><figcaption>{esc(p["caption"])}</figcaption></figure>'

def tabla_precios(rows):
    def nota(x):
        n = limpia(x.get('note'))
        return f'<small>{esc(n)}</small>' if n else ''
    tr = ''.join(f'<tr><td>{esc(limpia(x["concept"]))}{nota(x)}</td><td class="num">{esc(x["range"])}</td><td>{esc(x["unit"])}</td></tr>' for x in rows)
    return f'<div class="tabla-wrap"><table class="precios"><thead><tr><th>Qué</th><th>Precio orientativo</th><th>Por</th></tr></thead><tbody>{tr}</tbody></table></div><p class="nota">{NOTA_PRECIOS}</p>'

def frase1(t):
    return re.split(r'(?<=[.!?])\s', limpia(t))[0]

def faqs(lista):
    out = [(limpia(f['q']), limpia(f['a'])) for f in lista]
    return [(q, a) for q, a in out if q and a]

def faq_html(lista, titulo='Preguntas que nos hacen'):
    if not lista: return ''
    det = ''.join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in lista)
    return f'<section class="bloque noche"><div class="wrap dos-col"><div><p class="marca" style="color:var(--amarillo)">Dudas</p><h2>{titulo}</h2></div><div class="faq">{det}</div></div></section>'

def faq_schema(lista):
    return {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in lista]} if lista else None

def pasos_html():
    li = ''.join(f'<li><h3>{esc(t)}</h3><p>{esc(x)}</p></li>' for t, x in PASOS)
    return f'<section class="bloque gris"><div class="wrap"><p class="marca" style="color:var(--tinta-suave)">Cómo trabajamos</p><h2>Del diseño al montaje.</h2><ol class="pasos-4">{li}</ol></div></section>'

def hero(marca, h1, lead, fkey, extra='', cls=''):
    p = foto(fkey)
    f = f'<figure><img src="{{{{R}}}}img/{p["slug"]}.webp" alt="{esc(p["alt"])}" width="{p["w"]}" height="{p["h"]}" fetchpriority="high"></figure>' if p else ''
    return f'''<section class="sub-hero{cls}"><div class="wrap"><div>{{{{MIGAS}}}}<p class="marca">{esc(marca)}</p><h1>{esc(h1)}</h1><p class="lead">{esc(lead)}</p>
<div class="acciones"><a class="btn btn-luz" href="#presupuesto"><svg class="ico"><use href="#i-camara"/></svg>Pide presupuesto</a><a class="btn btn-linea" href="tel:+34957301773"><svg class="ico"><use href="#i-tel"/></svg>957 30 17 73</a></div>{extra}</div>{f}</div></section>'''

def pueblos_chips(slugs, titulo):
    a = ''.join(f'<a href="{{{{R}}}}rotulos-en/{s}/">{esc(LOC[s]["name"])}</a>' for s in slugs if s in PUB)
    return f'<section class="bloque claro"><div class="wrap"><p class="marca" style="color:var(--tinta-suave)">Dónde montamos</p><h2>{titulo}</h2><div class="chips-links">{a}</div></div></section>' if a else ''

# ───────────────────────── servicios y subservicios ─────────────────────────
for s in D['services']:
    base = f'/rotulos/{s["slug"]}/'
    fl = faqs(s['faqs'])
    subs = ''.join(f'<a class="tarjeta" href="{{{{R}}}}rotulos/{s["slug"]}/{x["slug"]}/"><b>{esc(x["name"])}</b><span>{esc(frase1(x["meta"]))}</span></a>' for x in s['subs'])
    gal = ''.join(fig(k) for k in s['gallery'][:5])
    donde = [l for l in PUB if s['slug'] in LOC[l]['typical']]
    cuerpo = (hero(s['label'], s['h1'], limpia(s['claim']), s['photo']) +
        f'''<section class="bloque claro"><div class="wrap dos-col"><div class="prosa">{''.join(f"<p>{esc(limpia(p))}</p>" for p in s["intro"])}</div>
<div><h2 style="font-size:1.8rem">Qué incluye</h2><ul class="checks">{''.join(f"<li>{esc(limpia(b))}</li>" for b in s["bullets"] if limpia(b))}</ul></div></div></section>
<section class="bloque gris"><div class="wrap"><p class="marca" style="color:var(--tinta-suave)">Tipos</p><h2>{esc(s["short"])}, uno a uno.</h2><div class="tarjetas">{subs}</div></div></section>
<section class="bloque"><div class="wrap"><p class="marca" style="color:var(--tinta-suave)">Trabajos nuestros</p><h2>Hechos en el taller.</h2><div class="galeria">{gal}</div></div></section>
<section class="bloque luz"><div class="wrap"><p class="marca">Precios</p><h2>Cuánto cuesta.</h2>{tabla_precios(s["prices"])}<p class="nota"><b>Plazo orientativo:</b> {esc(limpia(s["duration"]))}</p></div></section>''' +
        pasos_html() + faq_html(fl) + pueblos_chips(donde, f'{s["short"]} en tu pueblo.'))
    sch = [NEGOCIO, {'@type': 'Service', 'name': s['label'], 'serviceType': s['label'], 'provider': {'@id': DOM + '/#taller'},
            'areaServed': [LOC[x]['name'] for x in PUB], 'url': DOM + base}]
    if faq_schema(fl): sch.append(faq_schema(fl))
    pagina(base, limpia(s['title']), limpia(s['meta']), cuerpo, sch, [('Inicio', '/'), ('Qué hacemos', '/rotulos/'), (s['short'], None)])
    for x in s['subs']:
        fx = faqs(x['faqs'])
        cuerpo = (hero(s['label'], x['h1'], limpia(x['intro'][0]) if x['intro'] else '', x.get('photo') or s['photo']) +
            f'''<section class="bloque claro"><div class="wrap dos-col"><div class="prosa">{''.join(f"<p>{esc(limpia(p))}</p>" for p in x["intro"][1:])}<p>Es parte de nuestros <a href="{{{{R}}}}rotulos/{s["slug"]}/">{esc(s["short"].lower())}</a>.</p></div>
<div><h2 style="font-size:1.8rem">Qué incluye</h2><ul class="checks">{''.join(f"<li>{esc(limpia(b))}</li>" for b in x["bullets"] if limpia(b))}</ul></div></div></section>''' +
            (f'<section class="bloque luz"><div class="wrap"><p class="marca">Precios</p><h2>Cuánto cuesta.</h2>{tabla_precios(x["prices"])}</div></section>' if x['prices'] else '') +
            pasos_html() + faq_html(fx))
        sch = [NEGOCIO, {'@type': 'Service', 'name': x['name'], 'serviceType': s['label'], 'provider': {'@id': DOM + '/#taller'}}]
        if faq_schema(fx): sch.append(faq_schema(fx))
        pagina(f'{base}{x["slug"]}/', limpia(x['title']), limpia(x['meta']), cuerpo, sch,
               [('Inicio', '/'), ('Qué hacemos', '/rotulos/'), (s['short'], base), (x['name'], None)])

tarj = ''.join(f'<a class="tarjeta" href="{{{{R}}}}rotulos/{s["slug"]}/"><b>{esc(s["short"])}</b><span>{esc(limpia(s["claim"]))}</span></a>' for s in D['services'])
pagina('/rotulos/', 'Qué hacemos: rótulos, letras corpóreas, vehículos, vallas y señalización | Dígito Rotulación',
       'Todo lo que diseñamos, fabricamos y montamos desde nuestro taller de La Carlota: rótulos luminosos, letras corpóreas, rotulación de vehículos, vallas y monopostes, señalización, impresión digital, neón y LED.',
       hero('Qué hacemos', 'Siete oficios, un taller.', 'Todo sale de nuestra nave del Polígono Gallardo, en La Carlota: lo diseñamos, lo fabricamos y te lo montamos.', 'tallerCajon') +
       f'<section class="bloque claro"><div class="wrap"><div class="tarjetas">{tarj}</div></div></section>' + pasos_html(),
       [NEGOCIO], [('Inicio', '/'), ('Qué hacemos', None)])

# ───────────────────────── pueblos ─────────────────────────
PRUEBAS = {'la-carlota': ['camionCarlotena', 'senalVial', 'totemCarlotena', 'vallaVillas', 'carlotenaCorporeo', 'vallaNueva'], 'guadalcazar': ['paneles']}
for slug in PUB:
    l = LOC[slug]
    pob = f' Tiene {INE[slug]:,} habitantes (INE 2025).'.replace(',', '.') if slug in INE else ''
    dist = '' if slug == 'la-carlota' else f'Desde nuestro taller de La Carlota hay unos {l["km"]} km. '
    tip = [SERV[t] for t in l['typical'] if t in SERV]
    tarjetas = ''.join(f'<a class="tarjeta" href="{{{{R}}}}rotulos/{t["slug"]}/"><b>{esc(t["short"])}</b><span>{esc(limpia(t["claim"]))}</span></a>' for t in tip)
    pruebas = PRUEBAS.get(slug)
    if pruebas:
        fot = ''.join(fig(k) for k in pruebas[:6]); tit_f = f'Trabajos nuestros en {l["name"]}.'
    else:
        fot = ''.join(fig(SERV[t]['photo']) for t in l['typical'][:3] if t in SERV); tit_f = 'Algunos trabajos de nuestro archivo.'
    zonas = f'<p><b>Zonas:</b> {esc(", ".join(l["zones"]))}.</p>' if l.get('zones') and slug in ('la-carlota',) else ''
    permiso = ('<p>Antes de colgar un rótulo en la fachada, mira qué pide el ayuntamiento. En Córdoba capital lo explicamos en la <a href="{{R}}guias/licencia-rotulo-fachada-cordoba/">guía de permisos</a>.</p>'
               if slug == 'cordoba' else f'<p>Cada ayuntamiento tiene su propia ordenanza para rótulos y publicidad exterior. Antes de fabricar, confírmala con el de {esc(l["name"])}; en la <a href="{{{{R}}}}guias/licencia-rotulo-fachada-cordoba/">guía de permisos</a> tienes lo que se suele pedir.</p>')
    cerca = [x for x in l['nearby'] if x in PUB and x != slug]
    h1 = 'Rótulos en La Carlota, nuestro pueblo' if slug == 'la-carlota' else f'Rótulos en {l["name"]}'
    cuerpo = (hero(f'Rótulos en {l["name"]}', h1, f'{dist}Te lo diseñamos, lo fabricamos en el taller y te lo montamos en {l["name"]}.', (pruebas or [SERV[l["typical"][0]]["photo"]])[0]) +
        f'''<section class="bloque claro"><div class="wrap dos-col"><div class="prosa"><p>{esc(angulo(l))}{esc(pob)}</p>{zonas}{permiso}</div>
<div class="prosa"><h2 style="font-size:1.8rem;margin-top:0">Si estás en {esc(l["name"])}</h2><p>No hace falta que vengas al taller: mándanos por WhatsApp una foto de la fachada, el vehículo o el sitio, con medidas aproximadas. Con eso te preparamos el diseño y el presupuesto.</p>
<p><a class="btn btn-tinta" href="#presupuesto"><svg class="ico"><use href="#i-wa"/></svg>Pedir presupuesto</a></p></div></div></section>
<section class="bloque gris"><div class="wrap"><p class="marca" style="color:var(--tinta-suave)">Lo que hacemos</p><h2>Para negocios de {esc(l["name"])}.</h2><div class="tarjetas">{tarjetas}</div></div></section>
<section class="bloque"><div class="wrap"><p class="marca" style="color:var(--tinta-suave)">Trabajos</p><h2>{tit_f}</h2><div class="fotos-3">{fot}</div></div></section>''' +
        pasos_html() + pueblos_chips(cerca, 'Cerca de ' + l['name'] + '.'))
    sch = [NEGOCIO, {'@type': 'Service', 'name': f'Rótulos en {l["name"]}', 'serviceType': 'Rotulación', 'provider': {'@id': DOM + '/#taller'},
            'areaServed': {'@type': 'City', 'name': l['name'], 'containedInPlace': {'@type': 'AdministrativeArea', 'name': f'Provincia de {l["province"]}'}}}]
    t = f'Rótulos en {l["name"]}: luminosos, corpóreos y vehículos | Dígito, taller en La Carlota'
    m = f'Rótulos, letras corpóreas, rotulación de vehículos y señalización para negocios de {l["name"]}. Los fabricamos en nuestro taller de La Carlota{"" if slug == "la-carlota" else " (a unos " + str(l["km"]) + " km)"} y te los montamos. Presupuesto con una foto por WhatsApp.'
    pagina(f'/rotulos-en/{slug}/', t, m, cuerpo, sch, [('Inicio', '/'), ('Pueblos', '/rotulos-en/'), (l['name'], None)])

todos = ''.join(f'<a class="tarjeta" href="{{{{R}}}}rotulos-en/{s}/"><b>{esc(LOC[s]["name"])}</b><span>{"Nuestro pueblo" if s == "la-carlota" else "A unos " + str(LOC[s]["km"]) + " km del taller"}</span></a>' for s in PUB)
pagina('/rotulos-en/', 'Dónde montamos: rótulos en La Carlota, la Campiña, Córdoba y Écija | Dígito Rotulación',
       'Montamos rótulos desde La Carlota en los pueblos de la Campiña y la Vega, en Córdoba capital y en Écija. Elige tu pueblo.',
       hero('Dónde montamos', 'De La Carlota a tu fachada.', 'Estamos en la A-4, entre Córdoba y Écija. Estos son los pueblos donde montamos.', 'furgoneta') +
       f'<section class="bloque claro"><div class="wrap"><div class="tarjetas">{todos}</div></div></section>', [NEGOCIO], [('Inicio', '/'), ('Pueblos', None)])

# ───────────────────────── guías ─────────────────────────
URL_OK = lambda u: u
def reescribe_enlaces(soup, r):
    for a in soup.find_all('a', href=True):
        h = a['href']
        if h.startswith('http') or h.startswith('tel:') or h.startswith('mailto:') or h.startswith('#'): continue
        seg = [x for x in h.split('/') if x]
        dest = None
        if seg[:1] == ['rotulos'] and len(seg) >= 2 and seg[1] in SERV: dest = '/'.join(seg[:3]) + '/'
        elif seg[:1] == ['rotulos-en'] and len(seg) >= 2: dest = f'rotulos-en/{seg[1]}/' if seg[1] in PUB else (f'rotulos/{seg[2]}/' if len(seg) > 2 and seg[2] in SERV else None)
        elif seg[:1] == ['guias'] and len(seg) >= 2: dest = f'guias/{seg[1]}/'
        elif seg[:1] == ['trabajos']: dest = 'trabajos/'
        elif seg[:1] in (['presupuesto'], ['contacto']): dest = '#presupuesto'
        if dest is None: a.unwrap()
        else: a['href'] = dest if dest.startswith('#') else r + dest

def porta_guia(g, r):
    s = open(os.path.join(F, 'guias', g['slug'] + '.html'), encoding='utf-8').read()
    soup = BeautifulSoup(s, 'html.parser')
    prosa = soup.select_one('div.prose')
    for sel in ['p.lead', 'p.kicker', 'h1', 'div.byline', 'figure', 'p.guide__svc', '.prices__cta', '.wa', '.faq__wa', 'div.more-guides', '.section-head p.note', 'script']:
        for e in prosa.select(sel): e.decompose()
    for t in prosa.find_all(['p', 'li', 'td', 'summary']):
        if t.find(['p', 'ul', 'ol', 'table']): continue
        txt = t.get_text(' ', strip=True)
        if limpia(txt) != re.sub(r'\s{2,}', ' ', txt).strip():
            nuevo = limpia(txt)
            if not nuevo: t.decompose(); continue
            t.clear(); t.append(nuevo)
    for d in prosa.find_all('details'):
        if not d.find('p') or not d.find('summary'): d.decompose()
    for e in prosa.find_all(True):
        if e.name not in ('a',): e.attrs = {k: v for k, v in e.attrs.items() if k in ('open', 'colspan', 'rowspan')}
    for td in prosa.find_all('td'):
        for sp in td.find_all('span'): sp.name = 'small'
    for tb in prosa.find_all('table'):
        tb['class'] = 'precios'; w = soup.new_tag('div'); w['class'] = 'tabla-wrap'; tb.wrap(w)
    lead = prosa.find('p')
    if lead and 'Respuesta corta' in lead.get_text(): lead['class'] = 'corto'
    reescribe_enlaces(prosa, r)
    faqs_g = [(d.find('summary').get_text(' ', strip=True), d.find('p').get_text(' ', strip=True)) for d in prosa.find_all('details')]
    return prosa.decode_contents(), faqs_g

LICENCIA = open(os.path.join(F, 'guia-licencia.html'), encoding='utf-8').read()
for g in D['guides']:
    path = f'/guias/{g["slug"]}/'
    r = rel(2)
    if g['slug'] == 'licencia-rotulo-fachada-cordoba':
        cuerpo_g, fq = LICENCIA, []
    else:
        cuerpo_g, fq = porta_guia(g, r)
    serv = SERV.get(g.get('service'))
    enlace = f'<p class="nota">¿Buscas quién te lo haga? Mira nuestros <a href="{{{{R}}}}rotulos/{serv["slug"]}/">{esc(serv["short"].lower())}</a>.</p>' if serv else ''
    fk = serv['photo'] if serv else 'tallerCajon'
    cuerpo = (hero('Guía · septiembre de 2026', g['title'], limpia(g['desc']), fk, cls=' guia') +
              f'<section class="bloque claro"><div class="wrap"><article class="prosa">{cuerpo_g}{enlace}</article></div></section>')
    sch = [NEGOCIO, {'@type': 'Article', 'headline': g['title'], 'dateModified': '2026-09-24', 'author': {'@id': DOM + '/#taller'}, 'publisher': {'@id': DOM + '/#taller'}}]
    if faq_schema(fq): sch.append(faq_schema(fq))
    pagina(path, g['title'] + ' | Dígito Rotulación', limpia(g['desc']), cuerpo, sch, [('Inicio', '/'), ('Guías', '/guias/'), (g['short'], None)])

gl = ''.join(f'<a class="tarjeta" href="{{{{R}}}}guias/{g["slug"]}/"><b>{esc(g["short"])}</b><span>{esc(limpia(g["desc"]))}</span></a>' for g in D['guides'])
pagina('/guias/', 'Guías: precios de rótulos, permisos y materiales | Dígito Rotulación',
       'Lo que conviene saber antes de encargar un rótulo: precios orientativos, permisos en Córdoba, materiales y cómo pedir presupuesto sin visita.',
       hero('Guías', 'Antes de pedir un rótulo.', 'Precios orientativos, permisos, materiales y cómo pedir presupuesto sin que tengamos que ir.', 'tallerCajon') +
       f'<section class="bloque claro"><div class="wrap"><div class="tarjetas">{gl}</div></div></section>', [NEGOCIO], [('Inicio', '/'), ('Guías', None)])

# ───────────────────────── trabajos ─────────────────────────
CATS = {'luminosos': 'Rótulos luminosos', 'corporeos': 'Letras corpóreas', 'vehiculos': 'Vehículos', 'vallas': 'Vallas', 'monopostes': 'Monopostes',
        'senalizacion': 'Señalización', 'digital': 'Impresión digital', 'neon-leds': 'Neón y LED', 'varios': 'Taller y otros'}
secs = ''
for c, nombre in CATS.items():
    ks = [k for k, p in FOTOS.items() if p['cat'] == c]
    if not ks: continue
    secs += f'<section class="bloque {"claro" if len(secs) % 2 else ""}" id="{c}"><div class="wrap"><h2>{esc(nombre)}</h2><div class="galeria">{"".join(fig(k) for k in ks)}</div></div></section>'
otras = sorted(set(p['cat'] for p in FOTOS.values()) - set(CATS))
assert not otras, otras
pagina('/trabajos/', 'Trabajos de rotulación: luminosos, corpóreos, vehículos y vallas | Dígito Rotulación',
       'Fotos reales de trabajos fabricados y montados por nuestro taller de La Carlota: rótulos luminosos, letras corpóreas, vehículos, vallas, monopostes, señalización e impresión digital.',
       hero('Trabajos', 'Todo lo de esta página es nuestro.', f'{len(FOTOS)} fotos de trabajos fabricados en el taller y montados en la calle. Ni una de un banco de imágenes.', 'econaturNave') + secs,
       [NEGOCIO, {'@type': 'ImageGallery', 'name': 'Trabajos de Dígito Rotulación'}], [('Inicio', '/'), ('Trabajos', None)])

# ───────────────────────── home, css, sitemap, llms ─────────────────────────
os.makedirs(os.path.join(RAIZ, 'css'), exist_ok=True)
open(os.path.join(RAIZ, 'css', 'digito.css'), 'w', encoding='utf-8').write((CSS_BASE + CSS_SUB).replace("url('fonts/", "url('../fonts/"))
PIE_HOME = pie_links('')
exec(open(os.path.join(F, 'build_v2.py'), encoding='utf-8').read().replace("S = os.path.dirname(os.path.abspath(__file__))", f"S = r'{F}'"))
PAGINAS.insert(0, ('/', 'Inicio'))
urls = ''.join(f'<url><loc>{DOM}{p}</loc><lastmod>2026-09-24</lastmod></url>' for p, _ in PAGINAS)
open(os.path.join(RAIZ, 'sitemap.xml'), 'w', encoding='utf-8').write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
llms = ['# Dígito Rotulación', '', '> Taller de rótulos en La Carlota (Córdoba) desde 1993: diseño, fabricación en taller propio y montaje de rótulos luminosos, letras corpóreas, rotulación de vehículos, vallas y monopostes, señalización e impresión digital. Tel. 957 30 17 73 · WhatsApp 696 915 689 · P.I. Gallardo, C/ Ingeniero Juan de la Cierva, 38, 14100 La Carlota.', '']
for p, t in PAGINAS: llms.append(f'- [{t}]({DOM}{p})')
open(os.path.join(RAIZ, 'llms.txt'), 'w', encoding='utf-8').write('\n'.join(llms) + '\n')
print(len(PAGINAS), 'páginas ·', len(usadas), 'fotos usadas')
