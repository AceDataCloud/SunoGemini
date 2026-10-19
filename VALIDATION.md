# Validation and release boundary

2026-10-18. Candidate version 0.1.0, target Gemini CLI 0.64.0.

The package uses the existing `https://suno.mcp.acedata.cloud/mcp` service. No music generation, paid model request, account mutation or media purchase is part of this validation.

- `python3 -m unittest discover -s tests`: package, token boundary, tool allowlist and archive tests.
- `gemini extensions validate <repository>`: official CLI manifest/context validation.
- `tests/smoke_extension.py`: isolated install/list/native password configuration, Skill discovery/activation, tool result loop and uninstall. The model is a deterministic localhost fixture. MCP can be a local fixture or the real static Suno information tool. The native encrypted file fallback is forced only in this isolated test to avoid touching the user's OS keychain; it is not a product default.

Results are appended after running; a fixture pass must not be described as a real model/music result. Existing-task terminal/media/billing checks need an actual authorized task ID and separate evidence.

The current review branch can be installed explicitly. Main/release publication and the official gallery crawl are separate gates. No merge or featured placement is claimed.

## Executed 2026-10-18

- Five contract/archive tests passed.
- Official Gemini CLI 0.64.0 `extensions validate` passed.
- Full local installation with native password prompt passed. The native encrypted fallback was scoped to an isolated temporary home. No plaintext token was found in that home. Extension list, MCP connection, bundled Skill discovery/activation, `/suno-check` reference loop, forbidden-tool filtering and uninstall all passed.
- A second install used the **real Suno hosted MCP** with the same local model fixture. The native Token was supplied through the password prompt, the reference result returned to CLI, and uninstall passed. No song, lyrics generation, paid model or other billable operation was requested.

This is an actual CLI/extension/MCP integration check. Model decisions were deterministic test responses, not a real model reasoning evaluation. No completed audio/media or consumption/billing record is claimed.


## Stable publication, 2026-10-19

The initial implementation PR is merged under the owner's current merge/release authorization. Previously recorded review-commit/local/hosted checks remain historical evidence, not a claim that every released artifact has been rechecked. The release verifier installs both v0.1.0 and the unpinned ordinary command from GitHub, reads actual install metadata/version/bundled files, lists and uninstalls without a Token or any model/media request. It checks installed files against the exact release commit. The stable verification result is attached to its Actions run after publication. Official gallery search remains a distinct indexing gate.
