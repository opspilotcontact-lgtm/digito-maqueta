// Datos del taller. Lo marcado `pendiente` sale en la maqueta con la marca «a confirmar».
export const taller = {
  nombre: 'Dígito Rotulación',
  desde: 1993,
  calle: 'C/ Ingeniero Juan de la Cierva, 38',
  poligono: 'Polígono Industrial Gallardo',
  cp: '14100',
  localidad: 'La Carlota',
  provincia: 'Córdoba',
  fijo: '957 30 17 73',
  fijoTel: '+34957301773',
  whatsapp: '696 915 689',
  whatsappNum: '34696915689',
  email: 'info@digitorotulacion.com',
  // Horario de su ficha de Google; la web de 2018 dice otro. [pendiente · padre]
  horario: { corto: 'L-V 8-14 y 16-18', largo: 'Lunes a viernes, de 8:00 a 14:00 y de 16:00 a 18:00', pendiente: true },
  maps: 'https://www.google.com/maps/search/?api=1&query=Digito%20Rotulaci%C3%B3n%20La%20Carlota',
};

// Zona habitual: la de la v2 (fase 1). La real la confirma el taller. [pendiente · padre]
export const zona = {
  pendiente: true,
  cordoba: ['La Carlota', 'La Victoria', 'Guadalcázar', 'Fuente Palmera', 'Posadas', 'Almodóvar del Río', 'Palma del Río', 'Hornachuelos', 'Santaella', 'La Rambla', 'Fernán Núñez', 'Montemayor', 'Montilla', 'Aguilar de la Frontera', 'Puente Genil', 'Montalbán de Córdoba', 'Córdoba'],
  sevilla: ['Écija', 'La Luisiana', 'Fuentes de Andalucía'],
};

/** Ruta con la base del sitio: u('/trabajos/') → /digito-maqueta/trabajos/ */
export const u = (p = '/') => import.meta.env.BASE_URL.replace(/\/$/, '') + p;
export const img = (f: string) => u('/img/' + f);
export const euros = (n: number) => n.toLocaleString('es-ES') + ' €';
