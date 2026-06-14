# Bootstrap Memory Prompt

Copy the block below into your AI assistant. The assistant must reply using exactly the four Markdown sections requested at the end.

```text
You are helping populate the DevMemory AI memory store for an existing software project.

Detected technologies: Node.js / JavaScript / TypeScript, Python, Java / Kotlin (Maven/Gradle), .NET / C#, C / C++, FastAPI (Python).

Tracked files (these are the only files DevMemory AI has approved for analysis):
- .github/workflows/ci.yml
- # precheck.py
- alembic.ini
- api_server.py
- assignment_generator.py
- audit_kb.py
- book_new/CheatSheetSeries/LICENSE.md
- book_new/CheatSheetSeries/Makefile
- book_new/CheatSheetSeries/package.json
- book_new/CheatSheetSeries/README.md
- book_new/CheatSheetSeries/requirements.txt
- book_new/CheatSheetSeries/scripts/Generate_CheatSheets_TOC.py
- book_new/CheatSheetSeries/scripts/Generate_RSS_Feed.py
- book_new/CheatSheetSeries/scripts/Generate_Technologies_JSON.py
- book_new/CheatSheetSeries/scripts/Identify_Old_Issue_And_PR.py
- book_new/CheatSheetSeries/scripts/Update_CheatSheets_Index.py
- book_new/container-security-checklist/LICENSE
- book_new/container-security-checklist/README.md
- book_new/dostackbufferoverflowgood/dostackbufferoverflowgood/dostackbufferoverflowgood.sln
- book_new/dostackbufferoverflowgood/dostackbufferoverflowgood/dostackbufferoverflowgood/dostackbufferoverflowgood.c
- book_new/dostackbufferoverflowgood/dostackbufferoverflowgood/dostackbufferoverflowgood/dostackbufferoverflowgood.h
- book_new/dostackbufferoverflowgood/dostackbufferoverflowgood/dostackbufferoverflowgood/LICENSE
- book_new/dostackbufferoverflowgood/dostackbufferoverflowgood/dostackbufferoverflowgood/stdafx.c
- book_new/dostackbufferoverflowgood/dostackbufferoverflowgood/dostackbufferoverflowgood/stdafx.h
- book_new/dostackbufferoverflowgood/dostackbufferoverflowgood/dostackbufferoverflowgood/targetver.h
- book_new/dostackbufferoverflowgood/Makefile
- book_new/dostackbufferoverflowgood/README.md
- book_new/owasp-mstg/.github/scripts/check_duplicate_ids.py
- book_new/owasp-mstg/CHANGELOG.md
- book_new/owasp-mstg/Crackmes/README.md
- book_new/owasp-mstg/demos/android/MASVS-AUTH/MASTG-DEMO-0089/AndroidManifest.xml
- book_new/owasp-mstg/demos/android/MASVS-AUTH/MASTG-DEMO-0090/AndroidManifest.xml
- book_new/owasp-mstg/demos/android/MASVS-CODE/MASTG-DEMO-0050/build.gradle.kts
- book_new/owasp-mstg/demos/android/MASVS-NETWORK/MASTG-DEMO-0056/AndroidManifest.xml
- book_new/owasp-mstg/demos/android/MASVS-NETWORK/MASTG-DEMO-0057/AndroidManifest.xml
- book_new/owasp-mstg/demos/android/MASVS-PLATFORM/MASTG-DEMO-0029/AndroidManifest.xml
- book_new/owasp-mstg/demos/android/MASVS-PLATFORM/MASTG-DEMO-0030/AndroidManifest.xml
- book_new/owasp-mstg/demos/android/MASVS-PLATFORM/MASTG-DEMO-0030/server.py
- book_new/owasp-mstg/demos/android/MASVS-PLATFORM/MASTG-DEMO-0031/AndroidManifest.xml
- book_new/owasp-mstg/demos/android/MASVS-PLATFORM/MASTG-DEMO-0032/AndroidManifest.xml
- book_new/owasp-mstg/demos/android/MASVS-PLATFORM/MASTG-DEMO-0040/AndroidManifest.xml
- book_new/owasp-mstg/demos/android/MASVS-PLATFORM/MASTG-DEMO-0078/AndroidManifest.xml
- book_new/owasp-mstg/demos/android/MASVS-PLATFORM/MASTG-DEMO-0082/AndroidManifest.xml
- book_new/owasp-mstg/demos/android/MASVS-PRIVACY/MASTG-DEMO-0009/mitm_sensitive_logger.py
- book_new/owasp-mstg/demos/android/MASVS-PRIVACY/MASTG-DEMO-0033/AndroidManifest.xml
- book_new/owasp-mstg/demos/android/MASVS-RESILIENCE/MASTG-DEMO-0027/AndroidManifest.xml
- book_new/owasp-mstg/demos/android/MASVS-RESILIENCE/MASTG-DEMO-0028/AndroidManifest.xml
- book_new/owasp-mstg/demos/android/MASVS-RESILIENCE/MASTG-DEMO-0087/AndroidManifest.xml
- book_new/owasp-mstg/demos/android/MASVS-STORAGE/MASTG-DEMO-0003/AndroidManifest.xml
- book_new/owasp-mstg/demos/android/MASVS-STORAGE/MASTG-DEMO-0020/AndroidManifest.xml
- book_new/owasp-mstg/Document/CHANGELOG.md
- book_new/owasp-mstg/README.md
- book_new/owasp-mstg/src/contributors.py
- book_new/owasp-mstg/src/README.md
- book_new/owasp-mstg/src/scripts/combine_data_for_checklist.py
- book_new/owasp-mstg/src/scripts/excel_styles_and_validation.py
- book_new/owasp-mstg/src/scripts/requirements.txt
- book_new/owasp-mstg/src/scripts/testcase_diff.py
- book_new/owasp-mstg/src/scripts/tools_healthcheck.py
- book_new/owasp-mstg/src/scripts/yaml_to_excel.py
- book_new/OWASP-Testing-Guide/README.md
- CHANGELOG.md
- checker.py
- code_review.py
- config.py
- confirm.py
- context_budget.py
- courses.py
- daily_challenge.py
- db.py
- di.py
- docs/ГАЙД_VM.md
- docs/план релиза.md
- docs/помощь.md
- docs/adr/0001-lazy-loader.md
- docs/adr/0002-hybrid-rag.md
- docs/adr/0003-llm-caching.md
- docs/adr/0004-singleton-state.md
- docs/adr/0005-rate-limiting.md
- docs/BACKLOG.md
- docs/cyberteacher_vision_ideas_masterfile.md
- docs/DEPLOYMENT_GUIDE.md
- docs/DONE.md
- docs/FROZEN.md
- docs/IDEAS.md
- docs/PLAN_v5.md
- docs/PROBLEMS.md
- docs/ROADMAP.md
- export_project.py
- generators.py
- handlers/__init__.py
- handlers/achievements.py
- handlers/analytics.py
- handlers/api_handler.py
- handlers/assignment_templates.py
- handlers/async_handler.py
- handlers/bug_bounty.py
- handlers/chat.py
- handlers/code_review_v2.py
- handlers/code_scan.py
- handlers/config.py
- handlers/core.py
- handlers/ctf_flags.py
- handlers/cve.py
- handlers/daily.py
- handlers/dashboard.py
- handlers/docker_gen.py
- handlers/emotions.py
- handlers/equipment.py
- handlers/exploit_submit.py
- handlers/exploit_trainer.py
- handlers/export_extended.py
- handlers/features.py
- handlers/flags.py
- handlers/health.py
- handlers/hints.py
- handlers/history.py
- handlers/htb.py
- handlers/investigation.py
- handlers/jupyter.py
- handlers/kb_manager.py
- handlers/lang.py
- handlers/malware_analysis.py
- handlers/media.py
- handlers/mermaid.py
- handlers/metasploit.py
- handlers/mindmap.py
- handlers/misc.py
- handlers/missions.py
- handlers/mood.py
- handlers/network.py
- handlers/news.py
- handlers/offline.py
- handlers/osint.py
- handlers/pcap_analyzer.py
- handlers/phishing.py
- handlers/practice.py
- handlers/profile.py
- handlers/pwa.py
- handlers/quiz.py
- handlers/registry.py
- handlers/sandbox.py
- handlers/shodan_censys.py
- handlers/shop.py
- handlers/skills.py
- handlers/social.py
- handlers/subscribe.py
- handlers/summarize.py
- handlers/summary.py
- handlers/sync.py
- handlers/telegram_bot.py
- handlers/theme.py
- handlers/threats.py
- handlers/timeloop.py
- handlers/tracks.py
- handlers/tryhackme.py
- handlers/versus.py
- handlers/vision.py
- handlers/voice_stt.py
- handlers/voice.py
- handlers/walkthroughs.py
- handlers/writeup_auto.py
- i18n.py
- index_project.py
- knowledge.py
- labs.py
- launcher.py
- main.py
- mcp_server_faiss.py
- mcp_server.py
- memory.py
- migrations/env.py
- migrations/versions/01fcfe442709_initial_schema.py
- migrations/versions/8ff380d95f4a_add_app_state_table.py
- models/__init__.py
- models/achievements_state.py
- models/explanation_state.py
- models/hints_state.py
- models/learning_state.py
- models/metrics_state.py
- models/persona_state.py
- models/progress_state.py
- models/risk_state.py
- models/settings_state.py
- models/shop_state.py
- models/state_models.py
- models/user_profile_state.py
- models/user_state.py
- models/voice_state.py
- news_fetcher.py
- ollama_client.py
- pedagogy.py
- practice.py
- pyproject.toml
- question_generation.py
- quiz_generator.py
- README.md
- requirements.txt
- run_all_tests.py
- search_faiss.py

_116 additional tracked files omitted from this list._

Rules:
- Do not include any secrets, credentials, tokens, environment variables, certificates, private keys, or local database paths.
- Do not invent facts. If something is unclear or unverified, write "Unknown".
- Base your analysis only on the tracked files above and on file contents the user explicitly shares with you.
- If you do not have access to the file contents yet, ask the user to paste the relevant files. Do not guess.
- Keep each section compact, factual, and actionable.

Reply using EXACTLY these four Markdown sections, in this order, with these exact headings (no extras, no surrounding prose):

## PROJECT_SUMMARY
One short paragraph describing what this project is, who it serves, and the main technology stack.

## ARCHITECTURE
Bullet list (or short prose) covering main modules, boundaries, and data flow.

## CURRENT_STATE
Bullets describing what is working, what is in progress, and known issues.

## NEXT_ACTIONS
Bullet list of concrete near-term actions the next AI session should take.
```

After the AI replies, copy the full response and click "Save Project Understanding" in the DevMemory AI sidebar.
