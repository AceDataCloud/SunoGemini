---
name: suno-music
description: Create Suno songs, instrumental music, custom lyrics and covers through Ace Data Cloud in Gemini CLI, or retrieve the result of an existing Suno task. Use the installed Suno MCP tools; do not use for model-provider configuration.
---

# Suno music with Ace Data Cloud

## Choose the workflow

Use the `suno-by-ace-data-cloud` MCP server. Gemini CLI may prefix its tool names; select the tools actually loaded in the session.

- Setup/reference check: `suno_list_models`, `suno_list_actions`, or `suno_get_lyric_format_guide`. These return reference text, not an API generation result or proof of sufficient balance.
- A song from a prompt: `suno_generate_music`.
- User-written lyrics/style/title: `suno_generate_custom_music`.
- Extend or cover an existing authorized audio: `suno_extend_music` or `suno_cover_music`.
- Retrieve an existing task: `suno_get_task`; multiple known IDs: `suno_get_tasks_batch`.

## Before creating audio

Check the live tool schema and current model/service documentation; do not copy a dated model list or promise an unsupported duration. Confirm genre/mood, vocals versus instrumental, and any lyrics the user wants. For existing audio, verify the user has the rights needed for the requested use. Do not upload, clone a voice, train a model, or expand to a different paid action implicitly.

Use the requested generation only when its current price and the user's budget cover it. A reference check is a good first step when generation has not been authorized. Model inference in Gemini CLI and Ace music tool usage are billed separately.

Authentication is the native extension password setting `Ace Data Cloud Suno API Token`, stored by Gemini CLI. For setup, direct the user to the extension README and `gemini extensions config suno-by-ace-data-cloud`. Never read credential stores, print tokens, request tokens in a prompt, or bypass key restrictions.

## Submit once and follow the same task

1. Submit the chosen operation once. Record the returned task ID and trace ID if present.
2. Query `suno_get_task(task_id=...)` with that same ID. Keep pending/processing distinct from terminal complete/failed. Follow any server pacing guidance; when a bounded wait expires, return the task ID for later lookup.
3. On success, return the actual audio URLs and available title/metadata. On failure, preserve the service error and task ID. Do not claim a playable song until the task is successful and an audio URL exists.
4. Do not restart generation when a query fails, times out, or remains pending. A fresh paid submission requires a fresh user decision. If the user provided an old task ID, perform only its lookup.

## Errors

401: check the native extension Key setting and token expiry. 403: inspect the actual permission/moderation message. Balance failures require current balance review. For 429 or 5xx, keep the existing task/trace ID and do not automatically submit another generation. Report errors without revealing keys or private account data.
