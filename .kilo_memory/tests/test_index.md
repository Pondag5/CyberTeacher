# Test Index — tests/
# Source: /workspace/app/tests/ (85 files)

## By category
API/integration: test_api_integration, test_integration, test_integration_achievements,
  test_integration_analytics, test_integration_daily, test_integration_flag
Knowledge/RAG: test_knowledge, test_faiss_rerank
State/models: test_state, test_user_state, test_shop_state, test_types, test_settings,
  test_config, test_di
Handlers: test_handlers_core, test_handlers_flags, test_handlers_misc,
  test_handlers_news, test_handlers_practice, test_handlers_quiz, test_handlers_sandbox,
  test_handlers_story, test_handlers_writeup_auto, test_batch1-5_handlers
Services: test_services, test_spaced_repetition, test_weak_topics (n/a)
Story/risk: test_e2e_story_risk_factions, test_risk_integration, test_stability_integration,
  test_timeloop
PWA: test_pwa, test_docker_pwa, test_web_ui
Security: test_security_audit, test_bug_bounty, test_cve_handler, test_shodan_censys,
  test_osint, test_phishing_handler, test_malware_analysis, test_metasploit, test_htb,
  test_tryhackme
Other: test_achievements, test_achievements_c13, test_adaptive, test_analytics,
  test_auth_roles_courses, test_behavior_profile, test_code_review_v2, test_context_handler,
  test_core_helpers, test_ctf_flags, test_daily_challenge, test_dashboard, test_doctor_handler,
  test_event_engine, test_exploit_trainer, test_features_handler, test_health_handler,
  test_hints_handler, test_history, test_htb, test_i18n, test_jupyter, test_lang_handler,
  test_llm_integration, test_media, test_memory, test_missions_handler, test_mood_handler,
  test_new_features, test_numeric_menu_fix, test_offline_handler, test_pcap_analyzer,
  test_persona_router, test_profile_handler, test_quiz_generator, test_sandbox,
  test_scorm_export, test_summary, test_sync, test_theme_handler, test_threats_groups,
  test_threat_summary, test_tracks, test_versus, tools-tests

## Testing approach
- unittest.TestCase classes
- TestClient (FastAPI) for API integration tests
- Temporary directories + env vars (DB_FILE, STATE_FILE) for isolation
- setUpClass/tearDownClass pattern with importlib.reload of config/memory/state/api_server

## Known status (AGENTS.md)
105+ passed в ключевых модулях (knowledge, quiz, mood, persona, memory, services)
ruff 0, mypy 0
