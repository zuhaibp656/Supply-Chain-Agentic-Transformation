#!/usr/bin/env python3
"""Launches `uvicorn`, `adk web`, or `http.server` on dual IPv4 + IPv6 sockets.

On CloudTop workstations, `localhost` resolves to `[::1]` first and IDE port
forwarders inspect `/proc/net/tcp` (IPv4) and `/proc/net/tcp6` (IPv6).
- Binding only `0.0.0.0` rejects IPv6 `[::1]`.
- Binding only `::` with `IPV6_V6ONLY=0` omits the IPv4 listener from `/proc/net/tcp`.
- Binding BOTH an `AF_INET` (`0.0.0.0`) socket and an `AF_INET6` (`::`, `IPV6_V6ONLY=1`)
  socket on the same port registers kernel listeners in both `/proc/net/tcp`
  and `/proc/net/tcp6` simultaneously with zero `EADDRINUSE` conflict.
"""

from __future__ import annotations

import functools
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import os
import socket
import sys
import threading


def create_dual_stack_sockets(port: int, backlog: int = 2048) -> list[socket.socket]:
    """Creates bound, listening IPv4 (`0.0.0.0`) and IPv6 (`::`, `IPV6_V6ONLY=1`) sockets."""
    sockets: list[socket.socket] = []

    try:
        sock4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock4.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock4.bind(("0.0.0.0", port))
        sock4.listen(backlog)
        sockets.append(sock4)
    except OSError:
        pass

    try:
        sock6 = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        sock6.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock6.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 1)
        sock6.bind(("::", port))
        sock6.listen(backlog)
        sockets.append(sock6)
    except OSError:
        if not sockets:
            # Fallback to single IPv6 dual-mapped socket only if separate bind fails
            sock_dual = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            sock_dual.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock_dual.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
            sock_dual.bind(("::", port))
            sock_dual.listen(backlog)
            sockets.append(sock_dual)

    if not sockets:
        raise OSError(f"Unable to bind IPv4 or IPv6 socket on port {port}")
    return sockets


def _install_dual_stack_hook(port: int) -> None:
    import uvicorn

    orig_run = uvicorn.Server.run

    def dual_stack_run(self, sockets=None):
        if sockets is None and getattr(self.config, "host", "") in ("::", "0.0.0.0", ""):
            try:
                sockets = create_dual_stack_sockets(port)
            except OSError:
                sockets = None
        return orig_run(self, sockets=sockets)

    uvicorn.Server.run = dual_stack_run


class _PreboundThreadingHTTPServer(ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = True

    def __init__(self, sock: socket.socket, handler_cls):
        self._prebound_sock = sock
        super().__init__(sock.getsockname()[:2], handler_cls, bind_and_activate=False)
        self.socket = sock

    def server_close(self) -> None:
        try:
            super().server_close()
        except Exception:
            pass


def _serve_static_http(port: int, directory: str) -> None:
    sockets = create_dual_stack_sockets(port, backlog=256)
    handler = functools.partial(SimpleHTTPRequestHandler, directory=directory)
    servers = [_PreboundThreadingHTTPServer(s, handler) for s in sockets]
    threads = [threading.Thread(target=srv.serve_forever, daemon=False) for srv in servers[1:]]
    for t in threads:
        t.start()
    servers[0].serve_forever()


def main() -> None:
    os.environ.setdefault("GOOGLE_API_USE_CLIENT_CERTIFICATE", "false")
    args = sys.argv[1:]
    if len(args) < 3 or args[0] != "--port":
        raise SystemExit("Usage: dual_stack_serve.py --port <PORT> <uvicorn|adk|static-http> [args...]")
    port = int(args[1])
    mode = args[2]
    rest = args[3:]

    if mode == "static-http":
        directory = "."
        if "--directory" in rest:
            idx = rest.index("--directory")
            if idx + 1 < len(rest):
                directory = rest[idx + 1]
        _serve_static_http(port, directory)
        return

    _install_dual_stack_hook(port)

    if mode == "uvicorn":
        import uvicorn.main

        sys.argv = ["uvicorn", *rest]
        uvicorn.main.main()
    elif mode == "adk":
        from google.adk.cli import main as adk_main

        sys.argv = ["adk", *rest]
        sys.exit(adk_main())
    else:
        raise SystemExit(f"Unsupported mode: {mode}")


if __name__ == "__main__":
    main()
