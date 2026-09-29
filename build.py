# -*- coding: utf-8 -*-
"""
Generador del sitio estatico de RCKT (fotogrametria con dron + ingenieria hidraulica).

Uso:  python build.py
Genera todas las paginas HTML, el sitemap.xml y el robots.txt en esta misma carpeta.

Para editar el sitio:
  1. Cambia los datos de CONFIG (marca, telefono, email, dominio).
  2. Edita el texto de cada pagina en contenido.py
  3. Vuelve a ejecutar:  python build.py
"""

import os
import re
import json
import math
import hashlib
import datetime

# --------------------------------------------------------------------------
# CONFIG — CAMBIA ESTOS DATOS
# --------------------------------------------------------------------------
CONFIG = {
    "marca": "RCKT",
    "descriptor": "Topografía e Ingeniería Hidráulica",  # bajada de la marca (logo, pie, schema)
    "marca_legal": "RCKT SpA",                     # razón social — ajustar cuando exista
    "dominio": "https://rckt.cl",                   # sin barra final. Cambiar al registrar el dominio
    "telefono_display": "+56 9 9224 1636",
    "telefono_link": "+56992241636",
    "whatsapp": "56992241636",
    "email": "contacto@rckt.cl",
    "ciudad_base": "Santiago",
    "region_base": "Región Metropolitana",
    "pais": "CL",
    "og_image": "assets/img/og-portada.svg",       # respaldo: si dejas og-portada.jpg se usa ese
    "anio": datetime.date.today().year,

    # --- SEO local: coordenadas de la base de operaciones ---
    # AJUSTAR a la ubicación real (búscala en Google Maps, clic derecho sobre el punto).
    # Hoy apunta al centro de Santiago.
    "lat": -33.4489,
    "lon": -70.6693,
    # Días de atención. Hoy: todos los días de la semana (etapa de arranque, sin
    # restricción de fin de semana). Para volver a un horario de oficina, deja
    # solo ("Monday", ..., "Friday") — el texto de contacto y el schema se
    # actualizan solos, no hay que tocarlos aparte.
    "horario": [("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")],
    "hora_apertura": "09:00",
    "hora_cierre": "18:00",

    # --- Perfiles públicos (schema sameAs). Agrega las URLs cuando existan. ---
    # Ej: ["https://www.linkedin.com/company/rckt", "https://www.instagram.com/rckt.cl"]
    "redes": [],

    # --- Herramientas de medición (dejar vacío hasta tenerlas) ---
    # Search Console → Propiedad → Verificación por etiqueta HTML: pega solo el "content".
    "gsc_verificacion": "",
    # Google Analytics 4: pega el identificador, ej. "G-XXXXXXXXXX".
    "ga4_id": "",
}

# --------------------------------------------------------------------------
# SERVICIOS OCULTOS
#
# Agrega acá la ruta de cualquier servicio o zona que NO quieras ofrecer por
# ahora y vuelve a ejecutar `python build.py`. La página deja de generarse,
# desaparece del menú, del pie, del sitemap, de las tarjetas de servicio y del
# formulario de contacto, y los enlaces que la mencionaban en el texto quedan
# como texto normal (sin enlace roto). Para volver a ofrecerla, borra la línea
# y reconstruye.
#
# Ocultar un pilar completo oculta también todas sus subpáginas.
#
# Rutas disponibles:
#   dron-fotogrametria                                   (pilar completo)
#   dron-fotogrametria/fotogrametria
#   dron-fotogrametria/curvas-de-nivel
#   dron-fotogrametria/rectificacion-deslindes
#   dron-fotogrametria/mapas-ortomosaicos
#   cotizador
#   ingenieria-hidraulica                                (pilar completo)
#   ingenieria-hidraulica/modelacion-redes
#   ingenieria-hidraulica/dimensionamiento-bombas-impulsiones
#   ingenieria-hidraulica/estudios-inundacion
#   ingenieria-hidraulica/drenaje-pluvial
#   proyecto-sanitario                                   (pilar completo)
#   proyecto-sanitario/agua-potable-particular
#   proyecto-sanitario/alcantarillado-particular
#   proyecto-sanitario/agua-potable-sin-fuente-propia
#   proyecto-sanitario/autorizacion-de-funcionamiento
#   proyecto-sanitario/reutilizacion-aguas-grises
#   capacidades · blog · empresa
#
# Ejemplo — dejar de ofrecer estudios de inundación en temporada baja:
#   SERVICIOS_OCULTOS = ["ingenieria-hidraulica/estudios-inundacion"]
#
# "blog" y "capacidades" están ocultas por ahora (2026-08-14): el sitio recién
# arranca y esas dos páginas conviene publicarlas con contenido más maduro
# (artículos reales, entregables ya probados). Borra las dos líneas cuando
# quieras reactivarlas — no hace falta tocar nada más.
# --------------------------------------------------------------------------
SERVICIOS_OCULTOS = [
    "blog",
    "capacidades",
]


def esta_oculto(ruta):
    """True si la ruta está oculta, o cuelga de un pilar oculto."""
    if not ruta:
        return False
    r = ruta.strip("/")
    return any(r == o or r.startswith(o + "/") for o in SERVICIOS_OCULTOS)


_RE_ENLACE = re.compile(r'<a\b[^>]*href="([^"]*)"[^>]*>(.*?)</a>', re.S)


def desactivar_enlaces(html):
    """Convierte en texto plano los enlaces que apuntan a servicios ocultos."""
    if not SERVICIOS_OCULTOS:
        return html

    def reemplazo(m):
        destino = m.group(1)
        if destino.startswith(("http://", "https://", "mailto:", "tel:", "#")):
            return m.group(0)
        return m.group(2) if esta_oculto(re.sub(r"^(\.\./)+", "", destino)) else m.group(0)

    return _RE_ENLACE.sub(reemplazo, html)


# Opciones del selector "¿Qué necesitas?" del formulario de contacto.
# Cada una se asocia a una ruta para poder ocultarla junto con su servicio.
OPCIONES_CONSULTA = [
    ("Levantamiento con dron / topografía", "dron-fotogrametria/fotogrametria"),
    ("Curvas de nivel", "dron-fotogrametria/curvas-de-nivel"),
    ("Rectificación de deslindes", "dron-fotogrametria/rectificacion-deslindes"),
    ("Ortomosaico / mapa", "dron-fotogrametria/mapas-ortomosaicos"),
    ("Proyecto de agua potable particular (pozo o noria)", "proyecto-sanitario/agua-potable-particular"),
    ("Alcantarillado particular / fosa séptica", "proyecto-sanitario/alcantarillado-particular"),
    ("Agua potable sin fuente propia (camión aljibe)", "proyecto-sanitario/agua-potable-sin-fuente-propia"),
    ("Autorización de funcionamiento SEREMI", "proyecto-sanitario/autorizacion-de-funcionamiento"),
    ("Reutilización de aguas grises", "proyecto-sanitario/reutilizacion-aguas-grises"),
    ("Drenaje pluvial", "ingenieria-hidraulica/drenaje-pluvial"),
    ("Estudio de inundación", "ingenieria-hidraulica/estudios-inundacion"),
    ("Modelación de redes / bombas", "ingenieria-hidraulica/modelacion-redes"),
    ("Todavía no lo tengo claro", None),
]


def opciones_consulta():
    return "\n".join(
        f'            <option>{texto}</option>'
        for texto, ruta in OPCIONES_CONSULTA if not esta_oculto(ruta)
    )


ZONAS_SERVICIO = [
    "Región Metropolitana", "Santiago", "Colina", "Buin", "Melipilla",
    "Región de Coquimbo", "La Serena", "Coquimbo",
    "Región de Valparaíso", "Valparaíso", "Viña del Mar", "San Antonio", "Casablanca",
    "Región de O'Higgins", "Rancagua", "San Fernando", "Santa Cruz",
    "Región del Maule", "Talca", "Curicó", "Linares",
    "Región de La Araucanía", "Temuco", "Padre Las Casas", "Angol", "Victoria",
    "Villarrica", "Pucón", "Curarrehue", "Nueva Imperial", "Loncoche",
]

OUT = os.path.dirname(os.path.abspath(__file__))

# --------------------------------------------------------------------------
# CALCULADORA DE COTIZACIÓN — PARÁMETROS INTERNOS
#
# Todo el modelo de costos vive acá. El visitante NO ve ninguno de estos
# valores ni la fórmula: solo el precio final. Ajusta estos números y vuelve
# a ejecutar `python build.py`.
#
# ATENCIÓN: el cálculo ocurre en el navegador, así que alguien con
# conocimientos técnicos puede leer estos parámetros en el código fuente de la
# página. No es información secreta frente a un competidor decidido; sí queda
# oculta para el 99% de los visitantes. Si necesitas que sea realmente privado,
# hay que mover el cálculo a un servidor (ver README).
# --------------------------------------------------------------------------
COTIZADOR = {
    # --- Base económica ---
    "valor_jornada": 100000,        # CLP por jornada de trabajo (terreno o gabinete)
    "factor_gg_utilidades": 1.5,    # multiplicador final sobre todos los costos
    "incluye_iva": False,           # False = el valor mostrado es neto

    # --- Rendimiento y economía de escala ---
    "rendimiento_ha_jornada": 60,   # hectáreas por jornada de vuelo en condiciones normales
    "exp_terreno": 0.90,            # <1 = a mayor superficie, menos jornadas por hectárea
    "exp_gabinete": 0.75,           # el procesamiento escala aún menos que el terreno
    "coef_gabinete": 0.90,          # jornadas de gabinete respecto de las de terreno

    # --- Transición entre jornadas (evita saltos bruscos de precio) ---
    # Un excedente pequeño se cubre estirando la jornada: más horas de vuelo, baterías
    # adicionales y cargador portátil en terreno. Se cobra proporcional, con recargo.
    "tolerancia_horas_extra": 0.30,   # hasta un 30% de jornada extra se absorbe estirando el día
    "recargo_horas_extra": 1.40,      # esas horas se cobran 40% más caras
    "jornada_parcial_minima": 0.50,   # si hay que volver otro día, se cobra media jornada como piso
    "ha_por_km_lineal": 10,         # 1 km de faja ≈ 10 ha (ancho de 100 m)
    "superficie_maxima_ha": 5000,   # sobre esto no se cotiza en línea

    # --- Traslado y estadía ---
    "costo_km": 250,                # CLP por km recorrido (combustible + desgaste + peajes)
    "km_sin_alojamiento": 80,       # bajo esta distancia se viaja y vuelve el mismo día
    "jornadas_terreno_por_viaje": 5,  # jornadas de terreno que se cubren en una sola salida
    "costo_noche": 60000,           # alojamiento + alimentación por noche
    "factor_viaje_compartido": 0.5,  # descuento del traslado si se agrupa con otro trabajo
    "km_minimo_compartir": 150,     # desde esta distancia aplica la opción de compartir viaje

    # --- Equipos ---
    "valor_dron": 1500000,          # inversión en el equipo
    "vida_util_jornadas": 250,      # jornadas de vuelo antes de renovar
    "valor_bateria": 180000,        # batería adicional
    "jornadas_por_bateria_extra": 2,  # una batería más por cada N jornadas sobre el kit base
    "jornadas_kit_base": 2,         # jornadas que cubre el kit de baterías actual
    "max_baterias_extra": 6,
    "valor_cargador": 150000,       # cargador portátil / estación de carga en terreno
    # Se suma al equipo cuando el trabajo estira la jornada o dura más de un día.
    # Las baterías que exige un trabajo grande quedan en la empresa y sirven para los
    # siguientes, así que se amortizan igual que el dron. Si prefieres cargar la compra
    # completa al trabajo que la gatilla, pon esto en True (genera saltos de precio).
    "cobrar_baterias_completas": False,

    # --- Presentación ---
    "minimo": 350000,               # valor mínimo de un trabajo
    "redondeo": 10000,              # el precio final se redondea hacia arriba a este múltiplo

    # --- Zonas: (nombre visible, km desde la base, solo ida) ---
    "zonas": [
        ("Santiago y Región Metropolitana", 35),
        ("Rancagua y Región de O'Higgins", 110),
        ("Valparaíso, Viña del Mar y litoral", 130),
        ("Curicó, Talca y Región del Maule", 260),
        ("La Serena y Región de Coquimbo", 470),
        ("Temuco y La Araucanía", 675),
        ("Pucón, Villarrica y Caburgua", 780),
    ],
}

# --------------------------------------------------------------------------
# NAVEGACION
# --------------------------------------------------------------------------
NAV = [
    ("Dron y topografía", "dron-fotogrametria/", [
        ("Nube de puntos y modelo de terreno", "dron-fotogrametria/fotogrametria/"),
        ("Curvas de nivel", "dron-fotogrametria/curvas-de-nivel/"),
        ("Rectificación de deslindes", "dron-fotogrametria/rectificacion-deslindes/"),
        ("Mapas y ortomosaicos", "dron-fotogrametria/mapas-ortomosaicos/"),
        ("Calculadora de cotización", "cotizador/"),
    ]),
    ("Ingeniería hidráulica", "ingenieria-hidraulica/", [
        ("Modelación de redes", "ingenieria-hidraulica/modelacion-redes/"),
        ("Bombas e impulsiones", "ingenieria-hidraulica/dimensionamiento-bombas-impulsiones/"),
        ("Estudios de inundación", "ingenieria-hidraulica/estudios-inundacion/"),
        ("Drenaje pluvial", "ingenieria-hidraulica/drenaje-pluvial/"),
    ]),
    ("Proyecto sanitario", "proyecto-sanitario/", [
        ("Agua potable particular", "proyecto-sanitario/agua-potable-particular/"),
        ("Alcantarillado y fosa séptica", "proyecto-sanitario/alcantarillado-particular/"),
        ("Agua sin fuente propia", "proyecto-sanitario/agua-potable-sin-fuente-propia/"),
        ("Autorización de funcionamiento", "proyecto-sanitario/autorizacion-de-funcionamiento/"),
        ("Aguas grises", "proyecto-sanitario/reutilizacion-aguas-grises/"),
    ]),
    ("Capacidades", "capacidades/", []),
    ("Blog", "blog/", []),
    ("Empresa", "empresa/", []),
]

# Tercera columna del pie de página
PIE_ENLACES = [
    ("Calculadora de cotización", "cotizador/"),
    ("Capacidades", "capacidades/"),
    ("Blog técnico", "blog/"),
    ("Empresa", "empresa/"),
    ("Contacto", "contacto/"),
]


# --------------------------------------------------------------------------
# ICONOS (SVG en linea, trazo con currentColor — sin archivos externos)
# --------------------------------------------------------------------------
ICONOS = {
    "dron": '<circle cx="5.5" cy="5.5" r="2.5"/><circle cx="18.5" cy="5.5" r="2.5"/>'
            '<circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/>'
            '<rect x="9" y="9" width="6" height="6" rx="1.5"/>'
            '<path d="M7.3 7.3 9 9m6 0 1.7-1.7M9 15l-1.7 1.7M15 15l1.7 1.7"/>',
    "curvas": '<path d="M2 8c3.2-4.5 6.4 3 9.6-1.5S18 4 22 6"/><path d="M2 14c3.2-4.5 6.4 3 9.6-1.5S18 10 22 12"/>'
              '<path d="M2 20c3.2-4.5 6.4 3 9.6-1.5S18 16 22 18"/>',
    "deslindes": '<path d="M12 3.5 20.5 8v8L12 20.5 3.5 16V8z"/><circle cx="12" cy="3.5" r="1.4" fill="currentColor" stroke="none"/>'
                 '<circle cx="20.5" cy="8" r="1.4" fill="currentColor" stroke="none"/><circle cx="20.5" cy="16" r="1.4" fill="currentColor" stroke="none"/>'
                 '<circle cx="12" cy="20.5" r="1.4" fill="currentColor" stroke="none"/><circle cx="3.5" cy="16" r="1.4" fill="currentColor" stroke="none"/>'
                 '<circle cx="3.5" cy="8" r="1.4" fill="currentColor" stroke="none"/>',
    "mapa": '<path d="M9 4 3 6.2v14L9 18l6 2 6-2.2v-14L15 6z"/><path d="M9 4v14M15 6v14"/>',
    "red": '<circle cx="5" cy="6" r="2.2"/><circle cx="19" cy="6" r="2.2"/><circle cx="12" cy="18" r="2.2"/>'
           '<path d="M7.2 6h9.6M6.1 8l4.8 8.2M17.9 8l-4.8 8.2"/>',
    "bomba": '<circle cx="13" cy="13" r="5.2"/><path d="M13 7.8V4h5.5"/><path d="M7.8 13H4"/><path d="M13 18.2V21"/>'
             '<path d="M11 11.6l3.6 1.4-3.6 1.4z" fill="currentColor" stroke="none"/>',
    "inundacion": '<path d="M6.5 12.5V8.8L12 4.5l5.5 4.3v3.7"/><path d="M2 16.5c1.7 0 1.7 1.6 3.3 1.6s1.7-1.6 3.4-1.6 1.7 1.6 3.3 1.6 1.7-1.6 3.3-1.6 1.7 1.6 3.4 1.6 1.6-1.6 3.3-1.6"/>'
                  '<path d="M2 20.5c1.7 0 1.7 1.6 3.3 1.6"/>',
    "drenaje": '<path d="M6 2.5v4M12 2v5M18 2.5v4"/><rect x="3" y="10.5" width="18" height="9" rx="2"/>'
               '<path d="M8 10.5v9M12 10.5v9M16 10.5v9"/>',
    "sanitario": '<rect x="2.5" y="6.5" width="4.5" height="6" rx="1.2"/><path d="M7 9.5h6a4 4 0 0 1 4 4v3"/>'
                 '<path d="M17 16.5c1.6 1.8 2.5 3 2.5 4a2.5 2.5 0 0 1-5 0c0-1 .9-2.2 2.5-4z"/>',
    "objetivo": '<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="4"/><circle cx="12" cy="12" r="1" fill="currentColor" stroke="none"/>',
    "reloj": '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
    "capas": '<path d="M12 3.2 21 8l-9 4.8L3 8z"/><path d="M4.5 12 12 16l7.5-4M4.5 16 12 20l7.5-4"/>',
    "archivo": '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5"/><path d="M8.5 13h7M8.5 16.5h4.5"/>',
    "calculo": '<rect x="4" y="3" width="16" height="18" rx="2.5"/><path d="M8 7.5h8M8.5 12h.01M12 12h.01M15.5 12h.01M8.5 16h.01M12 16h.01M15.5 16h.01"/>',
    "pin": '<path d="M12 21.5s7-6 7-11a7 7 0 1 0-14 0c0 5 7 11 7 11z"/><circle cx="12" cy="10.5" r="2.6"/>',
    "chat": '<path d="M20.5 12c0 4.2-3.8 7.5-8.5 7.5-1.2 0-2.4-.2-3.4-.6L3.5 20.5l1.7-4.2A7 7 0 0 1 3.5 12C3.5 7.8 7.3 4.5 12 4.5s8.5 3.3 8.5 7.5z"/>',
    "escudo": '<path d="M12 3 4.5 6v6c0 4.5 3.2 7.8 7.5 9 4.3-1.2 7.5-4.5 7.5-9V6z"/><path d="M9 12l2.2 2.2L15.5 10"/>',
    "rayo": '<path d="M13.5 2 4.5 13.5H11l-.5 8.5 9-11.5H13z"/>',
    "engranaje": '<circle cx="12" cy="12" r="3.2"/><path d="M19.4 14.5a1.6 1.6 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.6 1.6 0 0 0-1.8-.3 1.6 1.6 0 0 0-1 1.5v.2a2 2 0 1 1-4 0v-.1a1.6 1.6 0 0 0-1-1.5 1.6 1.6 0 0 0-1.8.3l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.6 1.6 0 0 0 .3-1.8 1.6 1.6 0 0 0-1.5-1H3a2 2 0 1 1 0-4h.1a1.6 1.6 0 0 0 1.5-1 1.6 1.6 0 0 0-.3-1.8l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1.6 1.6 0 0 0 1.8.3H9a1.6 1.6 0 0 0 1-1.5V3a2 2 0 1 1 4 0v.1a1.6 1.6 0 0 0 1 1.5 1.6 1.6 0 0 0 1.8-.3l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.6 1.6 0 0 0-.3 1.8V9a1.6 1.6 0 0 0 1.5 1h.2a2 2 0 1 1 0 4h-.1a1.6 1.6 0 0 0-1.5 1z"/>',
    "gota": '<path d="M12 3.5c3.5 4 6 6.9 6 9.8A6 6 0 0 1 6 13.3c0-2.9 2.5-5.8 6-9.8z"/>',
    "montana": '<path d="M2.5 19.5 9 7l4 7 2.5-4 6 9.5z"/><circle cx="17.5" cy="5.5" r="2"/>',
    "flecha": '<path d="M4 12h15M13 6l6 6-6 6"/>',
    "check": '<path d="M4.5 12.5 9.5 17.5 19.5 6.5"/>',
    "mail": '<rect x="2.5" y="5" width="19" height="14" rx="2.5"/><path d="M3.5 7l8.5 6 8.5-6"/>',
    "telefono": '<path d="M7 3.5H4.8A1.8 1.8 0 0 0 3 5.4C3 13.5 10.5 21 18.6 21a1.8 1.8 0 0 0 1.9-1.8V17l-4.4-1.6-2 2.2a14 14 0 0 1-5.2-5.2l2.2-2z"/>',
    "reglas": '<rect x="2.5" y="8.5" width="19" height="7" rx="1.8"/><path d="M7 8.5v3M11 8.5v4.5M15 8.5v3M19 8.5v4.5"/>',
}


def icono(nombre, clase="icono"):
    d = ICONOS.get(nombre, ICONOS["check"])
    return (f'<svg class="{clase}" viewBox="0 0 24 24" width="24" height="24" fill="none" '
            f'stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" '
            f'aria-hidden="true" focusable="false">{d}</svg>')


# --------------------------------------------------------------------------
# PATRONES DE FONDO
#   curvas → zona dron (curvas de nivel concéntricas)
#   flujo  → zona hidráulica (líneas de flujo y nodos de red)
# --------------------------------------------------------------------------
def _patron_curvas():
    partes = []
    for cx, cy, n, base_rx, base_ry, paso, giro in (
        (300, 300, 11, 42, 30, 30, -14),
        (980, 210, 8, 34, 24, 28, 22),
    ):
        for i in range(n):
            rx = base_rx + i * paso
            ry = base_ry + i * (paso * 0.72)
            dx = cx + i * 5
            dy = cy + i * 3
            partes.append(f'<ellipse cx="{dx}" cy="{dy}" rx="{rx:.0f}" ry="{ry:.0f}" '
                          f'transform="rotate({giro} {dx} {dy})"/>')
    return ('<svg class="patron__svg" viewBox="0 0 1280 560" preserveAspectRatio="xMidYMid slice" '
            'aria-hidden="true" focusable="false"><g fill="none" stroke="currentColor" stroke-width="1.25">'
            + "".join(partes) + "</g></svg>")


def _patron_flujo():
    lineas = []
    for k in range(9):
        y = 30 + k * 62
        lineas.append(f'<path d="M-60 {y} C 140 {y - 40}, 300 {y + 40}, 480 {y} '
                      f'S 820 {y - 40}, 1000 {y} S 1240 {y + 34}, 1340 {y}"/>')
    nodos = []
    for x, y in ((240, 154), (620, 216), (900, 340), (420, 402), (1080, 92), (760, 464)):
        nodos.append(f'<circle cx="{x}" cy="{y}" r="4.5" fill="currentColor" stroke="none"/>')
        nodos.append(f'<circle cx="{x}" cy="{y}" r="11"/>')
    return ('<svg class="patron__svg" viewBox="0 0 1280 560" preserveAspectRatio="xMidYMid slice" '
            'aria-hidden="true" focusable="false"><g fill="none" stroke="currentColor" stroke-width="1.25">'
            + "".join(lineas) + "".join(nodos) + "</g></svg>")


def patron(tipo):
    svg = _patron_curvas() if tipo == "curvas" else _patron_flujo()
    return f'<div class="patron patron--{tipo}" aria-hidden="true">{svg}</div>'


# --------------------------------------------------------------------------
# COMPONENTES REUTILIZABLES
# --------------------------------------------------------------------------
EXTENSIONES_IMAGEN = (".webp", ".avif", ".jpg", ".jpeg", ".png")


def _dimensiones(ruta):
    """Ancho y alto de un PNG, JPEG o WebP sin librerías externas. None si no se puede leer."""
    try:
        with open(ruta, "rb") as f:
            datos = f.read(32)
            if datos[:8] == b"\x89PNG\r\n\x1a\n":
                w = int.from_bytes(datos[16:20], "big")
                h = int.from_bytes(datos[20:24], "big")
                return (w, h) if w and h else None
            if datos[:2] == b"\xff\xd8":                      # JPEG
                f.seek(2)
                while True:
                    marcador = f.read(2)
                    if len(marcador) < 2 or marcador[0] != 0xFF:
                        return None
                    largo = int.from_bytes(f.read(2), "big")
                    if marcador[1] in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
                                       0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                        f.read(1)
                        h = int.from_bytes(f.read(2), "big")
                        w = int.from_bytes(f.read(2), "big")
                        return (w, h) if w and h else None
                    f.seek(largo - 2, 1)
            if datos[:4] == b"RIFF" and datos[8:12] == b"WEBP":
                tipo, cab = datos[12:16], datos[16:32]
                if tipo == b"VP8X":
                    w = int.from_bytes(cab[8:11], "little") + 1
                    h = int.from_bytes(cab[11:14], "little") + 1
                    return (w, h)
                if tipo == b"VP8 ":
                    w = int.from_bytes(cab[10:12], "little") & 0x3FFF
                    h = int.from_bytes(cab[12:14], "little") & 0x3FFF
                    return (w, h) if w and h else None
                if tipo == b"VP8L":
                    b = int.from_bytes(cab[5:9], "little")
                    return ((b & 0x3FFF) + 1, ((b >> 14) & 0x3FFF) + 1)
    except (OSError, IndexError, ValueError):
        return None
    return None


# Imágenes que alguna página pide pero que todavía no están en assets/img/.
# Se listan al final de `python build.py`.
IMAGENES_FALTANTES = []


def figura(nombre, alt, pie="", ratio="3 / 2", prioritaria=False, estrecha=False, ancha=False):
    """
    Inserta una imagen del portafolio.

    `nombre` es el archivo dentro de assets/img/ SIN extensión (webp, avif, jpg, jpeg
    o png). Si todavía no existe, la página no muestra nada en ese lugar: un visitante
    nunca debe ver un recuadro vacío. Las que faltan se listan al construir el sitio.

    `prioritaria=True` para la imagen principal de una página (se carga sin demora,
    mejora el LCP). `estrecha=True` limita el ancho, para imágenes cuadradas o verticales.
    `ancha=True` dentro de una galería, la imagen ocupa todas las columnas.
    """
    for ext in EXTENSIONES_IMAGEN:
        ruta = os.path.join(OUT, "assets", "img", nombre + ext)
        if os.path.isfile(ruta):
            dim = _dimensiones(ruta)
            medidas = f' width="{dim[0]}" height="{dim[1]}"' if dim else f' style="aspect-ratio: {ratio};"'
            carga = ' fetchpriority="high"' if prioritaria else ' loading="lazy"'
            clase = "figura" + (" figura--estrecha" if estrecha else "") + (" figura--ancha" if ancha else "")
            return (f'<figure class="{clase}">\n'
                    f'  <img src="{{{{P}}}}assets/img/{nombre}{ext}"{medidas}{carga} decoding="async" alt="{alt}">\n'
                    + (f'  <figcaption>{pie}</figcaption>\n' if pie else "")
                    + '</figure>')

    if nombre not in IMAGENES_FALTANTES:
        IMAGENES_FALTANTES.append(nombre)
    return ""


def cta(titulo="Cuéntanos de tu proyecto",
        texto="Te respondemos en menos de 24 horas hábiles con alcance, plazo y valor."):
    return f'''<section class="cta">
  <div class="contenedor cta__caja">
    <div class="cta__texto">
      <h2>{titulo}</h2>
      <p>{texto}</p>
    </div>
    <div class="cta__botones">
      <a class="boton boton--acento" href="{{{{P}}}}contacto/">Solicitar cotización</a>
      <a class="boton boton--claro" href="https://wa.me/{CONFIG['whatsapp']}" rel="nofollow noopener" target="_blank">{icono("chat", "icono icono--sm")} WhatsApp</a>
    </div>
  </div>
</section>'''


def pasos(items):
    lis = "\n".join(
        f'  <li class="pasos__item"><h3>{t}</h3><p>{d}</p></li>' for t, d in items
    )
    return f'<ol class="pasos">\n{lis}\n</ol>'


def datos(items):
    """items: (cifra, etiqueta). Se muestra como una fila de ficha técnica."""
    lis = "\n".join(
        f'  <div class="dato"><span class="dato__cifra">{c}</span><span class="dato__label">{l}</span></div>'
        for c, l in items
    )
    return f'<div class="datos">\n{lis}\n</div>'


def tarjetas(items, clase="tarjetas", nivel=3):
    """items: (título, texto, href_o_None). Lista separada por líneas finas, como un
    índice: el título es el enlace. Los ítems de servicios ocultos se omiten.

    `nivel` es el nivel de encabezado de cada título (3 bajo un h2; 4 cuando la lista
    va dentro de una columna que ya tiene su propio h3)."""
    out = []
    for t, d, h in items:
        if esta_oculto(h):
            continue
        titulo = f'<a href="{{{{P}}}}{h}">{t}</a>' if h else t
        out.append(f'  <li class="tarjeta"><h{nivel}>{titulo}</h{nivel}><p>{d}</p></li>')
    return f'<ul class="{clase}">\n' + "\n".join(out) + "\n</ul>"


def lista(items):
    """items: textos. Lista simple."""
    lis = "\n".join(f"  <li>{t}</li>" for t in items)
    return f'<ul class="lista">\n{lis}\n</ul>'


def faq_html(faqs):
    if not faqs:
        return ""
    items = "\n".join(
        f'''  <details class="faq__item">
    <summary><h3>{q}</h3></summary>
    <div class="faq__respuesta">{a}</div>
  </details>''' for q, a in faqs
    )
    return f'''<section class="seccion" id="faq">
  <div class="contenedor">
    <h2>Preguntas frecuentes</h2>
    <div class="faq">
{items}
    </div>
  </div>
</section>'''


def limpiar(texto):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", texto)).strip()


def acciones_encabezado(servicio, calculadora=True):
    """Botones de contacto directo bajo el título de una página de servicio.

    El WhatsApp lleva el mensaje ya escrito con el nombre del servicio, para que
    la persona no tenga que explicar de qué se trata.
    """
    mensaje = "Hola, me interesa el servicio de %s. ¿Podemos cotizarlo?" % servicio
    from urllib.parse import quote
    wsp = "https://wa.me/%s?text=%s" % (CONFIG["whatsapp"], quote(mensaje))
    segundo = ('<a class="boton boton--claro" href="{{P}}cotizador/">Calcular el valor</a>'
               if calculadora else
               '<a class="boton boton--claro" href="{{P}}contacto/">Escribirnos</a>')
    return (f'<div class="encabezado__acciones">'
            f'<a class="boton boton--acento" href="{wsp}" rel="nofollow noopener" target="_blank">'
            f'{icono("chat", "icono icono--sm")} Consultar por WhatsApp</a>{segundo}</div>')


# --------------------------------------------------------------------------
# PRECIOS DE REFERENCIA
#
# Réplica en Python del mismo modelo que usa la calculadora, para publicar
# valores "desde" en las páginas de servicio sin que puedan quedar desfasados:
# ambos leen los parámetros de COTIZADOR.
#
# IMPORTANTE: si cambias la fórmula del cotizador (el <script> de
# `cotizador_html`), hay que cambiarla también acá. La función
# `verificar_precios()` avisa si las dos versiones dejan de coincidir.
# --------------------------------------------------------------------------
def precio_estimado(ha, km, compartir=False):
    C = COTIZADOR
    base = ha / C["rendimiento_ha_jornada"]
    crudas = base ** C["exp_terreno"]
    enteras = math.floor(crudas)
    resto = crudas - enteras

    if enteras < 1:
        dias_campo, j_terreno, estirada = 1, max(C["jornada_parcial_minima"], crudas), False
    elif resto <= C["tolerancia_horas_extra"]:
        dias_campo = enteras
        j_terreno = enteras + resto * C["recargo_horas_extra"]
        estirada = resto > 0
    else:
        dias_campo = enteras + 1
        j_terreno = enteras + max(C["jornada_parcial_minima"], resto)
        estirada = False

    j_gabinete = max(0.5, C["coef_gabinete"] * base ** C["exp_gabinete"])

    lejos = km > C["km_sin_alojamiento"]
    viajes = math.ceil(dias_campo / C["jornadas_terreno_por_viaje"]) if lejos else dias_campo
    j_traslado = 0 if km <= 80 else (0.5 if km <= 300 else (1 if km <= 600 else 1.5))
    j_traslado *= viajes
    noches = (dias_campo + viajes) if lejos else 0
    vehiculo = viajes * 2 * km * C["costo_km"]
    if compartir:
        vehiculo *= C["factor_viaje_compartido"]
        j_traslado *= C["factor_viaje_compartido"]

    baterias = min(C["max_baterias_extra"],
                   max(0, math.ceil((dias_campo - C["jornadas_kit_base"]) / C["jornadas_por_bateria_extra"])))
    if estirada and baterias == 0:
        baterias = 1
    cargador = C["valor_cargador"] if (estirada or dias_campo > 1) else 0
    equipos = j_terreno * ((C["valor_dron"] + cargador + baterias * C["valor_bateria"]) / C["vida_util_jornadas"])

    costo = ((j_terreno + j_gabinete + j_traslado) * C["valor_jornada"]
             + vehiculo + noches * C["costo_noche"] + equipos)
    total = costo * C["factor_gg_utilidades"]
    return max(C["minimo"], math.ceil(total / C["redondeo"]) * C["redondeo"])


def pesos(valor):
    return "$" + "{:,.0f}".format(valor).replace(",", ".")


_DIAS_ES = {"Monday": "lunes", "Tuesday": "martes", "Wednesday": "miércoles",
            "Thursday": "jueves", "Friday": "viernes", "Saturday": "sábado", "Sunday": "domingo"}
_ORDEN_DIAS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def horario_texto():
    """Traduce CONFIG['horario'] a una frase legible, coherente con el schema
    (openingHoursSpecification lee la misma lista, así que nunca quedan desincronizados)."""
    dias = list(CONFIG["horario"][0])
    if set(dias) == set(_ORDEN_DIAS):
        rango = "Todos los días"
    elif set(dias) == set(_ORDEN_DIAS[:5]):
        rango = "Lunes a viernes"
    elif set(dias) == set(_ORDEN_DIAS[:6]):
        rango = "Lunes a sábado"
    else:
        rango = ", ".join(_DIAS_ES[d].capitalize() for d in dias)
    return f'{rango}, {CONFIG["hora_apertura"]} a {CONFIG["hora_cierre"]}'


# Se repite igual en varios lugares (tabla de precios, "desde $X", calculadora)
# para que quede claro en cualquier punto donde el visitante vea un número.
NOTA_VALOR_CONVERSABLE = ("Estos valores son de referencia: el precio final se conversa según el "
                          "requerimiento exacto, el plazo, la extensión real del terreno y el formato "
                          "de entrega que necesites.")


def tabla_precios():
    """Valores de referencia en la Región Metropolitana, calculados con el modelo real."""
    km_rm = COTIZADOR["zonas"][0][1]
    # El valor mínimo cubre todo lo que se resuelve en una jornada de vuelo, así que
    # sitios urbanos, parcelas y predios chicos quedan en una sola fila.
    filas = [
        ("Sitio urbano, parcela o predio chico", "hasta 60 ha", 60),
        ("Predio mediano", "100 ha", 100),
        ("Fundo", "200 ha", 200),
        ("Fundo grande", "400 ha", 400),
        ("Gran extensión", "800 ha", 800),
    ]
    cuerpo = "\n".join(
        f'      <tr><td>{nombre}</td><td>{detalle}</td><td>{pesos(precio_estimado(ha, km_rm))}</td></tr>'
        for nombre, detalle, ha in filas
    )
    return f'''<div class="tabla-envoltura">
  <table>
    <caption>Valores de referencia en la Región Metropolitana, neto y sin IVA. Fuera de la RM se agrega el traslado.</caption>
    <thead><tr><th scope="col">Tipo de terreno</th><th scope="col">Superficie</th><th scope="col">Valor estimado</th></tr></thead>
    <tbody>
{cuerpo}
    </tbody>
  </table>
</div>
<p class="nota">{NOTA_VALOR_CONVERSABLE}</p>'''


def bloque_precio(ha_referencia=5):
    """Línea 'desde $X' con enlace a la calculadora, para páginas de servicio."""
    desde = precio_estimado(ha_referencia, COTIZADOR["zonas"][0][1])
    return f'''<div class="precio-desde">
  <p class="precio-desde__valor">Desde {pesos(desde)}<span> + IVA</span></p>
  <p class="precio-desde__nota">Referencia para un terreno de hasta 60 hectáreas en la Región
  Metropolitana. En la <a href="{{{{P}}}}cotizador/">calculadora</a> ves el valor de tu terreno según
  superficie y ubicación. El precio final lo conversamos según lo que necesites, el plazo, la extensión
  real y el formato de entrega.</p>
</div>'''


def cotizador_html():
    """Formulario + panel de resultado + lógica. El modelo de costos no se muestra."""
    opciones = "\n".join(
        f'          <option value="{km}">{nombre}</option>' for nombre, km in COTIZADOR["zonas"]
    )
    params = json.dumps({
        "vj": COTIZADOR["valor_jornada"],
        "gg": COTIZADOR["factor_gg_utilidades"],
        "rend": COTIZADOR["rendimiento_ha_jornada"],
        "et": COTIZADOR["exp_terreno"],
        "eg": COTIZADOR["exp_gabinete"],
        "cg": COTIZADOR["coef_gabinete"],
        "hakm": COTIZADOR["ha_por_km_lineal"],
        "haMax": COTIZADOR["superficie_maxima_ha"],
        "ckm": COTIZADOR["costo_km"],
        "kmSinAloj": COTIZADOR["km_sin_alojamiento"],
        "jpv": COTIZADOR["jornadas_terreno_por_viaje"],
        "noche": COTIZADOR["costo_noche"],
        "fcomp": COTIZADOR["factor_viaje_compartido"],
        "kmComp": COTIZADOR["km_minimo_compartir"],
        "dron": COTIZADOR["valor_dron"],
        "vida": COTIZADOR["vida_util_jornadas"],
        "bat": COTIZADOR["valor_bateria"],
        "jbat": COTIZADOR["jornadas_por_bateria_extra"],
        "jkit": COTIZADOR["jornadas_kit_base"],
        "maxBat": COTIZADOR["max_baterias_extra"],
        "batFull": COTIZADOR["cobrar_baterias_completas"],
        "carg": COTIZADOR["valor_cargador"],
        "tolEx": COTIZADOR["tolerancia_horas_extra"],
        "recEx": COTIZADOR["recargo_horas_extra"],
        "jMin": COTIZADOR["jornada_parcial_minima"],
        "min": COTIZADOR["minimo"],
        "red": COTIZADOR["redondeo"],
        "iva": COTIZADOR["incluye_iva"],
    }, ensure_ascii=False)

    return '''<div class="cotizador">
  <form class="cotizador__form" id="cot-form" novalidate>
    <h2 class="cotizador__titulo">Datos del levantamiento</h2>

    <fieldset class="campo">
      <legend>¿Cómo se mide el trabajo?</legend>
      <div class="segmentado">
        <input type="radio" name="tipo" id="tipo-ha" value="ha" checked>
        <label for="tipo-ha">Superficie (ha)</label>
        <input type="radio" name="tipo" id="tipo-km" value="km">
        <label for="tipo-km">Lineal (km)</label>
      </div>
      <p class="campo__ayuda" id="ayuda-tipo">Usa <strong>hectáreas</strong> para predios, loteos y paños.
      Usa <strong>kilómetros</strong> para caminos, canales, líneas y fajas.</p>
    </fieldset>

    <p class="campo">
      <label for="cot-magnitud">Magnitud <span id="cot-unidad">(hectáreas)</span></label>
      <input type="number" id="cot-magnitud" name="magnitud" min="0.1" step="0.1" inputmode="decimal"
             placeholder="Ej: 25" required>
    </p>

    <p class="campo">
      <label for="cot-zona">Ubicación del terreno</label>
      <select id="cot-zona" name="zona">
''' + opciones + '''
        <option value="otra">Otra zona (indicar distancia)</option>
      </select>
    </p>

    <p class="campo campo--oculto" id="campo-km">
      <label for="cot-km">Distancia desde Santiago (km, solo ida)</label>
      <input type="number" id="cot-km" name="km" min="0" step="10" inputmode="numeric" placeholder="Ej: 320">
    </p>

    <p class="campo">
      <label for="cot-comuna">Comuna o sector <span class="campo__opcional">(opcional)</span></label>
      <input type="text" id="cot-comuna" name="comuna" placeholder="Ej: Pirque, Fundo Los Maitenes">
    </p>

    <p class="campo campo--check campo--oculto" id="campo-compartir">
      <input type="checkbox" id="cot-compartir" name="compartir">
      <label for="cot-compartir">Puedo esperar a que el viaje se coordine con otro trabajo en la zona
      <span class="campo__ayuda">Reduce el costo del traslado. Puede significar algunas semanas de espera.</span></label>
    </p>

    <button class="boton boton--acento boton--ancho" type="submit">Calcular valor estimado</button>
    <p class="cotizador__legal">Valor referencial calculado con los mismos criterios que usamos para
    cotizar. La propuesta formal se confirma tras revisar el terreno, y el valor se puede conversar según
    el plazo, la extensión exacta y el formato de entrega que necesites.</p>
  </form>

  <div class="cotizador__resultado" id="cot-resultado" aria-live="polite">
    <div class="resultado resultado--vacio" id="cot-vacio">
      ''' + icono("calculo", "icono icono--grande") + '''
      <p>Completa los datos y presiona <strong>Calcular</strong> para ver el valor estimado de tu
      levantamiento.</p>
    </div>

    <div class="resultado resultado--valor" id="cot-valor" hidden>
      <p class="resultado__etiqueta">Valor estimado</p>
      <p class="resultado__cifra" id="cot-precio">—</p>
      <p class="resultado__nota" id="cot-nota"></p>
      <p class="resultado__conversable">El valor final se puede conversar según el requerimiento, el
      plazo, la extensión real del terreno y el tipo de archivo de entrega.</p>
      <div class="resultado__incluye">
        <p class="resultado__subtitulo">Incluye</p>
        <ul class="lista-check">
          <li>Planificación del vuelo y gestión de la operación aérea.</li>
          <li>Terreno completo: vuelo, puntos de control y registro del sitio.</li>
          <li>Procesamiento fotogramétrico y control de calidad.</li>
          <li>Ortomosaico, modelo digital de terreno y curvas de nivel.</li>
          <li>Entrega en formatos editables (DWG, DXF, GeoTIFF, LAS) e informe técnico.</li>
          <li>Traslados, equipos y todos los costos de operación.</li>
        </ul>
      </div>
      <div class="resultado__acciones">
        <a class="boton boton--acento" id="cot-wsp" href="#" rel="nofollow noopener" target="_blank">
          ''' + icono("chat", "icono icono--sm") + ''' Confirmar por WhatsApp</a>
        <a class="boton boton--claro" href="{{P}}contacto/">Enviar por formulario</a>
      </div>
    </div>

    <div class="resultado resultado--aviso" id="cot-aviso" hidden>
      ''' + icono("escudo", "icono icono--grande") + '''
      <p id="cot-aviso-texto"></p>
      <a class="boton boton--acento" href="{{P}}contacto/">Escribirnos</a>
    </div>
  </div>
</div>

<script>
(function () {
  var C = ''' + params + ''';
  var WSP = "https://wa.me/''' + CONFIG["whatsapp"] + '''";
  var f = document.getElementById("cot-form");
  if (!f) return;

  var elZona = document.getElementById("cot-zona");
  var campoKm = document.getElementById("campo-km");
  var campoComp = document.getElementById("campo-compartir");
  var elUnidad = document.getElementById("cot-unidad");
  var elMag = document.getElementById("cot-magnitud");
  var vacio = document.getElementById("cot-vacio");
  var panel = document.getElementById("cot-valor");
  var aviso = document.getElementById("cot-aviso");

  var money = new Intl.NumberFormat("es-CL", { style: "currency", currency: "CLP", maximumFractionDigits: 0 });

  function distancia() {
    return elZona.value === "otra"
      ? (parseFloat(document.getElementById("cot-km").value) || 0)
      : parseFloat(elZona.value);
  }

  function sincronizar() {
    var otra = elZona.value === "otra";
    campoKm.classList.toggle("campo--oculto", !otra);
    campoComp.classList.toggle("campo--oculto", distancia() < C.kmComp);
  }

  elZona.addEventListener("change", sincronizar);
  document.getElementById("cot-km").addEventListener("input", sincronizar);

  Array.prototype.forEach.call(f.tipo, function (r) {
    r.addEventListener("change", function () {
      var ha = f.tipo.value === "ha";
      elUnidad.textContent = ha ? "(hectáreas)" : "(kilómetros)";
      elMag.placeholder = ha ? "Ej: 25" : "Ej: 6";
    });
  });

  function mostrar(cual, texto) {
    vacio.hidden = cual !== "vacio";
    panel.hidden = cual !== "valor";
    aviso.hidden = cual !== "aviso";
    if (cual === "aviso") document.getElementById("cot-aviso-texto").textContent = texto;
  }

  f.addEventListener("submit", function (e) {
    e.preventDefault();

    var magnitud = parseFloat(elMag.value);
    if (!(magnitud > 0)) {
      mostrar("aviso", "Ingresa la superficie en hectáreas o la longitud en kilómetros del terreno a levantar.");
      elMag.focus();
      return;
    }

    var esLineal = f.tipo.value === "km";
    var ha = esLineal ? magnitud * C.hakm : magnitud;

    if (ha > C.haMax) {
      mostrar("aviso", "Es un proyecto de gran envergadura y merece una propuesta hecha a medida. Escríbenos y lo revisamos contigo.");
      return;
    }

    var km = distancia();
    var compartir = document.getElementById("cot-compartir").checked && km >= C.kmComp;

    // --- jornadas (economía de escala: exponentes menores a 1) ---
    var base = ha / C.rend;
    var crudas = Math.pow(base, C.et);
    var enteras = Math.floor(crudas);
    var resto = crudas - enteras;
    var jTerreno, diasCampo, estirada;

    if (enteras < 1) {                       // trabajo que cabe en un día
      diasCampo = 1;
      jTerreno = Math.max(C.jMin, crudas);
      estirada = false;
    } else if (resto <= C.tolEx) {           // el excedente se cubre con horas extra
      diasCampo = enteras;
      jTerreno = enteras + resto * C.recEx;
      estirada = resto > 0;
    } else {                                 // hay que volver otro día, cobrado a prorrata
      diasCampo = enteras + 1;
      jTerreno = enteras + Math.max(C.jMin, resto);
      estirada = false;
    }

    var jGabinete = Math.max(0.5, C.cg * Math.pow(base, C.eg));

    // --- viajes, traslado y estadía ---
    var lejos = km > C.kmSinAloj;
    var viajes = lejos ? Math.ceil(diasCampo / C.jpv) : diasCampo;
    var jTraslado = km <= 80 ? 0 : (km <= 300 ? 0.5 : (km <= 600 ? 1 : 1.5));
    jTraslado = jTraslado * viajes;
    var noches = lejos ? (diasCampo + viajes) : 0;
    var vehiculo = viajes * 2 * km * C.ckm;
    if (compartir) { vehiculo *= C.fcomp; jTraslado *= C.fcomp; }

    // --- equipos ---
    var baterias = Math.min(C.maxBat, Math.max(0, Math.ceil((diasCampo - C.jkit) / C.jbat)));
    if (estirada && baterias === 0) baterias = 1;   // estirar el día exige una batería más
    var cargador = (estirada || diasCampo > 1) ? C.carg : 0;
    var equipos = C.batFull
      ? jTerreno * ((C.dron + cargador) / C.vida) + baterias * C.bat
      : jTerreno * ((C.dron + cargador + baterias * C.bat) / C.vida);

    // --- total ---
    var costo = (jTerreno + jGabinete + jTraslado) * C.vj
              + vehiculo + noches * C.noche + equipos;
    var total = costo * C.gg;
    total = Math.max(C.min, Math.ceil(total / C.red) * C.red);

    document.getElementById("cot-precio").textContent = money.format(total);
    document.getElementById("cot-nota").textContent =
      "Valor " + (C.iva ? "con IVA incluido" : "neto, no incluye IVA") +
      " · Estimación referencial válida por 30 días" +
      (compartir ? " · Sujeto a coordinación con otro viaje a la zona" : "");

    var comuna = document.getElementById("cot-comuna").value.trim();
    var zonaTxt = elZona.options[elZona.selectedIndex].text;
    var msg = "Hola, calculé una cotización en el sitio.\\n\\n" +
      (esLineal ? "Longitud: " + magnitud + " km" : "Superficie: " + magnitud + " ha") + "\\n" +
      "Zona: " + zonaTxt + (comuna ? " (" + comuna + ")" : "") + "\\n" +
      "Valor estimado: " + money.format(total) + "\\n\\n" +
      "Quisiera confirmar el alcance.";
    document.getElementById("cot-wsp").href = WSP + "?text=" + encodeURIComponent(msg);

    mostrar("valor");
    document.getElementById("cot-resultado").scrollIntoView({ behavior: "smooth", block: "nearest" });
  });

  sincronizar();
})();
</script>'''


# --------------------------------------------------------------------------
# SCHEMA / JSON-LD
# --------------------------------------------------------------------------
def imagen_og():
    """Usa una imagen social real (JPG/PNG/WebP) si existe; si no, el SVG de respaldo."""
    for nombre in ("og-portada.jpg", "og-portada.jpeg", "og-portada.png", "og-portada.webp"):
        ruta = os.path.join(OUT, "assets", "img", nombre)
        if os.path.isfile(ruta):
            return "assets/img/" + nombre, (_dimensiones(ruta) or (1200, 630))
    return CONFIG["og_image"], (1200, 630)


def schema_negocio():
    negocio = {
        "@context": "https://schema.org",
        "@type": "ProfessionalService",
        "@id": CONFIG["dominio"] + "/#negocio",
        "name": CONFIG["marca"],
        "alternateName": CONFIG["marca"] + " " + CONFIG["descriptor"],
        "legalName": CONFIG["marca_legal"],
        "url": CONFIG["dominio"] + "/",
        "telephone": CONFIG["telefono_display"],
        "email": CONFIG["email"],
        "image": CONFIG["dominio"] + "/" + CONFIG["og_image"],
        "logo": CONFIG["dominio"] + "/assets/img/favicon.svg",
        "description": ("RCKT: fotogrametría y topografía con dron e ingeniería hidráulica. Curvas de nivel, "
                        "deslindes, ortomosaicos, modelación de redes de agua potable, drenaje pluvial y "
                        "estudios de inundación en Chile."),
        "areaServed": [{"@type": "AdministrativeArea", "name": z} for z in ZONAS_SERVICIO],
        "address": {
            "@type": "PostalAddress",
            "addressLocality": CONFIG["ciudad_base"],
            "addressRegion": CONFIG["region_base"],
            "addressCountry": CONFIG["pais"],
        },
        "knowsAbout": ["Fotogrametría con dron", "Topografía", "Curvas de nivel", "Ortomosaicos",
                       "Modelación hidráulica", "EPANET", "SWMM", "HEC-RAS", "Drenaje pluvial",
                       "Agua potable", "Alcantarillado", "Resolución sanitaria", "Fosa séptica",
                       "Agua potable rural", "Aguas grises"],
        "priceRange": "$$",
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": CONFIG["lat"],
            "longitude": CONFIG["lon"],
        },
        "openingHoursSpecification": [{
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": list(CONFIG["horario"][0]),
            "opens": CONFIG["hora_apertura"],
            "closes": CONFIG["hora_cierre"],
        }],
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Servicios",
            "itemListElement": [
                {"@type": "Offer", "itemOffered": {"@type": "Service", "name": t,
                 "url": CONFIG["dominio"] + "/" + h}}
                for t, h in (NAV[0][2] + NAV[1][2] + NAV[2][2]) if not esta_oculto(h)
            ],
        },
    }
    if CONFIG["redes"]:
        negocio["sameAs"] = CONFIG["redes"]
    return negocio


def schema_zona(nombre, descripcion, comunas):
    """Servicio acotado a una zona: refuerza el posicionamiento local de esa página."""
    return {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": nombre,
        "description": descripcion,
        "serviceType": "Levantamiento topográfico con dron e ingeniería hidráulica",
        "provider": {"@type": "ProfessionalService", "@id": CONFIG["dominio"] + "/#negocio",
                     "name": CONFIG["marca"]},
        "areaServed": [{"@type": "City", "name": c} for c in comunas],
        "availableChannel": {"@type": "ServiceChannel", "serviceUrl": CONFIG["dominio"] + "/contacto/"},
    }


def schema_servicio(nombre, descripcion, tipo):
    return {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": nombre,
        "serviceType": tipo,
        "description": descripcion,
        "provider": {"@type": "ProfessionalService", "@id": CONFIG["dominio"] + "/#negocio",
                     "name": CONFIG["marca"]},
        "areaServed": [{"@type": "AdministrativeArea", "name": z} for z in ZONAS_SERVICIO],
        "availableChannel": {"@type": "ServiceChannel", "serviceUrl": CONFIG["dominio"] + "/contacto/"},
    }


def schema_articulo(titular, fecha, descripcion, ruta):
    return {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": titular,
        "description": descripcion,
        "datePublished": fecha,
        "dateModified": fecha,
        "inLanguage": "es-CL",
        "mainEntityOfPage": {"@type": "WebPage", "@id": CONFIG["dominio"] + "/" + ruta + "/"},
        "image": CONFIG["dominio"] + "/" + CONFIG["og_image"],
        "author": {"@type": "Organization", "name": CONFIG["marca"]},
        "publisher": {"@type": "ProfessionalService", "@id": CONFIG["dominio"] + "/#negocio",
                      "name": CONFIG["marca"]},
    }


def schema_breadcrumb(crumbs, ruta):
    elementos = [{"@type": "ListItem", "position": 1, "name": "Inicio", "item": CONFIG["dominio"] + "/"}]
    for i, (nombre, href) in enumerate(crumbs, start=2):
        item = {"@type": "ListItem", "position": i, "name": nombre}
        item["item"] = (CONFIG["dominio"] + "/" + href) if href else \
                       (CONFIG["dominio"] + "/" + ruta + ("/" if ruta else ""))
        elementos.append(item)
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": elementos}


def schema_faq(faqs):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": limpiar(a)}} for q, a in faqs],
    }


# --------------------------------------------------------------------------
# PLANTILLA HTML
# --------------------------------------------------------------------------
def render_nav(P, activa):
    items = []
    for titulo, href, hijos in NAV:
        if esta_oculto(href):
            continue
        hijos = [(t, h) for t, h in hijos if not esta_oculto(h)]
        aria = ' aria-current="page"' if activa and activa.startswith(href) else ""
        if hijos:
            sub = "\n".join(f'        <li><a href="{P}{h}">{t}</a></li>' for t, h in hijos)
            items.append(f'''    <li class="nav__item nav__item--sub">
      <a href="{P}{href}"{aria}>{titulo}</a>
      <ul class="nav__sub">
{sub}
      </ul>
    </li>''')
        else:
            items.append(f'    <li class="nav__item"><a href="{P}{href}"{aria}>{titulo}</a></li>')
    return "\n".join(items)


def render_footer(P):
    def columna(hijos):
        return "\n".join(f'<li><a href="{P}{h}">{t}</a></li>'
                         for t, h in hijos if not esta_oculto(h))

    dron = columna(NAV[0][2]) if not esta_oculto(NAV[0][1]) else ""
    hidro = columna(NAV[1][2]) if not esta_oculto(NAV[1][1]) else ""
    sanitario = columna(NAV[2][2]) if not esta_oculto(NAV[2][1]) else ""
    zonas = columna(PIE_ENLACES)
    return f'''<footer class="pie">
  <div class="contenedor pie__grid">
    <div class="pie__col">
      <p class="pie__marca">{CONFIG["marca"]}</p>
      <p class="pie__descriptor">{CONFIG["descriptor"]}</p>
      <p class="pie__texto">Trabajamos con base en {CONFIG["ciudad_base"]}, con cobertura desde la
      Región de Coquimbo hasta La Araucanía.</p>
      <ul class="pie__contacto">
        <li>{icono("telefono", "icono icono--sm")}<a href="tel:{CONFIG['telefono_link']}">{CONFIG["telefono_display"]}</a></li>
        <li>{icono("mail", "icono icono--sm")}<a href="mailto:{CONFIG['email']}">{CONFIG["email"]}</a></li>
      </ul>
    </div>
    <div class="pie__col">
      <p class="pie__titulo">Dron y topografía</p>
      <ul>{dron}</ul>
    </div>
    <div class="pie__col">
      <p class="pie__titulo">Ingeniería hidráulica</p>
      <ul>{hidro}</ul>
    </div>
    <div class="pie__col">
      <p class="pie__titulo">Proyecto sanitario</p>
      <ul>{sanitario}</ul>
    </div>
    <div class="pie__col">
      <p class="pie__titulo">Más</p>
      <ul>{zonas}</ul>
    </div>
  </div>
  <div class="contenedor pie__legal">
    <p>© {CONFIG["anio"]} {CONFIG["marca"]}. Todos los derechos reservados.</p>
    <p><a href="{P}dron-fotogrametria/">Dron y topografía</a> · <a href="{P}ingenieria-hidraulica/">Ingeniería hidráulica</a> · <a href="{P}proyecto-sanitario/">Proyecto sanitario</a> · <a href="{P}contacto/">Contacto</a></p>
  </div>
</footer>'''


def render_breadcrumbs(P, crumbs):
    if not crumbs:
        return ""
    partes = [f'<li><a href="{P}">Inicio</a></li>']
    for nombre, href in crumbs:
        partes.append(f'<li><a href="{P}{href}">{nombre}</a></li>' if href
                      else f'<li aria-current="page">{nombre}</li>')
    return ('<nav class="migas" aria-label="Ruta de navegación"><div class="contenedor"><ol>'
            + "".join(partes) + "</ol></div></nav>")


LOGO_SVG = '''<svg class="logo__marca" viewBox="0 0 36 36" width="34" height="34" aria-hidden="true" focusable="false">
        <rect width="36" height="36" rx="9" fill="currentColor" opacity=".1"/>
        <path d="M18 7.5 24 20h-12z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>
        <circle cx="18" cy="15.5" r="1.7" fill="currentColor"/>
        <path d="M8 26c3.6-4.6 6.4 2.2 10-1.4S22.6 25 28 21.6" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round"/>
      </svg>'''

PLANTILLA = """<!DOCTYPE html>
<html lang="es-CL">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="#05090d">
<meta property="og:type" content="{og_type}">
<meta property="og:locale" content="es_CL">
<meta property="og:site_name" content="{marca}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_image}">
<meta property="og:image:width" content="{og_ancho}">
<meta property="og:image:height" content="{og_alto}">
<meta property="og:image:alt" content="{marca} — topografía con dron e ingeniería hidráulica">
<meta name="twitter:card" content="summary_large_image">
{seo_extra}
<link rel="icon" href="{P}assets/img/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{P}assets/css/estilos.css?v={css_v}">
{extra_head}
{jsonld}
</head>
<body>
<a class="saltar" href="#contenido">Saltar al contenido</a>

<header class="cabecera">
  <div class="contenedor cabecera__barra">
    <a class="logo" href="{P}">
      {logo}
      <span class="logo__texto"><strong>{marca}</strong><span>{descriptor}</span></span>
    </a>
    <button class="menu-boton" type="button" aria-expanded="false" aria-controls="nav-principal">
      <span class="menu-boton__barras" aria-hidden="true"></span>
      <span class="menu-boton__texto">Menú</span>
    </button>
    <nav id="nav-principal" class="nav" aria-label="Navegación principal">
      <ul class="nav__lista">
{nav}
        <li class="nav__item nav__item--cta"><a class="boton boton--acento boton--sm" href="{P}contacto/">Contacto</a></li>
      </ul>
    </nav>
  </div>
</header>
{migas}
<main id="contenido">
{body}
</main>
{footer}
{analitica}
<script>
(function () {{
  var b = document.querySelector('.menu-boton');
  var n = document.getElementById('nav-principal');
  if (!b || !n) return;
  b.addEventListener('click', function () {{
    var abierto = n.classList.toggle('nav--abierto');
    b.setAttribute('aria-expanded', abierto ? 'true' : 'false');
  }});
}})();
</script>
</body>
</html>
"""


def seo_extra(p):
    """Verificación de Search Console y metadatos de artículo."""
    partes = []
    if CONFIG["gsc_verificacion"]:
        partes.append(f'<meta name="google-site-verification" content="{CONFIG["gsc_verificacion"]}">')
    if p.get("schema_articulo"):
        fecha = p["schema_articulo"][1]
        partes.append(f'<meta property="article:published_time" content="{fecha}">')
        partes.append(f'<meta property="article:modified_time" content="{fecha}">')
        partes.append(f'<meta property="article:author" content="{CONFIG["marca"]}">')
    return "\n".join(partes)


def analitica():
    """Google Analytics 4, solo si hay identificador configurado."""
    if not CONFIG["ga4_id"]:
        return ""
    gid = CONFIG["ga4_id"]
    return (f'<script async src="https://www.googletagmanager.com/gtag/js?id={gid}"></script>\n'
            "<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}"
            f"gtag('js',new Date());gtag('config','{gid}');</script>")


def version_css():
    """Huella del CSS: fuerza a los navegadores a recargar la hoja al cambiarla."""
    return hashlib.md5(CSS.encode("utf-8")).hexdigest()[:8]


def escribir(ruta, contenido):
    destino = os.path.join(OUT, ruta)
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    with open(destino, "w", encoding="utf-8") as f:
        f.write(contenido)


def construir_pagina(p):
    ruta = p["path"].strip("/")
    profundidad = len([x for x in ruta.split("/") if x])
    P = "../" * profundidad if profundidad else ""
    canonical = CONFIG["dominio"] + "/" + (ruta + "/" if ruta else "")

    esquemas = []
    if not ruta:
        esquemas.append(schema_negocio())
    if p.get("schema_servicio"):
        esquemas.append(schema_servicio(*p["schema_servicio"]))
    if p.get("schema_articulo"):
        esquemas.append(schema_articulo(*p["schema_articulo"], ruta=ruta))
    if p.get("schema_zona"):
        esquemas.append(schema_zona(*p["schema_zona"]))
    if p.get("crumbs"):
        esquemas.append(schema_breadcrumb(p["crumbs"], ruta))
    if p.get("faq"):
        esquemas.append(schema_faq(p["faq"]))

    jsonld = "\n".join('<script type="application/ld+json">' + json.dumps(e, ensure_ascii=False) + "</script>"
                       for e in esquemas)

    body = p["body"] + faq_html(p.get("faq", [])) + (p.get("cierre") or cta())

    og_ruta, og_dim = imagen_og()
    html = PLANTILLA.format(
        title=p["title"], desc=p["desc"], canonical=canonical,
        robots=p.get("robots", "index, follow"),
        og_type="article" if (ruta.startswith("blog/") and profundidad > 1) else "website",
        og_image=CONFIG["dominio"] + "/" + og_ruta,
        og_ancho=og_dim[0], og_alto=og_dim[1],
        marca=CONFIG["marca"], descriptor=CONFIG["descriptor"], logo=LOGO_SVG,
        P=P, nav=render_nav(P, p.get("nav_activa")),
        migas=render_breadcrumbs(P, p.get("crumbs", [])),
        body=body, footer=render_footer(P), jsonld=jsonld,
        extra_head=p.get("extra_head", ""), css_v=version_css(),
        seo_extra=seo_extra(p), analitica=analitica(),
    )
    html = desactivar_enlaces(html.replace("{{P}}", P))
    salida = (ruta + "/index.html") if ruta else "index.html"
    escribir(salida, html)
    return ruta


# --------------------------------------------------------------------------
# HOJA DE ESTILOS
# --------------------------------------------------------------------------
CSS = """/* ==========================================================================
   RCKT — hoja de estilos.
   Sin dependencias externas: todo carga desde el propio dominio, lo que ayuda
   directamente a los Core Web Vitals (LCP e INP).
   ========================================================================== */

:root {
  /* Base oscura */
  --tinta-950: #05090d;
  --tinta-900: #0a1118;
  --tinta-800: #111c26;
  --tinta-700: #1b2b38;

  /* Neutros claros */
  --papel:     #ffffff;
  --papel-2:   #f5f7f9;
  --linea:     #e3e9ee;
  --linea-2:   #d3dce4;

  /* Texto */
  --texto:     #0d151c;
  --suave:     #5b6b78;
  --suave-osc: rgba(255, 255, 255, .66);

  /* Acento */
  --acento:      #17c3d4;   /* sobre fondo oscuro */
  --acento-txt:  #0c7c89;   /* sobre fondo claro (contraste AA) */
  --acento-sombra: rgba(23, 195, 212, .16);

  --radio: 6px;
  --radio-sm: 4px;
  --ancho: 1160px;
  --fuente: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  /* Rótulos técnicos (pies de figura, cifras): como en un plano */
  --mono: ui-monospace, "Cascadia Mono", "SF Mono", Consolas, "Liberation Mono", monospace;
}

*, *::before, *::after { box-sizing: border-box; }
/* Un elemento con el atributo hidden no se muestra aunque su clase le dé display:flex */
[hidden] { display: none !important; }
html { -webkit-text-size-adjust: 100%; scroll-behavior: smooth; }

body {
  margin: 0;
  font-family: var(--fuente);
  font-size: 17px;
  line-height: 1.62;
  color: var(--texto);
  background: var(--papel);
  -webkit-font-smoothing: antialiased;
}

img, svg, video { max-width: 100%; height: auto; }

h1, h2, h3, h4 { line-height: 1.15; margin: 0 0 .6em; font-weight: 650; letter-spacing: -.02em; }
h1 { font-size: clamp(2rem, 1.4rem + 2.4vw, 3rem); }
h2 { font-size: clamp(1.4rem, 1.15rem + 1.1vw, 1.85rem); }
h3 { font-size: 1.1rem; letter-spacing: -.01em; }
h4 { font-size: 1.02rem; letter-spacing: -.005em; }
p  { margin: 0 0 1.1em; }

a { color: var(--acento-txt); text-decoration-thickness: 1px; text-underline-offset: 2px; }
a:hover { color: var(--tinta-800); }

.contenedor { width: 100%; max-width: var(--ancho); margin: 0 auto; padding: 0 22px; }

.saltar { position: absolute; left: -9999px; top: 0; z-index: 100;
  background: var(--tinta-950); color: #fff; padding: 12px 18px; border-radius: 0 0 var(--radio-sm) 0; }
.saltar:focus { left: 0; }
:focus-visible { outline: 2.5px solid var(--acento); outline-offset: 2px; }

/* ---------- Iconos ---------- */
.icono { width: 24px; height: 24px; flex: none; }
.icono--sm { width: 18px; height: 18px; }
.icono--grande { width: 34px; height: 34px; opacity: .5; }

/* ---------- Cabecera ---------- */
.cabecera {
  position: sticky; top: 0; z-index: 50;
  background: var(--tinta-950);
  border-bottom: 1px solid rgba(255, 255, 255, .08);
  color: #fff;
}
.cabecera__barra { display: flex; align-items: center; gap: 16px; min-height: 70px; }

.logo { display: inline-flex; align-items: center; gap: 11px; color: #fff; text-decoration: none; }
.logo__marca { color: var(--acento); flex: none; }
.logo__texto { display: flex; flex-direction: column; line-height: 1.1; }
.logo__texto strong { font-size: 1.22rem; font-weight: 720; letter-spacing: .06em; }
.logo__texto span { font-size: .68rem; letter-spacing: .13em; text-transform: uppercase; color: rgba(255,255,255,.55); }

.menu-boton {
  margin-left: auto; display: inline-flex; align-items: center; gap: 9px;
  background: rgba(255,255,255,.07); border: 1px solid rgba(255,255,255,.14); color: #fff;
  border-radius: var(--radio-sm); padding: 10px 15px; font: inherit; font-size: .93rem; font-weight: 600;
  cursor: pointer; min-height: 44px;
}
.menu-boton__barras { width: 17px; height: 1.8px; background: currentColor; box-shadow: 0 -5.5px 0 currentColor, 0 5.5px 0 currentColor; display: block; }

.nav { display: none; width: 100%; }
.nav--abierto { display: block; }
.nav__lista { list-style: none; margin: 0 0 16px; padding: 0; }
.nav__item > a:not(.boton) {
  display: block; padding: 13px 4px; color: #fff; text-decoration: none; font-weight: 600; font-size: .97rem;
  border-bottom: 1px solid rgba(255,255,255,.09);
}
.nav__item > a[aria-current] { color: var(--acento); }
.nav__sub { list-style: none; margin: 0; padding: 4px 0 10px 14px; }
.nav__sub a { display: block; padding: 9px 4px; color: rgba(255,255,255,.62); text-decoration: none; font-size: .92rem; }
.nav__sub a:hover { color: var(--acento); }
.nav__item--cta { margin-top: 14px; }
.nav__item--cta a { display: inline-flex; }

@media (min-width: 1060px) {
  .menu-boton { display: none; }
  .nav { display: block; width: auto; margin-left: auto; }
  .nav__lista { display: flex; align-items: center; gap: 2px; margin: 0; }
  .nav__item { position: relative; }
  .nav__item > a:not(.boton) { border: 0; padding: 10px 13px; border-radius: var(--radio-sm); font-size: .93rem; }
  .nav__item > a:not(.boton):hover { background: rgba(255,255,255,.08); }
  .nav__sub {
    position: absolute; top: 100%; left: 0; min-width: 258px;
    background: var(--tinta-900); border: 1px solid rgba(255,255,255,.1); border-radius: var(--radio);
    box-shadow: 0 18px 40px rgba(0,0,0,.4); padding: 8px; opacity: 0; visibility: hidden;
    transform: translateY(6px); transition: opacity .14s ease, transform .14s ease;
  }
  .nav__item--sub:hover .nav__sub, .nav__item--sub:focus-within .nav__sub { opacity: 1; visibility: visible; transform: translateY(0); }
  .nav__sub a { padding: 9px 12px; border-radius: 8px; }
  .nav__sub a:hover { background: rgba(255,255,255,.07); }
  .nav__item--cta { margin: 0 0 0 10px; }
}

/* ---------- Botones ---------- */
.boton {
  display: inline-flex; align-items: center; justify-content: center; gap: 8px;
  min-height: 46px; padding: 11px 20px; border-radius: var(--radio-sm);
  font-weight: 600; font-size: .96rem; text-decoration: none; border: 1px solid transparent;
  transition: background .15s ease, color .15s ease, border-color .15s ease;
}
.boton--sm { min-height: 38px; padding: 7px 15px; font-size: .9rem; }
.boton--ancho { width: 100%; }
/* Principal: tinta sobre fondo claro; blanco sobre fondo oscuro */
.boton--acento { background: var(--tinta-950); color: #fff; }
.boton--acento:hover { background: var(--tinta-700); color: #fff; }
.cabecera .boton--acento, .hero .boton--acento, .resultado--valor .boton--acento { background: #fff; color: var(--tinta-950); }
.cabecera .boton--acento:hover, .hero .boton--acento:hover, .resultado--valor .boton--acento:hover { background: #dfe7ec; color: var(--tinta-950); }
.boton--claro { background: #fff; color: var(--tinta-900); border-color: var(--linea-2); }
.boton--claro:hover { border-color: var(--tinta-900); color: var(--tinta-900); }
.boton--fantasma { background: transparent; color: #fff; border-color: rgba(255,255,255,.34); }
.boton--fantasma:hover { border-color: #fff; color: #fff; }
.boton--oscuro { background: var(--tinta-900); color: #fff; }
.boton--oscuro:hover { background: var(--tinta-800); color: #fff; }

/* ---------- Migas ---------- */
.migas { background: var(--papel-2); font-size: .85rem; }
.migas ol { list-style: none; display: flex; flex-wrap: wrap; gap: 6px; margin: 0; padding: 18px 0 0; }
.migas li + li::before { content: "/"; margin-right: 6px; color: var(--linea-2); }
.migas a { color: var(--suave); text-decoration: none; }
.migas a:hover { color: var(--acento-txt); }
.migas [aria-current] { color: var(--texto); }

/* ---------- Patrones de fondo ---------- */
.patron { position: absolute; inset: 0; overflow: hidden; pointer-events: none; }
.patron__svg { width: 100%; height: 100%; display: block; }
/* Solo en las cabeceras de páginas internas, en tinta y muy tenue */
.patron--curvas, .patron--flujo { color: var(--tinta-950); opacity: .07; }
/* El patrón se desvanece hacia la izquierda para que nunca quede detrás del texto */
.patron__svg { mask-image: linear-gradient(to right, transparent 25%, #000 85%);
  -webkit-mask-image: linear-gradient(to right, transparent 25%, #000 85%); }

/* ---------- Hero (portada) ---------- */
.hero { background: var(--tinta-950); color: #fff; }
.hero__grilla { display: grid; gap: 34px; grid-template-columns: 1fr; padding-top: 56px; padding-bottom: 60px; align-items: center; }
@media (min-width: 980px) { .hero__grilla { grid-template-columns: 1fr 1.08fr; gap: 56px; padding-top: 72px; padding-bottom: 76px; } }
.hero h1 { color: #fff; margin-bottom: .45em; max-width: 16ch; }
.hero__bajada { font-size: 1.08rem; color: rgba(255,255,255,.74); max-width: 52ch; }
.hero__acciones { display: flex; flex-wrap: wrap; gap: 12px; margin: 28px 0 22px; }
.hero__nota { font-size: .88rem; color: rgba(255,255,255,.5); margin: 0; }
.hero .figura { margin: 0; }
.hero .figura img { border-radius: var(--radio-sm); }
.hero .figura figcaption { color: rgba(255,255,255,.52); }

/* ---------- Encabezado de páginas internas ---------- */
.encabezado { position: relative; background: var(--papel-2); border-bottom: 1px solid var(--linea); overflow: hidden; padding: 50px 0 46px; }
.encabezado > .contenedor { position: relative; z-index: 2; }
.encabezado h1 { color: var(--tinta-950); max-width: 22ch; }
.encabezado__bajada { font-size: 1.05rem; color: var(--suave); max-width: 68ch; margin: 0; }
.encabezado--post h1 { max-width: 26ch; }
.encabezado__meta { font-size: .86rem; color: var(--suave); margin: 0; }
/* Migas y cabecera se leen como un solo bloque */
.migas + main > .encabezado:first-child { padding-top: 26px; }

/* ---------- Secciones ---------- */
.seccion { position: relative; padding: 60px 0; }
.seccion > .contenedor, .seccion.contenedor { position: relative; z-index: 2; }
.seccion--clara { background: var(--papel-2); border-top: 1px solid var(--linea); border-bottom: 1px solid var(--linea); }
.seccion__bajada { color: var(--suave); max-width: 70ch; }
.seccion__titulo { max-width: 26ch; }

/* ---------- Índice de servicios (títulos enlazados separados por líneas finas) ---------- */
.tarjetas { list-style: none; margin: 22px 0 0; padding: 0; display: grid; column-gap: 48px;
  grid-template-columns: 1fr; border-top: 1px solid var(--linea); }
@media (min-width: 760px) { .tarjetas { grid-template-columns: repeat(2, 1fr); } }
.tarjetas--columna { grid-template-columns: 1fr !important; }
.tarjeta { padding: 16px 0 15px; border-bottom: 1px solid var(--linea); }
.tarjeta h3, .tarjeta h4 { margin: 0 0 .25em; font-size: 1.04rem; color: var(--tinta-900); }
.tarjeta h3 a, .tarjeta h4 a { color: inherit; text-decoration: none; }
.tarjeta h3 a::after, .tarjeta h4 a::after { content: " →"; color: var(--acento-txt); font-weight: 400;
  opacity: 0; transition: opacity .15s ease; }
.tarjeta h3 a:hover, .tarjeta h4 a:hover { color: var(--acento-txt); }
.tarjeta h3 a:hover::after, .tarjeta h4 a:hover::after { opacity: 1; }
.tarjeta p { color: var(--suave); font-size: .94rem; margin: 0; }
.columna__titulo { font-size: .8rem; font-weight: 600; letter-spacing: .02em; color: var(--suave);
  margin: 0 0 4px; font-family: var(--mono); }
.columna__titulo a { color: inherit; text-decoration: none; }
.columna__titulo a:hover { color: var(--acento-txt); }

.pilar__cabecera { max-width: 62ch; }
.pilar__pie { margin-top: 26px; }
.enlace-fuerte { display: inline-flex; align-items: center; gap: 7px; font-weight: 600; text-decoration: none; }
.enlace-fuerte:hover { text-decoration: underline; }

/* ---------- Ficha técnica (cifras) ---------- */
.datos { display: grid; grid-template-columns: repeat(2, 1fr); margin: 22px 0 8px;
  border-top: 1px solid var(--linea); border-bottom: 1px solid var(--linea); }
@media (min-width: 700px) { .datos { grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); } }
.dato { padding: 16px 18px 15px 0; }
.dato + .dato { padding-left: 18px; border-left: 1px solid var(--linea); }
.dato__cifra { display: block; font-size: 1.35rem; font-weight: 650; color: var(--tinta-900);
  letter-spacing: -.02em; font-variant-numeric: tabular-nums; }
.dato__label { display: block; font-size: .84rem; color: var(--suave); line-height: 1.4; margin-top: 2px; }

/* ---------- Pasos ---------- */
.pasos { list-style: none; counter-reset: paso; margin: 24px 0 0; padding: 0; display: grid;
  border-top: 1px solid var(--linea); }
.pasos__item { position: relative; padding: 17px 0 17px 40px; border-bottom: 1px solid var(--linea); }
.pasos__item::before {
  counter-increment: paso; content: counter(paso);
  position: absolute; left: 2px; top: 18px; font-family: var(--mono); font-size: .9rem; color: var(--suave);
}
.pasos__item h3 { margin-bottom: .2em; font-size: 1.04rem; }
.pasos__item p { margin: 0; color: var(--suave); font-size: .95rem; }

/* ---------- Listas ---------- */
.lista-check, .lista { list-style: none; padding: 0; margin: 18px 0 1.4em; display: grid; gap: 9px; }
.lista-check li, .lista li { position: relative; padding-left: 20px; }
.lista-check li::before, .lista li::before {
  content: ""; position: absolute; left: 2px; top: .72em; width: 8px; height: 1.5px; background: var(--acento-txt);
}
/* En pantalla ancha la lista fluye en dos columnas, sin huecos cuando un ítem ocupa dos líneas */
@media (min-width: 760px) {
  .lista { display: block; columns: 2; column-gap: 40px; }
  .lista li { break-inside: avoid; margin-bottom: 9px; }
}

.dos-columnas { display: grid; gap: 36px; grid-template-columns: 1fr; }
@media (min-width: 880px) { .dos-columnas { grid-template-columns: 1fr 1fr; gap: 56px; } }
.dos-columnas .lista { columns: 1; }
.tres-columnas { display: grid; gap: 36px; grid-template-columns: 1fr; }
@media (min-width: 760px) { .tres-columnas { grid-template-columns: 1fr 1fr; } }
@media (min-width: 1060px) { .tres-columnas { grid-template-columns: repeat(3, 1fr); gap: 40px; } }

/* ---------- Figuras ---------- */
.figura { margin: 26px 0; }
.figura img { width: 100%; border-radius: var(--radio-sm); display: block; }
.figura--estrecha { max-width: 620px; }
.figura figcaption { font-family: var(--mono); font-size: .78rem; line-height: 1.5; color: var(--suave); margin-top: 10px; }
.galeria { display: grid; gap: 28px; grid-template-columns: 1fr; margin-top: 24px; }
@media (min-width: 760px) { .galeria { grid-template-columns: repeat(3, 1fr); } .galeria .figura { margin: 0; } }
@media (min-width: 760px) { .galeria--2 { grid-template-columns: repeat(2, 1fr); } }
.galeria .figura--ancha { grid-column: 1 / -1; }

/* ---------- Tablas ---------- */
.tabla-envoltura { overflow-x: auto; margin: 0 0 1.5em; -webkit-overflow-scrolling: touch; }
table { border-collapse: collapse; width: 100%; min-width: 520px; font-size: .94rem; }
caption { text-align: left; font-size: .85rem; color: var(--suave); padding-bottom: 9px; }
th, td { text-align: left; padding: 12px 15px; border-bottom: 1px solid var(--linea); vertical-align: top; }
thead th { background: var(--papel-2); color: var(--tinta-900); font-size: .78rem; text-transform: uppercase; letter-spacing: .07em; }

/* ---------- Aviso / nota ---------- */
.aviso { border-left: 2px solid var(--tinta-900); padding: 4px 0 4px 18px; margin: 26px 0; }
.aviso p { margin: 0; font-size: .94rem; color: var(--suave); }
.nota { font-size: .87rem; color: var(--suave); background: var(--papel-2); border: 1px solid var(--linea); border-radius: var(--radio-sm); padding: 15px 17px; }

/* ---------- FAQ ---------- */
.faq { border-top: 1px solid var(--linea); margin-top: 24px; max-width: 88ch; }
.faq__item { border-bottom: 1px solid var(--linea); }
.faq__item summary { cursor: pointer; list-style: none; padding: 18px 36px 18px 0; position: relative; display: flex; align-items: center; min-height: 44px; }
.faq__item summary::-webkit-details-marker { display: none; }
.faq__item summary h3 { margin: 0; font-size: 1.01rem; color: var(--tinta-900); }
.faq__item summary::after {
  content: ""; position: absolute; right: 8px; top: 50%; width: 10px; height: 10px;
  border-right: 2px solid var(--acento-txt); border-bottom: 2px solid var(--acento-txt);
  transform: translateY(-70%) rotate(45deg); transition: transform .18s ease;
}
.faq__item[open] summary::after { transform: translateY(-30%) rotate(-135deg); }
.faq__respuesta { padding: 0 36px 20px 0; color: var(--suave); max-width: 78ch; }

/* ---------- CTA ---------- */
.cta { background: var(--papel); border-top: 1px solid var(--linea); }
.cta__caja { display: flex; flex-wrap: wrap; gap: 24px; align-items: center; justify-content: space-between; padding: 44px 22px; }
.cta h2 { margin-bottom: .25em; }
.cta p { color: var(--suave); margin: 0; max-width: 56ch; }
.cta__texto { flex: 1 1 380px; }
.cta__botones { display: flex; flex-wrap: wrap; gap: 12px; }

/* ---------- Bloques (dos listas lado a lado) ---------- */
.bloques { display: grid; gap: 36px; grid-template-columns: 1fr; margin-top: 22px; }
@media (min-width: 780px) { .bloques { grid-template-columns: repeat(2, 1fr); gap: 56px; } }
.bloque__cabecera h3 { margin: 0 0 4px; padding-bottom: 10px; border-bottom: 1px solid var(--linea); }
.bloque .lista-check { margin-bottom: 0; }

/* ---------- Blog ---------- */
.lista-posts { display: grid; gap: 18px; }
@media (min-width: 900px) { .lista-posts { grid-template-columns: repeat(3, 1fr); } }
.post-tarjeta { background: var(--papel); border: 1px solid var(--linea); border-radius: var(--radio); padding: 26px; display: flex; flex-direction: column; }
.post-tarjeta h2 { font-size: 1.18rem; margin-bottom: .45em; }
.post-tarjeta h2 a { color: var(--tinta-900); text-decoration: none; }
.post-tarjeta h2 a:hover { color: var(--acento-txt); }
.post-tarjeta__meta { display: inline-flex; align-items: center; gap: 7px; text-transform: uppercase; letter-spacing: .09em; font-size: .7rem; font-weight: 700; color: var(--acento-txt); margin-bottom: 12px; }
.post-tarjeta p { color: var(--suave); font-size: .94rem; }
.post-tarjeta .enlace-fuerte { margin-top: auto; }

.articulo { max-width: 72ch; }
.articulo h2 { margin-top: 1.8em; }
.articulo__entrada { font-size: 1.1rem; color: var(--texto); border-left: 2px solid var(--acento); padding-left: 20px; }
.articulo__cierre { margin-top: 2em; padding: 22px; background: var(--papel-2); border: 1px solid var(--linea); border-radius: var(--radio); }

/* ---------- Contacto ---------- */
.contacto { display: grid; gap: 42px; grid-template-columns: 1fr; }
@media (min-width: 920px) { .contacto { grid-template-columns: 1fr 1.05fr; gap: 56px; } }
.contacto__lista { list-style: none; padding: 0; margin: 0 0 32px; display: grid; gap: 20px; }
.contacto__lista li { display: flex; gap: 14px; align-items: flex-start; }
.contacto__lista .icono { color: var(--acento-txt); margin-top: 5px; }
.contacto__etiqueta { display: block; text-transform: uppercase; letter-spacing: .1em; font-size: .69rem; font-weight: 700; color: var(--suave); }
.contacto__valor { display: inline-block; font-size: 1.04rem; font-weight: 650; color: var(--tinta-900); text-decoration: none; }
a.contacto__valor:hover { color: var(--acento-txt); }
.contacto__nota { display: block; font-size: .85rem; color: var(--suave); }
.contacto__form { background: var(--papel-2); border: 1px solid var(--linea); border-radius: var(--radio); padding: 28px; }

.form__campo { display: block; margin: 0 0 16px; }
.form__campo label { display: block; font-size: .88rem; font-weight: 650; margin-bottom: 7px; }
.form input, .form select, .form textarea {
  width: 100%; font: inherit; font-size: 16px; padding: 12px 14px; min-height: 48px;
  border: 1px solid var(--linea-2); border-radius: var(--radio-sm); background: #fff; color: var(--texto);
}
.form input:focus, .form select:focus, .form textarea:focus { border-color: var(--acento); }
.form textarea { min-height: 130px; resize: vertical; }
.form__nota { font-size: .83rem; color: var(--suave); margin: 0; }

/* ---------- Acciones bajo el título de una página de servicio ---------- */
.encabezado__acciones { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 26px; }

/* ---------- Precio de referencia ---------- */
.precio-desde { border-top: 1px solid var(--linea); border-bottom: 1px solid var(--linea);
  padding: 18px 0; margin: 0 0 28px; }
.precio-desde__valor { font-size: 1.4rem; font-weight: 650; color: var(--tinta-900);
  letter-spacing: -.02em; margin: 0 0 4px; font-variant-numeric: tabular-nums; }
.precio-desde__valor span { font-size: .95rem; font-weight: 500; color: var(--suave); letter-spacing: 0; }
.precio-desde__nota { font-size: .89rem; color: var(--suave); margin: 0; max-width: 62ch; }

/* ---------- Calculadora de cotización ---------- */
.cotizador { display: grid; gap: 26px; grid-template-columns: 1fr; align-items: start; }
@media (min-width: 940px) { .cotizador { grid-template-columns: 1fr 1fr; gap: 34px; } }

.cotizador__form { background: var(--papel); border: 1px solid var(--linea); border-radius: var(--radio); padding: 28px; }
.cotizador__titulo { font-size: 1.15rem; margin-bottom: 22px; }
.cotizador__legal { font-size: .82rem; color: var(--suave); margin: 14px 0 0; }

.campo { display: block; margin: 0 0 20px; border: 0; padding: 0; }
.campo > label, .campo > legend { display: block; font-size: .88rem; font-weight: 650; margin-bottom: 8px; padding: 0; }
.campo__opcional { font-weight: 400; color: var(--suave); }
.campo__ayuda { display: block; font-size: .82rem; color: var(--suave); margin: 8px 0 0; font-weight: 400; }
.campo input[type="number"], .campo input[type="text"], .campo select {
  width: 100%; font: inherit; font-size: 16px; padding: 12px 14px; min-height: 48px;
  border: 1px solid var(--linea-2); border-radius: var(--radio-sm); background: #fff; color: var(--texto);
}
.campo input:focus, .campo select:focus { border-color: var(--acento); }
.campo--check { display: flex; gap: 12px; align-items: flex-start; }
.campo--check input { width: 22px; height: 22px; margin: 2px 0 0; flex: none; accent-color: var(--acento-txt); }
.campo--check label { font-size: .92rem; font-weight: 500; margin: 0; }
.campo.campo--oculto { display: none; }

.segmentado { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
.segmentado input { position: absolute; opacity: 0; width: 1px; height: 1px; }
.segmentado label {
  display: flex; align-items: center; justify-content: center; min-height: 48px; cursor: pointer;
  border: 1px solid var(--linea-2); border-radius: var(--radio-sm); font-size: .93rem; font-weight: 600;
  color: var(--suave); background: #fff; transition: border-color .14s ease, color .14s ease, background .14s ease;
}
.segmentado label:hover { border-color: var(--acento); }
.segmentado input:checked + label { border-color: var(--acento-txt); color: var(--acento-txt); background: rgba(23,195,212,.08); }
.segmentado input:focus-visible + label { outline: 2.5px solid var(--acento); outline-offset: 2px; }

.resultado { border-radius: var(--radio); padding: 30px; }
.resultado--vacio, .resultado--aviso {
  background: var(--papel-2); border: 1.5px dashed var(--linea-2); color: var(--suave);
  display: flex; flex-direction: column; align-items: center; text-align: center; gap: 14px; min-height: 260px; justify-content: center;
}
.resultado--vacio .icono, .resultado--aviso .icono { color: var(--acento-txt); opacity: .55; }
.resultado--vacio p, .resultado--aviso p { margin: 0; max-width: 40ch; }
.resultado--valor { background: var(--tinta-950); color: rgba(255,255,255,.72); position: relative; overflow: hidden; }
.resultado__etiqueta { text-transform: uppercase; letter-spacing: .13em; font-size: .7rem; font-weight: 700; color: var(--acento); margin: 0 0 6px; }
.resultado__cifra { font-size: clamp(2.1rem, 1.4rem + 3vw, 3rem); font-weight: 720; color: #fff; letter-spacing: -.035em; line-height: 1.05; margin: 0 0 10px; }
.resultado__nota { font-size: .83rem; color: rgba(255,255,255,.55); margin: 0 0 10px; }
.resultado__conversable { font-size: .83rem; color: rgba(255,255,255,.55); margin: 0 0 24px;
  padding-top: 10px; border-top: 1px dashed rgba(255,255,255,.14); }
.resultado__subtitulo { text-transform: uppercase; letter-spacing: .1em; font-size: .7rem; font-weight: 700; color: rgba(255,255,255,.5); margin: 0 0 12px; }
.resultado__incluye { border-top: 1px solid rgba(255,255,255,.12); padding-top: 22px; }
.resultado__incluye .lista-check { gap: 9px; margin-bottom: 0; }
.resultado__incluye .lista-check li { font-size: .92rem; }
.resultado__incluye .lista-check li::before { border-color: var(--acento); }
.resultado__acciones { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 26px; }

/* ---------- Pie ---------- */
.pie { background: var(--tinta-950); color: rgba(255,255,255,.62); padding: 54px 0 26px; font-size: .92rem; }
.pie__grid { display: grid; gap: 32px; grid-template-columns: 1fr; }
@media (min-width: 720px) { .pie__grid { grid-template-columns: repeat(2, 1fr); } }
@media (min-width: 1020px) { .pie__grid { grid-template-columns: 1.4fr 1fr 1fr 1fr .8fr; } }
.pie__marca { color: #fff; font-weight: 720; font-size: 1.3rem; letter-spacing: .06em; margin: 0; }
.pie__descriptor { text-transform: uppercase; letter-spacing: .13em; font-size: .67rem; color: var(--acento); margin: 2px 0 14px; }
.pie__titulo { color: #fff; font-weight: 650; margin: 0 0 14px; font-size: .93rem; }
.pie__texto { margin: 0 0 16px; max-width: 40ch; }
.pie ul { list-style: none; margin: 0; padding: 0; display: grid; gap: 10px; }
.pie__contacto li { display: flex; align-items: center; gap: 10px; }
.pie__contacto .icono { color: var(--acento); }
.pie a { color: rgba(255,255,255,.68); text-decoration: none; }
.pie a:hover { color: var(--acento); }
.pie__legal { display: flex; flex-wrap: wrap; gap: 10px; justify-content: space-between;
  border-top: 1px solid rgba(255,255,255,.1); margin-top: 42px; padding-top: 20px; font-size: .84rem; }
.pie__legal p { margin: 0; }

@media (prefers-reduced-motion: reduce) {
  * { animation-duration: .01ms !important; transition-duration: .01ms !important; scroll-behavior: auto !important; }
}
"""

FAVICON = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 36 36">
  <rect width="36" height="36" rx="9" fill="#05090d"/>
  <path d="M18 7.5 24 20h-12z" fill="none" stroke="#17c3d4" stroke-width="2" stroke-linejoin="round"/>
  <circle cx="18" cy="15.5" r="1.7" fill="#17c3d4"/>
  <path d="M8 26c3.6-4.6 6.4 2.2 10-1.4S22.6 25 28 21.6" fill="none" stroke="#ffffff" stroke-width="1.9" stroke-linecap="round" opacity=".85"/>
</svg>
"""

OG_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" width="1200" height="630">
  <rect width="1200" height="630" fill="#05090d"/>
  <g fill="none" stroke="#17c3d4" stroke-width="1.4" opacity=".22">
    <ellipse cx="330" cy="430" rx="120" ry="86" transform="rotate(-14 330 430)"/>
    <ellipse cx="336" cy="434" rx="180" ry="130" transform="rotate(-14 336 434)"/>
    <ellipse cx="342" cy="438" rx="240" ry="173" transform="rotate(-14 342 438)"/>
    <ellipse cx="348" cy="442" rx="300" ry="216" transform="rotate(-14 348 442)"/>
    <ellipse cx="960" cy="180" rx="110" ry="78" transform="rotate(20 960 180)"/>
    <ellipse cx="966" cy="184" rx="170" ry="122" transform="rotate(20 966 184)"/>
    <ellipse cx="972" cy="188" rx="230" ry="165" transform="rotate(20 972 188)"/>
  </g>
  <path d="M96 96 132 168H60z" fill="none" stroke="#17c3d4" stroke-width="5" stroke-linejoin="round"/>
  <circle cx="96" cy="134" r="7" fill="#17c3d4"/>
  <text x="180" y="152" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="74" font-weight="700" fill="#ffffff" letter-spacing="6">RCKT</text>
  <text x="182" y="192" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="22" fill="#17c3d4" letter-spacing="7">INGENIERIA Y GEOMATICA</text>
  <text x="96" y="360" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="58" font-weight="700" fill="#ffffff">Topografia con dron e</text>
  <text x="96" y="430" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="58" font-weight="700" fill="#ffffff">ingenieria hidraulica</text>
  <text x="96" y="500" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="27" fill="#8fa3b3">Curvas de nivel · Deslindes · Redes de agua · Drenaje</text>
</svg>
"""

PAGINA_404 = """<section class="encabezado">
  """ + patron("curvas") + """
  <div class="contenedor">
    <p class="encabezado__etiqueta">Error 404</p>
    <h1>Esta página no existe</h1>
    <p class="encabezado__bajada">Puede que el enlace esté mal escrito o que la página se haya movido.
    Prueba con alguna de estas secciones o escríbenos y te orientamos.</p>
  </div>
</section>
<section class="seccion"><div class="contenedor">
""" + tarjetas([
    ("Dron y topografía", "Nube de puntos, curvas de nivel, deslindes y ortomosaicos.", "dron-fotogrametria/"),
    ("Ingeniería hidráulica", "Redes de agua, bombas, drenaje pluvial y estudios de inundación.", "ingenieria-hidraulica/"),
    ("Proyecto sanitario", "Agua potable y alcantarillado particular para la SEREMI de Salud.", "proyecto-sanitario/"),
    ("Calculadora de cotización", "El valor de un levantamiento con dron según superficie y ubicación.", "cotizador/"),
    ("Empresa", "Quiénes somos y cómo trabajamos.", "empresa/"),
    ("Contacto", "Cuéntanos tu proyecto y te respondemos en 24 horas hábiles.", "contacto/"),
]) + """
</div></section>
"""

README = """# Sitio web — {marca}

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

- [ ] **Subir más imágenes reales a `assets/img/`.** Hoy hay cuatro (Patagua, modelo de elevación,
      rectificación de deslindes y modelación de redes). Faltan las de bombas, inundación, drenaje y
      proyecto sanitario. `python build.py`
      lista al final las que faltan.
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
- [ ] Completar la página `empresa/` con datos verificables (registro DGAC, RUT; el título de ingeniero civil
      hidráulico ya está publicado) y
      confirmar la razón social: hoy se publica `CONFIG["marca_legal"]` ("RCKT SpA") en esa página y en
      el schema, aunque en `CONFIG` está marcada como pendiente.
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

## Imágenes

Deja el archivo en `assets/img/` con el nombre exacto y ejecuta `python build.py`: la imagen aparece sola en
su lugar, con sus medidas y carga diferida. Mientras un archivo no exista, esa página simplemente no muestra
imagen (nunca un recuadro vacío) y el build lo lista al final. Acepta `.webp`, `.avif`, `.jpg` y `.png`.

| Archivo | Qué mostrar | Dónde aparece | Estado |
|---|---|---|---|
| `curvas-de-nivel-modelo-elevacion-dron-patagua` | DEM y curvas cada 5 m, Patagua | Portada · Pilar de dron · Curvas de nivel | Listo |
| `modelo-digital-elevacion-dron-ortomosaico` | DEM sobre ortomosaico | Portada · Nube de puntos | Listo |
| `rectificacion-deslindes-ortomosaico-dron` | Deslindes con grilla UTM | Portada · Deslindes | Listo |
| `modelacion-red-agua-potable-presiones` | Modelación de presiones de una red | Portada · Pilar de hidráulica · Modelación de redes | Listo |
| `ortomosaico-predio` | Ortomosaico real de un vuelo hecho | Mapas y ortomosaicos | Falta |
| `modelacion-golpe-de-ariete` | Gráfico de presión transitoria | Bombas e impulsiones | Falta |
| `mapa-inundacion-hecras` | Mancha de inundación por profundidad | Estudios de inundación | Falta |
| `drenaje-pluvial` | Plano de colectores o cámara en terreno | Drenaje pluvial | Falta |
| `plano-proyecto-sanitario-agua-potable-alcantarillado` | Plano de emplazamiento: pozo, estanque, fosa y drenes | Pilar de proyecto sanitario | Falta |
| `fosa-septica-drenes-alcantarillado-particular` | Detalle o foto de fosa séptica y drenes | Alcantarillado particular | Falta |
| `retrato-profesional-rckt` | Tu foto, retrato o en terreno | Empresa | Falta |
| `og-portada.jpg` | Composición 1200×630 para compartir | Todo el sitio (redes) | Falta |

Para agregar una imagen en una página nueva, usa `figura("nombre", "texto alternativo", "pie de foto")` en
`contenido.py`. Opciones: `prioritaria=True` para la imagen principal de la página (se carga primero) y
`estrecha=True` para imágenes cuadradas o verticales.

Recomendaciones:

- Nombre descriptivo, idealmente con la zona: `ortomosaico-predio-maule-2026.webp`, nunca `IMG_4821.jpg`.
- WebP, máximo 1600 px de ancho.
- En el pie de foto, describe solo lo que la imagen muestra (lugar, escala, cotas). Nada inventado.

La carpeta `imagenes-propuestas/` tiene ilustraciones técnicas dibujadas por código. No se usan en el sitio
y está excluida en `.gitignore` para que no se publique: las imágenes reales pesan más en la confianza de
un cliente que cualquier diagrama genérico.
"""


def construir_sitemap(rutas):
    hoy = datetime.date.today().isoformat()
    prioridades = {"": "1.0", "dron-fotogrametria": "0.9", "ingenieria-hidraulica": "0.9",
                   "proyecto-sanitario": "0.9", "contacto": "0.8"}
    urls = []
    for r in rutas:
        loc = CONFIG["dominio"] + "/" + (r + "/" if r else "")
        prio = prioridades.get(r, "0.7" if "/" in r else "0.8")
        urls.append(f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{hoy}</lastmod>\n"
                    f"    <changefreq>monthly</changefreq>\n    <priority>{prio}</priority>\n  </url>")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "\n".join(urls) + "\n</urlset>\n")


def main():
    import contenido

    # Borra de la carpeta las páginas que quedaron ocultas en una ejecución anterior.
    # Solo se elimina el index.html generado; la carpeta se quita si queda vacía
    # (en OneDrive a veces está bloqueada, y eso no debe detener la construcción).
    # Se procesan primero las rutas más profundas para que, al llegar a una página
    # pilar oculta (ej. "blog"), sus subpáginas ya hayan liberado la carpeta.
    ocultas = sorted((p for p in contenido.PAGINAS if p["path"].strip("/") and esta_oculto(p["path"])),
                     key=lambda p: -p["path"].count("/"))
    for p in ocultas:
        ruta = p["path"].strip("/")
        carpeta = os.path.join(OUT, ruta)
        archivo = os.path.join(carpeta, "index.html")
        if os.path.isfile(archivo):
            os.remove(archivo)
        try:
            os.rmdir(carpeta)
        except OSError:
            pass

    visibles = [p for p in contenido.PAGINAS if not esta_oculto(p["path"])]
    rutas = [construir_pagina(p) for p in visibles]

    html404 = PLANTILLA.format(
        title="Página no encontrada | " + CONFIG["marca"],
        desc="La página que buscas no existe o cambió de dirección. Revisa las secciones del sitio o escríbenos.",
        canonical=CONFIG["dominio"] + "/404.html", robots="noindex, follow", og_type="website",
        og_image=CONFIG["dominio"] + "/" + imagen_og()[0],
        og_ancho=imagen_og()[1][0], og_alto=imagen_og()[1][1],
        marca=CONFIG["marca"], descriptor=CONFIG["descriptor"], logo=LOGO_SVG,
        P="", nav=render_nav("", None), migas="",
        body=PAGINA_404, footer=render_footer(""), jsonld="", extra_head="",
        css_v=version_css(), seo_extra=seo_extra({}), analitica=analitica(),
    ).replace("{{P}}", "")
    escribir("404.html", desactivar_enlaces(html404))

    escribir("assets/css/estilos.css", CSS)
    escribir("assets/img/favicon.svg", FAVICON)
    escribir("assets/img/og-portada.svg", OG_SVG)
    escribir("sitemap.xml", construir_sitemap(rutas))
    escribir("robots.txt", "User-agent: *\nAllow: /\n\nSitemap: " + CONFIG["dominio"] + "/sitemap.xml\n")
    escribir(".nojekyll", "")
    escribir("README.md", README.format(marca=CONFIG["marca"]))

    print("Sitio generado en:", OUT)
    print("Paginas:", len(rutas) + 1)
    if SERVICIOS_OCULTOS:
        print("Servicios ocultos (" + str(len(contenido.PAGINAS) - len(visibles)) + " paginas):")
        for o in SERVICIOS_OCULTOS:
            print("  - " + o)
    # contenido.py importa este archivo como el módulo "build" (una copia distinta de la
    # que se está ejecutando), así que la lista que llenó figura() está en esa copia.
    import build as modulo_build
    if modulo_build.IMAGENES_FALTANTES:
        print("Imagenes pedidas que todavia no estan en assets/img/ (no se muestran):")
        for n in modulo_build.IMAGENES_FALTANTES:
            print("  - " + n)


if __name__ == "__main__":
    main()
