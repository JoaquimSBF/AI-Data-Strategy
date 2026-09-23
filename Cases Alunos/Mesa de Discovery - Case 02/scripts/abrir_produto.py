from __future__ import annotations

import http.server
import socketserver
import threading
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRODUTO = ROOT / "produto"
PORT = 8767
URL = f"http://127.0.0.1:{PORT}/index.html"


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, directory=str(PRODUTO), **kwargs)


def main() -> None:
    if not (PRODUTO / "index.html").exists():
        raise SystemExit(f"produto/index.html não encontrado em {PRODUTO}")
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("127.0.0.1", PORT), Handler) as httpd:
        print(URL)
        print("Deixe esta janela aberta. Encerre com Ctrl+C.")
        threading.Timer(0.8, lambda: webbrowser.open(URL)).start()
        httpd.serve_forever()


if __name__ == "__main__":
    main()
