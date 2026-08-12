# -*- coding: utf-8 -*-
"""
CONTENIDO DEL SITIO RCKT. Aquí vive todo el texto: edita esto y ejecuta `python build.py`.

Cada página es un diccionario:
  path            → carpeta/URL (sin barras al inicio ni al final). "" = home
  title           → etiqueta <title>, 50-60 caracteres, única por página
  desc            → meta description, 120-160 caracteres, con llamado a la acción
  crumbs          → migas de pan: [(nombre, href_o_None), ...]
  body            → HTML de la página
  faq             → [(pregunta, respuesta_html), ...]  → genera FAQ + schema FAQPage
  schema_servicio → (nombre, descripción, tipo) → genera schema Service
  schema_articulo → (titular, fecha, descripción) → genera schema BlogPosting

Componentes (definidos en build.py):
  icono("dron")                        → SVG en línea
  tarjetas([(icono, título, texto, href_o_None), ...])
  datos([(cifra, etiqueta, icono), ...])
  pasos([(título, descripción), ...])
  lista_iconos([(icono, texto), ...])
  patron("curvas") / patron("flujo")   → fondo suave
  figura("nombre-archivo", "texto alternativo", "pie de foto")
      → si assets/img/nombre-archivo.webp (o .jpg/.png/.avif) existe, inserta la
        imagen real; si no, deja un recuadro indicando qué archivo falta.
"""

from build import (CONFIG, icono, figura, pasos, datos, tarjetas, lista_iconos, patron,
                   cotizador_html, opciones_consulta)

WSP = "https://wa.me/" + CONFIG["whatsapp"]

# ==========================================================================
# HOME
# ==========================================================================
HOME = '''
<section class="hero">
  ''' + patron("curvas") + '''
  <div class="contenedor hero__caja">
    <p class="hero__etiqueta">''' + icono("rayo", "icono icono--sm") + ''' Dron · Topografía · Ingeniería hidráulica</p>
    <h1>Levantamos el terreno y resolvemos el agua</h1>
    <p class="hero__bajada">Topografía con dron y proyectos hidráulicos en una sola oficina. La misma base
    de terreno que levantamos alimenta el cálculo, sin coordinar dos proveedores.</p>
    <div class="hero__acciones">
      <a class="boton boton--acento" href="{{P}}cotizador/">Calcular mi cotización ''' + icono("flecha", "icono icono--sm") + '''</a>
      <a class="boton boton--fantasma" href="{{P}}contacto/">Hablemos</a>
    </div>
    <ul class="hero__chips">
      <li>''' + icono("objetivo", "icono icono--sm") + ''' Precisión de 2 a 5 cm</li>
      <li>''' + icono("reloj", "icono icono--sm") + ''' Entrega en 5 a 10 días</li>
      <li>''' + icono("escudo", "icono icono--sm") + ''' RPAS registrado ante la DGAC</li>
    </ul>
  </div>
</section>

<section class="seccion">
  <div class="contenedor">
    <h2 class="seccion__titulo">Dron y topografía</h2>
    ''' + tarjetas([
    ("dron", "Fotogrametría aérea",
     "Nube de puntos y modelo digital de terreno para cubicar, diseñar y controlar obra.",
     "dron-fotogrametria/fotogrametria/"),
    ("curvas", "Curvas de nivel",
     "Cada 0,25 · 0,5 o 1 m, en DWG listo para Civil 3D.",
     "dron-fotogrametria/curvas-de-nivel/"),
    ("deslindes", "Deslindes y linderos",
     "Límites reales del predio, con coordenadas por vértice.",
     "dron-fotogrametria/deslindes-linderos/"),
    ("mapa", "Mapas y ortomosaicos",
     "Imagen georreferenciada de 2 a 5 cm/píxel, medible a escala.",
     "dron-fotogrametria/mapas-ortomosaicos/"),
    ("calculo", "Calculadora de cotización",
     "Ingresa superficie y ubicación y obtén el valor al instante.",
     "cotizador/"),
]) + '''
  </div>
</section>

<section class="seccion seccion--clara">
  <div class="contenedor">
    <h2 class="seccion__titulo">Ingeniería hidráulica</h2>
    ''' + tarjetas([
    ("red", "Modelación de redes",
     "Presiones, velocidades y diámetros verificados en EPANET.",
     "ingenieria-hidraulica/modelacion-redes/"),
    ("bomba", "Bombas e impulsiones",
     "Punto de operación, golpe de ariete y eficiencia energética.",
     "ingenieria-hidraulica/dimensionamiento-bombas-impulsiones/"),
    ("inundacion", "Estudios de inundación",
     "Áreas inundables y cota de seguridad con HEC-RAS.",
     "ingenieria-hidraulica/estudios-inundacion/"),
    ("drenaje", "Drenaje pluvial",
     "Escorrentía, colectores y obras de retención o infiltración.",
     "ingenieria-hidraulica/drenaje-pluvial/"),
    ("sanitario", "Proyectos sanitarios",
     "Agua potable y alcantarillado con memoria y planos.",
     "ingenieria-hidraulica/proyectos-sanitarios/"),
]) + '''
  </div>
</section>

<section class="seccion">
  <div class="contenedor">
    <h2 class="seccion__titulo">Cómo se ve el trabajo</h2>
    <div class="galeria">
      ''' + figura("modelo-digital-elevacion",
                   "Modelo digital de elevación en escala de colores generado con dron",
                   "Modelo digital de elevación") + '''
      ''' + figura("curvas-de-nivel",
                   "Plano de curvas de nivel obtenidas de un levantamiento con dron",
                   "Curvas de nivel restituidas") + '''
      ''' + figura("modelacion-redes-epanet",
                   "Modelación hidráulica de una red de agua potable en EPANET",
                   "Modelación de red en EPANET") + '''
    </div>
  </div>
</section>

<section class="seccion seccion--oscura">
  ''' + patron("flujo") + '''
  <div class="contenedor">
    <h2 class="seccion__titulo">Por qué las dos especialidades juntas</h2>
    <p class="seccion__bajada">Todo cálculo hidráulico depende de la cota. Al levantar el terreno nosotros
    mismos, el modelo se construye sobre datos medidos con precisión centimétrica.</p>
    ''' + datos([
    ("2–5 cm", "Precisión con puntos de control", "objetivo"),
    ("60 ha", "Cubiertas por jornada de vuelo", "mapa"),
    ("5–10 días", "Plazo de entrega habitual", "reloj"),
    ("DWG · LAS", "Formatos editables", "archivo"),
]) + '''
  </div>
</section>

<section class="seccion">
  <div class="contenedor">
    <h2 class="seccion__titulo">Dónde trabajamos</h2>
    <p class="seccion__bajada">Base en ''' + CONFIG["ciudad_base"] + ''', con cobertura entre Coquimbo y
    La Araucanía.</p>
    ''' + tarjetas([
    ("pin", "Santiago y RM", "Deslindes, drenaje y proyectos sanitarios urbanos.", "zonas/santiago-rm/"),
    ("pin", "La Serena y Coquimbo", "Riego, pozos y quebradas de los valles del norte chico.", "zonas/coquimbo-la-serena-iv-region/"),
    ("pin", "Valparaíso y V Región", "Terrenos costeros, quebradas y pendiente fuerte.", "zonas/valparaiso-vina-v-region/"),
    ("pin", "O'Higgins", "Predios agrícolas y vitivinícolas, curvas para riego.", "zonas/ohiggins-vi-region/"),
    ("pin", "Maule", "Levantamientos prediales extensos y drenaje agrícola.", "zonas/maule-vii-region/"),
    ("pin", "Pucón y Villarrica", "Parcelaciones, deslindes y agua particular.", "zonas/pucon-villarrica-caburgua/"),
]) + '''
  </div>
</section>
'''

HOME_FAQ = [
    ("¿Cuánto cuesta un levantamiento con dron?",
     "Depende de la superficie y la ubicación. Puedes calcularlo al instante en la "
     "<a href='{{P}}cotizador/'>calculadora de cotización</a> o escribirnos con los datos del terreno."),
    ("¿Qué precisión tiene un levantamiento fotogramétrico?",
     "Con puntos de control medidos con GNSS, entre 2 y 5 cm en planta. Sin ellos queda sujeto al GPS del "
     "dron: 1 a 3 m, útil como referencia pero no para diseño ni deslindes."),
    ("¿El levantamiento con dron reemplaza a un topógrafo?",
     "En superficies medianas y grandes entrega mucha más información en el mismo tiempo, pero necesita "
     "apoyo en terreno para georreferenciar. Hay casos —vegetación densa, deslindes con validez legal— que "
     "requieren medición directa."),
    ("¿Entregan archivos editables?",
     "Sí: DWG y DXF para curvas y planimetría, GeoTIFF para el ortomosaico, LAS/LAZ para la nube de puntos. "
     "Listos para importar en Civil 3D, QGIS o ArcGIS."),
]

# ==========================================================================
# PILAR: DRON
# ==========================================================================
DRON_PILAR = '''
<section class="encabezado">
  ''' + patron("curvas") + '''
  <div class="contenedor">
    <p class="encabezado__etiqueta">Dron y topografía</p>
    <h1>Fotogrametría y topografía con dron en Chile</h1>
    <p class="encabezado__bajada">Fotografiamos el terreno desde el aire con alto traslape y procesamos esas
    imágenes para obtener un modelo tridimensional georreferenciado. De ahí salen el ortomosaico, el modelo
    digital de terreno y las curvas de nivel, con mucha más densidad de datos que un levantamiento
    tradicional y una fracción del tiempo de terreno.</p>
  </div>
</section>

<section class="seccion">
  <div class="contenedor">
    ''' + datos([
    ("2–5 cm", "Precisión con puntos de control", "objetivo"),
    ("2 cm/píxel", "Resolución del ortomosaico", "mapa"),
    ("60 ha", "Por jornada de vuelo", "capas"),
    ("5–10 días", "Plazo de entrega", "reloj"),
]) + '''
  </div>
</section>

<section class="seccion seccion--clara">
  <div class="contenedor">
    <h2 class="seccion__titulo">Qué servicio necesitas</h2>
    <p class="seccion__bajada">Todos parten del mismo vuelo; cambia el procesamiento y el entregable.</p>
    ''' + tarjetas([
    ("dron", "Fotogrametría aérea",
     "El servicio base: nube de puntos y modelo digital de terreno. Para cubicar, diseñar y controlar obra.",
     "dron-fotogrametria/fotogrametria/"),
    ("curvas", "Curvas de nivel",
     "Restitución a la equidistancia que necesite el proyecto. Es lo que pide un arquitecto o un proyectista de riego.",
     "dron-fotogrametria/curvas-de-nivel/"),
    ("deslindes", "Deslindes y linderos",
     "Cercos, muros y ocupación real contrastados con los planos existentes.",
     "dron-fotogrametria/deslindes-linderos/"),
    ("mapa", "Mapas y ortomosaicos",
     "Imagen aérea corregida y georreferenciada, medible a escala real.",
     "dron-fotogrametria/mapas-ortomosaicos/"),
    ("calculo", "Calculadora de cotización",
     "Superficie y ubicación, y obtienes el valor estimado al instante.",
     "cotizador/"),
]) + '''
  </div>
</section>

<section class="seccion">
  <div class="contenedor">
    <h2 class="seccion__titulo">Cómo es el proceso</h2>
    ''' + pasos([
    ("Planificación del vuelo",
     "Altura, traslape y patrón según la resolución objetivo y el relieve. Se revisan restricciones de espacio aéreo antes de salir."),
    ("Puntos de control",
     "Cuando se requiere precisión de diseño, se miden puntos de control en terreno más puntos de verificación independientes."),
    ("Vuelo y captura",
     "Ejecución del plan, control de calidad de las imágenes en sitio y registro de cercos, cámaras y cauces."),
    ("Procesamiento",
     "Nube de puntos, clasificación de suelo y vegetación, y generación del modelo de terreno y el ortomosaico."),
    ("Entrega",
     "Curvas, planimetría y superficies en los formatos que usa tu equipo, con informe técnico."),
]) + '''
    <p>Los vuelos se ejecutan con RPAS registrado ante la DGAC y bajo la normativa
    <a href="https://www.dgac.gob.cl/" rel="noopener" target="_blank">DAN 151</a>.</p>
  </div>
</section>
'''

DRON_FAQ = [
    ("¿Cuál es la diferencia entre ortomosaico, MDS y MDT?",
     "El ortomosaico es la imagen aérea corregida, sobre la que se puede medir. El MDS representa todo lo "
     "que ve el dron, incluidos árboles y techos. El MDT es el suelo desnudo, y es el que se usa para curvas "
     "de nivel y diseño."),
    ("¿Cuánta superficie se levanta en un día?",
     "Del orden de 60 hectáreas por jornada en trabajos de precisión, y bastante más si se vuela a mayor "
     "altura. En predios muy quebrados o con vegetación alta el rendimiento baja."),
    ("¿Se puede volar con viento o nubes bajas?",
     "El viento sostenido sobre 8–10 m/s y la lluvia impiden volar. La nubosidad alta ayuda: da luz difusa y "
     "evita sombras duras."),
    ("¿Necesito autorización para que vuelen mi terreno?",
     "La operación la gestionamos nosotros. De tu parte solo necesitamos la autorización para acceder al "
     "predio y, en zonas urbanas o cercanas a aeródromos, algo más de tiempo para tramitar."),
]

# ==========================================================================
# DRON — SUBPAGINAS
# ==========================================================================
FOTOGRAMETRIA = '''
<section class="encabezado">
  ''' + patron("curvas") + '''
  <div class="contenedor">
    <p class="encabezado__etiqueta">Dron y topografía</p>
    <h1>Fotogrametría aérea con dron: modelo 3D y nube de puntos</h1>
    <p class="encabezado__bajada">Convertimos cientos de fotografías aéreas en un modelo tridimensional
    medible del terreno. De esa nube de puntos salen el modelo digital de superficie, el de terreno y todos
    los productos derivados.</p>
  </div>
</section>

<section class="seccion">
  <div class="contenedor">
    ''' + figura("modelo-digital-elevacion",
                 "Modelo digital de elevación en escala de colores obtenido por fotogrametría con dron",
                 "Modelo digital de elevación: cada color representa una cota distinta del terreno",
                 "16 / 9") + '''
    <h2>Qué incluye el entregable</h2>
    ''' + lista_iconos([
    ("mapa", "<strong>Ortomosaico</strong> en GeoTIFF, de 2 a 5 cm/píxel."),
    ("capas", "<strong>Nube de puntos</strong> en LAS/LAZ, clasificada en suelo y no-suelo."),
    ("montana", "<strong>Modelo digital de superficie y de terreno</strong> en formato ráster."),
    ("curvas", "<strong>Curvas de nivel</strong> en DWG/DXF."),
    ("archivo", "<strong>Informe técnico</strong> con parámetros de vuelo y error verificado."),
]) + '''
  </div>
</section>

<section class="seccion seccion--clara">
  <div class="contenedor">
    <h2 class="seccion__titulo">Qué determina la precisión</h2>
    ''' + pasos([
    ("Altura de vuelo",
     "El tamaño de píxel en el terreno define el detalle máximo. A 80 m se obtienen unos 2 cm/píxel; a 120 m, unos 3 cm."),
    ("Puntos de control",
     "Sin puntos medidos con GNSS, el modelo queda con la precisión del GPS del dron: 1 a 3 m. Con 5 a 8 bien distribuidos, baja a 2–5 cm."),
    ("Cobertura del suelo",
     "Bajo vegetación densa el modelo de terreno se interpola y pierde exactitud; ahí se complementa con medición directa."),
]) + '''
    <p>Por eso la primera pregunta que hacemos no es cuántas hectáreas son, sino para qué se va a usar el
    levantamiento.</p>
  </div>
</section>

<section class="seccion">
  <div class="contenedor">
    <p><strong>Servicios relacionados:</strong> del mismo vuelo salen las
    <a href="{{P}}dron-fotogrametria/curvas-de-nivel/">curvas de nivel</a> y el
    <a href="{{P}}dron-fotogrametria/mapas-ortomosaicos/">ortomosaico</a>. Si el proyecto sigue con obras de
    agua, ese modelo alimenta el
    <a href="{{P}}ingenieria-hidraulica/drenaje-pluvial/">drenaje pluvial</a> y los
    <a href="{{P}}ingenieria-hidraulica/estudios-inundacion/">estudios de inundación</a> sin un segundo
    levantamiento.</p>
  </div>
</section>
'''

FOTOGRAMETRIA_FAQ = [
    ("¿En qué sistema de coordenadas se entrega?",
     "En WGS84 / UTM Huso 19 Sur por defecto. Si tu proyecto usa otro datum o un sistema local de obra, se "
     "entrega en ese."),
    ("¿Se puede volar un terreno con mucha pendiente?",
     "Sí, con vuelo adaptado al relieve para mantener constante la resolución, más pasadas con cámara "
     "inclinada que mejoran la reconstrucción de taludes."),
    ("¿Cuánto demora la entrega?",
     "Entre 5 y 10 días hábiles desde el vuelo para un predio de hasta 30 hectáreas."),
]

CURVAS = '''
<section class="encabezado">
  ''' + patron("curvas") + '''
  <div class="contenedor">
    <p class="encabezado__etiqueta">Dron y topografía</p>
    <h1>Levantamiento de curvas de nivel con dron</h1>
    <p class="encabezado__bajada">Las curvas de nivel unen puntos de igual altura y son la forma estándar de
    representar el relieve. Con dron cada curva se apoya en cientos de miles de puntos medidos, no en la
    interpolación entre unas decenas de estaciones.</p>
  </div>
</section>

<section class="seccion">
  <div class="contenedor">
    ''' + figura("curvas-de-nivel",
                 "Plano de curvas de nivel sobre ortomosaico levantado con dron",
                 "Curvas de nivel restituidas sobre el ortomosaico del predio",
                 "16 / 9") + '''
    <h2>Qué equidistancia necesitas</h2>
    <div class="tabla-envoltura">
    <table>
      <caption>Equidistancia recomendada según terreno y uso</caption>
      <thead><tr><th scope="col">Equidistancia</th><th scope="col">Terreno</th><th scope="col">Uso típico</th></tr></thead>
      <tbody>
        <tr><td>0,25 m</td><td>Plano (&lt; 2%)</td><td>Riego, nivelación, plataformas</td></tr>
        <tr><td>0,50 m</td><td>Ondulado suave (2–8%)</td><td>Loteos, urbanización, arquitectura</td></tr>
        <tr><td>1,00 m</td><td>Ondulado a quebrado (8–20%)</td><td>Anteproyecto, caminos, estudios prediales</td></tr>
        <tr><td>2,00 m o más</td><td>Cerro (&gt; 20%)</td><td>Prefactibilidad, grandes superficies</td></tr>
      </tbody>
    </table>
    </div>
    <p>Si el terreno mezcla sectores planos y de cerro, entregamos curvas de detalle solo en la zona de
    interés para que el plano siga siendo legible.</p>
  </div>
</section>

<section class="seccion seccion--clara">
  <div class="contenedor">
    <h2>Qué incluye el entregable</h2>
    ''' + lista_iconos([
    ("archivo", "Curvas en <strong>DWG y DXF</strong>, organizadas por capas."),
    ("mapa", "Curvas superpuestas al <strong>ortomosaico georreferenciado</strong>."),
    ("objetivo", "<strong>Puntos acotados</strong> en vértices, cámaras, cauces y accesos."),
    ("reglas", "<strong>Plano en PDF</strong> a escala, con coordenadas y grilla UTM."),
    ("montana", "<strong>Modelo digital de terreno</strong> del que se derivan las curvas."),
]) + '''
    <p><strong>Servicios relacionados:</strong> se generan del mismo vuelo de
    <a href="{{P}}dron-fotogrametria/fotogrametria/">fotogrametría aérea</a> y alimentan el
    <a href="{{P}}ingenieria-hidraulica/drenaje-pluvial/">proyecto de drenaje pluvial</a> cuando hay
    urbanización.</p>
  </div>
</section>
'''

CURVAS_FAQ = [
    ("¿Cada cuánto conviene pedirlas?",
     "Para riego o nivelación, cada 0,25 m; para loteos y arquitectura, cada 0,5 m; para estudios de gran "
     "superficie, cada 1 m. Pedir más detalle del necesario encarece el trabajo y hace ilegible el plano."),
    ("¿Sirven para presentar a la municipalidad?",
     "Sí para la mayoría de los trámites de anteproyecto y urbanización, con el plano firmado por el "
     "profesional competente. Algunos trámites exigen medición directa: conviene confirmarlo en la Dirección "
     "de Obras antes de encargar el trabajo."),
    ("¿Qué pasa si el terreno tiene mucha vegetación?",
     "Bajo bosque denso el modelo se interpola y pierde exactitud; esos sectores se complementan con puntos "
     "medidos en terreno. En praderas y cultivos bajos el resultado es muy bueno."),
]

DESLINDES = '''
<section class="encabezado">
  ''' + patron("curvas") + '''
  <div class="contenedor">
    <p class="encabezado__etiqueta">Dron y topografía</p>
    <h1>Rectificación de deslindes y linderos con dron</h1>
    <p class="encabezado__bajada">Documentamos con precisión centimétrica dónde están hoy los límites
    materializados de un predio —cercos, muros, canales, hitos— y los contrastamos con la escritura y los
    planos existentes. Permite cuantificar cuánta superficie está en discusión cuando no coinciden.</p>
  </div>
</section>

<section class="seccion">
  <div class="contenedor">
    ''' + figura("rectificacion-deslindes",
                 "Rectificación de deslindes: plano de título superpuesto al ortomosaico del predio",
                 "Deslindes materializados contrastados con el plano de título",
                 "16 / 9") + '''
    <h2>Qué incluye el entregable</h2>
    ''' + lista_iconos([
    ("mapa", "<strong>Ortomosaico</strong> del predio y su entorno inmediato."),
    ("deslindes", "<strong>Coordenadas UTM</strong> de cada vértice materializado."),
    ("calculo", "<strong>Superficie real</strong> ocupada, comparada con la del título."),
    ("capas", "<strong>Superposición</strong> del plano de escritura sobre la imagen."),
    ("archivo", "<strong>Informe técnico</strong> con metodología y diferencias detectadas."),
]) + '''
    <div class="aviso">
      ''' + icono("escudo") + '''
      <p><strong>Importante:</strong> entregamos el levantamiento técnico y su respaldo gráfico. La fijación
      legal de deslindes y la regularización de títulos requieren además la intervención de los organismos
      competentes.</p>
    </div>
  </div>
</section>

<section class="seccion seccion--clara">
  <div class="contenedor">
    <h2 class="seccion__titulo">Cuándo conviene hacerlo</h2>
    ''' + tarjetas([
    ("escudo", "Antes de comprar",
     "Verificar que la superficie y los límites que se venden coincidan con lo cercado y ocupado.", None),
    ("deslindes", "Diferencias con un vecino",
     "Un cerco corrido o un canal desviado quedan documentados con precisión y fecha cierta.", None),
    ("archivo", "Regularización o subdivisión",
     "Base topográfica para el plano que exige el trámite, con las superficies calculadas.", None),
    ("mapa", "Predios rurales grandes",
     "Kilómetros de cerco que a pie tomarían días se cubren en una jornada.", None),
]) + '''
  </div>
</section>
'''

DESLINDES_FAQ = [
    ("¿Tiene validez legal?",
     "Es un documento técnico: entrega mediciones, coordenadas y evidencia gráfica con fecha. Su valor en un "
     "trámite depende de que venga firmado por el profesional competente; para inscribir una subdivisión "
     "siempre intervienen además los organismos que correspondan."),
    ("¿Qué precisión tienen los vértices?",
     "Entre 2 y 5 cm en planta con puntos de control GNSS. Suficiente para detectar diferencias de ocupación, "
     "que en la práctica van de decenas de centímetros a varios metros."),
    ("¿Sirve si el cerco está bajo árboles?",
     "En sectores con copa cerrada el cerco no se ve desde el aire; esos tramos se levantan con medición "
     "directa y se integran al mismo plano."),
]

ORTOMOSAICOS = '''
<section class="encabezado">
  ''' + patron("curvas") + '''
  <div class="contenedor">
    <p class="encabezado__etiqueta">Dron y topografía</p>
    <h1>Mapas y ortomosaicos georreferenciados con dron</h1>
    <p class="encabezado__bajada">Un ortomosaico es una imagen aérea corregida geométricamente: queda a
    escala constante y georreferenciada, así que se pueden medir distancias, superficies y coordenadas con
    precisión centimétrica.</p>
  </div>
</section>

<section class="seccion">
  <div class="contenedor">
    ''' + datos([
    ("2–5 cm/píxel", "Resolución del ortomosaico", "objetivo"),
    ("30–50×", "Más detalle que una imagen satelital libre", "capas"),
    ("UTM 19S", "Sistema de referencia", "mapa"),
    ("GeoTIFF", "Compatible con CAD y SIG", "archivo"),
]) + '''
    <p>Las imágenes satelitales de uso libre entregan del orden de 0,5 a 1 m por píxel y se actualizan cada
    varios años. Con dron obtienes 2 a 5 cm por píxel con la fecha exacta de tu proyecto: se distinguen
    cercos, cámaras, hitos y el estado real de cada sector.</p>
  </div>
</section>

<section class="seccion seccion--clara">
  <div class="contenedor">
    <h2 class="seccion__titulo">Para qué se usa</h2>
    ''' + tarjetas([
    ("reglas", "Base cartográfica",
     "Todo proyecto parte de una imagen real y medible, no de una referencia satelital desactualizada.", None),
    ("pin", "Venta de terrenos",
     "Una imagen nítida con la subdivisión dibujada encima comunica mucho mejor que un plano de líneas.", None),
    ("reloj", "Seguimiento de obra",
     "Vuelos periódicos permiten comparar el avance mes a mes con evidencia visual.", None),
    ("capas", "Catastro agrícola",
     "Superficie efectiva por cuartel, conteo de plantas y detección de fallas.", None),
]) + '''
    <p><strong>Servicios relacionados:</strong> es un subproducto del mismo vuelo de
    <a href="{{P}}dron-fotogrametria/fotogrametria/">fotogrametría aérea</a> y la base sobre la que se dibujan
    las <a href="{{P}}dron-fotogrametria/curvas-de-nivel/">curvas de nivel</a> y los
    <a href="{{P}}dron-fotogrametria/deslindes-linderos/">deslindes</a>.</p>
  </div>
</section>
'''

ORTO_FAQ = [
    ("¿Qué diferencia hay con una foto aérea?",
     "Una fotografía tiene perspectiva cónica y las distancias medidas sobre ella no son reales. El "
     "ortomosaico corrige esa distorsión usando el modelo de elevación, dejando toda la imagen a escala "
     "uniforme."),
    ("¿Puedo abrirlo en AutoCAD?",
     "Sí. El GeoTIFF se inserta directamente en AutoCAD y Civil 3D con su georreferenciación, y también en "
     "QGIS o ArcGIS sin conversiones."),
    ("¿Cuánto pesa el archivo?",
     "Un ortomosaico de 20 hectáreas a 2 cm/píxel pesa entre 2 y 6 GB. Se entrega además una versión liviana "
     "para presentaciones."),
]

# ==========================================================================
# COTIZADOR
# ==========================================================================
COTIZADOR_PAGINA = '''
<section class="encabezado">
  ''' + patron("curvas") + '''
  <div class="contenedor">
    <p class="encabezado__etiqueta">Calculadora</p>
    <h1>Calcula el valor de tu levantamiento con dron</h1>
    <p class="encabezado__bajada">Ingresa la superficie del terreno —o la longitud, si es un trabajo lineal
    como un camino o un canal— y la zona donde está. Obtienes al instante un valor estimado con los mismos
    criterios que usamos para cotizar.</p>
  </div>
</section>

<section class="seccion">
  <div class="contenedor">
    ''' + cotizador_html() + '''
  </div>
</section>

<section class="seccion seccion--clara">
  <div class="contenedor">
    <h2 class="seccion__titulo">Qué considera el valor</h2>
    <p class="seccion__bajada">Un levantamiento tiene una parte fija que no depende del tamaño del predio y
    una variable que sí. Por eso 200 hectáreas cuestan bastante menos por hectárea que 20.</p>
    ''' + lista_iconos([
    ("dron", "<strong>Terreno.</strong> Planificación, traslado, puntos de control y vuelo."),
    ("calculo", "<strong>Gabinete.</strong> Procesamiento, restitución y control de calidad."),
    ("pin", "<strong>Ubicación.</strong> Define traslados y, en zonas lejanas, estadía."),
    ("capas", "<strong>Escala.</strong> Superficies mayores rinden más por jornada."),
]) + '''
  </div>
</section>
'''

COTIZADOR_FAQ = [
    ("¿El valor es definitivo?",
     "Es una estimación confiable para presupuestar, pero no reemplaza la propuesta formal. Vegetación densa, "
     "pendiente extrema o restricciones de vuelo pueden modificar el alcance."),
    ("¿Por qué baja el valor por hectárea en terrenos grandes?",
     "Porque buena parte del costo es fija: llegar al lugar, instalar los puntos de control y preparar la "
     "entrega cuestan casi lo mismo en 10 que en 100 hectáreas. Ese efecto ya está incorporado."),
    ("¿Y si mi terreno no está en la lista?",
     "Selecciona «Otra zona» e ingresa la distancia aproximada desde Santiago en kilómetros."),
    ("¿Cuándo conviene compartir el viaje?",
     "Cuando el terreno está lejos y no tienes urgencia. Agrupamos los viajes a zonas distantes y ese ahorro "
     "se traslada al valor, a cambio de algunas semanas de espera."),
    ("¿Incluye IVA?",
     "No. El valor mostrado es neto; el IVA se agrega en la factura."),
]

# ==========================================================================
# PILAR: HIDRAULICA
# ==========================================================================
HIDRO_PILAR = '''
<section class="encabezado">
  ''' + patron("flujo") + '''
  <div class="contenedor">
    <p class="encabezado__etiqueta">Ingeniería hidráulica</p>
    <h1>Ingeniería hidráulica y sanitaria para proyectos en Chile</h1>
    <p class="encabezado__bajada">Resolvemos cómo se conduce, se almacena, se impulsa y se evacúa el agua:
    la red que abastece un loteo, la bomba que eleva a un estanque, el colector que recibe la lluvia o el
    estudio que determina hasta dónde llega una crecida.</p>
  </div>
</section>

<section class="seccion">
  <div class="contenedor">
    <h2 class="seccion__titulo">Servicios</h2>
    ''' + tarjetas([
    ("red", "Modelación de redes de agua potable",
     "Presiones y velocidades verificadas en demanda de punta y escenario de incendio.",
     "ingenieria-hidraulica/modelacion-redes/"),
    ("bomba", "Bombas e impulsiones",
     "Curva del sistema, punto de operación, NPSH y golpe de ariete.",
     "ingenieria-hidraulica/dimensionamiento-bombas-impulsiones/"),
    ("inundacion", "Estudios de inundación",
     "Caudales de crecida, áreas inundables y cota de seguridad.",
     "ingenieria-hidraulica/estudios-inundacion/"),
    ("drenaje", "Drenaje pluvial",
     "Escorrentía, colectores, sumideros y obras de retención.",
     "ingenieria-hidraulica/drenaje-pluvial/"),
    ("sanitario", "Proyectos sanitarios",
     "Agua potable y alcantarillado con memoria, planos y especificaciones.",
     "ingenieria-hidraulica/proyectos-sanitarios/"),
]) + '''
  </div>
</section>

<section class="seccion seccion--oscura">
  ''' + patron("flujo") + '''
  <div class="contenedor">
    <h2 class="seccion__titulo">La topografía como punto de partida</h2>
    <p class="seccion__bajada">Una presión mal estimada, un colector con pendiente insuficiente o un área
    inundable mal delimitada casi siempre tienen el mismo origen: una base topográfica pobre. Al levantar el
    terreno con <a href="{{P}}dron-fotogrametria/">dron</a> antes de calcular, el modelo se construye sobre
    cotas reales y no sobre cartografía antigua.</p>
    ''' + lista_iconos([
    ("red", "<strong>EPANET</strong> para redes a presión: agua potable, riego e impulsiones."),
    ("drenaje", "<strong>SWMM</strong> para drenaje urbano y aguas lluvia."),
    ("inundacion", "<strong>HEC-RAS</strong> para escurrimiento en cauces, 1D y 2D."),
    ("escudo", "Diseño conforme a la normativa chilena aplicable (NCh, SISS, MOP–DOH)."),
]) + '''
  </div>
</section>
'''

HIDRO_FAQ = [
    ("¿Qué necesito antes de encargar un proyecto?",
     "Topografía del terreno —si no la tienes, la levantamos—, el plano de loteo o arquitectura, la ubicación "
     "del empalme o de la fuente, y el uso previsto. Con eso definimos alcance y valor sin ambigüedades."),
    ("¿Los proyectos quedan aptos para tramitar?",
     "Sí. Incluyen memoria de cálculo, planos y especificaciones en el formato que exige el organismo revisor."),
    ("¿Trabajan proyectos pequeños?",
     "Sí, desde el sistema de agua de una parcela hasta la red completa de un loteo. Los pequeños suelen ser "
     "los peor resueltos justamente porque nadie les hace el cálculo."),
    ("¿Cuánto demora?",
     "Entre 2 y 6 semanas según la complejidad. Los plazos de revisión del organismo competente van aparte."),
]

# ==========================================================================
# HIDRAULICA — SUBPAGINAS
# ==========================================================================
REDES = '''
<section class="encabezado">
  ''' + patron("flujo") + '''
  <div class="contenedor">
    <p class="encabezado__etiqueta">Ingeniería hidráulica</p>
    <h1>Modelación de redes de agua potable con EPANET</h1>
    <p class="encabezado__bajada">Reproducimos en un modelo matemático cómo se comporta el agua dentro de las
    tuberías: cuánta presión llega a cada arranque en el máximo consumo y qué pasa cuando se abre un grifo de
    incendio. Sin ese cálculo, el diámetro se elige por costumbre.</p>
  </div>
</section>

<section class="seccion">
  <div class="contenedor">
    ''' + figura("modelacion-redes-epanet",
                 "Modelo hidráulico de una red de agua potable en EPANET con presiones por nudo",
                 "Modelación de red de agua potable en EPANET",
                 "16 / 9") + '''
    <h2>Qué incluye el entregable</h2>
    ''' + lista_iconos([
    ("red", "<strong>Modelo en EPANET</strong> del sistema completo, como archivo editable."),
    ("objetivo", "<strong>Presiones verificadas</strong> en demanda máxima horaria."),
    ("calculo", "<strong>Velocidades y pérdidas de carga</strong> por tramo."),
    ("rayo", "<strong>Escenario de incendio</strong> con grifo en operación."),
    ("archivo", "<strong>Memoria de cálculo y planos</strong> de planta y perfiles."),
]) + '''
  </div>
</section>

<section class="seccion seccion--clara">
  <div class="contenedor">
    <h2>Criterios de diseño habituales</h2>
    <div class="tabla-envoltura">
    <table>
      <caption>Rangos de verificación en redes de distribución</caption>
      <thead><tr><th scope="col">Parámetro</th><th scope="col">Rango</th><th scope="col">Por qué</th></tr></thead>
      <tbody>
        <tr><td>Presión mínima</td><td>15 m.c.a.</td><td>Asegura suministro en el artefacto más desfavorable</td></tr>
        <tr><td>Presión máxima</td><td>70 m.c.a.</td><td>Sobre ese valor aumentan fugas y roturas</td></tr>
        <tr><td>Velocidad</td><td>0,6 – 2,0 m/s</td><td>Bajo el mínimo hay sedimentación; sobre el máximo, erosión</td></tr>
        <tr><td>Diámetro mínimo</td><td>75 – 110 mm</td><td>Condicionado por el caudal de incendio</td></tr>
      </tbody>
    </table>
    </div>
    <p><strong>Servicios relacionados:</strong> suele ir junto al
    <a href="{{P}}ingenieria-hidraulica/dimensionamiento-bombas-impulsiones/">dimensionamiento de bombas</a> y
    forma parte de los <a href="{{P}}ingenieria-hidraulica/proyectos-sanitarios/">proyectos sanitarios</a>.</p>
  </div>
</section>
'''

REDES_FAQ = [
    ("¿Qué es EPANET?",
     "El software de modelación de redes a presión desarrollado por la agencia ambiental de Estados Unidos, "
     "de uso libre y estándar en la disciplina. Resuelve el equilibrio hidráulico de toda la red "
     "simultáneamente."),
    ("¿Cuándo es necesario modelar?",
     "Cuando la red es mallada, cuando hay diferencias de cota importantes, cuando existen bombas o estanques "
     "intermedios, o cuando hay que verificar el escenario de incendio."),
    ("¿Sirve para una red existente con problemas?",
     "Sí, es uno de los usos más frecuentes. Se modela tal como está construida, se calibra con mediciones de "
     "presión en terreno y se identifica la restricción real."),
]

BOMBAS = '''
<section class="encabezado">
  ''' + patron("flujo") + '''
  <div class="contenedor">
    <p class="encabezado__etiqueta">Ingeniería hidráulica</p>
    <h1>Dimensionamiento de bombas e impulsiones</h1>
    <p class="encabezado__bajada">Determinamos qué diámetro debe tener la tubería y qué bomba instalar para
    elevar un caudal a una altura dada, al menor costo total entre inversión y energía. El cálculo correcto
    cruza la curva del sistema con la del equipo.</p>
  </div>
</section>

<section class="seccion">
  <div class="contenedor">
    ''' + figura("modelacion-golpe-de-ariete",
                 "Modelación de golpe de ariete: envolvente de presiones máximas y mínimas en la impulsión",
                 "Modelación de golpe de ariete en una impulsión",
                 "16 / 9") + '''
    <h2>Qué incluye el entregable</h2>
    ''' + lista_iconos([
    ("calculo", "<strong>Curva del sistema</strong>: altura estática más pérdidas según caudal."),
    ("bomba", "<strong>Punto de operación</strong> y rendimiento del equipo seleccionado."),
    ("gota", "<strong>Verificación de NPSH</strong> para descartar cavitación."),
    ("rayo", "<strong>Golpe de ariete</strong> y protecciones necesarias."),
    ("archivo", "<strong>Especificación técnica</strong> y consumo energético estimado."),
]) + '''
  </div>
</section>

<section class="seccion seccion--oscura">
  ''' + patron("flujo") + '''
  <div class="contenedor">
    <h2 class="seccion__titulo">Los errores más frecuentes</h2>
    ''' + pasos([
    ("Elegir la bomba por catálogo",
     "La bomba entrega el caudal donde su curva corta la del sistema. Si el sistema no se calculó, el punto de operación real es una incógnita."),
    ("No verificar el NPSH",
     "Si la presión a la entrada baja del valor requerido, el agua se vaporiza, la bomba cavita y se destruye el impulsor."),
    ("Elegir el diámetro más barato",
     "Un diámetro menor abarata la inversión pero aumenta las pérdidas al cuadrado del caudal, y eso se paga en energía durante veinte años."),
    ("Omitir el golpe de ariete",
     "En impulsiones largas, una detención brusca genera sobrepresiones que pueden romper la tubería."),
]) + '''
  </div>
</section>

<section class="seccion">
  <div class="contenedor">
    <p><strong>Servicios relacionados:</strong> se calcula junto con la
    <a href="{{P}}ingenieria-hidraulica/modelacion-redes/">modelación de la red</a> y forma parte de los
    <a href="{{P}}ingenieria-hidraulica/proyectos-sanitarios/">proyectos sanitarios</a>.</p>
  </div>
</section>
'''

BOMBAS_FAQ = [
    ("¿Cómo sé si mi bomba está bien dimensionada?",
     "Los síntomas son consumo alto para el caudal entregado, partidas y paradas constantes, ruido de "
     "cavitación o demora en llenar el estanque. Midiendo caudal, presión y consumo se determina el punto de "
     "operación real."),
    ("¿Conviene usar variador de frecuencia?",
     "Cuando la demanda es variable, sí: la potencia varía aproximadamente con el cubo de la velocidad. En "
     "impulsiones a estanque con caudal constante el beneficio es menor."),
    ("¿Incluyen la especificación eléctrica?",
     "Entregamos potencia requerida, tipo de partida y protecciones. El proyecto eléctrico lo desarrolla el "
     "especialista sobre esa base."),
]

INUNDACION = '''
<section class="encabezado">
  ''' + patron("flujo") + '''
  <div class="contenedor">
    <p class="encabezado__etiqueta">Ingeniería hidráulica</p>
    <h1>Estudios de inundación y modelación hidráulica de cauces</h1>
    <p class="encabezado__bajada">Determinamos hasta dónde llega el agua cuando el río, estero o quebrada
    crece, con qué profundidad y a qué velocidad. Es lo que exige la autoridad cuando un proyecto se emplaza
    cerca de un cauce, y lo que define la cota mínima segura para construir.</p>
  </div>
</section>

<section class="seccion">
  <div class="contenedor">
    ''' + datos([
    ("T = 100 años", "Período de retorno habitual", "inundacion"),
    ("HEC-RAS", "Modelación 1D y 2D", "calculo"),
    ("2–5 cm", "Precisión del terreno con dron", "objetivo"),
    ("3–6 sem", "Plazo típico del estudio", "reloj"),
]) + '''
    <h2>Qué incluye el entregable</h2>
    ''' + lista_iconos([
    ("gota", "<strong>Estudio hidrológico</strong>: caudales de crecida por período de retorno."),
    ("calculo", "<strong>Modelo del cauce</strong> en HEC-RAS sobre topografía propia."),
    ("mapa", "<strong>Mapas de área inundable</strong> con profundidad y velocidad."),
    ("objetivo", "<strong>Cota de seguridad</strong> para el emplazamiento."),
    ("escudo", "<strong>Obras de mitigación</strong> evaluadas si el proyecto queda comprometido."),
]) + '''
  </div>
</section>

<section class="seccion seccion--clara">
  <div class="contenedor">
    <h2 class="seccion__titulo">Cómo se hace</h2>
    ''' + pasos([
    ("Cuenca aportante",
     "Delimitación a partir del modelo de elevación, con superficie, pendiente media y tiempo de concentración."),
    ("Análisis hidrológico",
     "Estadística de precipitaciones o caudales y determinación de la crecida por período de retorno."),
    ("Topografía del cauce",
     "Vuelo del tramo y de la llanura de inundación. Es la etapa que más condiciona la calidad del resultado."),
    ("Modelación",
     "1D en tramos encauzados, 2D cuando el flujo se desborda y se expande."),
    ("Mapeo y conclusiones",
     "Manchas de inundación, cota de seguridad y alternativas de mitigación."),
]) + '''
    <p><strong>Servicios relacionados:</strong> la geometría se construye sobre el levantamiento de
    <a href="{{P}}dron-fotogrametria/fotogrametria/">fotogrametría con dron</a>. Si el problema es el agua que
    genera el propio proyecto, corresponde el
    <a href="{{P}}ingenieria-hidraulica/drenaje-pluvial/">drenaje pluvial</a>.</p>
  </div>
</section>
'''

INUNDACION_FAQ = [
    ("¿Qué significa período de retorno de 100 años?",
     "Que esa crecida tiene 1% de probabilidad de ser igualada o superada en cualquier año. No significa que "
     "ocurra una vez por siglo: en un horizonte de 50 años, la probabilidad de que se presente al menos una "
     "vez es cercana al 40%."),
    ("¿Por qué importa tanto la topografía?",
     "Porque el agua se desborda por diferencias de centímetros. Un modelo sobre cartografía 1:10.000 puede "
     "errar la cota en más de un metro, lo que en una llanura desplaza el límite de la inundación cientos de "
     "metros."),
    ("¿Cuál es la diferencia entre 1D y 2D?",
     "La 1D calcula a lo largo del eje del cauce mediante secciones; la 2D resuelve el flujo sobre una malla y "
     "representa mucho mejor los desbordes. Para áreas inundables en llanuras hoy se prefiere 2D."),
]

DRENAJE = '''
<section class="encabezado">
  ''' + patron("flujo") + '''
  <div class="contenedor">
    <p class="encabezado__etiqueta">Ingeniería hidráulica</p>
    <h1>Proyectos de drenaje pluvial y aguas lluvia</h1>
    <p class="encabezado__bajada">Al pavimentar calles y construir techos, el agua que antes se infiltraba
    pasa a escurrir: el caudal máximo aumenta varias veces y llega mucho más rápido al punto bajo. El
    proyecto calcula ese aumento y define las obras para no inundar el terreno ni trasladar el problema al
    vecino de aguas abajo.</p>
  </div>
</section>

<section class="seccion">
  <div class="contenedor">
    ''' + figura("drenaje-pluvial",
                 "Proyecto de drenaje pluvial: trazado de colectores y áreas aportantes",
                 "Trazado de drenaje pluvial sobre el modelo de terreno",
                 "16 / 9") + '''
    <h2>Qué incluye el entregable</h2>
    ''' + lista_iconos([
    ("gota", "<strong>Estudio hidrológico</strong> con curvas intensidad–duración–frecuencia."),
    ("calculo", "<strong>Caudal de diseño</strong> antes y después de urbanizar."),
    ("drenaje", "<strong>Red de colectores</strong>: trazado, diámetros, pendientes y descargas."),
    ("capas", "<strong>Obras de retención o infiltración</strong> cuando se exige no aumentar el caudal."),
    ("archivo", "<strong>Planos, memoria y especificaciones</strong> aptos para construcción."),
]) + '''
  </div>
</section>

<section class="seccion seccion--oscura">
  ''' + patron("flujo") + '''
  <div class="contenedor">
    <h2 class="seccion__titulo">El principio de fondo</h2>
    <p class="seccion__bajada">Todo proyecto moderno de aguas lluvia parte de no aumentar el caudal máximo que
    el terreno descarga hacia aguas abajo respecto de su condición natural. Por eso las soluciones actuales
    combinan conducción con almacenamiento e infiltración: estanques de retención, zanjas y pavimentos
    permeables. Casi siempre resultan más económicas que agrandar colectores kilómetros aguas abajo.</p>
  </div>
</section>

<section class="seccion">
  <div class="contenedor">
    <p><strong>Servicios relacionados:</strong> se apoya en las
    <a href="{{P}}dron-fotogrametria/curvas-de-nivel/">curvas de nivel</a>, porque el trazado depende de
    pendientes de centímetros. Si el terreno además está expuesto a la crecida de un cauce, corresponde un
    <a href="{{P}}ingenieria-hidraulica/estudios-inundacion/">estudio de inundación</a>.</p>
  </div>
</section>
'''

DRENAJE_FAQ = [
    ("¿Qué período de retorno se usa?",
     "Las redes secundarias de calles se diseñan del orden de 2 a 10 años, y los colectores principales para "
     "25, 50 o 100. El criterio se define según el organismo revisor y el riesgo asociado."),
    ("¿Qué es el coeficiente de escorrentía?",
     "La fracción de la lluvia que escurre en vez de infiltrarse. Va de 0,10–0,25 en suelo natural a 0,85–0,95 "
     "en pavimento: ese salto explica por qué urbanizar multiplica el caudal aunque llueva lo mismo."),
    ("¿Sirve la infiltración en cualquier terreno?",
     "No. Requiere suelo permeable y napa profunda. En suelos arcillosos hay que resolver con retención y "
     "descarga controlada, por eso el proyecto parte con el reconocimiento del suelo."),
]

SANITARIOS = '''
<section class="encabezado">
  ''' + patron("flujo") + '''
  <div class="contenedor">
    <p class="encabezado__etiqueta">Ingeniería hidráulica</p>
    <h1>Proyectos sanitarios: agua potable y alcantarillado</h1>
    <p class="encabezado__bajada">Definimos cómo llega el agua potable a cada unidad y cómo se evacúan las
    aguas servidas de un loteo, una parcelación o una edificación, con memoria de cálculo, planos y
    especificaciones para tramitar.</p>
  </div>
</section>

<section class="seccion">
  <div class="contenedor">
    <div class="bloques">
      <div class="bloque">
        <div class="bloque__cabecera">''' + icono("gota") + '''<h3>Agua potable</h3></div>
        <ul class="lista-check">
          <li>Dotación y demanda de diseño.</li>
          <li>Fuente: pozo, noria o empalme a red pública.</li>
          <li>Estanque de regulación y cota de fondo.</li>
          <li>Impulsión y equipos de bombeo.</li>
          <li>Red de distribución modelada y arranques.</li>
        </ul>
      </div>
      <div class="bloque">
        <div class="bloque__cabecera">''' + icono("sanitario") + '''<h3>Alcantarillado</h3></div>
        <ul class="lista-check">
          <li>Caudales y verificación de pendientes.</li>
          <li>Red de recolección por gravedad y cámaras.</li>
          <li>Planta elevadora si la topografía la exige.</li>
          <li>Empalme a colector o tratamiento particular.</li>
          <li>Planos de planta, perfiles y detalles.</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="seccion seccion--clara">
  <div class="contenedor">
    <h2 class="seccion__titulo">La secuencia del proyecto</h2>
    ''' + pasos([
    ("Factibilidad",
     "Determinar si hay red pública disponible o si el proyecto requiere fuente propia. Esta definición cambia por completo el alcance."),
    ("Topografía",
     "Sin cotas confiables no se puede definir la cota del estanque ni verificar que el alcantarillado escurra por gravedad."),
    ("Diseño y cálculo",
     "Dimensionamiento de cada componente y verificación de todos los escenarios de operación."),
    ("Planos, memoria y tramitación",
     "Documentación en el formato exigido y acompañamiento hasta la aprobación."),
]) + '''
    <p><strong>Servicios relacionados:</strong> integra la
    <a href="{{P}}ingenieria-hidraulica/modelacion-redes/">modelación de la red</a> y el
    <a href="{{P}}ingenieria-hidraulica/dimensionamiento-bombas-impulsiones/">dimensionamiento de bombas</a>,
    y en loteos se desarrolla junto al
    <a href="{{P}}ingenieria-hidraulica/drenaje-pluvial/">drenaje pluvial</a>.</p>
  </div>
</section>
'''

SANITARIOS_FAQ = [
    ("¿Cómo sé si mi terreno tiene factibilidad?",
     "Consultando a la empresa sanitaria de la zona. Si no hay red disponible, el proyecto debe resolver "
     "fuente propia —con sus derechos de aprovechamiento— y tratamiento particular de aguas servidas."),
    ("¿Y si el terreno queda más bajo que el colector?",
     "Se requiere una planta elevadora. Es una solución habitual, pero encarece la operación y exige "
     "mantención, por lo que conviene verificarlo con topografía antes de comprometer el trazado."),
    ("¿Cuánto demora la aprobación?",
     "El desarrollo toma entre 4 y 6 semanas. La revisión del organismo es un plazo aparte que suele incluir "
     "al menos una ronda de observaciones."),
]

# ==========================================================================
# CAPACIDADES
# ==========================================================================
CAPACIDADES = '''
<section class="encabezado">
  ''' + patron("curvas") + '''
  <div class="contenedor">
    <p class="encabezado__etiqueta">Capacidades</p>
    <h1>Qué entregamos, con qué herramientas y en qué formatos</h1>
    <p class="encabezado__bajada">RCKT es una oficina nueva con foco en hacer bien dos cosas: levantar
    terreno con dron y resolver ingeniería hidráulica. Acá está el detalle técnico de lo que recibes.</p>
  </div>
</section>

<section class="seccion">
  <div class="contenedor">
    <div class="bloques">
      <div class="bloque">
        <div class="bloque__cabecera">''' + icono("dron") + '''<h3>Topografía y fotogrametría</h3></div>
        <ul class="lista-check">
          <li>Ortomosaico en GeoTIFF, 2 a 5 cm/píxel.</li>
          <li>Nube de puntos en LAS/LAZ clasificada.</li>
          <li>Modelo digital de superficie y de terreno.</li>
          <li>Curvas de nivel en DWG/DXF por capas.</li>
          <li>Informe con error verificado por puntos independientes.</li>
        </ul>
      </div>
      <div class="bloque">
        <div class="bloque__cabecera">''' + icono("red") + '''<h3>Ingeniería hidráulica</h3></div>
        <ul class="lista-check">
          <li>Memoria con criterios y referencias normativas explícitas.</li>
          <li>Modelo hidráulico entregado como archivo editable.</li>
          <li>Planos de planta, perfiles y detalles.</li>
          <li>Mapas temáticos: áreas inundables, presiones por nudo.</li>
          <li>Respuesta a observaciones hasta la aprobación.</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="seccion seccion--clara">
  <div class="contenedor">
    <h2 class="seccion__titulo">Formatos de entrega</h2>
    <div class="tabla-envoltura">
    <table>
      <caption>Qué archivo recibes según el producto</caption>
      <thead><tr><th scope="col">Producto</th><th scope="col">Formato</th><th scope="col">Se abre con</th></tr></thead>
      <tbody>
        <tr><td>Ortomosaico</td><td>GeoTIFF (+ JPG liviano)</td><td>AutoCAD, Civil 3D, QGIS</td></tr>
        <tr><td>Nube de puntos</td><td>LAS / LAZ</td><td>CloudCompare, Civil 3D, Recap</td></tr>
        <tr><td>Modelo de terreno</td><td>GeoTIFF ráster</td><td>QGIS, Civil 3D</td></tr>
        <tr><td>Curvas y planimetría</td><td>DWG / DXF</td><td>AutoCAD, Civil 3D</td></tr>
        <tr><td>Modelos hidráulicos</td><td>INP (EPANET/SWMM), PRJ (HEC-RAS)</td><td>Software respectivo</td></tr>
      </tbody>
    </table>
    </div>
  </div>
</section>

<section class="seccion">
  <div class="contenedor">
    <h2 class="seccion__titulo">Desarrollos propios</h2>
    <p class="seccion__bajada">Trabajos y ejercicios técnicos desarrollados por cuenta propia, que son la
    base metodológica de la oficina.</p>
    <div class="galeria">
      ''' + figura("rectificacion-deslindes",
                   "Rectificación de deslindes de un predio levantado con dron",
                   "Rectificación de deslindes") + '''
      ''' + figura("modelacion-golpe-de-ariete",
                   "Modelación de golpe de ariete en una impulsión",
                   "Modelación de golpe de ariete") + '''
      ''' + figura("drenaje-pluvial",
                   "Proyecto de drenaje pluvial con trazado de colectores",
                   "Drenaje pluvial") + '''
    </div>
  </div>
</section>
'''

CAPACIDADES_FAQ = [
    ("¿Puedo pedir solo un producto puntual?",
     "Sí. Si solo necesitas el ortomosaico, o solo la memoria de una impulsión, se cotiza así. Lo que no "
     "hacemos es entregar algo que sabemos que no servirá para el uso declarado sin advertirlo antes."),
    ("¿Entregan archivos editables o solo PDF?",
     "Editables. El modelo de EPANET, el DWG de las curvas y la nube de puntos se entregan como archivos de "
     "trabajo, para que tu equipo siga trabajando sin depender de nosotros."),
    ("¿Trabajan como subcontrato de otras oficinas?",
     "Sí. Podemos usar el formato, la nomenclatura y las capas que ya usa tu oficina."),
]

# ==========================================================================
# ZONAS
# ==========================================================================
ZONAS_INDEX = '''
<section class="encabezado">
  ''' + patron("curvas") + '''
  <div class="contenedor">
    <p class="encabezado__etiqueta">Cobertura</p>
    <h1>Zonas de cobertura: dónde trabajamos</h1>
    <p class="encabezado__bajada">Base en ''' + CONFIG["ciudad_base"] + ''', con proyectos entre la Región de
    Coquimbo y La Araucanía. Si tu proyecto está fuera de estas zonas, escríbenos igual: lo evaluamos según
    la envergadura del trabajo.</p>
  </div>
</section>

<section class="seccion">
  <div class="contenedor">
    ''' + tarjetas([
    ("pin", "Santiago y Región Metropolitana",
     "Proyectos urbanos: deslindes, drenaje pluvial, proyectos sanitarios y modelación de redes.",
     "zonas/santiago-rm/"),
    ("pin", "La Serena, Coquimbo y IV Región",
     "Valles de riego, escasez hídrica, pozos y quebradas con crecidas aluvionales.",
     "zonas/coquimbo-la-serena-iv-region/"),
    ("pin", "Valparaíso, Viña del Mar y V Región",
     "Terrenos costeros y de quebrada: topografía en pendiente, escorrentía y drenaje.",
     "zonas/valparaiso-vina-v-region/"),
    ("pin", "Región de O'Higgins",
     "Zona agrícola y vitivinícola: curvas de detalle para riego y deslindes rurales.",
     "zonas/ohiggins-vi-region/"),
    ("pin", "Región del Maule",
     "Predios extensos, drenaje agrícola y estudios de inundación de esteros.",
     "zonas/maule-vii-region/"),
    ("pin", "Pucón, Villarrica y Caburgua",
     "Parcelaciones y loteos: topografía para venta, deslindes y soluciones sanitarias.",
     "zonas/pucon-villarrica-caburgua/"),
]) + '''
  </div>
</section>

<section class="seccion seccion--clara">
  <div class="contenedor">
    <h2 class="seccion__titulo">Cómo funcionan los proyectos fuera de Santiago</h2>
    <p class="seccion__bajada">El terreno se concentra en una sola visita bien planificada y el resto se
    desarrolla en gabinete. Eso mantiene el costo de traslado acotado y en un solo ítem, informado por
    adelantado. Para proyectos de <a href="{{P}}ingenieria-hidraulica/">ingeniería hidráulica</a> sin
    componente de terreno, la ubicación es indiferente.</p>
  </div>
</section>
'''

ZONA_RM = '''
<section class="encabezado">
  ''' + patron("curvas") + '''
  <div class="contenedor">
    <p class="encabezado__etiqueta">Zona de cobertura</p>
    <h1>Topografía con dron e ingeniería hidráulica en Santiago y la RM</h1>
    <p class="encabezado__bajada">Proyectos urbanos y periurbanos: urbanizaciones en el borde de la ciudad,
    deslindes en predios que se subdividen, drenaje pluvial y proyectos sanitarios. Es nuestra base, así que
    no hay costo de traslado y las visitas se coordinan con pocos días de anticipación.</p>
  </div>
</section>

<section class="seccion">
  <div class="contenedor">
    <p>Trabajamos en el Gran Santiago y en Colina, Lampa, Til Til, Buin, Paine, Melipilla, María Pinto,
    Curacaví, Talagante, Isla de Maipo, Peñaflor, Padre Hurtado, Pirque, San José de Maipo y Calera de Tango.</p>
    ''' + tarjetas([
    ("drenaje", "Drenaje pluvial para urbanizaciones",
     "Acreditar que la urbanización no aumenta el caudal descargado aguas abajo.",
     "ingenieria-hidraulica/drenaje-pluvial/"),
    ("sanitario", "Proyectos sanitarios",
     "Agua potable y alcantarillado para loteos y condominios, con planos para tramitación.",
     "ingenieria-hidraulica/proyectos-sanitarios/"),
    ("deslindes", "Deslindes antes de subdividir",
     "Verificación de la ocupación real en predios periurbanos con cercos antiguos.",
     "dron-fotogrametria/deslindes-linderos/"),
    ("reloj", "Control de avance de obra",
     "Vuelos periódicos para documentar el avance y cubicar movimientos de tierra.",
     "dron-fotogrametria/fotogrametria/"),
]) + '''
  </div>
</section>

<section class="seccion seccion--clara">
  <div class="contenedor">
    <h2 class="seccion__titulo">Consideraciones para volar en la RM</h2>
    <p class="seccion__bajada">Buena parte del área urbana está dentro de espacio aéreo controlado y volar
    sobre aglomeraciones tiene requisitos adicionales. Se gestiona, pero conviene avisar con una o dos
    semanas. En el sector rural la coordinación es mucho más simple.</p>
  </div>
</section>
'''

ZONA_IV = '''
<section class="encabezado">
  ''' + patron("curvas") + '''
  <div class="contenedor">
    <p class="encabezado__etiqueta">Zona de cobertura</p>
    <h1>Topografía con dron e hidráulica en La Serena, Coquimbo y la IV Región</h1>
    <p class="encabezado__bajada">La Región de Coquimbo tiene una condición que define casi todos los
    proyectos: el agua es escasa y los cauces son intermitentes pero violentos. Eso hace que la topografía de
    precisión y el cálculo hidráulico pesen más que en otras zonas, tanto para aprovechar cada litro de riego
    como para no construir en la línea de una quebrada.</p>
  </div>
</section>

<section class="seccion">
  <div class="contenedor">
    <p>Trabajamos en La Serena, Coquimbo, Ovalle, Vicuña, Paihuano, Andacollo, Monte Patria, Combarbalá,
    Illapel, Salamanca y Los Vilos, en los valles de Elqui, Limarí y Choapa.</p>
    ''' + tarjetas([
    ("curvas", "Curvas de nivel para riego",
     "Paltos, cítricos y uva pisquera en ladera: el diseño de riego por sectores exige curvas de detalle.",
     "dron-fotogrametria/curvas-de-nivel/"),
    ("bomba", "Impulsiones y pozos",
     "Elevación desde pozo o punto de captación hasta estanque o cabezal, con foco en eficiencia energética.",
     "ingenieria-hidraulica/dimensionamiento-bombas-impulsiones/"),
    ("inundacion", "Quebradas y aluviones",
     "Delimitación de áreas de riesgo en cauces secos que se activan con lluvias intensas.",
     "ingenieria-hidraulica/estudios-inundacion/"),
    ("sanitario", "Agua potable particular",
     "Sistemas autónomos para parcelaciones y proyectos sin red pública disponible.",
     "ingenieria-hidraulica/proyectos-sanitarios/"),
    ("deslindes", "Deslindes rurales",
     "Predios extensos de secano con cercos antiguos y planos descritos por referencias.",
     "dron-fotogrametria/deslindes-linderos/"),
]) + '''
  </div>
</section>

<section class="seccion seccion--clara">
  <div class="contenedor">
    <h2 class="seccion__titulo">Lo que distingue a esta zona</h2>
    <p class="seccion__bajada">Las quebradas de la región permanecen secas la mayor parte del año y se
    activan con lluvias intensas, arrastrando material. Un terreno que parece seguro en verano puede estar en
    la línea de escurrimiento: el modelo de terreno levantado con dron muestra esa vía preferente antes de
    emplazar nada. En riego, por su parte, la diferencia de cota es lo que define si un sector llega por
    gravedad o necesita bombeo, y eso solo se resuelve con curvas de detalle.</p>
  </div>
</section>
'''

ZONA_IV_FAQ = [
    ("¿Viajan a Ovalle, Illapel o Los Vilos?",
     "Sí. Los viajes a la región se agrupan para hacer varios trabajos en la misma salida, lo que reduce el "
     "costo de traslado de cada proyecto. Escríbenos y te avisamos cuándo es el próximo viaje programado."),
    ("¿Sirve el dron para terrenos de secano sin vegetación?",
     "Es donde mejor funciona: sin cobertura vegetal el modelo de terreno queda muy limpio y la precisión es "
     "la máxima alcanzable."),
    ("¿Pueden evaluar el riesgo de una quebrada seca?",
     "Sí, con un estudio de inundación sobre topografía propia. Determina la vía de escurrimiento y la cota "
     "de seguridad para emplazar construcciones."),
]

ZONA_V = '''
<section class="encabezado">
  ''' + patron("curvas") + '''
  <div class="contenedor">
    <p class="encabezado__etiqueta">Zona de cobertura</p>
    <h1>Fotogrametría con dron e hidráulica en Valparaíso y Viña del Mar</h1>
    <p class="encabezado__bajada">Pendiente fuerte, quebradas que concentran la escorrentía y alta densidad
    de proyectos en ladera. En una quebrada, un error de cota de un metro cambia por completo el resultado de
    un cálculo de drenaje.</p>
  </div>
</section>

<section class="seccion">
  <div class="contenedor">
    <p>Trabajamos en Valparaíso, Viña del Mar, Concón, Quilpué, Villa Alemana, Limache, Olmué, Casablanca,
    San Antonio, Cartagena, El Quisco, Algarrobo, Quintero, Puchuncaví, La Ligua y Zapallar.</p>
    ''' + tarjetas([
    ("montana", "Topografía en pendiente",
     "Vuelo adaptado al relieve y pasadas oblicuas, que reconstruyen taludes mucho mejor.",
     "dron-fotogrametria/fotogrametria/"),
    ("drenaje", "Escorrentía de quebradas",
     "Delimitación de cuencas aportantes y obras de conducción para proyectos en ladera.",
     "ingenieria-hidraulica/drenaje-pluvial/"),
    ("inundacion", "Esteros costeros",
     "Áreas inundables en esteros y desembocaduras, donde el desborde afecta terrenos de alto valor.",
     "ingenieria-hidraulica/estudios-inundacion/"),
    ("mapa", "Ortomosaicos inmobiliarios",
     "Base cartográfica actualizada y material visual para proyectos con vista.",
     "dron-fotogrametria/mapas-ortomosaicos/"),
]) + '''
  </div>
</section>

<section class="seccion seccion--clara">
  <div class="contenedor">
    <h2 class="seccion__titulo">Consideraciones locales</h2>
    <p class="seccion__bajada">La camanchaca puede impedir el vuelo en las mañanas y el viento de la tarde
    suele superar el límite operacional en el borde costero. La ventana útil se concentra en las horas
    centrales del día, y así planificamos la jornada.</p>
  </div>
</section>
'''

ZONA_VI = '''
<section class="encabezado">
  ''' + patron("curvas") + '''
  <div class="contenedor">
    <p class="encabezado__etiqueta">Zona de cobertura</p>
    <h1>Topografía con dron para agricultura en la Región de O'Higgins</h1>
    <p class="encabezado__bajada">Zona agrícola y vitivinícola, donde la pregunta relevante no es cuánto mide
    el terreno sino cómo se mueve el agua dentro de él: curvas de detalle para riego por sectores, nivelación
    y deslindes rurales.</p>
  </div>
</section>

<section class="seccion">
  <div class="contenedor">
    <p>Trabajamos en Rancagua, Machalí, Graneros, Rengo, San Vicente de Tagua Tagua, San Fernando,
    Chimbarongo, Santa Cruz, Nancagua, Palmilla, Peralillo, Pichidegua, Las Cabras y Peumo.</p>
    ''' + tarjetas([
    ("curvas", "Curvas de nivel para riego",
     "Cada 0,25 m en terreno plano: la única forma de sectorizar bien un riego tecnificado.",
     "dron-fotogrametria/curvas-de-nivel/"),
    ("mapa", "Catastro por cuartel",
     "Superficie efectiva, conteo de plantas y detección de fallas.",
     "dron-fotogrametria/mapas-ortomosaicos/"),
    ("deslindes", "Deslindes rurales",
     "Perímetros extensos con cercos antiguos, canales y caminos.",
     "dron-fotogrametria/deslindes-linderos/"),
    ("bomba", "Impulsiones de riego",
     "Dimensionamiento desde la captación hasta el estanque o el cabezal.",
     "ingenieria-hidraulica/dimensionamiento-bombas-impulsiones/"),
]) + '''
  </div>
</section>

<section class="seccion seccion--clara">
  <div class="contenedor">
    <h2 class="seccion__titulo">Cuándo volar un predio agrícola</h2>
    <p class="seccion__bajada">Para levantar el terreno y sus deslindes conviene volar con el suelo
    despejado, después de la cosecha o en invierno. Para catastro de plantación, con el cultivo desarrollado.
    Si el predio necesita ambas cosas, se planifican dos vuelos.</p>
  </div>
</section>
'''

ZONA_VII = '''
<section class="encabezado">
  ''' + patron("curvas") + '''
  <div class="contenedor">
    <p class="encabezado__etiqueta">Zona de cobertura</p>
    <h1>Levantamientos con dron e hidráulica en la Región del Maule</h1>
    <p class="encabezado__bajada">Agricultura de riego, secano y sector forestal, con una red de esteros y
    canales que atraviesa buena parte de los predios. Los encargos suelen cruzar las dos especialidades:
    levantar el predio y, sobre esa base, resolver el riego o el drenaje.</p>
  </div>
</section>

<section class="seccion">
  <div class="contenedor">
    <p>Trabajamos en Talca, Curicó, Molina, Sagrada Familia, San Clemente, Pencahue, San Javier, Villa Alegre,
    Linares, Longaví, Parral, Constitución y Cauquenes.</p>
    ''' + tarjetas([
    ("mapa", "Levantamientos prediales extensos",
     "Decenas o cientos de hectáreas donde el levantamiento tradicional sería inviable.",
     "dron-fotogrametria/fotogrametria/"),
    ("curvas", "Curvas para riego y nivelación",
     "Diseño sobre curvas de detalle, con cálculo de volúmenes de nivelación.",
     "dron-fotogrametria/curvas-de-nivel/"),
    ("inundacion", "Inundación de esteros",
     "Crecidas en cauces que atraviesan predios agrícolas o terrenos con proyectos.",
     "ingenieria-hidraulica/estudios-inundacion/"),
    ("sanitario", "Agua para parcelaciones",
     "Agua potable y aguas servidas en parcelaciones de agrado del secano y la precordillera.",
     "ingenieria-hidraulica/proyectos-sanitarios/"),
]) + '''
  </div>
</section>

<section class="seccion seccion--clara">
  <div class="contenedor">
    <h2 class="seccion__titulo">Consideraciones locales</h2>
    <p class="seccion__bajada">Los predios grandes suelen tener planos antiguos con deslindes descritos por
    referencias —canales, caminos, cercos— y no por coordenadas. Superponer ese plano al ortomosaico actual
    muestra de inmediato dónde coincide con la realidad y dónde no.</p>
  </div>
</section>
'''

ZONA_PUCON = '''
<section class="encabezado">
  ''' + patron("curvas") + '''
  <div class="contenedor">
    <p class="encabezado__etiqueta">Zona de cobertura</p>
    <h1>Fotogrametría y topografía con dron en Pucón, Villarrica y Caburgua</h1>
    <p class="encabezado__bajada">Alto volumen de parcelaciones, terrenos con bosque y pendiente, cercanía a
    lagos y ríos, y compradores que deciden mirando fotos y planos. Por eso pesan dos cosas: un levantamiento
    confiable que muestre la superficie realmente utilizable, y una solución de agua resuelta, porque casi
    nunca hay red pública.</p>
  </div>
</section>

<section class="seccion">
  <div class="contenedor">
    <p>Trabajamos en Pucón, Villarrica, Caburgua, Curarrehue, Lican Ray, Coñaripe, Panguipulli y Loncoche,
    incluidos los sectores de Quelhue, Paillaco, Candelaria, Palguín, Menetúe y Trancura.</p>
    ''' + tarjetas([
    ("curvas", "Topografía de parcelas",
     "Plataformas de construcción, accesos y superficie realmente utilizable de cada lote.",
     "dron-fotogrametria/curvas-de-nivel/"),
    ("mapa", "Ortomosaicos para venta",
     "Imagen de alta resolución con la subdivisión y los accesos dibujados encima.",
     "dron-fotogrametria/mapas-ortomosaicos/"),
    ("deslindes", "Deslindes con bosque",
     "Límites y superficie real donde el bosque y la pendiente dificultan recorrer el perímetro.",
     "dron-fotogrametria/deslindes-linderos/"),
    ("sanitario", "Agua y aguas servidas particulares",
     "Fuente, estanque, distribución y tratamiento para parcelaciones sin red pública.",
     "ingenieria-hidraulica/proyectos-sanitarios/"),
    ("inundacion", "Riberas de ríos y lagos",
     "Áreas inundables y cotas de seguridad para proyectos junto al Trancura, el Liucura o el lago.",
     "ingenieria-hidraulica/estudios-inundacion/"),
]) + '''
  </div>
</section>

<section class="seccion seccion--oscura">
  ''' + patron("flujo") + '''
  <div class="contenedor">
    <h2 class="seccion__titulo">Lo que más problemas genera</h2>
    ''' + lista_iconos([
    ("montana", "<strong>Superficie utilizable menor a la vendida.</strong> Un lote con quebrada y pendiente fuerte puede tener bastante menos superficie construible."),
    ("gota", "<strong>Agua no resuelta.</strong> Sin red pública, cada proyecto necesita fuente propia y su derecho de aprovechamiento."),
    ("inundacion", "<strong>Emplazamiento en zona inundable.</strong> Los ríos de la zona tienen crecidas importantes en invierno y con deshielo."),
]) + '''
  </div>
</section>
'''

ZONA_PUCON_FAQ = [
    ("¿Se puede volar cerca del volcán Villarrica?",
     "Hay restricciones asociadas al aeródromo de Pucón y al entorno de las áreas protegidas. Se gestionan "
     "las autorizaciones cuando corresponde; en la mayoría de los terrenos de parcelación no hay impedimento."),
    ("¿Cuánto cuesta traer un dron desde Santiago?",
     "El traslado se cotiza aparte y se reparte entre los trabajos de la misma salida. Si tu proyecto coincide "
     "con otro viaje programado, el costo baja bastante."),
    ("¿Se puede levantar un terreno con bosque nativo denso?",
     "El ortomosaico y los deslindes visibles sí. El modelo de terreno bajo copa cerrada pierde exactitud y se "
     "complementa con medición directa."),
]

# ==========================================================================
# EMPRESA
# ==========================================================================
EMPRESA = '''
<section class="encabezado">
  ''' + patron("curvas") + '''
  <div class="contenedor">
    <p class="encabezado__etiqueta">La empresa</p>
    <h1>RCKT: topografía con dron e ingeniería hidráulica</h1>
    <p class="encabezado__bajada">Combinamos dos capacidades que normalmente se contratan por separado: el
    levantamiento topográfico con dron y el diseño hidráulico y sanitario. Alcance cerrado por escrito, un
    solo interlocutor técnico y entregables editables.</p>
  </div>
</section>

<section class="seccion">
  <div class="contenedor">
    <div class="dos-columnas">
      <div>
        <h2>Por qué las dos juntas</h2>
        <p>Los proyectos hidráulicos tropiezan casi siempre con lo mismo: la topografía no existe, es antigua
        o tiene una resolución que no sirve para calcular. Y sin cotas confiables, cualquier modelo es una
        estimación con apariencia de cálculo.</p>
        <p>Al levantar el terreno nosotros mismos, con la precisión que el cálculo va a necesitar, el proyecto
        avanza sin la coordinación —y las esperas— entre dos proveedores que no hablan el mismo idioma
        técnico.</p>
      </div>
      <div>
        <h2>Cómo trabajamos</h2>
        ''' + lista_iconos([
    ("archivo", "<strong>Alcance por escrito antes de empezar.</strong> Qué recibes, en qué formato, en qué plazo y a qué precio."),
    ("chat", "<strong>Un solo interlocutor técnico.</strong> Quien responde el correo es quien hace el trabajo."),
    ("capas", "<strong>Entregables editables.</strong> En el formato que usa tu equipo, no PDF que hay que redibujar."),
    ("escudo", "<strong>Decir que no cuando corresponde.</strong> Si el dron no es la herramienta adecuada, lo decimos."),
]) + '''
      </div>
    </div>
  </div>
</section>

<section class="seccion seccion--clara">
  <div class="contenedor">
    <h2>Datos de la empresa</h2>
    <div class="tabla-envoltura">
    <table>
      <caption>Antecedentes generales</caption>
      <thead><tr><th scope="col">Dato</th><th scope="col">Detalle</th></tr></thead>
      <tbody>
        <tr><td>Nombre comercial</td><td>''' + CONFIG["marca"] + '''</td></tr>
        <tr><td>Razón social</td><td>''' + CONFIG["marca_legal"] + '''</td></tr>
        <tr><td>Base de operaciones</td><td>''' + CONFIG["ciudad_base"] + ", " + CONFIG["region_base"] + '''</td></tr>
        <tr><td>Cobertura</td><td>Coquimbo, Valparaíso, Metropolitana, O'Higgins, Maule y La Araucanía</td></tr>
        <tr><td>Especialidades</td><td>Geomática y fotogrametría · Ingeniería hidráulica y sanitaria</td></tr>
      </tbody>
    </table>
    </div>
    <p class="nota">Completa esta tabla con los datos definitivos —RUT, razón social inscrita, registro DGAC
    del operador y del RPAS, título profesional— editando la sección <code>EMPRESA</code> en
    <code>contenido.py</code>.</p>
  </div>
</section>
'''

# ==========================================================================
# CONTACTO
# ==========================================================================
CONTACTO = '''
<section class="encabezado">
  ''' + patron("flujo") + '''
  <div class="contenedor">
    <p class="encabezado__etiqueta">Contacto</p>
    <h1>Conversemos sobre tu proyecto</h1>
    <p class="encabezado__bajada">Cuéntanos qué necesitas y dónde está el terreno. Te respondemos con
    alcance, plazo y valor en menos de 24 horas hábiles.</p>
  </div>
</section>

<section class="seccion">
  <div class="contenedor">
  <div class="contacto">
    <div class="contacto__datos">
      <h2>Datos de contacto</h2>
      <ul class="contacto__lista">
        <li>''' + icono("chat") + '''<div>
          <span class="contacto__etiqueta">WhatsApp</span>
          <a class="contacto__valor" href="''' + WSP + '''" rel="nofollow noopener" target="_blank">''' + CONFIG["telefono_display"] + '''</a>
          <span class="contacto__nota">La vía más rápida. Puedes enviar la ubicación del terreno.</span>
        </div></li>
        <li>''' + icono("mail") + '''<div>
          <span class="contacto__etiqueta">Correo</span>
          <a class="contacto__valor" href="mailto:''' + CONFIG["email"] + '''">''' + CONFIG["email"] + '''</a>
        </div></li>
        <li>''' + icono("pin") + '''<div>
          <span class="contacto__etiqueta">Base</span>
          <span class="contacto__valor">''' + CONFIG["ciudad_base"] + ", " + CONFIG["region_base"] + '''</span>
          <span class="contacto__nota">Con proyectos entre Coquimbo y La Araucanía.</span>
        </div></li>
        <li>''' + icono("reloj") + '''<div>
          <span class="contacto__etiqueta">Horario</span>
          <span class="contacto__valor">Lunes a viernes, 9:00 a 18:00</span>
        </div></li>
      </ul>

      <h3>Qué nos sirve saber</h3>
      <ul class="lista-check">
        <li>Ubicación del terreno (una ubicación de Google Maps basta).</li>
        <li>Superficie aproximada, aunque sea estimada.</li>
        <li>Para qué vas a usar el resultado: vender, diseñar, tramitar, construir.</li>
        <li>Si hay algún plazo que cumplir.</li>
      </ul>
      <p>Si es un levantamiento con dron, puedes estimar el valor tú mismo en la
      <a href="{{P}}cotizador/">calculadora de cotización</a>.</p>
    </div>

    <div class="contacto__form">
      <h2>Formulario</h2>
      <form class="form" action="https://formsubmit.co/''' + CONFIG["email"] + '''" method="POST">
        <p class="form__campo">
          <label for="nombre">Nombre</label>
          <input type="text" id="nombre" name="nombre" autocomplete="name" required>
        </p>
        <p class="form__campo">
          <label for="email">Correo electrónico</label>
          <input type="email" id="email" name="email" autocomplete="email" required>
        </p>
        <p class="form__campo">
          <label for="telefono">Teléfono / WhatsApp</label>
          <input type="tel" id="telefono" name="telefono" autocomplete="tel" inputmode="tel">
        </p>
        <p class="form__campo">
          <label for="servicio">¿Qué necesitas?</label>
          <select id="servicio" name="servicio">
''' + opciones_consulta() + '''
          </select>
        </p>
        <p class="form__campo">
          <label for="ubicacion">Ubicación del terreno</label>
          <input type="text" id="ubicacion" name="ubicacion" placeholder="Comuna, sector o enlace de Google Maps">
        </p>
        <p class="form__campo">
          <label for="mensaje">Cuéntanos el proyecto</label>
          <textarea id="mensaje" name="mensaje" rows="5" required></textarea>
        </p>
        <p class="form__campo">
          <button class="boton boton--acento boton--ancho" type="submit">Enviar mensaje</button>
        </p>
        <p class="form__nota">Respondemos en menos de 24 horas hábiles. Tus datos se usan solo para responder
        esta consulta.</p>
      </form>
    </div>
  </div>
  </div>
</section>
'''

# ==========================================================================
# BLOG
# ==========================================================================
BLOG_INDEX = '''
<section class="encabezado">
  ''' + patron("curvas") + '''
  <div class="contenedor">
    <p class="encabezado__etiqueta">Blog técnico</p>
    <h1>Artículos sobre fotogrametría con dron e ingeniería hidráulica</h1>
    <p class="encabezado__bajada">Explicaciones claras sobre cómo se hacen las cosas y qué conviene pedir en
    cada caso. Escrito para quien contrata el servicio, no para quien lo ejecuta.</p>
  </div>
</section>

<section class="seccion">
  <div class="contenedor">
  <div class="lista-posts">
    <article class="post-tarjeta">
      <p class="post-tarjeta__meta">''' + icono("deslindes", "icono icono--sm") + ''' Fotogrametría · 7 min</p>
      <h2><a href="{{P}}blog/levantamiento-fotogrametrico-deslindes/">Cómo se hace un levantamiento fotogramétrico para deslindes</a></h2>
      <p>Desde la planificación del vuelo y los puntos de control hasta la superposición del plano de título
      sobre el ortomosaico.</p>
      <p><a class="enlace-fuerte" href="{{P}}blog/levantamiento-fotogrametrico-deslindes/">Leer ''' + icono("flecha", "icono icono--sm") + '''</a></p>
    </article>

    <article class="post-tarjeta">
      <p class="post-tarjeta__meta">''' + icono("red", "icono icono--sm") + ''' Hidráulica · 6 min</p>
      <h2><a href="{{P}}blog/que-es-modelacion-redes-agua-potable/">Qué es la modelación de redes de agua potable y cuándo se necesita</a></h2>
      <p>Qué hace un modelo hidráulico y por qué el diámetro elegido "por costumbre" suele salir caro.</p>
      <p><a class="enlace-fuerte" href="{{P}}blog/que-es-modelacion-redes-agua-potable/">Leer ''' + icono("flecha", "icono icono--sm") + '''</a></p>
    </article>

    <article class="post-tarjeta">
      <p class="post-tarjeta__meta">''' + icono("curvas", "icono icono--sm") + ''' Topografía · 5 min</p>
      <h2><a href="{{P}}blog/curvas-de-nivel-cada-cuanto/">Curvas de nivel: ¿cada 0,25, 0,5 o 1 metro?</a></h2>
      <p>Cómo elegir la equidistancia según la pendiente del terreno y el uso del plano.</p>
      <p><a class="enlace-fuerte" href="{{P}}blog/curvas-de-nivel-cada-cuanto/">Leer ''' + icono("flecha", "icono icono--sm") + '''</a></p>
    </article>
  </div>
  </div>
</section>
'''

POST_DESLINDES = '''
<section class="encabezado encabezado--post">
  ''' + patron("curvas") + '''
  <div class="contenedor">
    <p class="encabezado__etiqueta">Blog · Fotogrametría</p>
    <h1>Cómo se hace un levantamiento fotogramétrico para deslindes</h1>
    <p class="encabezado__meta"><time datetime="2026-08-11">11 de agosto de 2026</time> · 7 min de lectura</p>
  </div>
</section>

<section class="seccion"><div class="contenedor">
<article class="articulo">
  <p class="articulo__entrada">Consiste en volar el predio con dron, medir puntos de control en terreno con
  GNSS, procesar las imágenes para obtener un ortomosaico con precisión de 2 a 5 cm, y sobre esa imagen
  levantar las coordenadas de cada vértice materializado para compararlas con el plano de título. Permite
  cuantificar cuánta superficie está en discusión cuando lo escriturado y lo ocupado no coinciden.</p>

  <h2>Por qué la ocupación casi nunca coincide con el plano</h2>
  <p>En predios rurales chilenos la diferencia entre el título y el cerco es la regla. Las causas se repiten:
  planos antiguos con deslindes descritos por referencias ("hasta el canal", "siguiendo el camino"), cercos
  reconstruidos corridos algunos metros después de una crecida, subdivisiones mal replanteadas, y canales o
  caminos que cambiaron de trazado mientras el plano seguía citándolos como límite.</p>
  <p>El levantamiento no resuelve la controversia jurídica, pero pone la discusión sobre una base objetiva:
  una imagen a escala, con fecha, donde ambas partes ven lo mismo.</p>

  <h2>Los antecedentes primero</h2>
  <p>Antes de volar se reúne todo lo que exista: escritura, plano de subdivisión, certificado de rol y
  cualquier levantamiento anterior. Cuando el plano tiene coordenadas, la comparación es directa; cuando
  describe linderos por referencias, hay un trabajo de interpretación previo que define qué elementos hay que
  capturar con especial cuidado.</p>

  <h2>El vuelo</h2>
  <p>Para deslindes se vuela a una altura que entregue entre 2 y 3 cm por píxel: la resolución mínima para
  distinguir un poste de cerco, un hito o el eje de un muro. El vuelo cubre el predio completo más una franja
  perimetral de 30 a 50 m, para que el contexto quede dentro del ortomosaico.</p>

  <h2>Los puntos de control</h2>
  <p>Este es el paso que separa un levantamiento útil de uno decorativo. Sin puntos medidos con GNSS, la
  georreferenciación queda con el error del GPS del dron: entre 1 y 3 m, del mismo orden que la diferencia
  que se está tratando de medir.</p>
  <p>Se materializan entre 5 y 8 puntos distribuidos en el predio, más algunos de verificación independientes
  que no se usan en el ajuste y sirven para comprobar la precisión alcanzada. Ese valor debe aparecer en el
  informe.</p>

  <h2>La superposición</h2>
  <p>El paso final es dibujar el plano de título sobre el ortomosaico, ajustado por los elementos comunes. Ahí
  aparece —de forma visible para cualquiera, sin leer una tabla de coordenadas— dónde el cerco está adentro,
  dónde afuera y cuántos metros cuadrados representa cada diferencia.</p>

  <h2>Qué no puede resolver un dron</h2>
  <ul class="lista-check">
    <li><strong>Cercos bajo copa cerrada.</strong> Si el límite corre bajo bosque denso, hay que medirlo en terreno.</li>
    <li><strong>Hitos no materializados.</strong> Un vértice sin materialización debe replantearse desde coordenadas.</li>
    <li><strong>La definición legal del deslinde.</strong> El levantamiento entrega evidencia técnica; la determinación jurídica es otro ámbito.</li>
  </ul>

  <p class="articulo__cierre">¿Necesitas verificar los deslindes de un predio? Revisa el
  <a href="{{P}}dron-fotogrametria/deslindes-linderos/">servicio de rectificación de deslindes</a> o
  <a href="{{P}}contacto/">escríbenos</a>.</p>
</article>
</div></section>
'''

POST_REDES = '''
<section class="encabezado encabezado--post">
  ''' + patron("flujo") + '''
  <div class="contenedor">
    <p class="encabezado__etiqueta">Blog · Ingeniería hidráulica</p>
    <h1>Qué es la modelación de redes de agua potable y cuándo se necesita</h1>
    <p class="encabezado__meta"><time datetime="2026-08-11">11 de agosto de 2026</time> · 6 min de lectura</p>
  </div>
</section>

<section class="seccion"><div class="contenedor">
<article class="articulo">
  <p class="articulo__entrada">Es construir una representación matemática del sistema —tuberías, nudos,
  estanques, bombas y válvulas— y resolver el equilibrio hidráulico de toda la red para conocer la presión en
  cada punto bajo distintos escenarios. Se necesita cuando la red es mallada, cuando hay diferencias de cota
  relevantes, cuando existen bombas o estanques intermedios, o cuando hay que verificar el incendio.</p>

  <h2>El problema con calcular "por tramos"</h2>
  <p>En una red ramificada simple el caudal de cada tramo se conoce de antemano. Pero en cuanto hay circuitos
  cerrados, el agua se reparte entre los caminos según las pérdidas de carga de cada uno, y esas pérdidas
  dependen del caudal: el problema se vuelve un sistema de ecuaciones no lineales acopladas que no se resuelve
  a mano de forma razonable.</p>

  <h2>Los cuatro escenarios que hay que verificar</h2>
  ''' + pasos([
    ("Demanda máxima horaria",
     "La hora de mayor consumo del año. Es el escenario crítico por presión baja: si la red cumple aquí, cumple casi siempre."),
    ("Demanda mínima nocturna",
     "De madrugada el consumo cae y las presiones suben. Causa habitual de fugas y roturas repetidas en las zonas bajas."),
    ("Incendio",
     "Un grifo demandando su caudal de diseño mientras el resto opera normal. Suele definir el diámetro mínimo de las matrices."),
    ("Tramos fuera de servicio",
     "Verifica que la red mallada efectivamente entregue redundancia y no deje sectores sin servicio."),
]) + '''

  <h2>Por qué el diámetro "por costumbre" sale caro</h2>
  <p>Sobredimensionar significa pagar tubería de más en toda la red y tener velocidades tan bajas que
  favorecen la sedimentación. Subdimensionar significa presiones insuficientes en los puntos altos justo en la
  hora de mayor consumo, y corregirlo después implica romper calles ya pavimentadas.</p>

  <h2>El dato que más veces falta: la cota</h2>
  <p>Cada nudo necesita su cota, porque la presión disponible es esencialmente la diferencia de altura
  respecto del estanque menos las pérdidas. Un error de un metro en la cota es un error de un metro de columna
  de agua, y en el punto más desfavorable eso puede ser la diferencia entre cumplir y no cumplir. Por eso el
  levantamiento previo con <a href="{{P}}dron-fotogrametria/">dron</a> no es un lujo.</p>

  <h2>También sirve para redes existentes</h2>
  <p>Cuando una red da problemas de presión, se modela tal como está construida, se calibra con mediciones en
  terreno y se identifica la causa real: un diámetro insuficiente, una válvula parcialmente cerrada hace años
  o una demanda que creció por sobre lo previsto. Diagnosticar con modelo evita cambiar tubería que no era el
  problema.</p>

  <p class="articulo__cierre">¿Tienes una red que diseñar o una que da problemas? Revisa el servicio de
  <a href="{{P}}ingenieria-hidraulica/modelacion-redes/">modelación de redes</a> o
  <a href="{{P}}contacto/">escríbenos</a>.</p>
</article>
</div></section>
'''

POST_CURVAS = '''
<section class="encabezado encabezado--post">
  ''' + patron("curvas") + '''
  <div class="contenedor">
    <p class="encabezado__etiqueta">Blog · Topografía</p>
    <h1>Curvas de nivel: ¿cada 0,25, 0,5 o 1 metro?</h1>
    <p class="encabezado__meta"><time datetime="2026-08-11">11 de agosto de 2026</time> · 5 min de lectura</p>
  </div>
</section>

<section class="seccion"><div class="contenedor">
<article class="articulo">
  <p class="articulo__entrada">Depende de dos cosas: la pendiente del terreno y el uso del plano. Como regla,
  terreno plano con uso de riego o nivelación necesita curvas cada 0,25 m; terreno ondulado con uso de loteo o
  arquitectura, cada 0,5 m; y terreno quebrado o estudios de gran superficie, cada 1 m o más.</p>

  <h2>Si la equidistancia es muy grande</h2>
  <p>En un terreno con 2 m de desnivel total, curvas cada metro entregan dos líneas: el plano no contiene
  información utilizable. Es el error clásico al usar cartografía general para diseñar riego en un predio
  plano.</p>

  <h2>Si es demasiado pequeña</h2>
  <p>En una ladera con 40% de pendiente, curvas cada 0,25 m quedan tan juntas que se superponen: el plano se
  vuelve una mancha continua. Además agrega horas de trabajo sin aportar nada.</p>

  <h2>Tabla de referencia</h2>
  <div class="tabla-envoltura">
  <table>
    <caption>Equidistancia según pendiente y uso</caption>
    <thead><tr><th scope="col">Pendiente</th><th scope="col">Equidistancia</th><th scope="col">Usos típicos</th></tr></thead>
    <tbody>
      <tr><td>&lt; 2% (plano)</td><td>0,25 m</td><td>Riego tecnificado, nivelación, plataformas</td></tr>
      <tr><td>2 – 8%</td><td>0,50 m</td><td>Loteos, urbanización, drenaje, arquitectura</td></tr>
      <tr><td>8 – 20%</td><td>1,00 m</td><td>Anteproyectos, caminos, estudios prediales</td></tr>
      <tr><td>&gt; 20%</td><td>2,00 m o más</td><td>Prefactibilidad, grandes superficies</td></tr>
    </tbody>
  </table>
  </div>

  <h2>Terrenos mixtos</h2>
  <p>Muchos predios tienen un sector plano donde se va a construir y un cerro que solo interesa como contexto.
  No hay que elegir: se entregan curvas de detalle en la zona de interés y más espaciadas en el resto.</p>

  <h2>El punto que casi nadie considera</h2>
  <p>La equidistancia no crea precisión: la representa. Un plano con curvas cada 0,25 m generado a partir de un
  levantamiento con error de 30 cm en altura muestra detalle que el dato no respalda. Más importante que pedir
  curvas juntas es preguntar cuál fue el error vertical verificado con puntos independientes, y exigir que ese
  valor aparezca en el informe.</p>

  <h2>Qué pedir al cotizar</h2>
  <ul class="lista-check">
    <li>La equidistancia adecuada para el uso, no la más pequeña posible.</li>
    <li>El error vertical verificado con puntos independientes.</li>
    <li>Entrega en DWG/DXF por capas, no solo en PDF.</li>
    <li>El modelo digital de terreno y el ortomosaico asociados.</li>
  </ul>

  <p class="articulo__cierre">¿Necesitas curvas de nivel? Revisa el
  <a href="{{P}}dron-fotogrametria/curvas-de-nivel/">servicio de levantamiento con dron</a> o calcula el valor
  en la <a href="{{P}}cotizador/">calculadora</a>.</p>
</article>
</div></section>
'''

# ==========================================================================
# LISTA DE PAGINAS
# ==========================================================================
PAGINAS = [
    {
        "path": "",
        "title": "RCKT | Topografía con dron e ingeniería hidráulica",
        "desc": "RCKT: levantamientos con dron, curvas de nivel y deslindes + ingeniería hidráulica, drenaje y estudios de inundación en Chile. Calcula tu cotización en línea.",
        "body": HOME,
        "faq": HOME_FAQ,
        "nav_activa": None,
    },
    # ---- DRON ----
    {
        "path": "dron-fotogrametria",
        "title": "Topografía con dron en Chile | Levantamientos aéreos",
        "desc": "Levantamientos topográficos con dron: ortomosaicos, curvas de nivel, deslindes y modelos 3D con precisión de 2 a 5 cm. Solicita tu cotización sin costo.",
        "body": DRON_PILAR,
        "faq": DRON_FAQ,
        "crumbs": [("Dron y topografía", None)],
        "nav_activa": "dron-fotogrametria/",
        "schema_servicio": ("Fotogrametría y topografía con dron",
                            "Levantamientos topográficos con dron: ortomosaicos georreferenciados, nubes de puntos, modelos digitales de terreno, curvas de nivel y deslindes.",
                            "Levantamiento topográfico con dron"),
    },
    {
        "path": "dron-fotogrametria/fotogrametria",
        "title": "Fotogrametría aérea con dron: modelo 3D y nube de puntos",
        "desc": "Vuelo fotogramétrico con dron: nube de puntos densa, modelo digital de terreno y ortomosaico con precisión de 2 a 5 cm. Consulta plazos y valores.",
        "body": FOTOGRAMETRIA,
        "faq": FOTOGRAMETRIA_FAQ,
        "crumbs": [("Dron y topografía", "dron-fotogrametria/"), ("Fotogrametría aérea", None)],
        "nav_activa": "dron-fotogrametria/",
        "schema_servicio": ("Fotogrametría aérea con dron",
                            "Vuelo fotogramétrico, nube de puntos densa, modelo digital de superficie y de terreno, y ortomosaico georreferenciado con precisión centimétrica.",
                            "Fotogrametría aérea"),
    },
    {
        "path": "dron-fotogrametria/curvas-de-nivel",
        "title": "Curvas de nivel con dron en DWG | Levantamiento topográfico",
        "desc": "Curvas de nivel cada 0,25, 0,5 o 1 m levantadas con dron y entregadas en DWG/DXF sobre ortomosaico. Ideal para riego, loteos y arquitectura. Cotiza aquí.",
        "body": CURVAS,
        "faq": CURVAS_FAQ,
        "crumbs": [("Dron y topografía", "dron-fotogrametria/"), ("Curvas de nivel", None)],
        "nav_activa": "dron-fotogrametria/",
        "schema_servicio": ("Levantamiento de curvas de nivel con dron",
                            "Restitución de curvas de nivel a la equidistancia requerida a partir de vuelo fotogramétrico, entregadas en DWG/DXF junto al modelo digital de terreno.",
                            "Levantamiento de curvas de nivel"),
    },
    {
        "path": "dron-fotogrametria/deslindes-linderos",
        "title": "Rectificación de deslindes y linderos con dron",
        "desc": "Verifica los límites reales de tu predio: ortomosaico, coordenadas de cada vértice y comparación con el plano de título. Cotiza tu levantamiento de deslindes.",
        "body": DESLINDES,
        "faq": DESLINDES_FAQ,
        "crumbs": [("Dron y topografía", "dron-fotogrametria/"), ("Deslindes y linderos", None)],
        "nav_activa": "dron-fotogrametria/",
        "schema_servicio": ("Rectificación de deslindes y linderos con dron",
                            "Catastro de límites materializados de un predio con dron: coordenadas de vértices, cálculo de superficie real y comparación con el plano de título.",
                            "Levantamiento de deslindes"),
    },
    {
        "path": "dron-fotogrametria/mapas-ortomosaicos",
        "title": "Ortomosaicos y mapas georreferenciados con dron",
        "desc": "Ortomosaico georreferenciado de 2 a 5 cm/píxel en GeoTIFF, listo para AutoCAD y QGIS. Base cartográfica medible para tu proyecto. Pide tu cotización.",
        "body": ORTOMOSAICOS,
        "faq": ORTO_FAQ,
        "crumbs": [("Dron y topografía", "dron-fotogrametria/"), ("Mapas y ortomosaicos", None)],
        "nav_activa": "dron-fotogrametria/",
        "schema_servicio": ("Mapas y ortomosaicos georreferenciados con dron",
                            "Generación de ortomosaicos georreferenciados de alta resolución en GeoTIFF, con cálculo de superficies y planos temáticos a escala.",
                            "Cartografía y ortomosaicos"),
    },
    {
        "path": "cotizador",
        "title": "Calculadora: cotiza tu levantamiento con dron",
        "desc": "Ingresa la superficie en hectáreas y la zona de tu terreno y obtén al instante el valor estimado del levantamiento con dron. Sin registro y sin compromiso.",
        "body": COTIZADOR_PAGINA,
        "faq": COTIZADOR_FAQ,
        "crumbs": [("Dron y topografía", "dron-fotogrametria/"), ("Calculadora de cotización", None)],
        "nav_activa": "dron-fotogrametria/",
        "schema_servicio": ("Cotización de levantamiento topográfico con dron",
                            "Calculadora en línea del valor estimado de un levantamiento fotogramétrico con dron según superficie y ubicación del terreno.",
                            "Levantamiento topográfico con dron"),
    },
    # ---- HIDRAULICA ----
    {
        "path": "ingenieria-hidraulica",
        "title": "Ingeniería hidráulica y sanitaria | Proyectos y modelación",
        "desc": "Redes de agua potable, impulsiones, drenaje pluvial, estudios de inundación y proyectos sanitarios con memoria, planos y modelación. Consulta tu proyecto.",
        "body": HIDRO_PILAR,
        "faq": HIDRO_FAQ,
        "crumbs": [("Ingeniería hidráulica", None)],
        "nav_activa": "ingenieria-hidraulica/",
        "schema_servicio": ("Ingeniería hidráulica y sanitaria",
                            "Diseño, cálculo y modelación de sistemas de agua: redes de agua potable, impulsiones, drenaje pluvial, estudios de inundación y proyectos sanitarios.",
                            "Ingeniería hidráulica"),
    },
    {
        "path": "ingenieria-hidraulica/modelacion-redes",
        "title": "Modelación de redes de agua potable con EPANET",
        "desc": "Modelo hidráulico en EPANET: verificación de presiones, velocidades, escenario de incendio y optimización de diámetros. Solicita tu modelación de red.",
        "body": REDES,
        "faq": REDES_FAQ,
        "crumbs": [("Ingeniería hidráulica", "ingenieria-hidraulica/"), ("Modelación de redes", None)],
        "nav_activa": "ingenieria-hidraulica/",
        "schema_servicio": ("Modelación de redes de agua potable",
                            "Construcción y simulación de modelos hidráulicos de redes de agua potable en EPANET, con verificación de presiones, velocidades y escenarios de operación.",
                            "Modelación hidráulica de redes"),
    },
    {
        "path": "ingenieria-hidraulica/dimensionamiento-bombas-impulsiones",
        "title": "Dimensionamiento de bombas e impulsiones | Cálculo",
        "desc": "Cálculo de curva del sistema, punto de operación, NPSH y golpe de ariete para seleccionar la bomba correcta y reducir el consumo energético. Consúltalo aquí.",
        "body": BOMBAS,
        "faq": BOMBAS_FAQ,
        "crumbs": [("Ingeniería hidráulica", "ingenieria-hidraulica/"), ("Bombas e impulsiones", None)],
        "nav_activa": "ingenieria-hidraulica/",
        "schema_servicio": ("Dimensionamiento de bombas e impulsiones",
                            "Cálculo de impulsiones y selección de equipos de bombeo: curva del sistema, punto de operación, verificación de NPSH, golpe de ariete y consumo energético.",
                            "Diseño de sistemas de bombeo"),
    },
    {
        "path": "ingenieria-hidraulica/estudios-inundacion",
        "title": "Estudios de inundación y modelación hidráulica de cauces",
        "desc": "Determina el área inundable y la cota de seguridad de tu proyecto con modelación HEC-RAS sobre topografía propia levantada con dron. Solicita tu estudio.",
        "body": INUNDACION,
        "faq": INUNDACION_FAQ,
        "crumbs": [("Ingeniería hidráulica", "ingenieria-hidraulica/"), ("Estudios de inundación", None)],
        "nav_activa": "ingenieria-hidraulica/",
        "schema_servicio": ("Estudios de inundación y modelación de cauces",
                            "Estudios hidrológicos e hidráulicos para determinar caudales de crecida, áreas inundables y cotas de seguridad, con modelación 1D y 2D en HEC-RAS.",
                            "Estudio de inundación"),
    },
    {
        "path": "ingenieria-hidraulica/drenaje-pluvial",
        "title": "Proyectos de drenaje pluvial y aguas lluvia",
        "desc": "Cálculo de escorrentía y diseño de colectores, sumideros y obras de retención o infiltración para urbanizaciones y loteos. Cotiza tu proyecto de drenaje.",
        "body": DRENAJE,
        "faq": DRENAJE_FAQ,
        "crumbs": [("Ingeniería hidráulica", "ingenieria-hidraulica/"), ("Drenaje pluvial", None)],
        "nav_activa": "ingenieria-hidraulica/",
        "schema_servicio": ("Proyectos de drenaje pluvial y aguas lluvia",
                            "Estudio hidrológico, cálculo de caudales de diseño y diseño de redes de drenaje, sumideros y obras de retención o infiltración para urbanizaciones.",
                            "Diseño de drenaje pluvial"),
    },
    {
        "path": "ingenieria-hidraulica/proyectos-sanitarios",
        "title": "Proyectos sanitarios: agua potable y alcantarillado",
        "desc": "Proyectos de agua potable y alcantarillado para loteos, parcelaciones y edificaciones, con memoria de cálculo, planos y especificaciones. Consulta aquí.",
        "body": SANITARIOS,
        "faq": SANITARIOS_FAQ,
        "crumbs": [("Ingeniería hidráulica", "ingenieria-hidraulica/"), ("Proyectos sanitarios", None)],
        "nav_activa": "ingenieria-hidraulica/",
        "schema_servicio": ("Proyectos sanitarios de agua potable y alcantarillado",
                            "Diseño de sistemas de agua potable y alcantarillado para loteos, parcelaciones y edificaciones, con memoria de cálculo, planos y especificaciones técnicas.",
                            "Proyecto sanitario"),
    },
    # ---- OTRAS ----
    {
        "path": "capacidades",
        "title": "Capacidades: entregables, herramientas y formatos | RCKT",
        "desc": "Qué entrega RCKT en cada servicio, con qué software se produce y en qué formato: DWG, GeoTIFF, LAS, EPANET y HEC-RAS. Revisa el detalle técnico aquí.",
        "body": CAPACIDADES,
        "faq": CAPACIDADES_FAQ,
        "crumbs": [("Capacidades", None)],
        "nav_activa": "capacidades/",
    },
    {
        "path": "zonas",
        "title": "Zonas de cobertura | Dron e ingeniería hidráulica",
        "desc": "Cobertura desde la Región de Coquimbo hasta La Araucanía: Santiago, La Serena, Valparaíso, O'Higgins, Maule y Pucón. Consulta la disponibilidad en tu zona.",
        "body": ZONAS_INDEX,
        "crumbs": [("Zonas de cobertura", None)],
        "nav_activa": "zonas/",
    },
    {
        "path": "zonas/santiago-rm",
        "title": "Topografía con dron e hidráulica en Santiago y la RM",
        "desc": "Levantamientos con dron, drenaje pluvial y proyectos sanitarios en Santiago y comunas de la Región Metropolitana, sin costo de traslado. Cotiza tu proyecto.",
        "body": ZONA_RM,
        "crumbs": [("Zonas de cobertura", "zonas/"), ("Santiago y RM", None)],
        "nav_activa": "zonas/",
    },
    {
        "path": "zonas/coquimbo-la-serena-iv-region",
        "title": "Topografía con dron en La Serena, Coquimbo y IV Región",
        "desc": "Curvas de nivel para riego, impulsiones desde pozos y estudios de quebradas en La Serena, Coquimbo, Ovalle e Illapel. Consulta el próximo viaje a la zona.",
        "body": ZONA_IV,
        "faq": ZONA_IV_FAQ,
        "crumbs": [("Zonas de cobertura", "zonas/"), ("La Serena y Coquimbo", None)],
        "nav_activa": "zonas/",
    },
    {
        "path": "zonas/valparaiso-vina-v-region",
        "title": "Dron e ingeniería hidráulica en Valparaíso y Viña del Mar",
        "desc": "Topografía en pendiente, drenaje de quebradas y estudios de inundación en Valparaíso, Viña del Mar y el litoral de la V Región. Consulta disponibilidad.",
        "body": ZONA_V,
        "crumbs": [("Zonas de cobertura", "zonas/"), ("Valparaíso y V Región", None)],
        "nav_activa": "zonas/",
    },
    {
        "path": "zonas/ohiggins-vi-region",
        "title": "Topografía con dron para agricultura en O'Higgins",
        "desc": "Curvas de nivel para riego, catastro de cuarteles y deslindes rurales en Rancagua, San Fernando, Santa Cruz y toda la VI Región. Solicita tu cotización.",
        "body": ZONA_VI,
        "crumbs": [("Zonas de cobertura", "zonas/"), ("Región de O'Higgins", None)],
        "nav_activa": "zonas/",
    },
    {
        "path": "zonas/maule-vii-region",
        "title": "Levantamientos con dron e hidráulica en el Maule",
        "desc": "Levantamientos prediales, curvas de nivel para riego y estudios de inundación en Talca, Curicó, Linares y toda la Región del Maule. Consulta aquí.",
        "body": ZONA_VII,
        "crumbs": [("Zonas de cobertura", "zonas/"), ("Región del Maule", None)],
        "nav_activa": "zonas/",
    },
    {
        "path": "zonas/pucon-villarrica-caburgua",
        "title": "Topografía con dron en Pucón, Villarrica y Caburgua",
        "desc": "Topografía de parcelas, deslindes, agua potable particular y estudios de inundación en Pucón, Villarrica y Caburgua. Consulta el próximo viaje a la zona.",
        "body": ZONA_PUCON,
        "faq": ZONA_PUCON_FAQ,
        "crumbs": [("Zonas de cobertura", "zonas/"), ("Pucón, Villarrica y Caburgua", None)],
        "nav_activa": "zonas/",
    },
    {
        "path": "empresa",
        "title": "Empresa | RCKT Ingeniería y Geomática",
        "desc": "RCKT combina topografía con dron e ingeniería hidráulica en una sola oficina: alcance cerrado, un interlocutor técnico y entregables editables. Conócenos.",
        "body": EMPRESA,
        "crumbs": [("Empresa", None)],
        "nav_activa": "empresa/",
    },
    {
        "path": "blog",
        "title": "Blog técnico sobre dron e ingeniería hidráulica",
        "desc": "Artículos claros sobre fotogrametría, topografía con dron, curvas de nivel y modelación hidráulica, escritos para quien contrata el servicio. Léelos aquí.",
        "body": BLOG_INDEX,
        "crumbs": [("Blog", None)],
        "nav_activa": "blog/",
    },
    {
        "path": "blog/levantamiento-fotogrametrico-deslindes",
        "title": "Cómo se hace un levantamiento fotogramétrico de deslindes",
        "desc": "Paso a paso del levantamiento de deslindes con dron: vuelo, puntos de control, precisión alcanzable y superposición del plano de título. Guía completa.",
        "body": POST_DESLINDES,
        "crumbs": [("Blog", "blog/"), ("Levantamiento para deslindes", None)],
        "nav_activa": "blog/",
        "schema_articulo": ("Cómo se hace un levantamiento fotogramétrico para deslindes", "2026-08-11",
                            "Paso a paso del levantamiento de deslindes con dron: planificación del vuelo, puntos de control, precisión alcanzable y superposición del plano de título."),
    },
    {
        "path": "blog/que-es-modelacion-redes-agua-potable",
        "title": "Qué es la modelación de redes de agua potable",
        "desc": "Qué hace un modelo hidráulico en EPANET, los cuatro escenarios que hay que verificar y por qué elegir diámetros por costumbre termina saliendo caro.",
        "body": POST_REDES,
        "crumbs": [("Blog", "blog/"), ("Modelación de redes de agua potable", None)],
        "nav_activa": "blog/",
        "schema_articulo": ("Qué es la modelación de redes de agua potable y cuándo se necesita", "2026-08-11",
                            "Qué hace un modelo hidráulico en EPANET, los cuatro escenarios de operación que hay que verificar y por qué elegir diámetros por costumbre sale caro."),
    },
    {
        "path": "blog/curvas-de-nivel-cada-cuanto",
        "title": "Curvas de nivel: ¿cada 0,25, 0,5 o 1 metro?",
        "desc": "Cómo elegir la equidistancia de las curvas de nivel según la pendiente del terreno y el uso del plano, con tabla de referencia y qué pedir al cotizar.",
        "body": POST_CURVAS,
        "crumbs": [("Blog", "blog/"), ("Curvas de nivel: equidistancia", None)],
        "nav_activa": "blog/",
        "schema_articulo": ("Curvas de nivel: ¿cada 0,25, 0,5 o 1 metro?", "2026-08-11",
                            "Cómo elegir la equidistancia de las curvas de nivel según la pendiente del terreno y el uso del plano, con tabla de referencia y qué exigir al cotizar."),
    },
    {
        "path": "contacto",
        "title": "Contacto | Cotiza tu proyecto con RCKT",
        "desc": "Cuéntanos qué necesitas y dónde está el terreno: respondemos con alcance, plazo y valor en menos de 24 horas hábiles. WhatsApp, correo y formulario.",
        "body": CONTACTO,
        "crumbs": [("Contacto", None)],
        "nav_activa": "contacto/",
        "cierre": " ",
    },
]
