# Session End Prompt

Copy the block below into your AI assistant at the end of a coding session. The assistant must reply with exactly the eight Markdown sections requested below.

```text
Summarize this AI coding session for DevMemory AI.

Rules:
- Record only durable project memory, not conversation filler.
- Do not include secrets, credentials, tokens, certificates, private keys, environment variables, or local database paths.
- Do not invent facts. If something did not happen in this session, write "None".
- Keep each section short and objective.

Reply using EXACTLY these eight Markdown sections, in this order, with these exact headings:

## SESSION_SUMMARY
One short paragraph stating what this session accomplished.

## CHANGES_MADE
Bullet list of concrete code or configuration changes.

## FILES_TOUCHED
Bullet list of file paths that were created or modified.

## DECISIONS
Bullet list of durable decisions (write "None" if no notable decisions were made).

## BUGS_FIXED
Bullet list of bugs fixed, each with one-line root cause (write "None" if no bugs were fixed).

## COMMANDS_RUN
Bullet list of relevant commands run during the session (write "None" if not applicable).

## CURRENT_STATE
Bullets describing what is working, what is in progress, and known issues after this session.

## NEXT_ACTIONS
Bullet list of concrete near-term actions for the next session.
```

After the AI replies, copy the full response and click "Save Session Summary" in the DevMemory AI sidebar.
