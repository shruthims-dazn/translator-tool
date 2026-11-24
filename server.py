#!/usr/bin/env python3
import argparse
import json
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


APP_ROOT = Path(__file__).resolve().parent
STATIC_ROOT = APP_ROOT / "static"
TRANSLATE_URL = "https://api.mymemory.translated.net/get"


def translate_text(text, source, target, timeout=10):
    if source not in {"en", "ko"} or target not in {"en", "ko"}:
        raise ValueError("Only English and Korean are supported.")
    if source == target:
        raise ValueError("Source and target languages must be different.")
    text = text.strip()
    if not text:
        raise ValueError("Enter text to translate.")
    if len(text) > 500:
        raise ValueError("Text must be 500 characters or fewer.")

    params = urllib.parse.urlencode({"q": text, "langpair": f"{source}|{target}"})
    request = urllib.request.Request(
        f"{TRANSLATE_URL}?{params}",
        headers={"Accept": "application/json", "User-Agent": "English-Korean-Translator/1.0"},
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except Exception as error:
        raise RuntimeError("Could not reach the translation service.") from error

    translated = payload.get("responseData", {}).get("translatedText")
    if not translated:
        raise RuntimeError("The translation service returned no result.")
    return translated


class TranslatorHandler(BaseHTTPRequestHandler):
    def _send_json(self, value, status=200):
        body = json.dumps(value, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        if parsed.path == "/api/translate":
            text = params.get("text", [""])[0]
            source = params.get("source", ["en"])[0]
            target = params.get("target", ["ko"])[0]
            try:
                translated = translate_text(text, source, target)
                self._send_json({"translatedText": translated})
            except (ValueError, RuntimeError) as error:
                status = 400 if isinstance(error, ValueError) else 502
                self._send_json({"error": str(error)}, status)
            return

        static_files = {
            "/": ("index.html", "text/html; charset=utf-8"),
            "/index.html": ("index.html", "text/html; charset=utf-8"),
            "/app.css": ("app.css", "text/css; charset=utf-8"),
            "/app.js": ("app.js", "text/javascript; charset=utf-8"),
        }
        if parsed.path in static_files:
            filename, content_type = static_files[parsed.path]
            body = (STATIC_ROOT / filename).read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        self._send_json({"error": "Not found."}, 404)

    def log_message(self, format_string, *args):
        print("%s - %s" % (self.address_string(), format_string % args))


def main():
    parser = argparse.ArgumentParser(description="Run the English-Korean translator.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8790)
    args = parser.parse_args()
    server = ThreadingHTTPServer((args.host, args.port), TranslatorHandler)
    print("Translator is running at http://%s:%d" % (args.host, args.port))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping translator.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
