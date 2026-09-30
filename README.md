# Dígito Rotulación · propuesta de web (v4, 30-sep-2026)

Propuesta **en revisión**: `noindex`, `robots.txt` con `Disallow: /` y franja de propuesta.
La web oficial sigue en https://digitorotulacion.com.

| Ruta | Qué es |
|---|---|
| `/` | **v4 «el portfolio que filtra»**: la fachada muestrario, 7 oficios, casos pieza a pieza y la ficha de encargo. Astro, fuente en `sitio/`. |
| `/v2/` | v2 (24-sep): la fachada como un solo objeto + las 64 páginas SEO. HTML generado desde `_fuente/`. |
| `/v1/` | v1 archivada. Sus fotos y fuentes las toma de `/v2/`. |

Decisiones de diseño: NotionPilot, doc 915cb423. Método: skill `direccion-arte-web`.

## Cargar contenido en la v4

- **Un caso nuevo**: copiar `sitio/src/content/casos/_plantilla.md` con el nombre del caso (`farmacia-ecija.md`) y rellenarlo. Las fotos van en `sitio/public/img/`.
- **El «desde» de un oficio**: el campo `desde` de `sitio/src/content/categorias/<oficio>.md` (euros con IVA; `null` = sale «a confirmar»).
- **Horario y zona**: `sitio/src/data/site.ts` (poner `pendiente: false` cuando el taller los confirme).
- Si falta una foto o un campo obligatorio, el build se para y dice cuál.

## Publicar

```
cd sitio
npm install        # solo la primera vez
python publicar.py # construye y copia el resultado a la raíz
cd .. && git add -A && git commit -m "..." && git push
```

`publicar.py` borra antes lo que copió la vez anterior (`sitio/.publicado.txt`) y nunca toca `v1/`, `v2/`, `sitio/`, `_fuente/` ni `robots.txt`.
Para el dominio real: `BASE=/ SITE=https://digitorotulacion.com npm run build`.

## Créditos

- Logo: el REAL, vectorizado del PNG de su web de 2018 por capas de color (potrace). Provisional hasta el vector original del taller.
- Colores medidos en su logo y en la foto de su fachada. Fotos: archivo del taller y ficha de Google (provisional).
- Tipografías: Unbounded e Instrument Sans (v4), Anybody (v2) — SIL OFL. Iconos: Lucide (ISC).
