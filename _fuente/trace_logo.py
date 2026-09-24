"""Vectoriza el logo REAL de Dígito (digitorotulacion_logo.png, 216x108, de su web de 2018) por capas de color.
No se reescribe nada: cada forma sale del contorno de sus píxeles (potrace sobre un reescalado x8)."""
import sys, numpy as np, potrace
from PIL import Image, ImageFilter

SRC, OUT = sys.argv[1], sys.argv[2]
K = 8
im = Image.open(SRC).convert('RGBA')
W, H = im.size
big = im.resize((W * K, H * K), Image.BICUBIC).filter(ImageFilter.GaussianBlur(K * 0.35))
a = np.array(big).astype(float)
R, G, B, A = a[..., 0], a[..., 1], a[..., 2], a[..., 3]
mn = np.minimum(R, G)
lum = 0.299 * R + 0.587 * G + 0.114 * B
sat = np.max(a[..., :3], -1) - np.min(a[..., :3], -1)

sil = A > 128
yy, xx = np.mgrid[0:H * K, 0:W * K]
reg = ((xx / K - 192.3) ** 2 + (yy / K - 9.6) ** 2) < 6.2 ** 2     # el ® se dibuja aparte, limpio
sil &= ~reg
yellow = sil & (mn > 120) & (B < mn * 0.62)
black = sil & (lum < 112)
white = sil & (lum > 190) & (sat < 45)
def closing(m, n):
    img = Image.fromarray((m * 255).astype(np.uint8))
    img = img.filter(ImageFilter.MaxFilter(n)).filter(ImageFilter.MinFilter(n))
    return np.array(img) > 127
upper = closing(white | yellow | black, 13) & sil   # todo lo que no es el canto gris, sin halos de antialias
# el filo blanco exterior del original es de ~1 px: se limita el blanco a 0,9 px del borde
sil_in = np.array(Image.fromarray((sil * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(15))) > 127
upper &= sil_in | black

def trace(mask, turd=40):
    bm = potrace.Bitmap(~mask)
    path = bm.trace(turdsize=turd, turnpolicy=potrace.POTRACE_TURNPOLICY_MINORITY, alphamax=1.05, opticurve=True, opttolerance=0.35)
    f = lambda p: f'{p.x / K:.2f} {p.y / K:.2f}'
    d = []
    for c in path:
        d.append('M' + f(c.start_point))
        for s in c:
            if s.is_corner:
                d.append('L' + f(s.c) + 'L' + f(s.end_point))
            else:
                d.append('C' + f(s.c1) + ' ' + f(s.c2) + ' ' + f(s.end_point))
        d.append('Z')
    return ''.join(d)

def med(mask, q=50):
    px = a[..., :3][mask]
    return '#%02X%02X%02X' % tuple(int(np.percentile(px[:, i], q)) for i in range(3))

orig = np.array(im.convert('RGBA')).astype(float)
o_rgb, o_a = orig[..., :3], orig[..., 3]
omn = np.minimum(orig[..., 0], orig[..., 1]); olum = orig[..., :3] @ [0.299, 0.587, 0.114]
oy = (o_a > 200) & (omn > 150) & (orig[..., 2] < omn * .5)
ys = np.where(oy)[0]
top = '#%02X%02X%02X' % tuple(np.median(o_rgb[oy & (np.arange(H)[:, None] < np.percentile(ys, 30))], 0).astype(int))
bot = '#%02X%02X%02X' % tuple(np.median(o_rgb[oy & (np.arange(H)[:, None] > np.percentile(ys, 88))], 0).astype(int))
og = (o_a > 200) & (olum > 95) & (olum < 170) & ((o_rgb.max(-1) - o_rgb.min(-1)) < 40)
gys = np.where(og)[0]
gtop = '#%02X%02X%02X' % tuple(np.median(o_rgb[og & (np.arange(H)[:, None] < np.percentile(gys, 40))], 0).astype(int))
gbot = '#%02X%02X%02X' % tuple(np.median(o_rgb[og & (np.arange(H)[:, None] > np.percentile(gys, 70))], 0).astype(int))
print('colores medidos: amarillo', top, '->', bot, ' canto', gtop, '->', gbot, ' negro', med(black), ' blanco', med(white))

y0, y1 = np.percentile(np.where(yellow)[0], [0, 100]) / K
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="Dígito Rotulación">
<title>Dígito Rotulación</title>
<!-- Vectorizado del logo original (digitorotulacion_logo.png, 216x108, web de 2018) por capas de color con potrace.
     Geometría real del logo; provisional hasta tener el vector original del taller. -->
<defs>
<linearGradient id="dg-cara" gradientUnits="userSpaceOnUse" x1="0" y1="{y0:.1f}" x2="0" y2="{y1:.1f}"><stop offset=".55" stop-color="{top}"/><stop offset="1" stop-color="{bot}"/></linearGradient>
<linearGradient id="dg-canto" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="{H}"><stop offset=".3" stop-color="{gtop}"/><stop offset="1" stop-color="{gbot}"/></linearGradient>
</defs>
<path class="dg-canto" fill="url(#dg-canto)" fill-rule="evenodd" d="{trace(sil)}"/>
<path class="dg-blanco" fill="#FFFFFF" fill-rule="evenodd" d="{trace(upper)}"/>
<path class="dg-cara" fill="url(#dg-cara)" fill-rule="evenodd" d="{trace(yellow)}"/>
<path class="dg-letras" fill="#0B0B0B" fill-rule="evenodd" d="{trace(black, 12)}"/>
<g class="dg-reg"><circle cx="192.3" cy="9.6" r="5.3" fill="#FFFFFF"/><circle cx="192.3" cy="9.6" r="4.2" fill="none" stroke="#4A4F57" stroke-width=".9"/><text x="192.3" y="11.75" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" font-weight="700" font-size="5.6" fill="#4A4F57">R</text></g>
</svg>
'''
open(OUT, 'w', encoding='utf-8').write(svg)
print('ok', len(svg), 'bytes')
