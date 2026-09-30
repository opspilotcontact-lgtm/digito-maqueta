// @ts-check
import { defineConfig } from 'astro/config';

// Maqueta: se publica en GitHub Pages bajo /digito-maqueta/ (con la v2 guardada en /v2/).
// El día que vaya a su dominio: BASE=/ SITE=https://digitorotulacion.com
export default defineConfig({
  site: process.env.SITE ?? 'https://opspilotcontact-lgtm.github.io',
  base: process.env.BASE ?? '/digito-maqueta/',
  trailingSlash: 'always',
  build: { format: 'directory' },
  devToolbar: { enabled: false },
});
