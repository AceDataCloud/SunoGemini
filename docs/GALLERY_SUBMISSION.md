# Official gallery handoff

Candidate: **Suno by Ace Data Cloud** / manifest ID `suno-by-ace-data-cloud`, version 0.1.0.

Official mechanism (checked 2026-10-18): https://github.com/google-gemini/gemini-cli/blob/main/docs/extensions/releasing.md

The gallery crawls public repositories daily when the root contains `gemini-extension.json` and the repository has the `gemini-cli-extension` topic. It does not require an email or issue. An indexed card is not guaranteed by a topic or source PR.

## Repository metadata ready to apply after review/merge

- Repository: https://github.com/AceDataCloud/SunoGemini
- Description: Suno by Ace Data Cloud for Gemini CLI — music generation, lyrics guidance, covers and same-task results. Independent integration, not Suno official.
- Topics: `gemini-cli-extension`, `gemini-cli`, `suno`, `ai-music`, `music-generation`, `lyrics`, `mcp`, `agent-skills`, `acedata-cloud`.
- Scope/category expressed through manifest: MCP + Skills + Context + Commands.
- Branding: service first, Ace publisher clear, no official Suno/Google claim. The current official manifest has no custom icon/category/keyword field; the gallery uses repository publisher avatar and manifest/source metadata. Do not invent unsupported fields or unrelated search terms.
- No hooks, no local dependency installation, no automatic paid operation.

## Gates

1. Review and merge the implementation PR into `main` (human authorization; not performed here).
2. Apply the topics only after `main` contains the tested package, optionally create a version-matching GitHub release from the reviewed commit. The self-contained archive is available from CI; do not publish a release pointing at empty main.
3. Check the ordinary command `gemini extensions install https://github.com/AceDataCloud/SunoGemini` in an isolated home. Review-branch/local installs are separate evidence.
4. After the daily crawler, search the official gallery for `suno`, `music` and `suno-by-ace-data-cloud`, check publisher AceDataCloud, and install from that result. Record date, card URL and exact source/version. This is required before claiming official discoverability.
5. Paid music and terminal-media/billing checks need a separately authorized operation or an existing successful task ID; never generate just to populate a screenshot.

## Native model-provider boundary

This extension adds Suno tools; it does not add an Ace main-model option. Current official AuthDialog has Google, Gemini API Key and Vertex AI. The maintainer stated Gemini-model/endpoint focus in https://github.com/google-gemini/gemini-cli/issues/1515#issuecomment-3145970081 . A native provider feature PR needs an existing maintainer-approved feature issue and the Google CLA under https://github.com/google-gemini/gemini-cli/blob/main/CONTRIBUTING.md . No agreement is signed by this package.
