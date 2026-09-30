import { defineCollection, reference, z } from 'astro:content';
import { glob } from 'astro/loaders';
import { existsSync } from 'node:fs';

// Si una foto no existe en public/img, el build se para y dice cuál: nunca se publica un caso roto.
const foto = z
  .string()
  .refine((f) => existsSync(new URL(`../public/img/${f}`, import.meta.url)), (f) => ({ message: `No existe public/img/${f}` }));

const categorias = defineCollection({
  loader: glob({ pattern: '*.md', base: './src/content/categorias' }),
  schema: z.object({
    nombre: z.string(),                 // «Letras corpóreas»
    palabra: z.string(),                // la palabra de la lona: «Corpóreas»
    orden: z.number(),
    resumen: z.string(),                // una línea, para el índice y la meta
    // «Desde»: lo pone el taller. null = aún no lo ha dado (sale «a confirmar»).
    desde: z.number().nullable(),
    desdeQue: z.string(),               // a qué se refiere el «desde»: «una letra de 30 cm, montada»
    depende: z.array(z.object({ factor: z.string(), texto: z.string() })).min(3),
    fotos: z.array(z.object({ src: foto, alt: z.string(), pie: z.string(), w: z.number(), h: z.number() })).min(4),
  }),
});

const casos = defineCollection({
  loader: glob({ pattern: '[!_]*.md', base: './src/content/casos' }),
  schema: z.object({
    titulo: z.string(),
    categoria: reference('categorias'),
    cliente: z.string(),
    localidad: z.string().nullable(),    // null = a confirmar
    anio: z.number().nullable(),
    resumen: z.string(),
    destacado: z.boolean().default(false),
    permisoCliente: z.boolean(),         // ¿acepta salir en la web con su nombre y precio?
    portada: z.object({ src: foto, alt: z.string() }),
    piezas: z
      .array(z.object({ nombre: z.string(), src: foto, alt: z.string(), precio: z.number().nullable() }))
      .min(1),
  }),
});

export const collections = { categorias, casos };
