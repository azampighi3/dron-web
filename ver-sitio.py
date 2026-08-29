# -*- coding: utf-8 -*-
"""
Genera el sitio, lo publica en un servidor local y lo abre en el navegador.

No se ejecuta directamente: usa `ver-sitio.bat` (doble clic).
"""

import os
import sys
import http.server
import subprocess
import threading
import webbrowser

CARPETA = os.path.dirname(os.path.abspath(__file__))
PUERTO_INICIAL = 8000


class Handler(http.server.SimpleHTTPRequestHandler):
    """Sirve la carpeta del sitio sin caché, para ver siempre la última versión."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=CARPETA, **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store, must-revalidate")
        super().end_headers()

    def log_message(self, formato, *args):
        pass  # sin ruido en la consola


def construir():
    print("Generando el sitio...\n")
    resultado = subprocess.run([sys.executable, "build.py"], cwd=CARPETA)
    if resultado.returncode != 0:
        print("\n" + "=" * 60)
        print("  ERROR al generar el sitio. Revisa el mensaje de arriba.")
        print("  Suele ser una comilla o un parentesis sin cerrar en")
        print("  contenido.py o en build.py.")
        print("=" * 60)
        input("\nPresiona Enter para cerrar...")
        sys.exit(1)


class Servidor(http.server.ThreadingHTTPServer):
    """Atiende varias peticiones a la vez.

    Con un servidor de un solo hilo el navegador mantiene abierta la primera
    conexión y las páginas siguientes quedan esperando indefinidamente.
    """
    allow_reuse_address = True
    daemon_threads = True


def servir():
    for puerto in range(PUERTO_INICIAL, PUERTO_INICIAL + 20):
        try:
            servidor = Servidor(("127.0.0.1", puerto), Handler)
        except OSError:
            continue

        url = "http://localhost:%d/" % puerto
        threading.Timer(1.0, lambda: webbrowser.open(url)).start()

        print("\n" + "=" * 60)
        print("  Sitio disponible en:  " + url)
        print("=" * 60)
        print("\n  Deja esta ventana abierta mientras revisas el sitio.")
        print("  Para terminar: cierra esta ventana o presiona Ctrl+C.")
        print("\n  Si cambias contenido.py o build.py, cierra esta ventana")
        print("  y vuelve a abrir ver-sitio.bat para ver los cambios.\n")

        try:
            servidor.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor detenido.")
        finally:
            servidor.server_close()
        return

    print("No se encontro un puerto libre entre %d y %d." % (PUERTO_INICIAL, PUERTO_INICIAL + 19))
    input("\nPresiona Enter para cerrar...")


if __name__ == "__main__":
    construir()
    servir()
