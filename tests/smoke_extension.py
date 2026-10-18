#!/usr/bin/env python3
"""Native extension lifecycle; model is localhost, no music is generated.
Optional --live-info calls only Suno's static model-reference tool. Uses an
isolated encrypted native fallback; never touches the user's keychain.
"""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import threading
import secrets
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import pexpect

ROOT = Path(__file__).resolve().parents[1]
NAME = "suno-by-ace-data-cloud"
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--cli", type=Path, required=True)
parser.add_argument("--output", type=Path, required=True)
parser.add_argument("--live-info", action="store_true")
parser.add_argument("--source", help="Install actual remote URL instead of local copy")
parser.add_argument("--ref")
args = parser.parse_args()
token = os.environ.get("ACEDATACLOUD_SUNO_TEST_TOKEN") if args.live_info else "local-fixture-" + secrets.token_hex(16)
if not token:
    parser.error("Export ACEDATACLOUD_SUNO_TEST_TOKEN for a live information-only check")
base = Path(tempfile.mkdtemp(prefix="suno-gemini-extension-"))
workspace = base / "workspace"
workspace.mkdir()
user = base / "user"
(user / ".gemini").mkdir(parents=True)
source = base / NAME
shutil.copytree(ROOT, source, ignore=shutil.ignore_patterns(".git", "artifacts", "__pycache__", "dist"))
evidence = {"as_of": "2026-10-18", "model": "local deterministic fixture", "mcp": "hosted Suno static information" if args.live_info else "local fixture", "paid_requests": 0, "native_secret_storage": "isolated encrypted fallback", "checks": {}, "commands": [], "model_requests": [], "mcp_calls": []}

class Fixture(BaseHTTPRequestHandler):
    def log_message(self, *unused):
        pass

    def do_GET(self):
        self.send_response(405)
        self.end_headers()

    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
        if self.path.startswith("/mcp"):
            method = body.get("method")
            if method and method.startswith("notifications/"):
                self.send_response(202)
                self.end_headers()
                return
            result = {}
            if method == "initialize":
                result = {"protocolVersion": "2025-03-26", "capabilities": {"tools": {}}, "serverInfo": {"name": "suno-local-fixture", "version": "test-only"}}
            elif method == "tools/list":
                manifest = json.loads((source / "gemini-extension.json").read_text())
                names = manifest["mcpServers"][NAME]["includeTools"] + ["suno_delete_persona"]
                result = {"tools": [{"name": name, "description": "LOCAL FIXTURE ONLY", "inputSchema": {"type": "object", "properties": {}}} for name in names]}
            elif method == "tools/call":
                name = body["params"]["name"]
                evidence["mcp_calls"].append(name)
                if name != "suno_list_models":
                    raise RuntimeError("Test attempted a non-reference operation")
                result = {"content": [{"type": "text", "text": "LOCAL_SUNO_REFERENCE: chirp-v6; no generation"}]}
            elif method == "resources/list":
                result = {"resources": []}
            elif method == "prompts/list":
                result = {"prompts": []}
            evidence["checks"]["local_header_expanded"] = self.headers.get("Authorization") == "Bearer " + token
            data = {"jsonrpc": "2.0", "id": body.get("id"), "result": result}
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())
            return
        declarations = [d for tool in body.get("tools", []) for d in tool.get("functionDeclarations", [])]
        names = [d["name"] for d in declarations]
        responses = [part["functionResponse"] for content in body.get("contents", []) for part in content.get("parts", []) if "functionResponse" in part]
        seen = [response["name"] for response in responses]
        info_tool = next((name for name in names if name.endswith("suno_list_models")), None)
        command_loaded = "Activate the suno-music skill. Call only suno_list_models" in json.dumps(body)
        evidence["model_requests"].append({"path": self.path, "tools": names, "responses": seen, "command_prompt_loaded": command_loaded})
        if info_tool and info_tool in seen:
            result_text = json.dumps(responses)
            evidence["checks"]["reference_result_returned"] = "chirp-v6" in result_text
            part = {"text": "SUNO_EXTENSION_REFERENCE_OK: reference returned; no song generated."}
        elif "activate_skill" in names and "activate_skill" not in seen:
            part = {"functionCall": {"name": "activate_skill", "args": {"name": "suno-music"}}}
        elif info_tool:
            part = {"functionCall": {"name": info_tool, "args": {}}}
        else:
            part = {"text": "Required extension tool is missing."}
        data = {"candidates": [{"content": {"role": "model", "parts": [part]}, "finishReason": "STOP", "index": 0}], "usageMetadata": {"promptTokenCount": 1, "candidatesTokenCount": 1, "totalTokenCount": 2}}
        streaming = ":streamGenerateContent" in self.path
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream" if streaming else "application/json")
        self.end_headers()
        self.wfile.write((("data: " + json.dumps(data) + "\n\n") if streaming else json.dumps(data)).encode())

server = ThreadingHTTPServer(("127.0.0.1", 0), Fixture)
threading.Thread(target=server.serve_forever, daemon=True).start()
manifest_file = source / "gemini-extension.json"
manifest = json.loads(manifest_file.read_text())
if not args.live_info:
    manifest["mcpServers"][NAME]["httpUrl"] = f"http://127.0.0.1:{server.server_port}/mcp"
    manifest_file.write_text(json.dumps(manifest))
if args.source and not args.live_info:
    parser.error("Remote package retains hosted endpoint; use --live-info for remote installation")
settings = {"security": {"auth": {"selectedType": "gemini-api-key"}}, "telemetry": {"enabled": False}, "experimental": {"extensionConfig": True}}
(user / ".gemini/settings.json").write_text(json.dumps(settings))
(user / ".gemini/trustedFolders.json").write_text(json.dumps({str(source.resolve()): "TRUST_FOLDER", str(workspace.resolve()): "TRUST_FOLDER"}))
env = {key: value for key, value in os.environ.items() if key in ("PATH", "LANG", "TMPDIR")}
env.update(HOME=str(user), GEMINI_CLI_HOME=str(user), NO_COLOR="1", TERM="xterm-256color", GEMINI_FORCE_FILE_STORAGE="true", GEMINI_API_KEY="local-model-dummy", GOOGLE_GEMINI_BASE_URL=f"http://127.0.0.1:{server.server_port}", GOOGLE_GENAI_API_VERSION="v1beta", GEMINI_API_KEY_AUTH_MECHANISM="bearer")
exe = ["node", str(args.cli.resolve())]

def run(command, timeout=60):
    result = subprocess.run(exe + command, cwd=workspace, env=env, text=True, capture_output=True, timeout=timeout)
    evidence["commands"].append({"args": command, "exit": result.returncode, "stdout": result.stdout.replace(token, "[REDACTED]"), "stderr": result.stderr.replace(token, "[REDACTED]")})
    if result.returncode:
        raise RuntimeError("Command failed: " + str(command) + ": " + result.stderr[-500:])
    return result.stdout + result.stderr

try:
    evidence["cli_version"] = run(["--version"]).strip()
    run(["extensions", "validate", str(source)])
    install_source = args.source or str(source)
    command = ["extensions", "install", install_source, "--consent"]
    if args.ref:
        command += ["--ref", args.ref]
    child = pexpect.spawn(exe[0], exe[1:] + command, cwd=str(workspace), env=env, encoding="utf-8", timeout=90, echo=False)
    transcript = ""
    child.expect("Ace Data Cloud Suno API Token")
    transcript += child.before + child.after
    child.sendline(token)
    child.expect(pexpect.EOF)
    transcript += child.before
    child.close()
    evidence["commands"].append({"args": command, "exit": child.exitstatus, "transcript": transcript.replace(token, "[REDACTED]")})
    evidence["checks"]["native_password_prompt"] = True
    evidence["checks"]["installed"] = child.exitstatus == 0 and "installed successfully" in transcript
    if not evidence["checks"]["installed"]:
        raise RuntimeError("Native extension install failed: " + transcript[-700:].replace(token, "[REDACTED]"))
    evidence["checks"]["listed"] = NAME in run(["extensions", "list"])
    evidence["checks"]["mcp_connected"] = "Connected" in run(["mcp", "list"])
    evidence["checks"]["skill_discovered"] = "suno-music [Enabled]" in run(["skills", "list"])
    plaintext = [str(path.relative_to(user)) for path in user.rglob("*") if path.is_file() and token.encode() in path.read_bytes()]
    evidence["checks"]["no_plaintext_token_file"] = not plaintext
    evidence["plaintext_token_files"] = plaintext
    result = run(["-m", "gemini-3.5-flash-lite", "-p", "/suno-check", "--approval-mode", "yolo", "--output-format", "json"], timeout=90)
    evidence["checks"]["skill_activated"] = any("activate_skill" in request["responses"] for request in evidence["model_requests"])
    evidence["checks"]["forbidden_tool_filtered"] = bool(evidence["model_requests"]) and all(not any(name.endswith("suno_delete_persona") for name in request["tools"]) for request in evidence["model_requests"])
    evidence["checks"]["reference_result_visible"] = "SUNO_EXTENSION_REFERENCE_OK" in result
    evidence["checks"]["check_command_resolved"] = any(request["command_prompt_loaded"] for request in evidence["model_requests"])
    run(["extensions", "uninstall", NAME])
    evidence["checks"]["uninstalled"] = NAME not in run(["extensions", "list"])
    evidence["status"] = "PASS" if all(evidence["checks"].values()) else "FAIL"
except Exception as error:
    evidence["status"] = "FAIL"
    evidence["error"] = str(error).replace(token, "[REDACTED]")
finally:
    server.shutdown()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(evidence, ensure_ascii=False, indent=2).replace(token, "[REDACTED]") + "\n")
print(json.dumps({key: evidence.get(key) for key in ("status", "cli_version", "checks", "error")}, indent=2))
raise SystemExit(0 if evidence["status"] == "PASS" else 1)
