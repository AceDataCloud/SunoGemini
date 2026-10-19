#!/usr/bin/env python3
"""Check real fixed-release and ordinary GitHub extension installations.
No Token, model or media request. Copies only content digests and metadata.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = json.loads((ROOT / 'gemini-extension.json').read_text())
NAME = MANIFEST['name']
REPO = 'SunoGemini'
SOURCE = 'https://github.com/AceDataCloud/' + REPO
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cli', type=Path, required=True)
parser.add_argument('--tag', default='v0.1.0')
parser.add_argument('--output', type=Path, required=True)
args = parser.parse_args()
expected = {}
for relative in ('gemini-extension.json', 'GEMINI.md', 'README.md', 'LICENSE', 'VALIDATION.md', 'THIRD_PARTY_NOTICES.md'):
    path = ROOT / relative
    if path.is_file():
        expected[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
for directory in ('commands', 'skills', 'readme', '_assets', 'docs'):
    for path in sorted((ROOT / directory).rglob('*')):
        if path.is_file():
            expected[str(path.relative_to(ROOT))] = hashlib.sha256(path.read_bytes()).hexdigest()
evidence = {'repo': REPO, 'source': SOURCE, 'tag': args.tag, 'token_supplied': False, 'model_requests': 0, 'media_requests': 0, 'modes': []}
try:
    for fixed in (True, False):
        mode = {'name': 'fixed-tag' if fixed else 'ordinary-default', 'commands': [], 'checks': {}}
        base = Path(tempfile.mkdtemp(prefix='gemini-release-check-'))
        user = base / 'user'
        workspace = base / 'workspace'
        (user / '.gemini').mkdir(parents=True)
        workspace.mkdir()
        (user / '.gemini/settings.json').write_text(json.dumps({'telemetry': {'enabled': False}}))
        env = {k: v for k, v in os.environ.items() if k in ('PATH', 'LANG', 'TMPDIR')}
        env.update(HOME=str(user), GEMINI_CLI_HOME=str(user), GEMINI_FORCE_FILE_STORAGE='true', NO_COLOR='1')
        def run(command):
            result = subprocess.run(['node', str(args.cli.resolve())] + command, env=env, cwd=workspace, capture_output=True, text=True, timeout=180)
            mode['commands'].append({'args': command, 'exit_code': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr})
            if result.returncode:
                raise RuntimeError('Install command failed: ' + result.stderr[-600:])
            return result.stdout + result.stderr
        command = ['extensions', 'install', SOURCE, '--consent', '--skip-settings']
        if fixed:
            command += ['--ref', args.tag]
        run(command)
        installed = user / '.gemini/extensions' / NAME
        config = json.loads((installed / 'gemini-extension.json').read_text())
        metadata = json.loads((installed / '.gemini-extension-install.json').read_text())
        mode['metadata'] = metadata
        mode['checks']['manifest_version'] = config['version'] == MANIFEST['version']
        mode['checks']['source_recorded'] = SOURCE in json.dumps(metadata)
        mode['checks']['github_release_transport'] = metadata.get('type') == 'github-release'
        mode['checks']['exact_release_tag'] = metadata.get('releaseTag') == args.tag
        mismatches = [relative for relative, digest in expected.items() if not (installed / relative).is_file() or hashlib.sha256((installed / relative).read_bytes()).hexdigest() != digest]
        mode['checks']['installed_content_matches_release_commit'] = not mismatches
        mode['content_mismatches'] = mismatches
        mode['checks']['extension_listed'] = NAME in run(['extensions', 'list'])
        run(['extensions', 'uninstall', NAME])
        mode['checks']['removed'] = not installed.exists()
        mode['status'] = 'PASS' if all(mode['checks'].values()) else 'FAIL'
        evidence['modes'].append(mode)
    evidence['status'] = 'PASS' if all(m['status'] == 'PASS' for m in evidence['modes']) else 'FAIL'
except Exception as error:
    evidence['status'] = 'FAIL'
    evidence['error'] = str(error)
args.output.parent.mkdir(parents=True, exist_ok=True)
args.output.write_text(json.dumps(evidence, indent=2) + '\n')
print(json.dumps({'status': evidence['status'], 'modes': [{'name': m['name'], 'checks': m['checks']} for m in evidence['modes']], 'error': evidence.get('error')}, indent=2))
raise SystemExit(0 if evidence['status'] == 'PASS' else 1)
