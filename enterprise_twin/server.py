"""Decoupled Backend Agent Server for Enterprise Twin Generation.

Provides a REST API for the frontend (hosted on Zipline, Cloud Run, or local)
to trigger autonomous research, profiling, and customized portal compilation.
Supports local testing and is ready for containerized Cloud Run / Argolis deployment.
"""

import json
import argparse
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Dict, Any

from enterprise_twin.tools.company_profiler import profile_company, KNOWN_COMPANIES
from enterprise_twin.tools.industry_archetypes import INDUSTRY_ARCHETYPES
from enterprise_twin.generator.html_compiler import compile_enterprise_twin


class EnterpriseTwinApiHandler(BaseHTTPRequestHandler):
    """CORS-enabled REST API handler for decoupled Enterprise Twin Agent."""

    def _send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")

    def do_OPTIONS(self):
        self.send_response(204)
        self._send_cors_headers()
        self.end_headers()

    def do_GET(self):
        if self.path == "/api/v1/health":
            self.send_response(200)
            self._send_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            resp = {
                "status": "healthy",
                "service": "EnterpriseTwinAgent",
                "version": "1.0.0",
                "available_archetypes": list(INDUSTRY_ARCHETYPES.keys()),
                "known_presets": list(KNOWN_COMPANIES.keys())
            }
            self.wfile.write(json.dumps(resp, indent=2).encode("utf-8"))
        elif self.path == "/api/v1/archetypes":
            self.send_response(200)
            self._send_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(INDUSTRY_ARCHETYPES, indent=2).encode("utf-8"))
        else:
            self.send_response(404)
            self._send_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Not found"}).encode("utf-8"))

    def do_POST(self):
        if self.path == "/api/v1/generate-twin":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            try:
                data = json.loads(body) if body else {}
            except Exception as e:
                self.send_response(400)
                self._send_cors_headers()
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": f"Invalid JSON payload: {e}"}).encode("utf-8"))
                return

            company_name = data.get("company_name", "").strip()
            industry = data.get("industry", None)
            focus = data.get("focus", "")

            if not company_name:
                self.send_response(400)
                self._send_cors_headers()
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Missing required field: 'company_name'"}).encode("utf-8"))
                return

            print(f"⚡ [Backend Agent] Received request to generate twin for: '{company_name}' (Industry: {industry})")
            
            try:
                # 1. Autonomous Research & Profiling
                profile = profile_company(company_name, industry)
                if focus:
                    profile['executiveThesis'] += f" Strategic focus: {focus}."

                # 2. Compile customized portal & Zipline bundle
                out_dir = compile_enterprise_twin(profile)
                slug = out_dir.name
                
                resp = {
                    "status": "success",
                    "company_name": profile['canonicalName'],
                    "industry": profile['industryId'],
                    "executive_title": profile['executiveTitle'],
                    "brand_accent": profile['brandAccent'],
                    "brand_secondary": profile['brandSecondary'],
                    "flagship_sites": profile.get('flagshipSites', ''),
                    "output_dir": str(out_dir),
                    "index_file": str(out_dir / "index.html"),
                    "periodic_table_file": str(out_dir / "periodic_table.html"),
                    "mind_map_file": str(out_dir / "mind_map.html"),
                    "zipline_bundle_file": str(out_dir / f"{slug}_zipline_bundle.zip"),
                    "profile": profile
                }

                self.send_response(200)
                self._send_cors_headers()
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(resp, indent=2).encode("utf-8"))
                print(f"✅ [Backend Agent] Successfully generated twin for: '{company_name}'")

            except Exception as e:
                print(f"❌ [Backend Agent] Error generating twin: {e}")
                self.send_response(500)
                self._send_cors_headers()
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
        else:
            self.send_response(404)
            self._send_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Endpoint not found"}).encode("utf-8"))


def run_server(port: int = 8080, host: str = "0.0.0.0"):
    server_address = (host, port)
    httpd = HTTPServer(server_address, EnterpriseTwinApiHandler)
    print("="*70)
    print(f"🚀 ENTERPRISE TWIN DECOUPLED BACKEND AGENT SERVICE")
    print(f"   Listening on http://{host}:{port}")
    print(f"   Health check: http://localhost:{port}/api/v1/health")
    print(f"   API endpoint: POST http://localhost:{port}/api/v1/generate-twin")
    print("="*70)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server.")
        httpd.server_close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Enterprise Twin Backend Agent Server")
    parser.add_argument("--port", type=int, default=8080, help="Port to listen on (default: 8080)")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host address (default: 0.0.0.0)")
    args = parser.parse_args()
    run_server(args.port, args.host)
