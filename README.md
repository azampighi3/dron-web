# Sitio web — RCKT

Sitio estático (HTML + CSS, sin dependencias externas) construido siguiendo la arquitectura en silos y el
checklist SEO definidos en la investigación previa.

## Dónde se edita cada cosa

Solo se tocan dos archivos: `contenido.py` (los textos) y `build.py` (todo lo demás).

| Qué quieres cambiar | Archivo | Dónde exactamente |
|---|---|---|
| Textos de cualquier página | `contenido.py` | La variable con el nombre de la página (`HOME`, `CURVAS`, `EMPRESA`…) |
| Títulos y descripciones para Google | `contenido.py` | Lista `PAGINAS`, campos `title` y `desc` |
| Preguntas frecuentes | `contenido.py` | Listas que terminan en `_FAQ` |
| Teléfono, correo, marca, dominio | `build.py` | Diccionario `CONFIG` |
| Precios de la calculadora | `build.py` | Diccionario `COTIZADOR` |
| Zonas y distancias de la calculadora | `build.py` | `COTIZADOR["zonas"]` |
| Ocultar un servicio | `build.py` | Lista `SERVICIOS_OCULTOS` |
| Menú de navegación | `build.py` | Lista `NAV` |
| Colores, tamaños, diseño | `build.py` | Bloque `CSS`, variables de `:root` |
| Iconos | `build.py` | Diccionario `ICONOS` |
| Comunas del schema (SEO local) | `build.py` | Lista `ZONAS_SERVICIO` |

Después de cualquier cambio: doble clic en `ver-sitio.bat` (o `python build.py` si prefieres la consola).

**Nunca edites los archivos `.html`**: se regeneran completos en cada ejecución y perderías el cambio.

## Estructura visual

- **Color principal**: `--tinta-950` (#05090d) para cabecera, hero, CTA y pie; contenido sobre blanco.
- **Acento**: cian `--acento` (#17c3d4) sobre fondo oscuro y `--acento-txt` (#0c7c89) sobre fondo claro,
  para mantener contraste AA en texto.
- **Iconos**: SVG en línea definidos en el diccionario `ICONOS` de `build.py`. Para agregar uno nuevo,
  añade su `path` al diccionario y úsalo con `icono("nombre")`.
- **Patrones de fondo**: `patron("curvas")` (curvas de nivel concéntricas) para las secciones de dron y
  topografía; `patron("flujo")` (líneas de flujo y nodos de red) para las de ingeniería hidráulica.
  La opacidad se controla en el CSS, en `.patron--curvas` y `.patron--flujo`.

## Calculadora de cotización (`/cotizador/`)

Todo el modelo de costos vive en el diccionario `COTIZADOR`, arriba en `build.py`. El visitante solo ve
el precio final: ni la fórmula ni los parámetros aparecen en pantalla.

**Cómo se arma el valor** (para tu referencia, no se muestra en el sitio):

1. Jornadas de terreno y de gabinete, calculadas con exponentes menores a 1 sobre la superficie — de ahí
   sale la economía de escala: a más hectáreas, menos costo por hectárea.
2. Traslados: viajes según distancia, km recorridos, jornadas de viaje y noches de alojamiento cuando
   el terreno está lejos de la base.
3. Equipos: dron y baterías amortizados por jornada de vuelo. Los trabajos grandes exigen más baterías
   y eso sube el costo por jornada.
4. Todo lo anterior se multiplica por `factor_gg_utilidades` (1,5) y se redondea hacia arriba.

**Transición entre jornadas.** El precio no salta de golpe al cruzar una jornada: un excedente de hasta
`tolerancia_horas_extra` (30%) se cubre estirando el día —más horas de vuelo, una batería adicional y
cargador portátil— y se cobra proporcional con un recargo de `recargo_horas_extra`. Si el excedente es
mayor, hay que volver otro día, pero se cobra a prorrata con un piso de media jornada
(`jornada_parcial_minima`). Resultado: entre 5 y 1.000 ha el mayor salto de precio entre dos tamaños
consecutivos es de unos $70.000 sobre valores de más de un millón.

**Dos advertencias importantes:**

- *El cálculo ocurre en el navegador.* Alguien con conocimientos técnicos puede abrir el código fuente
  de la página y leer los parámetros. Queda oculto para el 99% de los visitantes, pero no es secreto
  frente a un competidor decidido. Para que sea realmente privado hay que mover el cálculo a un
  servidor, lo que ya no es compatible con GitHub Pages (requiere hosting con backend o una función
  serverless).
- *El mínimo cubre una franja amplia.* Con 60 ha/jornada, todo trabajo de hasta ~65 ha en la RM queda en
  el valor mínimo de $350.000. Si esos encargos son frecuentes, conviene subir `minimo`.

Para cambiar zonas y distancias, edita la lista `COTIZADOR["zonas"]`: cada tupla es
`(nombre visible, km desde la base solo ida)`.

## Ocultar servicios temporalmente

Si en alguna época no quieres ofrecer un servicio, agrega su ruta a la lista `SERVICIOS_OCULTOS`, arriba
en `build.py`, y reconstruye. Por ejemplo:

```python
SERVICIOS_OCULTOS = [
    "ingenieria-hidraulica/estudios-inundacion",
]
```

Con eso, ese servicio desaparece automáticamente de:

- el menú de navegación y el pie de página;
- las tarjetas de servicio de la home, del pilar y de las páginas de zona;
- el selector "¿Qué necesitas?" del formulario de contacto;
- el `sitemap.xml`;
- la carpeta publicada (se borra el `index.html` de esa página).

Además, los enlaces que lo mencionaban dentro del texto quedan convertidos en texto normal, así que no
se generan enlaces rotos. Para volver a ofrecerlo, borra la línea y reconstruye.

**Dos detalles a tener en cuenta:**

- El texto sigue mencionando el servicio en algunas frases (por ejemplo, "estudios de inundación" aparece
  como palabra dentro de párrafos de otras páginas). Se quita el enlace, no la mención. Si te molesta,
  edita esos párrafos en `contenido.py`.
- Si el servicio ya estaba publicado, Google puede tener su URL indexada por un tiempo. Al desaparecer el
  archivo, la URL responde 404, que es el comportamiento correcto. En OneDrive puede quedar la carpeta
  vacía sin borrar: no importa, git no versiona carpetas vacías y GitHub Pages devolverá 404 igual.

La lista completa de rutas disponibles está comentada junto a `SERVICIOS_OCULTOS`.

## Ver el sitio en tu computador

**Doble clic en `ver-sitio.bat`.** Eso genera el sitio con los últimos cambios, lo publica en un servidor
local y abre el navegador solo. Deja la ventana negra abierta mientras revisas; para terminar, ciérrala.

Si cambias `contenido.py` o `build.py` mientras el sitio está abierto, cierra la ventana negra y vuelve a
hacer doble clic en `ver-sitio.bat` para ver los cambios.

*No abras los archivos `.html` con doble clic*: la página se ve, pero los enlaces del menú no funcionan
porque el navegador no resuelve las carpetas sin un servidor.

## Publicar en GitHub Pages (Fase 2, gratis)

1. Crea un repositorio público, por ejemplo `rckt-web`.
2. Sube **el contenido de esta carpeta** (incluido `.nojekyll`).
3. Settings → Pages → Source: *Deploy from a branch* → rama `main`, carpeta `/ (root)`.
4. El sitio queda en `https://TUUSUARIO.github.io/rckt-web/`.

Las rutas internas son relativas, así que el sitio funciona igual en un subdirectorio de GitHub Pages
que en un dominio propio.

## Antes de publicar en el dominio definitivo

Ordenado por impacto en visibilidad:

- [ ] **Subir las fotos a `assets/img/`.** Hoy el sitio no tiene ni una imagen real, y Google Imágenes es
      una fuente de tráfico relevante para este rubro. Los nombres esperados aparecen en cada recuadro
      punteado del sitio.
- [ ] **Crear `assets/img/og-portada.jpg` de 1200x630 px.** Se detecta sola: basta dejarla ahí y
      reconstruir. Sin ella, los enlaces compartidos por WhatsApp o LinkedIn no muestran vista previa,
      porque el respaldo actual es un SVG y varias plataformas no lo renderizan.
- [ ] Cambiar `CONFIG["dominio"]` al dominio real y reconstruir (afecta canonical, Open Graph, sitemap
      y JSON-LD).
- [ ] Completar teléfono, email y razón social en `CONFIG`.
- [ ] Ajustar `CONFIG["lat"]` y `CONFIG["lon"]` a la ubicación real de la base (hoy apuntan al centro de
      Santiago). Van al schema de negocio y ayudan al posicionamiento local.
- [ ] Agregar las URLs de LinkedIn e Instagram en `CONFIG["redes"]` cuando existan: se publican como
      `sameAs`, que es una señal de entidad para Google y para los buscadores de IA.
- [ ] Pegar el código de verificación en `CONFIG["gsc_verificacion"]`, registrar el sitio en
      **Google Search Console** y enviar el `sitemap.xml`.
- [ ] Pegar el identificador en `CONFIG["ga4_id"]` para activar Google Analytics 4.
- [ ] Completar la página `empresa/` con datos verificables (título profesional, registro DGAC, RUT).
- [ ] Crear el perfil de **Google Business** como *negocio con área de servicio*, declarando todas las
      comunas de `ZONAS_SERVICIO`.

## Qué SEO ya está resuelto en el generador

No hay que hacer nada de esto a mano: se genera solo en cada `python build.py`.

- Un `<h1>` único por página y jerarquía de encabezados sin saltos.
- `title` y `meta description` únicos, dentro de los rangos recomendados.
- `canonical` autorreferente y Open Graph completo (incluidas dimensiones y `alt` de la imagen).
- JSON-LD: `ProfessionalService` con geo, horario, catálogo de servicios y `areaServed` por comuna;
  `Service` por cada servicio y por cada zona; `BreadcrumbList`; `FAQPage`; `BlogPosting`.
- `sitemap.xml` y `robots.txt` sincronizados con las páginas realmente publicadas.
- Cero peticiones a servidores externos: todo el CSS, los iconos y los gráficos van en el propio dominio.
- Versionado automático del CSS para que los cambios de diseño no queden ocultos por la caché.
- `404.html` con `noindex, follow`.

## Cuando tengas proyectos que mostrar

El sitio no tiene sección de casos de éxito: en su lugar está `capacidades/`, que describe entregables,
metodología y herramientas. Cuando existan trabajos publicables:

1. Agrega los ejemplos en la sección "Desarrollos propios" de `capacidades/` (en `contenido.py`), o
2. Crea una página `proyectos/` nueva agregando su diccionario a la lista `PAGINAS` y su entrada al `NAV`.

## Imágenes que el sitio está esperando

Deja el archivo en `assets/img/` con el nombre exacto y ejecuta `python build.py`: el recuadro punteado se
reemplaza solo por la foto, con sus medidas y carga diferida. Acepta `.webp`, `.avif`, `.jpg` y `.png`.

| Archivo | Qué mostrar | Dónde aparece |
|---|---|---|
| `dron-en-vuelo-terreno` | El dron operando en terreno real | Pilar de dron |
| `modelo-digital-elevacion` | Modelo de elevación en escala de colores | Home · Nube de puntos |
| `curvas-de-nivel` | Plano de curvas sobre foto aérea | Home · Curvas de nivel |
| `rectificacion-deslindes` | Plano de deslindes con vértices marcados | Deslindes · Capacidades |
| `ortomosaico-predio` | Ortomosaico real de un vuelo hecho | Mapas y ortomosaicos |
| `captura-modelacion-hidraulica` | Pantalla de EPANET o HEC-RAS | Pilar de hidráulica |
| `modelacion-redes-epanet` | Red modelada en EPANET | Home · Modelación de redes |
| `modelacion-golpe-de-ariete` | Gráfico de presión transitoria | Bombas · Capacidades |
| `mapa-inundacion-hecras` | Mancha de inundación por profundidad | Estudios de inundación |
| `drenaje-pluvial` | Plano de colectores o cámara en terreno | Drenaje · Capacidades |
| `plano-red-agua-potable` | Plano de red domiciliaria | Proyectos sanitarios |
| `retrato-profesional-rckt` | Tu foto, retrato o en terreno | Empresa |
| `og-portada.jpg` | Composición 1200×630 para compartir | Todo el sitio (redes) |

Si prefieres nombres que incluyan la zona del proyecto —recomendable para Google Imágenes, por ejemplo
`ortomosaico-predio-pucon-2026.webp`— renombra el archivo y cambia el nombre en la llamada a `figura(...)`
correspondiente dentro de `contenido.py`.

## Cómo poner las imágenes

Cada recuadro punteado tiene, justo debajo en el HTML generado, un comentario con el `<img>` que hay que
dejar en su lugar. En `contenido.py` el bloque se genera con la función `figura(...)`.

- Guardar en `assets/img/` con nombre descriptivo: `ortomosaico-predio-maule-2026.webp`, nunca `IMG_4821.jpg`.
- Convertir a **WebP**, máximo 1600 px de ancho.
- Mantener `width`, `height`, `loading="lazy"` y `alt` descriptivo (80-140 caracteres).
- La primera imagen visible de cada página no debe llevar `loading="lazy"`.
