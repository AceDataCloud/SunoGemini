# SunoGemini

This repository owns the Gemini CLI extension manifest, Suno workflow skill, commands and bilingual onboarding. SunoMCP owns service implementation; reuse its hosted endpoint and do not duplicate the server here. Keep a focused Suno tool allowlist and native sensitive settings. Never add trust bypass, hooks or default paid requests.

Run `python3 -m unittest discover -s tests` for package/contract tests and `python3 scripts/package_extension.py --output /tmp/suno-by-ace-data-cloud.tar.gz` for a self-contained archive. Run the official Gemini CLI `extensions validate` and isolated installation/loop smoke test described in tests/README.md when changing the manifest/settings/skill. Keep the ordinary CI test discovery command; do not use test file allowlists.

English README.md and readme/README_zh_Hans.md must agree on Key setup, free reference checks, billing and same-ID polling. Use only authentic screenshots or clearly labeled official screenshot edits with source/date. Never commit secrets, .env files or user transcripts containing real tokens. Publish through a reviewed PR; no auto-merge.
