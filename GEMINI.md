# Suno by Ace Data Cloud

This independent extension connects Suno music tools through Ace Data Cloud. It does not change Gemini CLI's model provider or Google sign-in. It is not affiliated with or endorsed by Suno or Google.

Use the bundled `suno-music` skill for Suno music requests. First-time checks should call only `suno_list_models` or `suno_get_lyric_format_guide`; these return reference information and do not generate music. Inspect current tool schemas and the current service price before a generation. The Token is configured through native extension settings; never ask the user to paste it in chat or expose it in output.

Submit a generation only within the user's requested operation and budget. Preserve its task ID. Poll `suno_get_task` with the same ID until terminal success or failure; never call a generation tool to poll. A submitted ID, connected server, or green CLI turn is not a completed song. On timeout, retain the task ID for a later lookup and do not automatically regenerate.

For an old task supplied by the user, query only that ID. Read-only task lookup does not grant generation permission. Show the terminal state and returned audio URLs; do not invent a result or claim that references prove a paid API/billing check.
