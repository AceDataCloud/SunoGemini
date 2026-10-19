#!/usr/bin/env python3
"""Install the published review commit with native CLI, no Token or generation.
This checks real GitHub source resolution and lifecycle only. Missing Token
means it does not validate a hosted MCP connection; that is a separate check.
"""
import argparse
import json
import os
from pathlib import Path
import subprocess
import tempfile

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cli', type=Path, required=True)
parser.add_argument('--ref', required=True)
parser.add_argument('--output', type=Path, required=True)
args = parser.parse_args()
base = Path(tempfile.mkdtemp(prefix='suno-remote-install-'))
user = base / 'user'
workspace = base / 'workspace'
(user / '.gemini').mkdir(parents=True)
workspace.mkdir()
(user / '.gemini/settings.json').write_text(json.dumps({'telemetry': {'enabled': False}}))
env = {k: v for k, v in os.environ.items() if k in ('PATH', 'LANG', 'TMPDIR')}
env.update(HOME=str(user), GEMINI_CLI_HOME=str(user), GEMINI_FORCE_FILE_STORAGE='true', NO_COLOR='1')
evidence = {'source': 'https://github.com/AceDataCloud/SunoGemini', 'ref': args.ref, 'token_supplied': False, 'paid_requests': 0, 'commands': [], 'checks': {}}

def run(command):
    result = subprocess.run(['node', str(args.cli.resolve())] + command, env=env, cwd=workspace, capture_output=True, text=True, timeout=120)
    evidence['commands'].append({'args': command, 'exit': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr})
    if result.returncode:
        raise RuntimeError('Remote lifecycle failed: ' + result.stderr[-800:])
    return result.stdout + result.stderr

try:
    run(['extensions', 'install', evidence['source'], '--ref', args.ref, '--consent', '--skip-settings'])
    path = user / '.gemini/extensions/suno-by-ace-data-cloud'
    manifest = json.loads((path / 'gemini-extension.json').read_text())
    metadata = json.loads((path / '.gemini-extension-install.json').read_text())
    evidence['metadata'] = metadata
    evidence['checks']['manifest_version'] = manifest['version'] == '0.1.0'
    evidence['checks']['remote_source_recorded'] = evidence['source'] in json.dumps(metadata)
    evidence['checks']['skill_bundled'] = (path / 'skills/suno-music/SKILL.md').is_file()
    evidence['checks']['listed'] = 'suno-by-ace-data-cloud' in run(['extensions', 'list'])
    run(['extensions', 'uninstall', 'suno-by-ace-data-cloud'])
    evidence['checks']['removed'] = not path.exists()
    evidence['status'] = 'PASS' if all(evidence['checks'].values()) else 'FAIL'
except Exception as exc:
    evidence['status'] = 'FAIL'
    evidence['error'] = str(exc)
args.output.parent.mkdir(parents=True, exist_ok=True)
args.output.write_text(json.dumps(evidence, indent=2) + '\n')
print(json.dumps({key: evidence.get(key) for key in ('status', 'checks', 'error')}, indent=2))
raise SystemExit(0 if evidence['status'] == 'PASS' else 1)
