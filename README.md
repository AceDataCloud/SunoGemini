# Suno by Ace Data Cloud for Gemini CLI

Create Suno songs, instrumental music, custom lyrics and covers from Gemini CLI, then retrieve results using the original task ID. This independent extension is provided by **Ace Data Cloud**; it is not an official Suno or Google product.

[简体中文](readme/README_zh_Hans.md) · [Current API and pricing](https://platform.acedata.cloud/models?utm_source=gemini-cli&utm_medium=referral&utm_campaign=evergreen&utm_content=sunogemini_readme_pricing)

## 1. Install the extension

Install [Google Gemini CLI](https://geminicli.com/docs/get-started/installation/) and complete its current model authentication first. Tested with **Gemini CLI 0.64.0**. Google currently directs unpaid-tier / Google One users to [Antigravity CLI](https://github.com/google-gemini/gemini-cli#readme); this extension targets Gemini CLI and does not claim Antigravity compatibility.

Install the released extension from its public repository:

```bash
gemini extensions install https://github.com/AceDataCloud/SunoGemini
```

For a reproducible installation, select version **v0.1.0**:

```bash
gemini extensions install https://github.com/AceDataCloud/SunoGemini --ref v0.1.0
```

The official gallery indexes tagged public extension repositories independently. A release or successful installation does not prove that its search card has appeared. [Versioned release](https://github.com/AceDataCloud/SunoGemini/releases/tag/v0.1.0) · [Official gallery](https://geminicli.com/extensions/).

Read the extension consent information. It connects only to the hosted Suno MCP endpoint, loads a Suno workflow skill and adds `/suno-check` and `/suno-task`. It has no hooks or local server dependency. Installing does not generate music.

Look for **suno-by-ace-data-cloud**, published from **AceDataCloud/SunoGemini**. The brand keywords are Suno, music, songs, lyrics and covers; this does not imply affiliation with Suno.

## 2. Get an Ace API Token

1. [Register or sign in to Ace Data Cloud](https://platform.acedata.cloud?utm_source=gemini-cli&utm_medium=referral&utm_campaign=evergreen&utm_content=sunogemini_readme_register).
2. Open [Applications](https://platform.acedata.cloud/console/applications?utm_source=gemini-cli&utm_medium=referral&utm_campaign=evergreen&utm_content=sunogemini_readme_api_key). If **General application** does not exist, initialize it. Check Suno access and the current balance. A service application's key is limited to its service; a general key uses services the account is entitled to access.
3. Copy the **API KEY** value from the application card, or open **Manage Keys → Create** for a separate key named `Gemini CLI Suno`.

![Copy a masked application Key or open Manage Keys](_assets/tutorial/get-api-key-en.png)

4. Review expiration, usage limits and **Allowed APIs**. For the basic song and task workflow, allow `/suno/audios` and `/suno/tasks`. Grant only the operations you intend to call. Check [current pricing](https://platform.acedata.cloud/models?utm_source=gemini-cli&utm_medium=referral&utm_campaign=evergreen&utm_content=sunogemini_readme_before_run) before a paid operation.

![Optional dedicated API key](_assets/tutorial/create-api-key-en.png)

The screenshot's example name is from an existing Dify tutorial; use `Gemini CLI Suno` here. It is a real shared Ace key-management screen, not a Gemini installation result. Original capture date was not published; retrieved and reviewed 2026-10-18. [Image sources and limitations](_assets/tutorial/sources.json).

Copy the raw token only: no `Bearer ` prefix, quotes or masked screenshot characters. A `platform-...` account-management token cannot replace a service API key. Trial allowances and account permissions are whatever your current account shows.

## 3. Paste the Token in Gemini CLI

During installation Gemini CLI asks for **Ace Data Cloud Suno API Token** as a password. Paste the raw value there, never into the chat prompt. The manifest marks this setting `sensitive: true`; Gemini CLI uses its native secret storage (OS keychain where supported, its secure fallback otherwise).

To change or enter it later:

```bash
gemini extensions config suno-by-ace-data-cloud "Ace Data Cloud Suno API Token"
```

The extension-specific variable is `ACEDATACLOUD_SUNO_TOKEN`. You do not need to hand-edit `settings.json` or configure an MCP URL. This Token authenticates the music tools; it does not change Gemini CLI's model provider, Google login or model subscription.

Restart the Gemini session after installation/configuration. Check:

```bash
gemini extensions list
gemini mcp list
```

Expect the extension and its `suno-by-ace-data-cloud` server to be listed as enabled/connected. If your administrator disables extensions/MCP, use the normal administrator process rather than bypassing it.

![Official Gemini CLI interface reference, edited preview](_assets/tutorial/gemini-cli-reference.png)

**Official screenshot edit, not an Ace execution screenshot.** Edited 2026-10-17; original asset updated 2025-12-01, capture date and CLI version not specified. Type requests in the bottom input; view replies/tool results above. The shown `WriteFile`, Hello World and “2 MCP servers” belong to Google's example, not this extension. This image does not show the Suno password prompt or prove installation. Actual Suno installation/reference-check evidence is recorded in [VALIDATION.md](VALIDATION.md); no generated song is claimed.

## 4. First use: reference check without music generation

In Gemini CLI enter:

```text
/suno-check
```

This activates the Suno skill and asks `suno_list_models` for reference information only. It does not call a music-generation API. Your configured Gemini model can still have its own inference cost. A reference response proves the tool connection, not paid generation access, balance or billing.

You can also ask: “Use Suno by Ace Data Cloud to show the lyric format guide. Do not generate music.” Actual tool names can include Gemini CLI's server prefix.

## 5. Create music, then follow the same task

After checking current price and authorizing the specific operation, ask for a song, for example:

> Use Suno by Ace Data Cloud to create an instrumental lo-fi track about a quiet evening. Show the chosen model, parameters and current cost before submitting.

The skill selects `suno_generate_music` or `suno_generate_custom_music` using the current tool schema. **Submit once.** Preserve the returned task ID. Query `suno_get_task` until complete or failed; pending/processing is not success. A bounded wait may end before generation does.

For a task you already submitted:

```text
/suno-task YOUR_ORIGINAL_TASK_ID
```

This retrieves that task; it does not submit a new generation. Reuse the same ID after a timeout. On success, inspect the returned audio URLs and media. Do not rerun generation to poll. A connected tool, task ID or green CLI turn is not a completed song or proof of a unique consumption record.

## Included tools

Reference: `suno_list_models`, `suno_list_actions`, `suno_get_lyric_format_guide`.

Music: `suno_generate_music`, `suno_generate_custom_music`, `suno_extend_music`, `suno_cover_music`.

Task results: `suno_get_task`, `suno_get_tasks_batch`.

The package intentionally does not expose voice cloning, uploads, custom-model training or deletion tools. For other Suno workflows use the maintained [Suno MCP](https://github.com/AceDataCloud/SunoMCP) and its current documentation.

## Common problems

| Symptom | Check |
|---|---|
| 401 / token required | Run `gemini extensions config`, use the raw service key and check expiry. |
| 403 | Read the actual permission/moderation message; check Suno access and Allowed APIs. |
| No password prompt | Ensure Gemini CLI extension settings are enabled; use the config command. Do not paste keys in chat. |
| Missing tools | Restart, inspect `gemini extensions list`, `gemini mcp list` and administrator policy. A pre-existing settings entry with the same server name takes precedence. |
| Pending / timeout | Keep and query the original task ID; do not regenerate. |
| 429 / 5xx / task failed | Preserve task/trace ID; inspect the returned error before any new paid submission. |
| Audio URL does not play | Confirm terminal success and inspect the actual returned URL; installation tests are not a media playback test. |

Ace tool usage and your Gemini model usage have separate pricing. Check [Applications and usage](https://platform.acedata.cloud/console/applications?utm_source=gemini-cli&utm_medium=referral&utm_campaign=evergreen&utm_content=sunogemini_readme_usage). Consumption is measured in Credits; USD conversion uses the current package price divided by amount. No registration, usage or revenue result is claimed by this repository.

## Maintain, update and remove

```bash
gemini extensions update suno-by-ace-data-cloud
gemini extensions uninstall suno-by-ace-data-cloud
```

[Hosted service source](https://github.com/AceDataCloud/SunoMCP) · [Official extension mechanism](https://geminicli.com/docs/extensions/releasing/) · [Validation and release boundary](VALIDATION.md)

Extension code: MIT; official screenshot derivative: Apache-2.0, see [notices](THIRD_PARTY_NOTICES.md). Suno and Google/Gemini names identify the integrated service and target client; their marks belong to their respective owners. Ace Data Cloud provides this integration independently.
