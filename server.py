import concurrent.futures
import json
import socket
import time
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


def tcp(host, port, timeout=5):
    started = time.time()
    try:
        conn = socket.create_connection((host, port), timeout)
        conn.close()
        return {"ok": True, "ms": round((time.time() - started) * 1000)}
    except Exception as exc:
        return {
            "ok": False,
            "ms": round((time.time() - started) * 1000),
            "error": type(exc).__name__ + ": " + str(exc),
        }


def dns(name):
    started = time.time()
    try:
        infos = socket.getaddrinfo(name, 443, socket.AF_INET, socket.SOCK_STREAM)
        ips = sorted({info[4][0] for info in infos})
        return {"ok": True, "ms": round((time.time() - started) * 1000), "ips": ips}
    except Exception as exc:
        return {
            "ok": False,
            "ms": round((time.time() - started) * 1000),
            "error": type(exc).__name__ + ": " + str(exc),
        }


def https(url, timeout=6):
    started = time.time()
    try:
        request = urllib.request.Request(
            url, headers={"User-Agent": "cranl-egress-test/1.0"}
        )
        with urllib.request.urlopen(request, timeout=timeout) as response:
            response.read(64)
            return {
                "ok": True,
                "ms": round((time.time() - started) * 1000),
                "status": response.status,
            }
    except Exception as exc:
        return {
            "ok": False,
            "ms": round((time.time() - started) * 1000),
            "error": type(exc).__name__ + ": " + str(exc),
        }


def interfaces():
    try:
        return [name for _, name in socket.if_nameindex()]
    except Exception:
        return []


def run_all():
    checks = {
        "dns_example_com": lambda: dns("example.com"),
        "tcp_1.1.1.1_443": lambda: tcp("1.1.1.1", 443),
        "tcp_8.8.8.8_53": lambda: tcp("8.8.8.8", 53),
        "https_example_com": lambda: https("https://example.com"),
        "https_google_com": lambda: https("https://www.google.com"),
    }
    started = time.time()
    results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(checks)) as pool:
        futures = {key: pool.submit(fn) for key, fn in checks.items()}
        for key, future in futures.items():
            try:
                results[key] = future.result(timeout=12)
            except Exception as exc:
                results[key] = {"ok": False, "error": type(exc).__name__ + ": " + str(exc)}
    return {
        "time_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "hostname": socket.gethostname(),
        "interfaces": interfaces(),
        "elapsed_ms": round((time.time() - started) * 1000),
        "checks": results,
    }


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/healthz":
            body = b"OK\n"
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        body = (json.dumps(run_all(), indent=2) + "\n").encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        pass


if __name__ == "__main__":
    ThreadingHTTPServer(("0.0.0.0", 3000), Handler).serve_forever()
