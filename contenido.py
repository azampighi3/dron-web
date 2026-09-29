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
  tarjetas([(título, texto, href_o_None), ...])   → índice con líneas finas
  datos([(cifra, etiqueta), ...])                 → fila de ficha técnica
  pasos([(título, descripción), ...])             → lista numerada
  lista([texto, ...])                             → lista simple
  patron("curvas") / patron("flujo")              → fondo tenue, solo en cabeceras
  icono("chat")                                   → solo para íconos funcionales
                                                    (WhatsApp, teléfono, correo)
  figura("nombre-archivo", "texto alternativo", "pie de foto")
      → si assets/img/nombre-archivo.webp (o .jpg/.png/.avif) existe, inserta la
        imagen; si no, no muestra nada y la lista al construir el sitio.

Criterio de redacción: frases concretas, sin guiones largos para enfatizar, sin
listas que empiezan con negrita, y nada que no se pueda sostener con un trabajo real.
"""

from build import (CONFIG, icono, figura, pasos, datos, tarjetas, lista, patron,
                   cotizador_html, opciones_consulta, acciones_encabezado, bloque_precio,
                   tabla_precios, horario_texto)

WSP = "https://wa.me/" + CONFIG["whatsapp"]

# ==========================================================================
# HOME
# ==========================================================================
HOME = '''
<section class="hero">
  <div class="contenedor hero__grilla">
    <div class="hero__texto">
      <h1>Levantamiento de terreno e ingeniería hidráulica</h1>
      <p class="hero__bajada">Hacemos topografía con dron, ingeniería hidráulica y proyectos sanitarios de
      agua potable y alcantarillado para la SEREMI de Salud. El mismo levantamiento sirve de base para el
      cálculo, así que no hay que coordinar a dos oficinas.</p>
      <div class="hero__acciones">
        <a class="boton boton--acento" href="{{P}}cotizador/">Calcular el valor de un levantamiento</a>
        <a class="boton boton--fantasma" href="''' + WSP + '''" rel="nofollow noopener" target="_blank">''' + icono("chat", "icono icono--sm") + ''' WhatsApp</a>
      </div>
      <p class="hero__nota">Oficina en ''' + CONFIG["ciudad_base"] + '''. Terreno entre Coquimbo y La Araucanía.</p>
    </div>
    <div class="hero__imagen">
      ''' + figura("curvas-de-nivel-modelo-elevacion-dron-patagua",
                   "Modelo digital de elevación con curvas de nivel cada 5 metros sobre el ortomosaico "
                   "de un predio en Patagua, levantado con dron",
                   "Patagua. Modelo de elevación y curvas cada 5 m sobre el ortomosaico del vuelo, "
                   "entre 175 y 270 m de altitud.",
                   prioritaria=True) + '''
    </div>
  </div>
</section>

<section class="seccion">
  <div class="contenedor">
    <h2>Servicios</h2>
    <div class="tres-columnas">
      <div>
        <h3 class="columna__titulo"><a href="{{P}}dron-fotogrametria/">Topografía con dron</a></h3>
        ''' + tarjetas([
    ("Nube de puntos y modelo de terreno",
     "Para cubicar movimientos de tierra, diseñar y controlar avance de obra.",
     "dron-fotogrametria/fotogrametria/"),
    ("Curvas de nivel",
     "Cada 0,25, 0,5 o 1 m, en DWG listo para Civil 3D.",
     "dron-fotogrametria/curvas-de-nivel/"),
    ("Rectificación de deslindes",
     "Dónde están de verdad los límites del predio, con coordenadas por vértice.",
     "dron-fotogrametria/rectificacion-deslindes/"),
    ("Mapas y ortomosaicos",
     "Imagen aérea a escala, de 2 a 5 cm por píxel, sobre la que se puede medir.",
     "dron-fotogrametria/mapas-ortomosaicos/"),
], nivel=4, clase="tarjetas tarjetas--columna") + '''
      </div>
      <div>
        <h3 class="columna__titulo"><a href="{{P}}ingenieria-hidraulica/">Ingeniería hidráulica</a></h3>
        ''' + tarjetas([
    ("Modelación de redes",
     "Presiones, velocidades y diámetros verificados en EPANET.",
     "ingenieria-hidraulica/modelacion-redes/"),
    ("Bombas e impulsiones",
     "Punto de operación, golpe de ariete y consumo de energía.",
     "ingenieria-hidraulica/dimensionamiento-bombas-impulsiones/"),
    ("Estudios de inundación",
     "Hasta dónde llega una crecida y a qué cota conviene construir.",
     "ingenieria-hidraulica/estudios-inundacion/"),
    ("Drenaje pluvial",
     "Colectores y obras de retención o infiltración para urbanizaciones.",
     "ingenieria-hidraulica/drenaje-pluvial/"),
], nivel=4, clase="tarjetas tarjetas--columna") + '''
      </div>
      <div>
        <h3 class="columna__titulo"><a href="{{P}}proyecto-sanitario/">Proyecto sanitario</a></h3>
        ''' + tarjetas([
    ("Agua potable particular",
     "Pozo, noria o vertiente, con el proyecto que pide la SEREMI de Salud.",
     "proyecto-sanitario/agua-potable-particular/"),
    ("Alcantarillado particular",
     "Fosa séptica y drenes dimensionados con prueba de infiltración.",
     "proyecto-sanitario/alcantarillado-particular/"),
    ("Agua potable sin fuente propia",
     "Estanque abastecido por camión aljibe.",
     "proyecto-sanitario/agua-potable-sin-fuente-propia/"),
    ("Autorización de funcionamiento",
     "La resolución final, con la obra construida.",
     "proyecto-sanitario/autorizacion-de-funcionamiento/"),
], nivel=4, clase="tarjetas tarjetas--columna") + '''
      </div>
    </div>
  </div>
</section>

<section class="seccion seccion--clara">
  <div class="contenedor">
    <h2>Trabajos realizados</h2>
    <div class="galeria galeria--2">
      ''' + figura("modelo-digital-elevacion-dron-ortomosaico",
                   "Modelo digital de elevación sobre ortomosaico, con cotas entre 85,3 y 136,4 metros",
                   "Modelo de elevación sobre el ortomosaico. En rojo las cotas más bajas (85,3 m), "
                   "en azul las más altas (136,4 m).") + '''
      ''' + figura("rectificacion-deslindes-ortomosaico-dron",
                   "Rectificación de deslindes dibujada sobre ortomosaico con grilla de coordenadas UTM",
                   "Rectificación de deslindes sobre ortomosaico, con grilla de coordenadas UTM.") + '''
      ''' + figura("modelacion-red-agua-potable-presiones",
                   "Modelación de presiones de una red de agua potable dibujada sobre imagen aérea de un "
                   "sector agrícola",
                   "Modelación de presiones de una red de agua potable, con las tuberías y nudos del "
                   "modelo sobre la imagen aérea.",
                   ancha=True) + '''
    </div>
  </div>
</section>

<section class="seccion">
  <div class="contenedor dos-columnas">
    <div>
      <h2>Topografía e hidráulica en la misma oficina</h2>
    </div>
    <div>
      <p>Casi todos los proyectos de agua dependen de una buena topografía. La presión en una red, la
      pendiente de un colector o el límite de una zona inundable se deciden por diferencias de
      centímetros.</p>
      <p>Cuando el levantamiento lo hacemos nosotros, el modelo hidráulico parte de cotas medidas en
      terreno y no de cartografía antigua. Y hablas con una sola contraparte de principio a fin.</p>
      ''' + datos([
    ("2 a 5 cm", "de precisión con puntos de control"),
    ("60 ha", "por jornada de vuelo"),
    ("5 a 10 días", "hábiles de entrega"),
]) + '''
    </div>
  </div>
</section>

<section class="seccion seccion--clara">
  <div class="contenedor">
    <h2>Dónde trabajamos</h2>
    <p class="seccion__bajada">Tenemos oficina en ''' + CONFIG["ciudad_base"] + ''' y hacemos terreno entre la
    Región de Coquimbo y La Araucanía: La Serena y los valles de Elqui, Limarí y Choapa; Valparaíso, Viña
    del Mar y el litoral; Rancagua, San Fernando y Santa Cruz; Curicó, Talca y Linares; Temuco, Angol,
    Villarrica y Pucón. Fuera de Santiago el terreno se hace en una sola salida, y el traslado va como un
    ítem aparte en la propuesta.</p>
    <p>¿Tu terreno está en otra zona? <a href="{{P}}contacto/">Escríbenos</a> y lo vemos.</p>
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
     "apoyo en terreno para georreferenciar. Hay casos, como vegetación densa o deslindes con validez legal, "
     "que requieren medición directa."),
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
    <h1>Fotogrametría y topografía con dron</h1>
    <p class="encabezado__bajada">Fotografiamos el terreno desde el aire y procesamos esas imágenes para
    obtener un modelo tridimensional medible. De ahí salen el plano de curvas de nivel, la imagen aérea a
    escala y el modelo del terreno, con mucha más información que un levantamiento tradicional y en una
    fracción del tiempo.</p>
    ''' + acciones_encabezado("topografía con dron") + '''
  </div>
</section>

<section class="seccion">
  <div class="contenedor">
    ''' + figura("curvas-de-nivel-modelo-elevacion-dron-patagua",
                 "Modelo digital de elevación con curvas de nivel cada 5 metros sobre el ortomosaico "
                 "de un predio en Patagua, levantado con dron",
                 "Patagua. Del mismo vuelo salen el ortomosaico, el modelo de elevación y las curvas "
                 "cada 5 m.",
                 prioritaria=True) + '''
    ''' + datos([
    ("2 a 5 cm", "de precisión con puntos de control"),
    ("2 cm/píxel", "de resolución del ortomosaico"),
    ("60 ha", "por jornada de vuelo"),
    ("5 a 10 días", "hábiles de entrega"),
]) + '''
  </div>
</section>

<section class="seccion seccion--clara">
  <div class="contenedor">
    <h2 class="seccion__titulo">Qué servicio necesitas</h2>
    <p class="seccion__bajada">Todos parten del mismo vuelo; cambia el procesamiento y el entregable.</p>
    ''' + tarjetas([
    ("Nube de puntos y modelo de terreno",
     "La base de todo lo demás. Sirve para cubicar movimientos de tierra, diseñar y controlar obra.",
     "dron-fotogrametria/fotogrametria/"),
    ("Curvas de nivel",
     "A la equidistancia que pida el proyecto. Es lo que suele pedir un arquitecto o un proyectista de riego.",
     "dron-fotogrametria/curvas-de-nivel/"),
    ("Rectificación de deslindes",
     "Cercos, muros y ocupación real comparados con los planos existentes.",
     "dron-fotogrametria/rectificacion-deslindes/"),
    ("Mapas y ortomosaicos",
     "Imagen aérea corregida y georreferenciada, sobre la que se puede medir.",
     "dron-fotogrametria/mapas-ortomosaicos/"),
    ("Calculadora de cotización",
     "Con la superficie y la ubicación te da un valor estimado.",
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

<section class="seccion seccion--clara">
  <div class="contenedor">
    <h2 class="seccion__titulo">Cuánto cuesta</h2>
    <p class="seccion__bajada">Estos son valores de referencia para que tengas un orden de magnitud sin
    tener que preguntar. El valor exacto depende de la superficie y de dónde esté el terreno, y lo obtienes
    en segundos en la <a href="{{P}}cotizador/">calculadora</a>: te entrega un precio, no un rango.</p>
    ''' + tabla_precios() + '''
    <p><a class="enlace-fuerte" href="{{P}}cotizador/">Calcular el valor de mi terreno ''' + icono("flecha", "icono icono--sm") + '''</a></p>
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
    <h1>Nube de puntos y modelo digital de terreno con dron</h1>
    <p class="encabezado__bajada">Convertimos cientos de fotografías aéreas en un modelo tridimensional
    medible del terreno. De esa nube de puntos salen el modelo digital de superficie, el de terreno y todos
    los productos derivados.</p>
  </div>
</section>

<section class="seccion">
  <div class="contenedor">
    ''' + figura("modelo-digital-elevacion-dron-ortomosaico",
                 "Modelo digital de elevación sobre ortomosaico, con cotas entre 85,3 y 136,4 metros",
                 "Modelo de elevación sobre el ortomosaico. En rojo las cotas más bajas (85,3 m), en "
                 "azul las más altas (136,4 m).",
                 estrecha=True) + '''
    <h2>Qué incluye el entregable</h2>
    ''' + lista([
    ("Ortomosaico en GeoTIFF, de 2 a 5 cm/píxel."),
    ("Nube de puntos en LAS/LAZ, clasificada en suelo y no-suelo."),
    ("Modelo digital de superficie y de terreno en formato ráster."),
    ("Curvas de nivel en DWG/DXF."),
    ("Informe técnico con parámetros de vuelo y error verificado."),
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
    <h1>Levantamiento de curvas de nivel con dron</h1>
    <p class="encabezado__bajada">El plano que muestra cómo sube y baja tu terreno. Es lo que te van a pedir
    para subdividir un predio, diseñar el riego, emplazar una casa en pendiente o presentar un proyecto en la
    municipalidad. Con dron cada curva se apoya en cientos de miles de puntos medidos, no en la interpolación
    entre unas pocas estaciones.</p>
    ''' + acciones_encabezado("levantamiento de curvas de nivel") + '''
  </div>
</section>

<section class="seccion">
  <div class="contenedor">
    ''' + figura("curvas-de-nivel-modelo-elevacion-dron-patagua",
                 "Curvas de nivel cada 5 metros sobre el modelo de elevación y el ortomosaico de un "
                 "predio en Patagua",
                 "Patagua. Curvas cada 5 m entre 175 y 270 m, sobre el ortomosaico del vuelo.",
                 prioritaria=True) + '''
    ''' + bloque_precio() + '''
    <h2>Para qué se piden</h2>
    <p>Lo más común es para subdividir un terreno y presentar el plano en la Dirección de Obras o en el
    Conservador de Bienes Raíces. También para diseñar el riego de un predio agrícola, para emplazar una
    casa en pendiente y saber cuánto hay que excavar, o para un trámite en el SAG o la municipalidad. Cada
    caso pide un nivel de detalle distinto, por eso lo primero que preguntamos es para qué lo vas a usar.</p>
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
    ''' + lista([
    ("Curvas en <strong>DWG y DXF</strong>, organizadas por capas."),
    ("Curvas superpuestas al <strong>ortomosaico georreferenciado</strong>."),
    ("Puntos acotados en vértices, cámaras, cauces y accesos."),
    ("Plano en PDF a escala, con coordenadas y grilla UTM."),
    ("Modelo digital de terreno del que se derivan las curvas."),
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
    <h1>Rectificación de deslindes con dron</h1>
    <p class="encabezado__bajada">Para saber exactamente dónde terminan los límites de tu terreno. Volamos
    el predio y medimos dónde están hoy los cercos, muros y canales, para compararlos con lo que dice la
    escritura. Así sabes si la superficie que compraste es la que realmente tienes, y cuántos metros están
    en discusión si no coinciden.</p>
    ''' + acciones_encabezado("rectificación de deslindes") + '''
  </div>
</section>

<section class="seccion">
  <div class="contenedor">
    ''' + bloque_precio() + '''
    ''' + figura("rectificacion-deslindes-ortomosaico-dron",
                 "Rectificación de deslindes dibujada sobre ortomosaico con grilla de coordenadas UTM",
                 "Rectificación de deslindes sobre ortomosaico, con grilla de coordenadas UTM.",
                 estrecha=True) + '''
    <h2>Cuándo se pide</h2>
    <p>Los motivos más frecuentes son concretos: <strong>antes de comprar o vender</strong> un terreno, para
    verificar que la superficie sea la que dice el papel; <strong>antes de subdividir</strong> un predio;
    cuando hay una <strong>diferencia con un vecino</strong> por un cerco corrido; o cuando el plano que
    existe es antiguo y describe los límites por referencias ("hasta el canal", "siguiendo el camino") en
    vez de coordenadas.</p>
    <h2>Qué incluye el entregable</h2>
    ''' + lista([
    ("Ortomosaico del predio y su entorno inmediato."),
    ("Coordenadas UTM de cada vértice materializado."),
    ("Superficie real ocupada, comparada con la del título."),
    ("Superposición del plano de escritura sobre la imagen."),
    ("Informe técnico con metodología y diferencias detectadas."),
]) + '''
    <div class="aviso">
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
    ("Antes de comprar",
     "Verificar que la superficie y los límites que se venden coincidan con lo cercado y ocupado.", None),
    ("Diferencias con un vecino",
     "Un cerco corrido o un canal desviado quedan documentados con precisión y fecha cierta.", None),
    ("Regularización o subdivisión",
     "Base topográfica para el plano que exige el trámite, con las superficies calculadas.", None),
    ("Predios rurales grandes",
     "Kilómetros de cerco que a pie tomarían días se cubren en una jornada.", None),
]) + '''
    <p><strong>Servicios relacionados:</strong> se apoya en el mismo vuelo de
    <a href="{{P}}dron-fotogrametria/fotogrametria/">fotogrametría aérea</a>, se entrega sobre el
    <a href="{{P}}dron-fotogrametria/mapas-ortomosaicos/">ortomosaico del predio</a> y suele acompañarse de
    <a href="{{P}}dron-fotogrametria/curvas-de-nivel/">curvas de nivel</a> cuando se va a subdividir.
    Puedes estimar el valor en la <a href="{{P}}cotizador/">calculadora</a> o leer el detalle del proceso en
    <a href="{{P}}blog/levantamiento-fotogrametrico-deslindes/">cómo se hace un levantamiento para
    deslindes</a>.</p>
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
    <h1>Mapas y ortomosaicos georreferenciados con dron</h1>
    <p class="encabezado__bajada">Un ortomosaico es una imagen aérea corregida geométricamente: queda a
    escala constante y georreferenciada, así que se pueden medir distancias, superficies y coordenadas con
    precisión centimétrica.</p>
  </div>
</section>

<section class="seccion">
  <div class="contenedor">
    ''' + datos([
    ("2–5 cm/píxel", "Resolución del ortomosaico"),
    ("30–50×", "Más detalle que una imagen satelital libre"),
    ("UTM 19S", "Sistema de referencia"),
    ("GeoTIFF", "Compatible con CAD y SIG"),
]) + '''
    ''' + figura("ortomosaico-predio",
                 "Ortomosaico georreferenciado de alta resolución de un predio levantado con dron",
                 "Ortomosaico de un predio completo, medible a escala real",
                 "16 / 9") + '''
    <p>Las imágenes satelitales de uso libre entregan del orden de 0,5 a 1 m por píxel y se actualizan cada
    varios años. Con dron obtienes 2 a 5 cm por píxel con la fecha exacta de tu proyecto: se distinguen
    cercos, cámaras, hitos y el estado real de cada sector.</p>
  </div>
</section>

<section class="seccion seccion--clara">
  <div class="contenedor">
    <h2 class="seccion__titulo">Para qué se usa</h2>
    ''' + tarjetas([
    ("Base cartográfica",
     "Todo proyecto parte de una imagen real y medible, no de una referencia satelital desactualizada.", None),
    ("Venta de terrenos",
     "Una imagen nítida con la subdivisión dibujada encima comunica mucho mejor que un plano de líneas.", None),
    ("Seguimiento de obra",
     "Vuelos periódicos permiten comparar el avance mes a mes con evidencia visual.", None),
    ("Catastro agrícola",
     "Superficie efectiva por cuartel, conteo de plantas y detección de fallas.", None),
]) + '''
    <p><strong>Servicios relacionados:</strong> es un subproducto del mismo vuelo de
    <a href="{{P}}dron-fotogrametria/fotogrametria/">fotogrametría aérea</a> y la base sobre la que se dibujan
    las <a href="{{P}}dron-fotogrametria/curvas-de-nivel/">curvas de nivel</a> y los
    <a href="{{P}}dron-fotogrametria/rectificacion-deslindes/">deslindes</a>.</p>
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
    <h1>Calcula el valor de tu levantamiento con dron</h1>
    <p class="encabezado__bajada">Ingresa la superficie del terreno (o la longitud, si es un trabajo lineal
    como un camino o un canal) y la zona donde está. Obtienes al instante un valor estimado con los mismos
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
    ''' + lista([
    ("Terreno. Planificación, traslado, puntos de control y vuelo."),
    ("Gabinete. Procesamiento, restitución y control de calidad."),
    ("Ubicación. Define traslados y, en zonas lejanas, estadía."),
    ("Escala. Superficies mayores rinden más por jornada."),
]) + '''
    <p>La calculadora cubre solo el levantamiento con dron:
    <a href="{{P}}dron-fotogrametria/fotogrametria/">fotogrametría aérea</a>,
    <a href="{{P}}dron-fotogrametria/curvas-de-nivel/">curvas de nivel</a>,
    <a href="{{P}}dron-fotogrametria/rectificacion-deslindes/">deslindes</a> y
    <a href="{{P}}dron-fotogrametria/mapas-ortomosaicos/">ortomosaicos</a>. Para proyectos de
    <a href="{{P}}ingenieria-hidraulica/">ingeniería hidráulica</a>,
    <a href="{{P}}contacto/">escríbenos</a> y te respondemos con una propuesta a medida. Si tienes dudas
    sobre qué equidistancia pedir, revisa
    <a href="{{P}}blog/curvas-de-nivel-cada-cuanto/">cada cuánto conviene pedir las curvas de nivel</a>.</p>
  </div>
</section>
'''

COTIZADOR_FAQ = [
    ("¿El valor es definitivo?",
     "Es una estimación confiable para presupuestar, pero no reemplaza la propuesta formal. Vegetación densa, "
     "pendiente extrema o restricciones de vuelo pueden modificar el alcance. El valor final también se "
     "conversa según el requerimiento específico, el plazo que necesites, la extensión real del terreno y "
     "el tipo de archivo de entrega."),
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
    <h1>Ingeniería hidráulica</h1>
    <p class="encabezado__bajada">Resolvemos cómo se conduce, se almacena, se impulsa y se evacúa el agua:
    la red que abastece un loteo, la bomba que eleva a un estanque, el colector que recibe la lluvia o el
    estudio que determina hasta dónde llega una crecida.</p>
    ''' + acciones_encabezado("ingeniería hidráulica", calculadora=False) + '''
  </div>
</section>

<section class="seccion">
  <div class="contenedor">
    ''' + figura("modelacion-red-agua-potable-presiones",
                 "Modelación de presiones de una red de agua potable dibujada sobre imagen aérea de un "
                 "sector agrícola",
                 "Modelación de presiones de una red de agua potable, con las tuberías y nudos del modelo "
                 "sobre la imagen aérea.",
                 prioritaria=True) + '''
    <h2 class="seccion__titulo">Servicios</h2>
    ''' + tarjetas([
    ("Modelación de redes de agua potable",
     "Presiones y velocidades verificadas en demanda de punta y escenario de incendio.",
     "ingenieria-hidraulica/modelacion-redes/"),
    ("Bombas e impulsiones",
     "Curva del sistema, punto de operación, NPSH y golpe de ariete.",
     "ingenieria-hidraulica/dimensionamiento-bombas-impulsiones/"),
    ("Estudios de inundación",
     "Caudales de crecida, áreas inundables y cota de seguridad.",
     "ingenieria-hidraulica/estudios-inundacion/"),
    ("Drenaje pluvial",
     "Escorrentía, colectores, sumideros y obras de retención.",
     "ingenieria-hidraulica/drenaje-pluvial/"),
]) + '''
    <p>Los sistemas particulares de agua potable y alcantarillado que aprueba la SEREMI de Salud están en
    <a href="{{P}}proyecto-sanitario/">proyecto sanitario</a>.</p>
  </div>
</section>

<section class="seccion seccion--clara">
  <div class="contenedor">
    <h2 class="seccion__titulo">La topografía como punto de partida</h2>
    <p class="seccion__bajada">Una presión mal estimada, un colector con pendiente insuficiente o un área
    inundable mal delimitada casi siempre tienen el mismo origen: una base topográfica pobre. Al levantar el
    terreno con <a href="{{P}}dron-fotogrametria/">dron</a> antes de calcular, el modelo se construye sobre
    cotas reales y no sobre cartografía antigua.</p>
    ''' + lista([
    ("EPANET para redes a presión: agua potable, riego e impulsiones."),
    ("SWMM para drenaje urbano y aguas lluvia."),
    ("HEC-RAS para escurrimiento en cauces, 1D y 2D."),
    ("Diseño conforme a la normativa chilena aplicable (NCh, SISS, MOP–DOH)."),
]) + '''
  </div>
</section>
'''

HIDRO_FAQ = [
    ("¿Qué necesito antes de encargar un proyecto?",
     "Topografía del terreno (si no la tienes, la levantamos), el plano de loteo o arquitectura, la ubicación "
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
    <h1>Modelación de redes de agua potable con EPANET</h1>
    <p class="encabezado__bajada">Reproducimos en un modelo matemático cómo se comporta el agua dentro de las
    tuberías: cuánta presión llega a cada arranque en el máximo consumo y qué pasa cuando se abre un grifo de
    incendio. Sin ese cálculo, el diámetro se elige por costumbre.</p>
  </div>
</section>

<section class="seccion">
  <div class="contenedor">
    ''' + figura("modelacion-red-agua-potable-presiones",
                 "Modelación de presiones de una red de agua potable dibujada sobre imagen aérea de un "
                 "sector agrícola",
                 "Modelación de presiones de una red de agua potable, con las tuberías y nudos del modelo "
                 "sobre la imagen aérea.",
                 prioritaria=True) + '''
    <h2>Qué incluye el entregable</h2>
    ''' + lista([
    ("Modelo en EPANET del sistema completo, como archivo editable."),
    ("Presiones verificadas en demanda máxima horaria."),
    ("Velocidades y pérdidas de carga por tramo."),
    ("Escenario de incendio con grifo en operación."),
    ("Memoria de cálculo y planos de planta y perfiles."),
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
    en sistemas rurales forma parte del <a href="{{P}}proyecto-sanitario/agua-potable-particular/">proyecto de
    agua potable particular</a>.</p>
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
    ''' + lista([
    ("Curva del sistema: altura estática más pérdidas según caudal."),
    ("Punto de operación y rendimiento del equipo seleccionado."),
    ("Verificación de NPSH para descartar cavitación."),
    ("Golpe de ariete y protecciones necesarias."),
    ("Especificación técnica y consumo energético estimado."),
]) + '''
  </div>
</section>

<section class="seccion seccion--clara">
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
    <a href="{{P}}ingenieria-hidraulica/modelacion-redes/">modelación de la red</a> y se usa en los
    <a href="{{P}}proyecto-sanitario/agua-potable-particular/">sistemas de agua potable con pozo</a>.</p>
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
    <h1>Estudios de inundación y modelación hidráulica de cauces</h1>
    <p class="encabezado__bajada">Determinamos hasta dónde llega el agua cuando el río, estero o quebrada
    crece, con qué profundidad y a qué velocidad. Es lo que exige la autoridad cuando un proyecto se emplaza
    cerca de un cauce, y lo que define la cota mínima segura para construir.</p>
  </div>
</section>

<section class="seccion">
  <div class="contenedor">
    ''' + datos([
    ("T = 100 años", "Período de retorno habitual"),
    ("HEC-RAS", "Modelación 1D y 2D"),
    ("2–5 cm", "Precisión del terreno con dron"),
    ("3–6 sem", "Plazo típico del estudio"),
]) + '''
    ''' + figura("mapa-inundacion-hecras",
                 "Mapa de inundación con la mancha coloreada por profundidad, modelado en HEC-RAS",
                 "Mancha de inundación por período de retorno, coloreada por profundidad",
                 "16 / 9") + '''
    <h2>Qué incluye el entregable</h2>
    ''' + lista([
    ("Estudio hidrológico: caudales de crecida por período de retorno."),
    ("Modelo del cauce en HEC-RAS sobre topografía propia."),
    ("Mapas de área inundable con profundidad y velocidad."),
    ("Cota de seguridad para el emplazamiento."),
    ("Obras de mitigación evaluadas si el proyecto queda comprometido."),
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
    ''' + lista([
    ("Estudio hidrológico con curvas intensidad–duración–frecuencia."),
    ("Caudal de diseño antes y después de urbanizar."),
    ("Red de colectores: trazado, diámetros, pendientes y descargas."),
    ("Obras de retención o infiltración cuando se exige no aumentar el caudal."),
    ("Planos, memoria y especificaciones aptos para construcción."),
]) + '''
  </div>
</section>

<section class="seccion seccion--clara">
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

# ==========================================================================
# PILAR: PROYECTO SANITARIO (SEREMI de Salud)
# Fuentes: fichas ChileAtiende 16614 y 16932, preguntas frecuentes de Seremi en
# Línea (asdigital.minsal.cl) e instructivos regionales. Aranceles 2026.
# ==========================================================================
SANITARIO_PILAR = '''
<section class="encabezado">
  ''' + patron("flujo") + '''
  <div class="contenedor">
    <h1>Proyecto sanitario de agua potable y alcantarillado particular</h1>
    <p class="encabezado__bajada">Cuando el terreno no tiene red de una empresa sanitaria, el agua potable y
    el tratamiento de las aguas servidas se resuelven con un sistema propio. La SEREMI de Salud tiene que
    aprobar ese proyecto antes de construir y autorizar su funcionamiento antes de usarlo. Preparamos el
    proyecto, lo firma un ingeniero civil hidráulico inscrito como proyectista y lo tramitamos en las dos
    etapas.</p>
    ''' + acciones_encabezado("proyecto sanitario", calculadora=False) + '''
  </div>
</section>

<section class="seccion">
  <div class="contenedor">
    <h2 class="seccion__titulo">Qué necesitas tramitar</h2>
    ''' + tarjetas([
    ("Agua potable particular",
     "Pozo, noria o vertiente: captación, desinfección, estanque y red.",
     "proyecto-sanitario/agua-potable-particular/"),
    ("Alcantarillado particular",
     "Fosa séptica con drenes o pozo absorbente, o planta de tratamiento.",
     "proyecto-sanitario/alcantarillado-particular/"),
    ("Agua potable sin fuente propia",
     "Estanque abastecido por camión aljibe, con desinfección y distribución.",
     "proyecto-sanitario/agua-potable-sin-fuente-propia/"),
    ("Autorización de funcionamiento",
     "La segunda etapa: inspección de la obra construida y análisis del agua.",
     "proyecto-sanitario/autorizacion-de-funcionamiento/"),
    ("Reutilización de aguas grises",
     "Agua de duchas y lavamanos tratada para riego o inodoros, según la Ley 21.075.",
     "proyecto-sanitario/reutilizacion-aguas-grises/"),
]) + '''
  </div>
</section>

<section class="seccion seccion--clara">
  <div class="contenedor">
    <h2 class="seccion__titulo">Cuándo se necesita</h2>
    <p class="seccion__bajada">El artículo 71 del Código Sanitario (DFL 725 de 1968) entrega a la autoridad
    sanitaria la aprobación de toda obra, pública o privada, que provea agua potable o que evacúe y trate
    aguas servidas. En la práctica el trámite aparece en estos casos:</p>
    ''' + lista([
    "Una casa en una parcela o un sector rural sin red pública de agua ni alcantarillado.",
    "La recepción final de una vivienda o una ampliación, cuando la Dirección de Obras pide acreditar la "
    "solución sanitaria.",
    "Un local, restaurante, cabaña de turismo o sala de procesos que necesita resolución sanitaria para "
    "funcionar.",
    "Un condominio o loteo rural que se abastece de un pozo común.",
    "Un sistema que ya está construido y nunca se aprobó.",
]) + '''
    <p>Si el terreno está dentro del área de concesión de una empresa sanitaria, el camino es otro: la casa se
    conecta a la red y el proyecto se tramita ante esa empresa. Lo primero que hacemos es confirmar cuál de los
    dos corresponde.</p>
  </div>
</section>

<section class="seccion">
  <div class="contenedor">
    <h2 class="seccion__titulo">Cómo es el trámite</h2>
    ''' + pasos([
    ("Factibilidad",
     "La empresa sanitaria o la DOH certifica que no puede dar servicio al terreno. Ese certificado negativo "
     "es la puerta de entrada al proyecto particular."),
    ("Proyecto",
     "Memoria técnica, memoria de cálculo, planos y especificaciones. Para el agua potable se suma el análisis "
     "del agua de la fuente."),
    ("Aprobación del proyecto",
     "Se ingresa en Seremi en Línea con ClaveÚnica. La SEREMI revisa los antecedentes y emite la resolución "
     "que aprueba el proyecto, o las observaciones que hay que responder."),
    ("Construcción",
     "La obra se ejecuta según los planos aprobados. Si algo cambia en terreno, conviene resolverlo antes de "
     "pedir la inspección."),
    ("Autorización de funcionamiento",
     "Con la obra terminada se pide la visita. La SEREMI inspecciona, puede tomar muestras y emite la "
     "resolución que autoriza usar el sistema."),
]) + '''
    <p>Las fichas oficiales están en ChileAtiende:
    <a href="https://www.chileatiende.gob.cl/fichas/16614-aprobacion-de-proyectos-de-agua-potable-o-aguas-servidas-domesticas-particular" rel="noopener" target="_blank">aprobación
    de proyectos</a> y
    <a href="https://www.chileatiende.gob.cl/fichas/16932" rel="noopener" target="_blank">autorización de
    funcionamiento</a>.</p>
  </div>
</section>

<section class="seccion seccion--clara">
  <div class="contenedor">
    ''' + figura("plano-proyecto-sanitario-agua-potable-alcantarillado",
                 "Plano de emplazamiento de un proyecto de agua potable y alcantarillado particular con "
                 "pozo, estanque, fosa séptica y drenes",
                 "Plano de emplazamiento de un sistema particular de agua potable y alcantarillado.",
                 "16 / 9") + '''
    <div class="dos-columnas">
      <div>
        <h2>Qué preparamos</h2>
        ''' + lista([
    "Memoria técnica y memoria de cálculo.",
    "Planos de ubicación, emplazamiento, planta general y detalles.",
    "Perfil de canalizaciones con materiales, diámetros y pendientes.",
    "Especificaciones técnicas.",
    "Firma del proyecto por un ingeniero civil hidráulico inscrito como proyectista.",
    "Solicitud del certificado de factibilidad.",
    "Coordinación del análisis de agua con un laboratorio.",
    "Respuesta a las observaciones de la SEREMI hasta la aprobación.",
]) + '''
      </div>
      <div>
        <h2>Qué necesitamos de ti</h2>
        ''' + lista([
    "Certificado de dominio vigente del terreno.",
    "La ubicación y, si existe, el plano de arquitectura.",
    "Cuántas personas van a usar el sistema y para qué.",
    "De dónde sale el agua: pozo, noria, vertiente o camión aljibe.",
    "Si el pozo ya existe, sus antecedentes ante la DGA.",
]) + '''
      </div>
    </div>
  </div>
</section>

<section class="seccion">
  <div class="contenedor">
    <h2 class="seccion__titulo">Cuánto cuesta</h2>
    <div class="precio-desde">
      <p class="precio-desde__valor">Desde $400.000</p>
      <p class="precio-desde__nota">El valor depende del tamaño del sistema, de si incluye agua potable,
      alcantarillado o ambos, y de dónde está el terreno. Antes de empezar te enviamos una propuesta cerrada,
      que también detalla el arancel que cobra la SEREMI en cada etapa.</p>
    </div>
    <h2 class="seccion__titulo">Normas que aplican</h2>
    <div class="tabla-envoltura">
    <table>
      <caption>Normativa de los sistemas sanitarios particulares</caption>
      <thead><tr><th scope="col">Norma</th><th scope="col">Qué regula</th></tr></thead>
      <tbody>
        <tr><td>Código Sanitario (DFL 725 de 1968), art. 71</td><td>Aprobación de proyectos y autorización de funcionamiento por la autoridad sanitaria</td></tr>
        <tr><td>DFL 1 de 1989, Minsal</td><td>Materias que requieren autorización sanitaria expresa</td></tr>
        <tr><td>DS 735 de 1969</td><td>Servicios de agua destinados al consumo humano</td></tr>
        <tr><td>NCh 409/1</td><td>Calidad del agua potable</td></tr>
        <tr><td>DS 236 de 1926</td><td>Alcantarillados particulares: fosas sépticas y disposición de aguas servidas</td></tr>
        <tr><td>DS 41 de 2016, Minsal</td><td>Provisión de agua potable con camiones aljibe</td></tr>
        <tr><td>Ley 21.075 y Decreto 40, Minsal</td><td>Reutilización de aguas grises</td></tr>
      </tbody>
    </table>
    </div>
  </div>
</section>

<section class="seccion seccion--clara">
  <div class="contenedor">
    <h2 class="seccion__titulo">De Coquimbo a La Araucanía</h2>
    <p class="seccion__bajada">Cada SEREMI de Salud publica su propio instructivo, con exigencias de formato
    que cambian de una región a otra. Armamos el expediente según el de la región donde está tu terreno.</p>
    <p>El plano de emplazamiento tiene que mostrar las distancias entre el pozo, la fosa, los drenes, las
    construcciones y los deslindes. Si no tienes un plano confiable del terreno, lo levantamos con
    <a href="{{P}}dron-fotogrametria/curvas-de-nivel/">curvas de nivel</a> o una
    <a href="{{P}}dron-fotogrametria/rectificacion-deslindes/">rectificación de deslindes</a>. Si el sistema
    necesita bomba, el cálculo va con el
    <a href="{{P}}ingenieria-hidraulica/dimensionamiento-bombas-impulsiones/">dimensionamiento de bombas e
    impulsiones</a>.</p>
  </div>
</section>
'''

SANITARIO_FAQ = [
    ("¿Qué es la resolución sanitaria de agua potable y alcantarillado?",
     "Es como se conoce a las resoluciones de la SEREMI de Salud sobre un sistema particular. Son dos: la que "
     "aprueba el proyecto antes de construir y la que autoriza el funcionamiento cuando la obra está "
     "terminada."),
    ("¿Cuánto cuesta un proyecto sanitario?",
     "Desde $400.000. El valor final depende del tamaño del sistema, de si incluye agua potable, "
     "alcantarillado o ambos, y de la ubicación del terreno. El arancel de la SEREMI se paga aparte y va "
     "detallado en la propuesta."),
    ("¿Quién firma el proyecto?",
     "Un ingeniero civil hidráulico inscrito como proyectista, que es quien responde por el proyecto ante la "
     "SEREMI de Salud."),
    ("¿Puedo construir antes de tener el proyecto aprobado?",
     "No conviene. La norma pide la aprobación antes de construir, y una obra que no coincide con los planos "
     "aprobados es la causa más común de problemas en la inspección final."),
    ("¿Se puede regularizar un sistema que ya está construido?",
     "Sí. Se revisa lo construido, se verifica si cumple y se presenta el proyecto. Si algo no cumple, como la "
     "distancia entre el pozo y los drenes, el proyecto incluye la corrección."),
    ("¿Cuánto demora?",
     "Preparar el proyecto de una vivienda o un local nos toma entre 2 y 4 semanas desde que tenemos los "
     "antecedentes. El plazo de revisión de la SEREMI es aparte y varía según la región."),
]

# ==========================================================================
# PROYECTO SANITARIO — SUBPAGINAS
# ==========================================================================
AGUA_PARTICULAR = '''
<section class="encabezado">
  ''' + patron("flujo") + '''
  <div class="contenedor">
    <h1>Proyecto de agua potable particular con pozo, noria o vertiente</h1>
    <p class="encabezado__bajada">Cuando el agua sale de una fuente propia, la SEREMI de Salud necesita saber
    que llega potable a cada llave: de dónde se capta, cómo se desinfecta, dónde se almacena y cómo se
    reparte. Eso es lo que define el proyecto.</p>
  </div>
</section>

<section class="seccion">
  <div class="contenedor">
    <h2>Qué incluye el proyecto</h2>
    ''' + lista([
    "Captación: pozo profundo, noria o vertiente, con su caudal y ubicación.",
    "Bombeo y conducción hasta el estanque.",
    "Desinfección con cloro y, si el análisis lo exige, tratamiento de hierro, manganeso o arsénico.",
    "Estanque de regulación con su volumen y cota.",
    "Red de distribución con las pérdidas de carga verificadas.",
    "Distancias a fosas, drenes y descargas del propio predio y de los vecinos.",
]) + '''
  </div>
</section>

<section class="seccion seccion--clara">
  <div class="contenedor">
    <h2 class="seccion__titulo">El análisis del agua</h2>
    <p class="seccion__bajada">El proyecto se acompaña con un análisis físico-químico y bacteriológico del
    agua de la fuente, hecho por un laboratorio. Se compara con la NCh 409/1, la norma chilena de calidad del
    agua potable, y de ese resultado depende el tratamiento. Si solo aparecen coliformes, basta con
    desinfectar. Si hay hierro, manganeso o arsénico sobre el límite, el proyecto tiene que incluir un
    tratamiento específico. Para la autorización de funcionamiento el análisis no puede tener más de un
    año.</p>
    <h2 class="seccion__titulo">Los derechos de agua</h2>
    <p>La SEREMI pide acreditar que el agua del pozo se puede usar. Para bebida y uso doméstico en suelo
    propio, el Código de Aguas permite pozos con requisitos más simples (artículo 56). Para otros usos se
    necesita un derecho de aprovechamiento. Lo revisamos al principio, porque condiciona todo lo demás.</p>
    <p><strong>Servicios relacionados:</strong> casi siempre va junto al
    <a href="{{P}}proyecto-sanitario/alcantarillado-particular/">alcantarillado particular</a>. Si el sistema
    abastece varias casas, la red se verifica con
    <a href="{{P}}ingenieria-hidraulica/modelacion-redes/">modelación hidráulica</a>. Si no hay pozo, la
    alternativa es un <a href="{{P}}proyecto-sanitario/agua-potable-sin-fuente-propia/">sistema sin fuente
    propia</a>.</p>
  </div>
</section>
'''

AGUA_PARTICULAR_FAQ = [
    ("¿Por qué importa dónde está la fosa del vecino?",
     "Porque un dren de infiltración contamina el agua subterránea a su alrededor. El plano de emplazamiento "
     "muestra las fosas, drenes y descargas cercanas, propias y del vecino, y la SEREMI revisa que la captación "
     "quede a distancia segura."),
    ("¿Sirve una noria?",
     "Sí, si el análisis cumple y la captación queda protegida de las aguas que escurren por la superficie: "
     "brocal, tapa y sello sanitario."),
    ("¿Y si varias casas comparten el pozo?",
     "Se proyecta un sistema común. El diseño crece con el número de personas, y la red de distribución pasa "
     "a necesitar cálculo hidráulico."),
]

ALCANTARILLADO = '''
<section class="encabezado">
  ''' + patron("flujo") + '''
  <div class="contenedor">
    <h1>Proyecto de alcantarillado particular: fosa séptica y drenes</h1>
    <p class="encabezado__bajada">Sin colector público, las aguas servidas se tratan en el mismo terreno. El
    proyecto dimensiona la fosa séptica y la infiltración al suelo, o una planta de tratamiento cuando el
    caudal es mayor, y ubica todo a distancia segura de pozos, construcciones y deslindes.</p>
  </div>
</section>

<section class="seccion">
  <div class="contenedor">
    ''' + figura("fosa-septica-drenes-alcantarillado-particular",
                 "Detalle de fosa séptica y drenes de infiltración de un alcantarillado particular",
                 "Detalle de fosa séptica y drenes de infiltración.",
                 "16 / 9") + '''
    <h2>Qué incluye el proyecto</h2>
    ''' + lista([
    "Caudal de aguas servidas según el número de personas y el uso.",
    "Fosa séptica dimensionada, con sus cámaras de inspección.",
    "Disposición del efluente: drenes, zanjas de infiltración o pozo absorbente.",
    "Prueba de infiltración del suelo y profundidad de la napa.",
    "Planta general, detalles, perfil de canalizaciones y especificaciones.",
    "Manual de operación y mantención del sistema.",
]) + '''
  </div>
</section>

<section class="seccion seccion--clara">
  <div class="contenedor">
    <h2 class="seccion__titulo">Todo depende del suelo</h2>
    <p class="seccion__bajada">La fosa séptica retiene los sólidos, pero el líquido que sale todavía tiene que
    infiltrarse. Un suelo arcilloso o una napa alta obligan a alargar los drenes o a cambiar de solución. Por
    eso el proyecto parte con una prueba de infiltración donde irán los drenes, y no con un valor de
    tabla.</p>
    <h2 class="seccion__titulo">Fosa séptica o planta de tratamiento</h2>
    <p>Para una vivienda o un local pequeño lo habitual es fosa séptica con drenes. Cuando el caudal es mayor,
    como en un condominio o un restaurante, o cuando el suelo no infiltra, conviene una planta de tratamiento
    compacta. Si el efluente se descarga a un curso de agua, además tiene que cumplir la norma de emisión
    (DS 90) y contar con la autorización de descarga.</p>
    <p><strong>Servicios relacionados:</strong> el agua de la casa se tramita con el
    <a href="{{P}}proyecto-sanitario/agua-potable-particular/">proyecto de agua potable particular</a>. Las
    pendientes de la red salen de las <a href="{{P}}dron-fotogrametria/curvas-de-nivel/">curvas de
    nivel</a>. Con la obra construida sigue la
    <a href="{{P}}proyecto-sanitario/autorizacion-de-funcionamiento/">autorización de funcionamiento</a>.</p>
  </div>
</section>
'''

ALCANTARILLADO_FAQ = [
    ("¿Qué es la prueba de infiltración?",
     "Una excavación de prueba donde se llena de agua y se mide cuánto demora en bajar el nivel. Con ese tiempo "
     "se calcula la superficie de infiltración que necesitan los drenes."),
    ("¿Cada cuánto hay que limpiar la fosa?",
     "Depende de su volumen y del uso. El manual de mantención del proyecto indica la frecuencia y cómo revisar "
     "el nivel de lodos. La limpieza la hace un camión limpiafosas que cumpla las condiciones sanitarias de la "
     "SEREMI."),
    ("¿Sirve la fosa que ya tengo?",
     "Si funciona y cumple las distancias, se incorpora al proyecto. Si no, el proyecto define qué hay que "
     "reemplazar."),
]

SIN_FUENTE = '''
<section class="encabezado">
  ''' + patron("flujo") + '''
  <div class="contenedor">
    <h1>Agua potable sin fuente propia: estanque abastecido por camión aljibe</h1>
    <p class="encabezado__bajada">En sectores sin red y sin pozo, el agua llega en camión aljibe a un estanque
    del terreno. La SEREMI de Salud trata ese estanque y su distribución como un sistema particular de agua
    potable, así que también necesita proyecto aprobado y autorización de funcionamiento.</p>
  </div>
</section>

<section class="seccion">
  <div class="contenedor">
    <h2>Qué incluye el proyecto</h2>
    <p>La revisión de la SEREMI se concentra en el tratamiento, la desinfección, la regulación y la
    distribución del agua.</p>
    ''' + lista([
    "Volumen del estanque según personas, consumo y frecuencia de recarga.",
    "Estanque de material apto para agua potable, con tapa, ventilación y rebalse protegidos.",
    "Punto de carga accesible para el camión.",
    "Desinfección y control del cloro libre residual.",
    "Presurización y red de distribución hasta cada artefacto.",
]) + '''
  </div>
</section>

<section class="seccion seccion--clara">
  <div class="contenedor">
    <h2 class="seccion__titulo">El camión también tiene que estar autorizado</h2>
    <p class="seccion__bajada">El DS 41 del Minsal regula la provisión de agua potable con camiones aljibe:
    el proveedor necesita autorización sanitaria para ese transporte. El proyecto se acompaña con los
    antecedentes del proveedor autorizado que va a abastecer el sistema.</p>
    <p>Si después se perfora un pozo o llega la red pública, el sistema cambia de fuente y hay que tramitar el
    proyecto que corresponda.</p>
    <p><strong>Servicios relacionados:</strong> si hay agua subterránea disponible, compara con un
    <a href="{{P}}proyecto-sanitario/agua-potable-particular/">sistema con pozo o noria</a>. Las aguas
    servidas se resuelven con el
    <a href="{{P}}proyecto-sanitario/alcantarillado-particular/">alcantarillado particular</a>, y al terminar
    la obra sigue la <a href="{{P}}proyecto-sanitario/autorizacion-de-funcionamiento/">autorización de
    funcionamiento</a>.</p>
  </div>
</section>
'''

SIN_FUENTE_FAQ = [
    ("¿De qué tamaño debe ser el estanque?",
     "Se calcula con el número de personas, el consumo diario y los días entre cargas, más una reserva. "
     "Tampoco conviene sobredimensionarlo: el agua pasa más días guardada y pierde el cloro."),
    ("¿Puedo comprar el agua a cualquier camión?",
     "No. Tiene que ser un proveedor con autorización sanitaria para transportar agua potable."),
    ("¿Qué normas aplican?",
     "El Código Sanitario, el DS 735 sobre servicios de agua para consumo humano y el DS 41 sobre provisión "
     "de agua con camiones aljibe."),
]

AUTORIZACION = '''
<section class="encabezado">
  ''' + patron("flujo") + '''
  <div class="contenedor">
    <h1>Autorización de funcionamiento de sistema particular de agua potable y alcantarillado</h1>
    <p class="encabezado__bajada">Es la segunda resolución del trámite. Con la obra construida, la SEREMI de
    Salud verifica en terreno que el sistema coincide con el proyecto aprobado y que el agua cumple. Recién
    entonces autoriza su uso.</p>
  </div>
</section>

<section class="seccion">
  <div class="contenedor">
    <h2>Qué se presenta</h2>
    ''' + lista([
    "Copia de la resolución que aprobó el proyecto.",
    "Copia de los planos timbrados en la aprobación.",
    "Análisis físico-químico y bacteriológico del agua de la fuente, con menos de un año.",
    "Autorización de descarga a un curso de agua, cuando corresponde.",
    "Los antecedentes adicionales que haya pedido la resolución de aprobación.",
]) + '''
  </div>
</section>

<section class="seccion seccion--clara">
  <div class="contenedor">
    <h2 class="seccion__titulo">Qué hacemos antes de pedir la visita</h2>
    ''' + pasos([
    ("Revisión de la obra",
     "Comparamos lo construido con los planos aprobados: ubicación de la fosa y los drenes, estanque, "
     "cloración y cámaras."),
    ("Correcciones",
     "Si algo cambió en terreno, se corrige la obra o se regulariza el cambio antes de la inspección."),
    ("Análisis del agua",
     "Coordinamos la toma de muestra con el laboratorio para que el resultado esté vigente al ingresar."),
    ("Ingreso y visita",
     "Preparamos el ingreso en Seremi en Línea y acompañamos la inspección."),
]) + '''
    <p>La resolución que aprueba el proyecto rige hasta que se autoriza el funcionamiento. Desde ahí, la
    autorización se mantiene mientras exista la fuente de agua y las instalaciones sigan en regla.</p>
    <p><strong>Servicios relacionados:</strong> la primera etapa es la
    <a href="{{P}}proyecto-sanitario/">aprobación del proyecto sanitario</a>, ya sea de
    <a href="{{P}}proyecto-sanitario/agua-potable-particular/">agua potable particular</a> o de
    <a href="{{P}}proyecto-sanitario/alcantarillado-particular/">alcantarillado particular</a>.</p>
  </div>
</section>
'''

AUTORIZACION_FAQ = [
    ("¿Qué pasa si la obra no quedó igual al plano?",
     "Depende del cambio. Uno menor se puede aclarar en la inspección; uno que afecta distancias o dimensiones "
     "obliga a modificar antes el proyecto aprobado. Revisarlo antes de pedir la visita evita una segunda "
     "inspección."),
    ("¿La SEREMI toma muestras?",
     "Puede hacerlo. La inspección verifica la obra y su funcionamiento, y puede incluir muestras del agua."),
    ("¿Hay que pagar de nuevo?",
     "Sí. La autorización de funcionamiento tiene su propio arancel de la SEREMI, que va detallado en nuestra "
     "propuesta."),
]

AGUAS_GRISES = '''
<section class="encabezado">
  ''' + patron("flujo") + '''
  <div class="contenedor">
    <h1>Proyecto de reutilización de aguas grises</h1>
    <p class="encabezado__bajada">Las aguas grises son las que salen de duchas, tinas, lavamanos y lavadoras.
    Tratadas, sirven para regar el jardín o descargar los inodoros. La Ley 21.075 permite reutilizarlas con un
    sistema aprobado por la SEREMI de Salud, en zonas urbanas y rurales.</p>
  </div>
</section>

<section class="seccion">
  <div class="contenedor">
    <h2>Qué incluye el proyecto</h2>
    ''' + lista([
    "Separación de la red de aguas grises y la de aguas negras.",
    "Tratamiento según el uso: filtración y desinfección.",
    "Estanque de acumulación y rebalse hacia el alcantarillado o la disposición final.",
    "Red de reutilización identificada y separada de la de agua potable.",
    "Manual de operación y mantención.",
]) + '''
  </div>
</section>

<section class="seccion seccion--clara">
  <div class="contenedor">
    <h2 class="seccion__titulo">Para qué se pueden usar</h2>
    <p class="seccion__bajada">La ley permite usos como el riego de áreas verdes y la descarga de inodoros.
    Prohíbe, entre otros, el consumo humano y el riego de frutas y hortalizas que crecen a ras de suelo y se
    comen crudas. El tratamiento se diseña para el uso que se declara.</p>
    <p>El trámite tiene las mismas dos etapas ante la SEREMI de Salud: aprobación del proyecto y autorización
    de funcionamiento.</p>
    <p><strong>Servicios relacionados:</strong> en terrenos sin colector se proyecta junto al
    <a href="{{P}}proyecto-sanitario/alcantarillado-particular/">alcantarillado particular</a>. Revisa también
    cómo funciona la <a href="{{P}}proyecto-sanitario/autorizacion-de-funcionamiento/">autorización de
    funcionamiento</a> o <a href="{{P}}contacto/">escríbenos</a> con los datos de tu casa.</p>
  </div>
</section>
'''

AGUAS_GRISES_FAQ = [
    ("¿Sirve en una casa conectada al alcantarillado público?",
     "Sí. La ley se aplica en zonas urbanas y rurales. Lo que cambia es hacia dónde descarga el rebalse del "
     "sistema."),
    ("¿Qué norma lo regula?",
     "La Ley 21.075 de 2018 y su reglamento, el Decreto 40 del Minsal, que fija las condiciones sanitarias del "
     "sistema."),
]

# ==========================================================================
# CAPACIDADES
# ==========================================================================
CAPACIDADES = '''
<section class="encabezado">
  ''' + patron("curvas") + '''
  <div class="contenedor">
    <h1>Qué entregamos, con qué herramientas y en qué formatos</h1>
    <p class="encabezado__bajada">RCKT es una oficina nueva con foco en hacer bien dos cosas: levantar
    terreno con dron y resolver ingeniería hidráulica. Acá está el detalle técnico de lo que recibes.</p>
  </div>
</section>

<section class="seccion">
  <div class="contenedor">
    <h2 class="seccion__titulo">Entregables por área</h2>
    <div class="bloques">
      <div class="bloque">
        <div class="bloque__cabecera"><h3>Topografía y fotogrametría</h3></div>
        <ul class="lista-check">
          <li>Ortomosaico en GeoTIFF, 2 a 5 cm/píxel.</li>
          <li>Nube de puntos en LAS/LAZ clasificada.</li>
          <li>Modelo digital de superficie y de terreno.</li>
          <li>Curvas de nivel en DWG/DXF por capas.</li>
          <li>Informe con error verificado por puntos independientes.</li>
        </ul>
      </div>
      <div class="bloque">
        <div class="bloque__cabecera"><h3>Ingeniería hidráulica</h3></div>
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
      ''' + figura("rectificacion-deslindes-ortomosaico-dron",
                   "Rectificación de deslindes de un predio levantado con dron",
                   "Rectificación de deslindes") + '''
      ''' + figura("modelacion-golpe-de-ariete",
                   "Modelación de golpe de ariete en una impulsión",
                   "Modelación de golpe de ariete") + '''
      ''' + figura("drenaje-pluvial",
                   "Proyecto de drenaje pluvial con trazado de colectores",
                   "Drenaje pluvial") + '''
    </div>
    <p>Cada uno corresponde a un servicio: <a href="{{P}}dron-fotogrametria/rectificacion-deslindes/">rectificación
    de deslindes</a>, <a href="{{P}}ingenieria-hidraulica/dimensionamiento-bombas-impulsiones/">modelación de
    golpe de ariete</a> y <a href="{{P}}ingenieria-hidraulica/drenaje-pluvial/">drenaje pluvial</a>. Revisa
    también la <a href="{{P}}dron-fotogrametria/">línea de topografía con dron</a>, la de
    <a href="{{P}}ingenieria-hidraulica/">ingeniería hidráulica</a> o calcula un levantamiento en la
    <a href="{{P}}cotizador/">calculadora</a>.</p>
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
# EMPRESA
# ==========================================================================
EMPRESA = '''
<section class="encabezado">
  ''' + patron("curvas") + '''
  <div class="contenedor">
    <h1>RCKT: topografía con dron e ingeniería hidráulica</h1>
    <p class="encabezado__bajada">Hacemos dos cosas que normalmente se contratan por separado:
    levantamientos topográficos con dron y proyectos de ingeniería hidráulica y sanitaria, incluidos los
    sistemas particulares de agua potable y alcantarillado que aprueba la SEREMI de Salud.</p>
  </div>
</section>

<section class="seccion">
  <div class="contenedor">
    ''' + figura("retrato-profesional-rckt",
                 "Retrato profesional del equipo de RCKT en terreno junto al dron",
                 "Quien conversa el proyecto es quien vuela el terreno y firma la entrega",
                 "16 / 9") + '''
    <div class="dos-columnas">
      <div>
        <h2>Por qué las dos juntas</h2>
        <p>En los proyectos de agua el problema suele empezar por la topografía: no existe, es antigua o no
        tiene el detalle necesario para calcular. Sin cotas confiables, el cálculo hidráulico queda apoyado en
        supuestos.</p>
        <p>Por eso levantamos el terreno nosotros mismos, con la precisión que va a necesitar el cálculo. Así
        no hay que coordinar a una oficina de topografía con otra de ingeniería, ni esperar a que se
        entiendan.</p>
      </div>
      <div>
        <h2>Cómo trabajamos</h2>
        <p>Antes de empezar te enviamos por escrito qué vas a recibir, en qué formato, en qué plazo y cuánto
        cuesta. La persona que conversa contigo el proyecto es la misma que hace el terreno y el cálculo.</p>
        <p>Entregamos los archivos de trabajo (DWG, nubes de puntos, modelos hidráulicos) y no solo PDF, para
        que tu equipo pueda seguir usándolos. Y si un levantamiento con dron no es lo que tu caso necesita, te
        lo decimos antes de cotizar.</p>
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
        <tr><td>Título profesional</td><td>Ingeniero civil hidráulico, inscrito como proyectista</td></tr>
        <tr><td>Especialidades</td><td>Topografía y fotogrametría con dron · Ingeniería hidráulica · Proyectos sanitarios particulares</td></tr>
      </tbody>
    </table>
    </div>
    <p>Trabajamos en tres líneas: <a href="{{P}}dron-fotogrametria/">topografía con dron</a>,
    <a href="{{P}}ingenieria-hidraulica/">ingeniería hidráulica</a> y
    <a href="{{P}}proyecto-sanitario/">proyectos sanitarios</a> para la SEREMI de Salud. Puedes estimar un levantamiento en la
    <a href="{{P}}cotizador/">calculadora de cotización</a> o <a href="{{P}}contacto/">escribirnos</a>
    directamente.</p>
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
          <span class="contacto__valor">''' + horario_texto() + '''</span>
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
      <a href="{{P}}cotizador/">calculadora de cotización</a>. También puedes revisar los servicios de
      <a href="{{P}}dron-fotogrametria/">topografía con dron</a>,
      <a href="{{P}}ingenieria-hidraulica/">ingeniería hidráulica</a> y
      <a href="{{P}}proyecto-sanitario/">proyecto sanitario</a>.</p>
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
          <label for="mensaje">Cuéntanos el proyecto</label>
          <textarea id="mensaje" name="mensaje" rows="5" placeholder="Qué necesitas, dónde está el terreno y cualquier plazo que debamos considerar" required></textarea>
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

<section class="seccion seccion--clara">
  <div class="contenedor">
    <h2 class="seccion__titulo">Zonas de cobertura</h2>
    <p class="seccion__bajada"><strong>Región Metropolitana (base):</strong> Santiago y comunas, Colina,
    Lampa, Buin, Paine, Melipilla, Curacaví, Talagante, Peñaflor, Pirque y San José de Maipo ·
    <strong>Coquimbo:</strong> La Serena, Coquimbo, Ovalle, Vicuña, Monte Patria, Illapel, Salamanca y
    Los Vilos · <strong>Valparaíso:</strong> Valparaíso, Viña del Mar, Concón, Quilpué, Casablanca,
    San Antonio, Algarrobo y La Ligua · <strong>O'Higgins:</strong> Rancagua, Machalí, Rengo,
    San Fernando, Santa Cruz y Peumo · <strong>Maule:</strong> Talca, Curicó, Molina, San Javier, Linares
    y Constitución · <strong>La Araucanía:</strong> Temuco, Padre Las Casas, Angol, Victoria, Villarrica,
    Pucón, Curarrehue, Nueva Imperial y Loncoche.</p>
    <p>Fuera de la Región Metropolitana se agrega el traslado, informado por adelantado en la propuesta.
    Los viajes a zonas distantes se agrupan para repartir ese costo entre varios trabajos.</p>
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
    <h1>Artículos sobre fotogrametría con dron e ingeniería hidráulica</h1>
    <p class="encabezado__bajada">Explicaciones claras sobre cómo se hacen las cosas y qué conviene pedir en
    cada caso. Escrito para quien contrata el servicio, no para quien lo ejecuta.</p>
  </div>
</section>

<section class="seccion">
  <div class="contenedor">
  <div class="lista-posts">
    <article class="post-tarjeta">
      <p class="post-tarjeta__meta">Fotogrametría · 7 min</p>
      <h2><a href="{{P}}blog/levantamiento-fotogrametrico-deslindes/">Cómo se hace un levantamiento fotogramétrico para deslindes</a></h2>
      <p>Desde la planificación del vuelo y los puntos de control hasta la superposición del plano de título
      sobre el ortomosaico.</p>
      <p><a class="enlace-fuerte" href="{{P}}blog/levantamiento-fotogrametrico-deslindes/">Leer ''' + icono("flecha", "icono icono--sm") + '''</a></p>
    </article>

    <article class="post-tarjeta">
      <p class="post-tarjeta__meta">Hidráulica · 6 min</p>
      <h2><a href="{{P}}blog/que-es-modelacion-redes-agua-potable/">Qué es la modelación de redes de agua potable y cuándo se necesita</a></h2>
      <p>Qué hace un modelo hidráulico y por qué el diámetro elegido "por costumbre" suele salir caro.</p>
      <p><a class="enlace-fuerte" href="{{P}}blog/que-es-modelacion-redes-agua-potable/">Leer ''' + icono("flecha", "icono icono--sm") + '''</a></p>
    </article>

    <article class="post-tarjeta">
      <p class="post-tarjeta__meta">Topografía · 5 min</p>
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
  describe los deslindes por referencias, hay un trabajo de interpretación previo que define qué hay que
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
    <li>Cercos bajo copa cerrada. Si el límite corre bajo bosque denso, hay que medirlo en terreno.</li>
    <li>Hitos no materializados. Un vértice sin materialización debe replantearse desde coordenadas.</li>
    <li>La definición legal del deslinde. El levantamiento entrega evidencia técnica; la determinación jurídica es otro ámbito.</li>
  </ul>

  <p class="articulo__cierre">¿Necesitas verificar los deslindes de un predio? Revisa el
  <a href="{{P}}dron-fotogrametria/rectificacion-deslindes/">servicio de rectificación de deslindes</a>, estima el
  valor en la <a href="{{P}}cotizador/">calculadora</a> o <a href="{{P}}contacto/">escríbenos</a>. Si además
  vas a subdividir, te servirá el <a href="{{P}}dron-fotogrametria/curvas-de-nivel/">levantamiento de curvas
  de nivel</a>.</p>
</article>
</div></section>
'''

POST_REDES = '''
<section class="encabezado encabezado--post">
  ''' + patron("flujo") + '''
  <div class="contenedor">
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
        "desc": "RCKT: levantamientos con dron, curvas de nivel y deslindes, ingeniería hidráulica y proyectos sanitarios para la SEREMI de Salud. Cotiza en línea.",
        "body": HOME,
        "faq": HOME_FAQ,
        "nav_activa": None,
    },
    # ---- DRON ----
    {
        "path": "dron-fotogrametria",
        "title": "Topografía con dron | Levantamientos aéreos y fotogrametría",
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
        "title": "Nube de puntos y modelo digital de terreno con dron",
        "desc": "Vuelo fotogramétrico con dron: nube de puntos densa, modelo digital de terreno y ortomosaico con precisión de 2 a 5 cm. Consulta plazos y valores.",
        "body": FOTOGRAMETRIA,
        "faq": FOTOGRAMETRIA_FAQ,
        "crumbs": [("Dron y topografía", "dron-fotogrametria/"), ("Nube de puntos y modelo de terreno", None)],
        "nav_activa": "dron-fotogrametria/",
        "schema_servicio": ("Nube de puntos y modelo digital de terreno con dron",
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
        "path": "dron-fotogrametria/rectificacion-deslindes",
        "title": "Rectificación de deslindes de predios con dron",
        "desc": "Verifica los límites reales de tu predio: ortomosaico, coordenadas de cada vértice y comparación con el plano de título. Cotiza tu rectificación de deslindes.",
        "body": DESLINDES,
        "faq": DESLINDES_FAQ,
        "crumbs": [("Dron y topografía", "dron-fotogrametria/"), ("Rectificación de deslindes", None)],
        "nav_activa": "dron-fotogrametria/",
        "schema_servicio": ("Rectificación de deslindes con dron",
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
        "title": "Ingeniería hidráulica | Redes, bombas, drenaje e inundación",
        "desc": "Modelación de redes de agua potable, impulsiones, drenaje pluvial y estudios de inundación, con memoria, planos y cálculo sobre topografía propia. Consúltanos.",
        "body": HIDRO_PILAR,
        "faq": HIDRO_FAQ,
        "crumbs": [("Ingeniería hidráulica", None)],
        "nav_activa": "ingenieria-hidraulica/",
        "schema_servicio": ("Ingeniería hidráulica",
                            "Diseño, cálculo y modelación de sistemas de agua: redes de agua potable, impulsiones, drenaje pluvial y estudios de inundación.",
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
    # ---- PROYECTO SANITARIO ----
    {
        "path": "proyecto-sanitario",
        "title": "Proyecto sanitario particular: agua potable y alcantarillado",
        "desc": "Proyecto de agua potable y alcantarillado particular para la SEREMI de Salud, firmado por ingeniero civil hidráulico. Desde $400.000. Consúltanos.",
        "body": SANITARIO_PILAR,
        "faq": SANITARIO_FAQ,
        "crumbs": [("Proyecto sanitario", None)],
        "nav_activa": "proyecto-sanitario/",
        "schema_servicio": ("Proyecto sanitario de agua potable y alcantarillado particular",
                            "Proyecto y tramitación ante la SEREMI de Salud de sistemas particulares de agua potable y alcantarillado, según el artículo 71 del Código Sanitario: aprobación del proyecto y autorización de funcionamiento.",
                            "Proyecto sanitario"),
    },
    {
        "path": "proyecto-sanitario/agua-potable-particular",
        "title": "Proyecto de agua potable particular con pozo o noria",
        "desc": "Proyecto de agua potable particular con pozo, noria o vertiente para la SEREMI de Salud: captación, cloración, estanque, red y análisis de agua. Consúltanos.",
        "body": AGUA_PARTICULAR,
        "faq": AGUA_PARTICULAR_FAQ,
        "crumbs": [("Proyecto sanitario", "proyecto-sanitario/"), ("Agua potable particular", None)],
        "nav_activa": "proyecto-sanitario/",
        "schema_servicio": ("Proyecto de agua potable particular",
                            "Proyecto de sistema particular de agua potable con fuente propia (pozo, noria o vertiente): captación, desinfección, estanque de regulación y red de distribución, para aprobación de la SEREMI de Salud.",
                            "Proyecto de agua potable particular"),
    },
    {
        "path": "proyecto-sanitario/alcantarillado-particular",
        "title": "Proyecto de fosa séptica y alcantarillado particular",
        "desc": "Proyecto de alcantarillado particular con fosa séptica, drenes o pozo absorbente, con prueba de infiltración y planos para la SEREMI de Salud. Cotiza el tuyo.",
        "body": ALCANTARILLADO,
        "faq": ALCANTARILLADO_FAQ,
        "crumbs": [("Proyecto sanitario", "proyecto-sanitario/"), ("Alcantarillado particular", None)],
        "nav_activa": "proyecto-sanitario/",
        "schema_servicio": ("Proyecto de alcantarillado particular y fosa séptica",
                            "Proyecto de tratamiento particular de aguas servidas domésticas: fosa séptica, drenes, pozo absorbente o planta de tratamiento, con prueba de infiltración, para aprobación de la SEREMI de Salud.",
                            "Proyecto de alcantarillado particular"),
    },
    {
        "path": "proyecto-sanitario/agua-potable-sin-fuente-propia",
        "title": "Agua potable sin fuente propia: estanque y camión aljibe",
        "desc": "Proyecto de sistema de agua potable sin fuente propia, con estanque abastecido por camión aljibe, desinfección y red, para aprobación de la SEREMI de Salud.",
        "body": SIN_FUENTE,
        "faq": SIN_FUENTE_FAQ,
        "crumbs": [("Proyecto sanitario", "proyecto-sanitario/"), ("Agua potable sin fuente propia", None)],
        "nav_activa": "proyecto-sanitario/",
        "schema_servicio": ("Proyecto de agua potable sin fuente propia",
                            "Proyecto de sistema particular de agua potable sin fuente propia, abastecido por camión aljibe: estanque, desinfección, regulación y distribución, según el DS 735 y el DS 41 del Minsal.",
                            "Proyecto de agua potable particular"),
    },
    {
        "path": "proyecto-sanitario/autorizacion-de-funcionamiento",
        "title": "Autorización de funcionamiento: agua potable y alcantarillado",
        "desc": "Autorización de funcionamiento de sistemas particulares de agua potable y alcantarillado ante la SEREMI de Salud: revisión de obra, análisis de agua e ingreso.",
        "body": AUTORIZACION,
        "faq": AUTORIZACION_FAQ,
        "crumbs": [("Proyecto sanitario", "proyecto-sanitario/"), ("Autorización de funcionamiento", None)],
        "nav_activa": "proyecto-sanitario/",
        "schema_servicio": ("Autorización de funcionamiento de sistema sanitario particular",
                            "Preparación y tramitación de la autorización de funcionamiento de sistemas particulares de agua potable y aguas servidas ante la SEREMI de Salud: revisión de obra, análisis de agua e inspección.",
                            "Tramitación sanitaria"),
    },
    {
        "path": "proyecto-sanitario/reutilizacion-aguas-grises",
        "title": "Proyecto de reutilización de aguas grises | Ley 21.075",
        "desc": "Proyecto de reutilización de aguas grises según la Ley 21.075: separación de redes, tratamiento y riego o inodoros, con aprobación de la SEREMI de Salud.",
        "body": AGUAS_GRISES,
        "faq": AGUAS_GRISES_FAQ,
        "crumbs": [("Proyecto sanitario", "proyecto-sanitario/"), ("Reutilización de aguas grises", None)],
        "nav_activa": "proyecto-sanitario/",
        "schema_servicio": ("Proyecto de reutilización de aguas grises",
                            "Proyecto de sistema de reutilización de aguas grises según la Ley 21.075 y el Decreto 40 del Minsal: recolección, tratamiento, reutilización y disposición, para aprobación de la SEREMI de Salud.",
                            "Proyecto de aguas grises"),
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
        "path": "empresa",
        "title": "Empresa | RCKT Topografía e Ingeniería Hidráulica",
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
