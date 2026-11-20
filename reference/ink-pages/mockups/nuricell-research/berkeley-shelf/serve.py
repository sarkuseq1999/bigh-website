"""Serve this review on a chosen local interface. Only the named public assets are available."""
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

HERE = Path(__file__).resolve().parent
PUBLIC = next(p for p in HERE.parents if (p / "package.json").is_file()) / "public"
FILES = {"/": HERE / "preview/index.html", "/shelf.webp": HERE / "preview/shelf.webp"}
for asset in ["fonts/switzer/switzer-variable-v1.woff2", "images/home-v2/ink/paper.webp"]:
    FILES["/" + asset] = PUBLIC / asset


class Review(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        return str(FILES.get(urlsplit(path).path, HERE / "missing-file"))


if __name__ == "__main__":
    bind, port = sys.argv[1], int(sys.argv[2])
    with ThreadingHTTPServer((bind, port), Review) as server:
        print(f"NuriCell review http://{bind}:{port}/", flush=True)
        server.serve_forever()
