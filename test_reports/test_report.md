# CyberTeacher Test Report
**Date:** 2026-05-29T00:03:55.691944
**Total test files:** 85
**Total test cases:** 576
**Failures:** 22
**Errors:** 340
**Skipped:** 5

## Summary per file
| File | Total | Failures | Errors | Skipped | Status |
|------|-------|----------|--------|---------|--------|
| tests\test_achievements.py | 0 | 0 | 1 | 0 | IMPORT_ERROR |
| tests\test_achievements_c13.py | 14 | 6 | 4 | 0 | OK |
| tests\test_adaptive.py | 13 | 0 | 12 | 0 | OK |
| tests\test_analytics.py | 0 | 0 | 1 | 0 | IMPORT_ERROR |
| tests\test_api_integration.py | 12 | 12 | 0 | 0 | OK |
| tests\test_basic.py | 4 | 0 | 0 | 1 | OK |
| tests\test_batch1_handlers.py | 20 | 0 | 20 | 0 | OK |
| tests\test_batch2_handlers.py | 28 | 0 | 26 | 0 | OK |
| tests\test_batch3_handlers.py | 32 | 0 | 27 | 0 | OK |
| tests\test_batch4_handlers.py | 20 | 0 | 16 | 0 | OK |
| tests\test_batch5_handlers.py | 13 | 0 | 13 | 0 | OK |
| tests\test_bug_bounty.py | 0 | 0 | 1 | 0 | IMPORT_ERROR |
| tests\test_code_review_v2.py | 57 | 0 | 0 | 0 | OK |
| tests\test_config.py | 2 | 0 | 0 | 0 | OK |
| tests\test_core_helpers.py | 0 | 0 | 1 | 0 | IMPORT_ERROR |
| tests\test_ctf_flags.py | 0 | 0 | 1 | 0 | IMPORT_ERROR |
| tests\test_cve_handler.py | 0 | 0 | 1 | 0 | IMPORT_ERROR |
| tests\test_daily_challenge.py | 10 | 0 | 0 | 0 | OK |
| tests\test_dashboard.py | 0 | 0 | 1 | 0 | IMPORT_ERROR |
| tests\test_di.py | 14 | 0 | 0 | 0 | OK |
| tests\test_docker_pwa.py | 5 | 0 | 5 | 0 | OK |
| tests\test_exploit_trainer.py | 0 | 0 | 1 | 0 | IMPORT_ERROR |
| tests\test_faiss_rerank.py | 0 | 0 | 1 | 0 | IMPORT_ERROR |
| tests\test_features_handler.py | 12 | 0 | 10 | 0 | OK |
| tests\test_handlers_core.py | 0 | 0 | 1 | 0 | IMPORT_ERROR |
| tests\test_handlers_flags.py | 9 | 0 | 9 | 0 | OK |
| tests\test_handlers_misc.py | 30 | 0 | 30 | 0 | OK |
| tests\test_handlers_news.py | 6 | 0 | 6 | 0 | OK |
| tests\test_handlers_practice.py | 8 | 0 | 8 | 0 | OK |
| tests\test_handlers_quiz.py | 18 | 0 | 18 | 0 | OK |
| tests\test_handlers_sandbox.py | 15 | 0 | 15 | 0 | OK |
| tests\test_handlers_story.py | 14 | 0 | 0 | 0 | OK |
| tests\test_handlers_writeup_auto.py | 6 | 0 | 6 | 0 | OK |
| tests\test_health_handler.py | 3 | 0 | 3 | 0 | OK |
| tests\test_hints_handler.py | 0 | 0 | 1 | 0 | IMPORT_ERROR |
| tests\test_history.py | 0 | 0 | 1 | 0 | IMPORT_ERROR |
| tests\test_htb.py | 17 | 0 | 17 | 0 | OK |
| tests\test_i18n.py | 10 | 0 | 0 | 0 | OK |
| tests\test_integration.py | 17 | 0 | 1 | 0 | OK |
| tests\test_integration_achievements.py | 2 | 0 | 2 | 0 | OK |
| tests\test_integration_analytics.py | 0 | 0 | 1 | 0 | IMPORT_ERROR |
| tests\test_integration_daily.py | 0 | 0 | 1 | 0 | IMPORT_ERROR |
| tests\test_integration_flag.py | 3 | 0 | 3 | 0 | OK |
| tests\test_investigation.py | 0 | 0 | 1 | 0 | IMPORT_ERROR |
| tests\test_jupyter.py | 0 | 0 | 1 | 0 | IMPORT_ERROR |
| tests\test_knowledge.py | 0 | 0 | 1 | 0 | IMPORT_ERROR |
| tests\test_lang_handler.py | 0 | 0 | 1 | 0 | IMPORT_ERROR |
| tests\test_llm_integration.py | 4 | 0 | 0 | 4 | OK |
| tests\test_malware_analysis.py | 0 | 0 | 1 | 0 | IMPORT_ERROR |
| tests\test_media.py | 0 | 0 | 1 | 0 | IMPORT_ERROR |
| tests\test_memory.py | 10 | 1 | 0 | 0 | OK |
| tests\test_metasploit.py | 6 | 0 | 6 | 0 | OK |
| tests\test_missions_handler.py | 0 | 0 | 1 | 0 | IMPORT_ERROR |
| tests\test_new_features.py | 0 | 0 | 1 | 0 | IMPORT_ERROR |
| tests\test_numeric_menu_fix.py | 0 | 0 | 1 | 0 | IMPORT_ERROR |
| tests\test_osint.py | 0 | 0 | 1 | 0 | IMPORT_ERROR |
| tests\test_pcap_analyzer.py | 0 | 0 | 1 | 0 | IMPORT_ERROR |
| tests\test_phishing_handler.py | 0 | 0 | 1 | 0 | IMPORT_ERROR |
| tests\test_profile_handler.py | 0 | 0 | 1 | 0 | IMPORT_ERROR |
| tests\test_pwa.py | 0 | 0 | 1 | 0 | IMPORT_ERROR |
| tests\test_quiz_generator.py | 6 | 0 | 0 | 0 | OK |
| tests\test_remaining_features.py | 0 | 0 | 1 | 0 | IMPORT_ERROR |
| tests\test_risk_integration.py | 0 | 0 | 1 | 0 | IMPORT_ERROR |
| tests\test_sandbox.py | 0 | 0 | 1 | 0 | IMPORT_ERROR |
| tests\test_services.py | 23 | 0 | 0 | 0 | OK |
| tests\test_settings.py | 8 | 0 | 0 | 0 | OK |
| tests\test_shodan_censys.py | 0 | 0 | 1 | 0 | IMPORT_ERROR |
| tests\test_shop.py | 0 | 0 | 1 | 0 | IMPORT_ERROR |
| tests\test_shop_state.py | 8 | 0 | 0 | 0 | OK |
| tests\test_skills_handler.py | 0 | 0 | 1 | 0 | IMPORT_ERROR |
| tests\test_social.py | 0 | 0 | 1 | 0 | IMPORT_ERROR |
| tests\test_spaced_repetition.py | 14 | 2 | 11 | 0 | OK |
| tests\test_state.py | 38 | 1 | 12 | 0 | OK |
| tests\test_summary.py | 0 | 0 | 1 | 0 | IMPORT_ERROR |
| tests\test_sync.py | 0 | 0 | 1 | 0 | IMPORT_ERROR |
| tests\test_theme_handler.py | 0 | 0 | 1 | 0 | IMPORT_ERROR |
| tests\test_threats_groups.py | 0 | 0 | 1 | 0 | IMPORT_ERROR |
| tests\test_threat_summary.py | 0 | 0 | 1 | 0 | IMPORT_ERROR |
| tests\test_timeloop.py | 0 | 0 | 1 | 0 | IMPORT_ERROR |
| tests\test_tracks.py | 32 | 0 | 16 | 0 | OK |
| tests\test_tryhackme.py | 0 | 0 | 1 | 0 | IMPORT_ERROR |
| tests\test_user_state.py | 6 | 0 | 0 | 0 | OK |
| tests\test_voice.py | 0 | 0 | 1 | 0 | IMPORT_ERROR |
| tests\test_voice_stt.py | 0 | 0 | 1 | 0 | IMPORT_ERROR |
| tests\test_web_ui.py | 7 | 0 | 0 | 0 | OK |

## Detailed failures and errors
### IMPORT ERROR: tests\test_achievements.py
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\run_all_tests.py", line 76, in run_test_file
    module = importlib.import_module(module_name)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1406, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 938, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 759, in exec_module
  File "<frozen importlib._bootstrap>", line 491, in _call_with_frames_removed
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_achievements.py", line 9, in <module>
    from handlers.achievements import handle_achievements
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\__init__.py", line 14, in <module>
    from .core import (  # основной диспетчер
        handle_commands,
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\core.py", line 30, in <module>
    from .misc import (
    ...<25 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\misc.py", line 15, in <module>
    from generators import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\generators.py", line 8, in <module>
    from knowledge import get_relevant_docs
  File "M:\Cyber_Teacher\Cyber_Teacher\knowledge.py", line 9, in <module>
    from langchain.text_splitter import RecursiveCharacterTextSplitter
ModuleNotFoundError: No module named 'langchain.text_splitter'

```

### tests\test_achievements_c13.py
**ERROR**: `test_achievements_not_awarded_twice (tests.test_achievements_c13.TestAchievementsC13.test_achievements_not_awarded_twice)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_achievements_c13.py", line 100, in test_achievements_not_awarded_twice
    self.state.increment_social_success()
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'AppState' object has no attribute 'increment_social_success'

```

**FAIL**: `test_apt_hunter_achievement_unlocked (tests.test_achievements_c13.TestAchievementsC13.test_apt_hunter_achievement_unlocked)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_achievements_c13.py", line 52, in test_apt_hunter_achievement_unlocked
    self.assertIn("apt_hunter_10", self.state.earned_achievements)
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'apt_hunter_10' not found in []

```

**FAIL**: `test_apt_hunter_expert_achievement (tests.test_achievements_c13.TestAchievementsC13.test_apt_hunter_expert_achievement)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_achievements_c13.py", line 58, in test_apt_hunter_expert_achievement
    self.assertIn("apt_hunter_25", self.state.earned_achievements)
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'apt_hunter_25' not found in []

```

**FAIL**: `test_ghost_in_the_shell_achievement_unlocked (tests.test_achievements_c13.TestAchievementsC13.test_ghost_in_the_shell_achievement_unlocked)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_achievements_c13.py", line 70, in test_ghost_in_the_shell_achievement_unlocked
    self.assertIn("ghost_in_the_shell_5", self.state.earned_achievements)
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'ghost_in_the_shell_5' not found in []

```

**FAIL**: `test_ghost_in_the_shell_legend_achievement (tests.test_achievements_c13.TestAchievementsC13.test_ghost_in_the_shell_legend_achievement)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_achievements_c13.py", line 76, in test_ghost_in_the_shell_legend_achievement
    self.assertIn("ghost_in_the_shell_15", self.state.earned_achievements)
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'ghost_in_the_shell_15' not found in []

```

**FAIL**: `test_snowden_achievement_unlocked (tests.test_achievements_c13.TestAchievementsC13.test_snowden_achievement_unlocked)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_achievements_c13.py", line 88, in test_snowden_achievement_unlocked
    self.assertIn("snowden_10", self.state.earned_achievements)
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'snowden_10' not found in []

```

**FAIL**: `test_snowden_legend_achievement (tests.test_achievements_c13.TestAchievementsC13.test_snowden_legend_achievement)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_achievements_c13.py", line 94, in test_snowden_legend_achievement
    self.assertIn("snowden_25", self.state.earned_achievements)
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'snowden_25' not found in []

```

**ERROR**: `test_social_engineer_achievement_unlocked (tests.test_achievements_c13.TestAchievementsC13.test_social_engineer_achievement_unlocked)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_achievements_c13.py", line 31, in test_social_engineer_achievement_unlocked
    self.state.increment_social_success()
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'AppState' object has no attribute 'increment_social_success'

```

**ERROR**: `test_social_engineer_master_achievement (tests.test_achievements_c13.TestAchievementsC13.test_social_engineer_master_achievement)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_achievements_c13.py", line 39, in test_social_engineer_master_achievement
    self.state.increment_social_success()
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'AppState' object has no attribute 'increment_social_success'

```

**ERROR**: `test_social_success_counter (tests.test_achievements_c13.TestAchievementsC13.test_social_success_counter)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_achievements_c13.py", line 25, in test_social_success_counter
    self.state.increment_social_success()
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'AppState' object has no attribute 'increment_social_success'

```

### tests\test_adaptive.py
**ERROR**: `test_handle_adaptive_with_no_weak_topics (tests.test_adaptive.TestAdaptiveCommand.test_handle_adaptive_with_no_weak_topics)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_adaptive.py", line 136, in test_handle_adaptive_with_no_weak_topics
    from handlers.misc import handle_adaptive
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\__init__.py", line 14, in <module>
    from .core import (  # основной диспетчер
        handle_commands,
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\core.py", line 30, in <module>
    from .misc import (
    ...<25 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\misc.py", line 15, in <module>
    from generators import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\generators.py", line 8, in <module>
    from knowledge import get_relevant_docs
  File "M:\Cyber_Teacher\Cyber_Teacher\knowledge.py", line 9, in <module>
    from langchain.text_splitter import RecursiveCharacterTextSplitter
ModuleNotFoundError: No module named 'langchain.text_splitter'

```

**ERROR**: `test_handle_adaptive_with_weak_topics (tests.test_adaptive.TestAdaptiveCommand.test_handle_adaptive_with_weak_topics)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_adaptive.py", line 148, in test_handle_adaptive_with_weak_topics
    from handlers.misc import handle_adaptive
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\__init__.py", line 14, in <module>
    from .core import (  # основной диспетчер
        handle_commands,
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\core.py", line 30, in <module>
    from .misc import (
    ...<25 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\misc.py", line 15, in <module>
    from generators import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\generators.py", line 8, in <module>
    from knowledge import get_relevant_docs
  File "M:\Cyber_Teacher\Cyber_Teacher\knowledge.py", line 9, in <module>
    from langchain.text_splitter import RecursiveCharacterTextSplitter
ModuleNotFoundError: No module named 'langchain.text_splitter'

```

**ERROR**: `test_clear_weak_topics (tests.test_adaptive.TestAdaptiveLearning.test_clear_weak_topics)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_adaptive.py", line 92, in test_clear_weak_topics
    self.state.update_weak_topic("sql", 50, 100)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^
TypeError: AppState.update_weak_topic() takes 3 positional arguments but 4 were given

```

**ERROR**: `test_get_next_weak_topic_returns_none_when_all_good (tests.test_adaptive.TestAdaptiveLearning.test_get_next_weak_topic_returns_none_when_all_good)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_adaptive.py", line 85, in test_get_next_weak_topic_returns_none_when_all_good
    self.state.update_weak_topic("sql", 80, 100)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^
TypeError: AppState.update_weak_topic() takes 3 positional arguments but 4 were given

```

**ERROR**: `test_get_next_weak_topic_returns_weakest (tests.test_adaptive.TestAdaptiveLearning.test_get_next_weak_topic_returns_weakest)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_adaptive.py", line 78, in test_get_next_weak_topic_returns_weakest
    self.state.update_weak_topic("sql", 30, 100)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^
TypeError: AppState.update_weak_topic() takes 3 positional arguments but 4 were given

```

**ERROR**: `test_get_weak_topics_filters_by_threshold (tests.test_adaptive.TestAdaptiveLearning.test_get_weak_topics_filters_by_threshold)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_adaptive.py", line 54, in test_get_weak_topics_filters_by_threshold
    self.state.update_weak_topic("sql", 50, 100)  # 50%
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^
TypeError: AppState.update_weak_topic() takes 3 positional arguments but 4 were given

```

**ERROR**: `test_get_weak_topics_sorted_by_success_rate (tests.test_adaptive.TestAdaptiveLearning.test_get_weak_topics_sorted_by_success_rate)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_adaptive.py", line 67, in test_get_weak_topics_sorted_by_success_rate
    self.state.update_weak_topic("sql", 30, 100)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^
TypeError: AppState.update_weak_topic() takes 3 positional arguments but 4 were given

```

**ERROR**: `test_save_and_load_weak_topics (tests.test_adaptive.TestAdaptiveLearning.test_save_and_load_weak_topics)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_adaptive.py", line 104, in test_save_and_load_weak_topics
    self.state.update_weak_topic("sql", 75, 100)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^
TypeError: AppState.update_weak_topic() takes 3 positional arguments but 4 were given

```

**ERROR**: `test_update_weak_topic_creates_new_entry (tests.test_adaptive.TestAdaptiveLearning.test_update_weak_topic_creates_new_entry)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_adaptive.py", line 19, in test_update_weak_topic_creates_new_entry
    self.state.update_weak_topic("sql", 8.0, 10.0)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^
TypeError: AppState.update_weak_topic() takes 3 positional arguments but 4 were given

```

**ERROR**: `test_update_weak_topic_multiple_topics (tests.test_adaptive.TestAdaptiveLearning.test_update_weak_topic_multiple_topics)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_adaptive.py", line 41, in test_update_weak_topic_multiple_topics
    self.state.update_weak_topic("sql", 5, 10)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^
TypeError: AppState.update_weak_topic() takes 3 positional arguments but 4 were given

```

**ERROR**: `test_update_weak_topic_updates_existing (tests.test_adaptive.TestAdaptiveLearning.test_update_weak_topic_updates_existing)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_adaptive.py", line 30, in test_update_weak_topic_updates_existing
    self.state.update_weak_topic("sql", 5.0, 10.0)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^
TypeError: AppState.update_weak_topic() takes 3 positional arguments but 4 were given

```

**ERROR**: `test_update_weak_topic_zero_max_score (tests.test_adaptive.TestAdaptiveLearning.test_update_weak_topic_zero_max_score)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_adaptive.py", line 121, in test_update_weak_topic_zero_max_score
    self.state.update_weak_topic("sql", 0, 0)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
TypeError: AppState.update_weak_topic() takes 3 positional arguments but 4 were given

```

### IMPORT ERROR: tests\test_analytics.py
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\run_all_tests.py", line 76, in run_test_file
    module = importlib.import_module(module_name)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1406, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 938, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 759, in exec_module
  File "<frozen importlib._bootstrap>", line 491, in _call_with_frames_removed
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_analytics.py", line 6, in <module>
    from handlers.analytics import (
    ...<3 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\__init__.py", line 14, in <module>
    from .core import (  # основной диспетчер
        handle_commands,
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\core.py", line 30, in <module>
    from .misc import (
    ...<25 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\misc.py", line 15, in <module>
    from generators import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\generators.py", line 8, in <module>
    from knowledge import get_relevant_docs
  File "M:\Cyber_Teacher\Cyber_Teacher\knowledge.py", line 9, in <module>
    from langchain.text_splitter import RecursiveCharacterTextSplitter
ModuleNotFoundError: No module named 'langchain.text_splitter'

```

### tests\test_api_integration.py
**FAIL**: `test_chat_endpoint_structure (tests.test_api_integration.TestAPIChatE2E.test_chat_endpoint_structure)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_api_integration.py", line 327, in test_chat_endpoint_structure
    self.assertEqual(response.status_code, 200)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 404 != 200

```

**FAIL**: `test_achievements_endpoint (tests.test_api_integration.TestAPIIntegration.test_achievements_endpoint)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_api_integration.py", line 111, in test_achievements_endpoint
    self.assertEqual(response.status_code, 200)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 404 != 200

```

**FAIL**: `test_courses_endpoint (tests.test_api_integration.TestAPIIntegration.test_courses_endpoint)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_api_integration.py", line 99, in test_courses_endpoint
    self.assertEqual(response.status_code, 200)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 404 != 200

```

**FAIL**: `test_health_endpoint (tests.test_api_integration.TestAPIIntegration.test_health_endpoint)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_api_integration.py", line 75, in test_health_endpoint
    self.assertEqual(response.status_code, 200)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 404 != 200

```

**FAIL**: `test_labs_endpoint (tests.test_api_integration.TestAPIIntegration.test_labs_endpoint)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_api_integration.py", line 155, in test_labs_endpoint
    self.assertEqual(response.status_code, 200)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 404 != 200

```

**FAIL**: `test_progress_endpoint (tests.test_api_integration.TestAPIIntegration.test_progress_endpoint)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_api_integration.py", line 89, in test_progress_endpoint
    self.assertEqual(response.status_code, 200)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 404 != 200

```

**FAIL**: `test_quiz_result_endpoint (tests.test_api_integration.TestAPIIntegration.test_quiz_result_endpoint)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_api_integration.py", line 147, in test_quiz_result_endpoint
    self.assertEqual(response.status_code, 200)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 404 != 200

```

**FAIL**: `test_select_course_endpoint (tests.test_api_integration.TestAPIIntegration.test_select_course_endpoint)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_api_integration.py", line 131, in test_select_course_endpoint
    self.assertEqual(response.status_code, 200)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 404 != 200

```

**FAIL**: `test_stats_endpoint (tests.test_api_integration.TestAPIIntegration.test_stats_endpoint)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_api_integration.py", line 120, in test_stats_endpoint
    self.assertEqual(response.status_code, 200)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 404 != 200

```

**FAIL**: `test_full_learning_cycle_api (tests.test_api_integration.TestAPILearningCycleE2E.test_full_learning_cycle_api)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_api_integration.py", line 269, in test_full_learning_cycle_api
    self.assertEqual(response.status_code, 200)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 404 != 200

```

**FAIL**: `test_versus_scenarios_endpoint (tests.test_api_integration.TestAPIVersusE2E.test_versus_scenarios_endpoint)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_api_integration.py", line 201, in test_versus_scenarios_endpoint
    self.assertEqual(response.status_code, 200)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 404 != 200

```

**FAIL**: `test_versus_start_stop_cycle (tests.test_api_integration.TestAPIVersusE2E.test_versus_start_stop_cycle)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_api_integration.py", line 210, in test_versus_start_stop_cycle
    self.assertEqual(response.status_code, 200)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 404 != 200

```

### tests\test_batch1_handlers.py
**ERROR**: `test_daily_hint (tests.test_batch1_handlers.TestDailyHandler.test_daily_hint)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_daily_show_challenge (tests.test_batch1_handlers.TestDailyHandler.test_daily_show_challenge)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_daily_status (tests.test_batch1_handlers.TestDailyHandler.test_daily_status)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_equip_exceeds_ram (tests.test_batch1_handlers.TestEquipmentHandler.test_equip_exceeds_ram)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_equip_toggle_off (tests.test_batch1_handlers.TestEquipmentHandler.test_equip_toggle_off)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_equip_tool (tests.test_batch1_handlers.TestEquipmentHandler.test_equip_tool)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_equip_unknown_tool (tests.test_batch1_handlers.TestEquipmentHandler.test_equip_unknown_tool)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_tools_list (tests.test_batch1_handlers.TestEquipmentHandler.test_tools_list)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_mermaid_generate_no_topic (tests.test_batch1_handlers.TestMermaidHandler.test_mermaid_generate_no_topic)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_mermaid_list (tests.test_batch1_handlers.TestMermaidHandler.test_mermaid_list)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_mermaid_no_args (tests.test_batch1_handlers.TestMermaidHandler.test_mermaid_no_args)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_mermaid_show_invalid (tests.test_batch1_handlers.TestMermaidHandler.test_mermaid_show_invalid)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_mermaid_show_no_topic (tests.test_batch1_handlers.TestMermaidHandler.test_mermaid_show_no_topic)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_mermaid_show_valid (tests.test_batch1_handlers.TestMermaidHandler.test_mermaid_show_valid)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_mermaid_unknown_subcommand (tests.test_batch1_handlers.TestMermaidHandler.test_mermaid_unknown_subcommand)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_build_ascii_tree_no_cycles (tests.test_batch1_handlers.TestMindmapHandler.test_build_ascii_tree_no_cycles)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_batch1_handlers.py", line 293, in test_build_ascii_tree_no_cycles
    from handlers.mindmap import _build_ascii_tree
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\__init__.py", line 14, in <module>
    from .core import (  # основной диспетчер
        handle_commands,
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\core.py", line 30, in <module>
    from .misc import (
    ...<25 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\misc.py", line 15, in <module>
    from generators import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\generators.py", line 8, in <module>
    from knowledge import get_relevant_docs
  File "M:\Cyber_Teacher\Cyber_Teacher\knowledge.py", line 9, in <module>
    from langchain.text_splitter import RecursiveCharacterTextSplitter
ModuleNotFoundError: No module named 'langchain.text_splitter'

```

**ERROR**: `test_mindmap_full_tree (tests.test_batch1_handlers.TestMindmapHandler.test_mindmap_full_tree)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_mindmap_help (tests.test_batch1_handlers.TestMindmapHandler.test_mindmap_help)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_mindmap_specific_topic (tests.test_batch1_handlers.TestMindmapHandler.test_mindmap_specific_topic)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_network_display (tests.test_batch1_handlers.TestNetworkHandler.test_network_display)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

### tests\test_batch2_handlers.py
**ERROR**: `test_code_scan_no_args (tests.test_batch2_handlers.TestCodeScanHandler.test_code_scan_no_args)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_dockergen_create_invalid (tests.test_batch2_handlers.TestDockerGenHandler.test_dockergen_create_invalid)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_dockergen_create_sqli (tests.test_batch2_handlers.TestDockerGenHandler.test_dockergen_create_sqli)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_dockergen_create_web (tests.test_batch2_handlers.TestDockerGenHandler.test_dockergen_create_web)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_dockergen_custom (tests.test_batch2_handlers.TestDockerGenHandler.test_dockergen_custom)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_dockergen_list (tests.test_batch2_handlers.TestDockerGenHandler.test_dockergen_list)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_dockergen_no_args (tests.test_batch2_handlers.TestDockerGenHandler.test_dockergen_no_args)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_dockergen_unknown_subcommand (tests.test_batch2_handlers.TestDockerGenHandler.test_dockergen_unknown_subcommand)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_exploit_submit_file_not_found (tests.test_batch2_handlers.TestExploitSubmitHandler.test_exploit_submit_file_not_found)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_exploit_submit_invalid_step (tests.test_batch2_handlers.TestExploitSubmitHandler.test_exploit_submit_invalid_step)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_exploit_submit_no_args (tests.test_batch2_handlers.TestExploitSubmitHandler.test_exploit_submit_no_args)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_exploit_submit_unsupported_ext (tests.test_batch2_handlers.TestExploitSubmitHandler.test_exploit_submit_unsupported_ext)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_htb_login_no_args (tests.test_batch2_handlers.TestHTBHandler.test_htb_login_no_args)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_htb_login_success (tests.test_batch2_handlers.TestHTBHandler.test_htb_login_success)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_htb_machine_invalid_id (tests.test_batch2_handlers.TestHTBHandler.test_htb_machine_invalid_id)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_htb_machine_no_id (tests.test_batch2_handlers.TestHTBHandler.test_htb_machine_no_id)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_htb_machines_no_type (tests.test_batch2_handlers.TestHTBHandler.test_htb_machines_no_type)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_htb_no_args_shows_help (tests.test_batch2_handlers.TestHTBHandler.test_htb_no_args_shows_help)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_htb_status (tests.test_batch2_handlers.TestHTBHandler.test_htb_status)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_htb_submit_invalid_id (tests.test_batch2_handlers.TestHTBHandler.test_htb_submit_invalid_id)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_htb_submit_no_args (tests.test_batch2_handlers.TestHTBHandler.test_htb_submit_no_args)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_htb_unknown_subcommand (tests.test_batch2_handlers.TestHTBHandler.test_htb_unknown_subcommand)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_exploit_cve_not_found (tests.test_batch2_handlers.TestWalkthroughsHandler.test_exploit_cve_not_found)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_exploit_no_query (tests.test_batch2_handlers.TestWalkthroughsHandler.test_exploit_no_query)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_exploit_non_cve_query (tests.test_batch2_handlers.TestWalkthroughsHandler.test_exploit_non_cve_query)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_walkthrough_no_topic (tests.test_batch2_handlers.TestWalkthroughsHandler.test_walkthrough_no_topic)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

### tests\test_batch3_handlers.py
**ERROR**: `test_emotions_auto (tests.test_batch3_handlers.TestEmotionsHandler.test_emotions_auto)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_emotions_no_args (tests.test_batch3_handlers.TestEmotionsHandler.test_emotions_no_args)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_emotions_set_happy (tests.test_batch3_handlers.TestEmotionsHandler.test_emotions_set_happy)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_emotions_set_invalid (tests.test_batch3_handlers.TestEmotionsHandler.test_emotions_set_invalid)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_emotions_show (tests.test_batch3_handlers.TestEmotionsHandler.test_emotions_show)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_get_emotion_prompt_modifier_auto (tests.test_batch3_handlers.TestEmotionsHandler.test_get_emotion_prompt_modifier_auto)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_get_emotion_status (tests.test_batch3_handlers.TestEmotionsHandler.test_get_emotion_status)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_get_kb_status_empty (tests.test_batch3_handlers.TestKBManagerHandler.test_get_kb_status_empty)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_batch3_handlers.py", line 331, in test_get_kb_status_empty
    from handlers.kb_manager import _get_kb_status
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\__init__.py", line 14, in <module>
    from .core import (  # основной диспетчер
        handle_commands,
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\core.py", line 30, in <module>
    from .misc import (
    ...<25 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\misc.py", line 15, in <module>
    from generators import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\generators.py", line 8, in <module>
    from knowledge import get_relevant_docs
  File "M:\Cyber_Teacher\Cyber_Teacher\knowledge.py", line 9, in <module>
    from langchain.text_splitter import RecursiveCharacterTextSplitter
ModuleNotFoundError: No module named 'langchain.text_splitter'

```

**ERROR**: `test_kb_help (tests.test_batch3_handlers.TestKBManagerHandler.test_kb_help)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_kb_status (tests.test_batch3_handlers.TestKBManagerHandler.test_kb_status)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_kb_unknown_subcommand (tests.test_batch3_handlers.TestKBManagerHandler.test_kb_unknown_subcommand)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_subscribe_add_invalid (tests.test_batch3_handlers.TestSubscribeHandler.test_subscribe_add_invalid)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_subscribe_add_valid (tests.test_batch3_handlers.TestSubscribeHandler.test_subscribe_add_valid)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_subscribe_help (tests.test_batch3_handlers.TestSubscribeHandler.test_subscribe_help)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_subscribe_list_empty (tests.test_batch3_handlers.TestSubscribeHandler.test_subscribe_list_empty)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_subscribe_notify_empty (tests.test_batch3_handlers.TestSubscribeHandler.test_subscribe_notify_empty)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_subscribe_unknown_subcommand (tests.test_batch3_handlers.TestSubscribeHandler.test_subscribe_unknown_subcommand)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_telegram_help (tests.test_batch3_handlers.TestTelegramBotHandler.test_telegram_help)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_telegram_start_no_token (tests.test_batch3_handlers.TestTelegramBotHandler.test_telegram_start_no_token)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_telegram_status (tests.test_batch3_handlers.TestTelegramBotHandler.test_telegram_status)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_telegram_stop_not_running (tests.test_batch3_handlers.TestTelegramBotHandler.test_telegram_stop_not_running)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_telegram_unknown_subcommand (tests.test_batch3_handlers.TestTelegramBotHandler.test_telegram_unknown_subcommand)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_vision_analysis_dict_not_empty (tests.test_batch3_handlers.TestVisionHandler.test_vision_analysis_dict_not_empty)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_batch3_handlers.py", line 298, in test_vision_analysis_dict_not_empty
    from handlers.vision import VISION_ANALYSIS
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\__init__.py", line 14, in <module>
    from .core import (  # основной диспетчер
        handle_commands,
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\core.py", line 30, in <module>
    from .misc import (
    ...<25 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\misc.py", line 15, in <module>
    from generators import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\generators.py", line 8, in <module>
    from knowledge import get_relevant_docs
  File "M:\Cyber_Teacher\Cyber_Teacher\knowledge.py", line 9, in <module>
    from langchain.text_splitter import RecursiveCharacterTextSplitter
ModuleNotFoundError: No module named 'langchain.text_splitter'

```

**ERROR**: `test_vision_analyze_file_not_found (tests.test_batch3_handlers.TestVisionHandler.test_vision_analyze_file_not_found)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_vision_help (tests.test_batch3_handlers.TestVisionHandler.test_vision_help)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_vision_ocr_file_not_found (tests.test_batch3_handlers.TestVisionHandler.test_vision_ocr_file_not_found)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_vision_unknown_subcommand (tests.test_batch3_handlers.TestVisionHandler.test_vision_unknown_subcommand)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

### tests\test_batch4_handlers.py
**ERROR**: `test_api_empty (tests.test_batch4_handlers.TestAPIHandler.test_api_empty)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_api_help (tests.test_batch4_handlers.TestAPIHandler.test_api_help)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_api_start (tests.test_batch4_handlers.TestAPIHandler.test_api_start)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_api_status (tests.test_batch4_handlers.TestAPIHandler.test_api_status)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_api_stop (tests.test_batch4_handlers.TestAPIHandler.test_api_stop)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_api_unknown (tests.test_batch4_handlers.TestAPIHandler.test_api_unknown)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_async_combined_query_both_fail (tests.test_batch4_handlers.TestAsyncHandler.test_async_combined_query_both_fail)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_batch4_handlers.py", line 93, in test_async_combined_query_both_fail
    from handlers.async_handler import async_combined_query
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\__init__.py", line 14, in <module>
    from .core import (  # основной диспетчер
        handle_commands,
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\core.py", line 30, in <module>
    from .misc import (
    ...<25 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\misc.py", line 15, in <module>
    from generators import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\generators.py", line 8, in <module>
    from knowledge import get_relevant_docs
  File "M:\Cyber_Teacher\Cyber_Teacher\knowledge.py", line 9, in <module>
    from langchain.text_splitter import RecursiveCharacterTextSplitter
ModuleNotFoundError: No module named 'langchain.text_splitter'

```

**ERROR**: `test_async_combined_query_rag_success (tests.test_batch4_handlers.TestAsyncHandler.test_async_combined_query_rag_success)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_batch4_handlers.py", line 108, in test_async_combined_query_rag_success
    from handlers.async_handler import async_combined_query
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\__init__.py", line 14, in <module>
    from .core import (  # основной диспетчер
        handle_commands,
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\core.py", line 30, in <module>
    from .misc import (
    ...<25 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\misc.py", line 15, in <module>
    from generators import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\generators.py", line 8, in <module>
    from knowledge import get_relevant_docs
  File "M:\Cyber_Teacher\Cyber_Teacher\knowledge.py", line 9, in <module>
    from langchain.text_splitter import RecursiveCharacterTextSplitter
ModuleNotFoundError: No module named 'langchain.text_splitter'

```

**ERROR**: `test_async_llm_call_error (tests.test_batch4_handlers.TestAsyncHandler.test_async_llm_call_error)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_batch4_handlers.py", line 82, in test_async_llm_call_error
    from handlers.async_handler import async_llm_call
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\__init__.py", line 14, in <module>
    from .core import (  # основной диспетчер
        handle_commands,
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\core.py", line 30, in <module>
    from .misc import (
    ...<25 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\misc.py", line 15, in <module>
    from generators import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\generators.py", line 8, in <module>
    from knowledge import get_relevant_docs
  File "M:\Cyber_Teacher\Cyber_Teacher\knowledge.py", line 9, in <module>
    from langchain.text_splitter import RecursiveCharacterTextSplitter
ModuleNotFoundError: No module named 'langchain.text_splitter'

```

**ERROR**: `test_async_rag_search_error (tests.test_batch4_handlers.TestAsyncHandler.test_async_rag_search_error)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_batch4_handlers.py", line 71, in test_async_rag_search_error
    from handlers.async_handler import async_rag_search
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\__init__.py", line 14, in <module>
    from .core import (  # основной диспетчер
        handle_commands,
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\core.py", line 30, in <module>
    from .misc import (
    ...<25 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\misc.py", line 15, in <module>
    from generators import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\generators.py", line 8, in <module>
    from knowledge import get_relevant_docs
  File "M:\Cyber_Teacher\Cyber_Teacher\knowledge.py", line 9, in <module>
    from langchain.text_splitter import RecursiveCharacterTextSplitter
ModuleNotFoundError: No module named 'langchain.text_splitter'

```

**ERROR**: `test_run_async_query_no_loop (tests.test_batch4_handlers.TestAsyncHandler.test_run_async_query_no_loop)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_batch4_handlers.py", line 120, in test_run_async_query_no_loop
    from handlers.async_handler import run_async_query
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\__init__.py", line 14, in <module>
    from .core import (  # основной диспетчер
        handle_commands,
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\core.py", line 30, in <module>
    from .misc import (
    ...<25 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\misc.py", line 15, in <module>
    from generators import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\generators.py", line 8, in <module>
    from knowledge import get_relevant_docs
  File "M:\Cyber_Teacher\Cyber_Teacher\knowledge.py", line 9, in <module>
    from langchain.text_splitter import RecursiveCharacterTextSplitter
ModuleNotFoundError: No module named 'langchain.text_splitter'

```

**ERROR**: `test_export_extended_html (tests.test_batch4_handlers.TestExportExtendedHandler.test_export_extended_html)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_export_extended_no_args (tests.test_batch4_handlers.TestExportExtendedHandler.test_export_extended_no_args)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_export_extended_unknown_format (tests.test_batch4_handlers.TestExportExtendedHandler.test_export_extended_unknown_format)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_generate_summary_llm_unavailable (tests.test_batch4_handlers.TestSummarizeHandler.test_generate_summary_llm_unavailable)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_batch4_handlers.py", line 241, in test_generate_summary_llm_unavailable
    from handlers.summarize import _generate_summary
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\__init__.py", line 14, in <module>
    from .core import (  # основной диспетчер
        handle_commands,
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\core.py", line 30, in <module>
    from .misc import (
    ...<25 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\misc.py", line 15, in <module>
    from generators import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\generators.py", line 8, in <module>
    from knowledge import get_relevant_docs
  File "M:\Cyber_Teacher\Cyber_Teacher\knowledge.py", line 9, in <module>
    from langchain.text_splitter import RecursiveCharacterTextSplitter
ModuleNotFoundError: No module named 'langchain.text_splitter'

```

**ERROR**: `test_summarize_short_history (tests.test_batch4_handlers.TestSummarizeHandler.test_summarize_short_history)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

### tests\test_batch5_handlers.py
**ERROR**: `test_default_templates_have_required_keys (tests.test_batch5_handlers.TestAssignmentTemplatesHandler.test_default_templates_have_required_keys)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_batch5_handlers.py", line 82, in test_default_templates_have_required_keys
    from handlers.assignment_templates import DEFAULT_TEMPLATES
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\__init__.py", line 14, in <module>
    from .core import (  # основной диспетчер
        handle_commands,
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\core.py", line 30, in <module>
    from .misc import (
    ...<25 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\misc.py", line 15, in <module>
    from generators import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\generators.py", line 8, in <module>
    from knowledge import get_relevant_docs
  File "M:\Cyber_Teacher\Cyber_Teacher\knowledge.py", line 9, in <module>
    from langchain.text_splitter import RecursiveCharacterTextSplitter
ModuleNotFoundError: No module named 'langchain.text_splitter'

```

**ERROR**: `test_default_templates_not_empty (tests.test_batch5_handlers.TestAssignmentTemplatesHandler.test_default_templates_not_empty)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_batch5_handlers.py", line 78, in test_default_templates_not_empty
    from handlers.assignment_templates import DEFAULT_TEMPLATES
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\__init__.py", line 14, in <module>
    from .core import (  # основной диспетчер
        handle_commands,
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\core.py", line 30, in <module>
    from .misc import (
    ...<25 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\misc.py", line 15, in <module>
    from generators import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\generators.py", line 8, in <module>
    from knowledge import get_relevant_docs
  File "M:\Cyber_Teacher\Cyber_Teacher\knowledge.py", line 9, in <module>
    from langchain.text_splitter import RecursiveCharacterTextSplitter
ModuleNotFoundError: No module named 'langchain.text_splitter'

```

**ERROR**: `test_templates_generate_invalid (tests.test_batch5_handlers.TestAssignmentTemplatesHandler.test_templates_generate_invalid)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_templates_generate_valid (tests.test_batch5_handlers.TestAssignmentTemplatesHandler.test_templates_generate_valid)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_templates_list (tests.test_batch5_handlers.TestAssignmentTemplatesHandler.test_templates_list)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_templates_no_args (tests.test_batch5_handlers.TestAssignmentTemplatesHandler.test_templates_no_args)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_templates_show_invalid (tests.test_batch5_handlers.TestAssignmentTemplatesHandler.test_templates_show_invalid)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_templates_show_valid (tests.test_batch5_handlers.TestAssignmentTemplatesHandler.test_templates_show_valid)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_groups_no_threats_dir (tests.test_batch5_handlers.TestThreatsHandler.test_groups_no_threats_dir)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_threat_summary_llm_unavailable (tests.test_batch5_handlers.TestThreatsHandler.test_threat_summary_llm_unavailable)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_threat_summary_no_news (tests.test_batch5_handlers.TestThreatsHandler.test_threat_summary_no_news)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_threats_group_not_found (tests.test_batch5_handlers.TestThreatsHandler.test_threats_group_not_found)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_threats_no_args (tests.test_batch5_handlers.TestThreatsHandler.test_threats_no_args)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

### IMPORT ERROR: tests\test_bug_bounty.py
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\run_all_tests.py", line 76, in run_test_file
    module = importlib.import_module(module_name)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1406, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 938, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 759, in exec_module
  File "<frozen importlib._bootstrap>", line 491, in _call_with_frames_removed
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_bug_bounty.py", line 8, in <module>
    from handlers.bug_bounty import handle_bounty, _select_scenario, _get_llm_review
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\__init__.py", line 14, in <module>
    from .core import (  # основной диспетчер
        handle_commands,
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\core.py", line 30, in <module>
    from .misc import (
    ...<25 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\misc.py", line 15, in <module>
    from generators import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\generators.py", line 8, in <module>
    from knowledge import get_relevant_docs
  File "M:\Cyber_Teacher\Cyber_Teacher\knowledge.py", line 9, in <module>
    from langchain.text_splitter import RecursiveCharacterTextSplitter
ModuleNotFoundError: No module named 'langchain.text_splitter'

```

### IMPORT ERROR: tests\test_core_helpers.py
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\run_all_tests.py", line 76, in run_test_file
    module = importlib.import_module(module_name)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1406, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 938, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 759, in exec_module
  File "<frozen importlib._bootstrap>", line 491, in _call_with_frames_removed
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_core_helpers.py", line 8, in <module>
    from handlers.core import (
    ...<6 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\__init__.py", line 14, in <module>
    from .core import (  # основной диспетчер
        handle_commands,
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\core.py", line 30, in <module>
    from .misc import (
    ...<25 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\misc.py", line 15, in <module>
    from generators import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\generators.py", line 8, in <module>
    from knowledge import get_relevant_docs
  File "M:\Cyber_Teacher\Cyber_Teacher\knowledge.py", line 9, in <module>
    from langchain.text_splitter import RecursiveCharacterTextSplitter
ModuleNotFoundError: No module named 'langchain.text_splitter'

```

### IMPORT ERROR: tests\test_ctf_flags.py
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\run_all_tests.py", line 76, in run_test_file
    module = importlib.import_module(module_name)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1406, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 938, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 759, in exec_module
  File "<frozen importlib._bootstrap>", line 491, in _call_with_frames_removed
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_ctf_flags.py", line 8, in <module>
    from handlers.ctf_flags import (
    ...<6 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\__init__.py", line 14, in <module>
    from .core import (  # основной диспетчер
        handle_commands,
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\core.py", line 30, in <module>
    from .misc import (
    ...<25 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\misc.py", line 15, in <module>
    from generators import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\generators.py", line 8, in <module>
    from knowledge import get_relevant_docs
  File "M:\Cyber_Teacher\Cyber_Teacher\knowledge.py", line 9, in <module>
    from langchain.text_splitter import RecursiveCharacterTextSplitter
ModuleNotFoundError: No module named 'langchain.text_splitter'

```

### IMPORT ERROR: tests\test_cve_handler.py
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\run_all_tests.py", line 76, in run_test_file
    module = importlib.import_module(module_name)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1406, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 938, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 759, in exec_module
  File "<frozen importlib._bootstrap>", line 491, in _call_with_frames_removed
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_cve_handler.py", line 8, in <module>
    from handlers.cve import _cve_cache, handle_cve
ImportError: cannot import name '_cve_cache' from 'handlers.cve' (M:\Cyber_Teacher\Cyber_Teacher\handlers\cve.py)

```

### IMPORT ERROR: tests\test_dashboard.py
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\run_all_tests.py", line 76, in run_test_file
    module = importlib.import_module(module_name)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1406, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 938, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 759, in exec_module
  File "<frozen importlib._bootstrap>", line 491, in _call_with_frames_removed
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_dashboard.py", line 8, in <module>
    from handlers.dashboard import handle_dashboard
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\__init__.py", line 14, in <module>
    from .core import (  # основной диспетчер
        handle_commands,
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\core.py", line 30, in <module>
    from .misc import (
    ...<25 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\misc.py", line 15, in <module>
    from generators import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\generators.py", line 8, in <module>
    from knowledge import get_relevant_docs
  File "M:\Cyber_Teacher\Cyber_Teacher\knowledge.py", line 9, in <module>
    from langchain.text_splitter import RecursiveCharacterTextSplitter
ModuleNotFoundError: No module named 'langchain.text_splitter'

```

### tests\test_docker_pwa.py
**ERROR**: `test_list_containers (tests.test_docker_pwa.TestDockerContainers.test_list_containers)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1439, in patched
    return func(*newargs, **newkeywargs)
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_docker_pwa.py", line 51, in test_list_containers
    result = docker_containers()
TypeError: APIRouter.api_route.<locals>.decorator() missing 1 required positional argument: 'func'

```

**ERROR**: `test_no_containers (tests.test_docker_pwa.TestDockerContainers.test_no_containers)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1439, in patched
    return func(*newargs, **newkeywargs)
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_docker_pwa.py", line 59, in test_no_containers
    result = docker_containers()
TypeError: APIRouter.api_route.<locals>.decorator() missing 1 required positional argument: 'func'

```

**ERROR**: `test_docker_available (tests.test_docker_pwa.TestDockerStatus.test_docker_available)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_docker_not_available (tests.test_docker_pwa.TestDockerStatus.test_docker_not_available)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1439, in patched
    return func(*newargs, **newkeywargs)
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_docker_pwa.py", line 30, in test_docker_not_available
    result = docker_status()
TypeError: APIRouter.api_route.<locals>.decorator() missing 1 required positional argument: 'func'

```

**ERROR**: `test_docker_not_installed (tests.test_docker_pwa.TestDockerStatus.test_docker_not_installed)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1439, in patched
    return func(*newargs, **newkeywargs)
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_docker_pwa.py", line 37, in test_docker_not_installed
    result = docker_status()
TypeError: APIRouter.api_route.<locals>.decorator() missing 1 required positional argument: 'func'

```

### IMPORT ERROR: tests\test_exploit_trainer.py
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\run_all_tests.py", line 76, in run_test_file
    module = importlib.import_module(module_name)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1406, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 938, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 759, in exec_module
  File "<frozen importlib._bootstrap>", line 491, in _call_with_frames_removed
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_exploit_trainer.py", line 6, in <module>
    from handlers.exploit_trainer import (
    ...<6 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\__init__.py", line 14, in <module>
    from .core import (  # основной диспетчер
        handle_commands,
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\core.py", line 30, in <module>
    from .misc import (
    ...<25 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\misc.py", line 15, in <module>
    from generators import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\generators.py", line 8, in <module>
    from knowledge import get_relevant_docs
  File "M:\Cyber_Teacher\Cyber_Teacher\knowledge.py", line 9, in <module>
    from langchain.text_splitter import RecursiveCharacterTextSplitter
ModuleNotFoundError: No module named 'langchain.text_splitter'

```

### IMPORT ERROR: tests\test_faiss_rerank.py
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\run_all_tests.py", line 76, in run_test_file
    module = importlib.import_module(module_name)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1406, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 938, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 759, in exec_module
  File "<frozen importlib._bootstrap>", line 491, in _call_with_frames_removed
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_faiss_rerank.py", line 15, in <module>
    from config import RERANK_TOP_K, RERANKER_MODEL, LazyLoader
ImportError: cannot import name 'RERANKER_MODEL' from 'config' (M:\Cyber_Teacher\Cyber_Teacher\config.py)

```

### tests\test_features_handler.py
**ERROR**: `test_disable_feature (tests.test_features_handler.TestFeaturesHandler.test_disable_feature)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_enable_feature (tests.test_features_handler.TestFeaturesHandler.test_enable_feature)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_enable_no_module_specified (tests.test_features_handler.TestFeaturesHandler.test_enable_no_module_specified)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_enable_unknown_feature (tests.test_features_handler.TestFeaturesHandler.test_enable_unknown_feature)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_is_feature_enabled_default (tests.test_features_handler.TestFeaturesHandler.test_is_feature_enabled_default)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_is_feature_enabled_from_state (tests.test_features_handler.TestFeaturesHandler.test_is_feature_enabled_from_state)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_list_features (tests.test_features_handler.TestFeaturesHandler.test_list_features)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_reset_features (tests.test_features_handler.TestFeaturesHandler.test_reset_features)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_toggle_feature (tests.test_features_handler.TestFeaturesHandler.test_toggle_feature)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_toggle_feature_off (tests.test_features_handler.TestFeaturesHandler.test_toggle_feature_off)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

### IMPORT ERROR: tests\test_handlers_core.py
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\run_all_tests.py", line 76, in run_test_file
    module = importlib.import_module(module_name)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1406, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 938, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 759, in exec_module
  File "<frozen importlib._bootstrap>", line 491, in _call_with_frames_removed
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_handlers_core.py", line 6, in <module>
    from handlers.core import handle_extended_commands
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\__init__.py", line 14, in <module>
    from .core import (  # основной диспетчер
        handle_commands,
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\core.py", line 30, in <module>
    from .misc import (
    ...<25 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\misc.py", line 15, in <module>
    from generators import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\generators.py", line 8, in <module>
    from knowledge import get_relevant_docs
  File "M:\Cyber_Teacher\Cyber_Teacher\knowledge.py", line 9, in <module>
    from langchain.text_splitter import RecursiveCharacterTextSplitter
ModuleNotFoundError: No module named 'langchain.text_splitter'

```

### tests\test_handlers_flags.py
**ERROR**: `test_handle_flag_check_active_assignment_completes_task (tests.test_handlers_flags.TestHandlersFlags.test_handle_flag_check_active_assignment_completes_task)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_handle_flag_check_active_assignment_failure (tests.test_handlers_flags.TestHandlersFlags.test_handle_flag_check_active_assignment_failure)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_handle_flag_check_active_assignment_success (tests.test_handlers_flags.TestHandlersFlags.test_handle_flag_check_active_assignment_success)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_handle_flag_check_global_flags_file_missing (tests.test_handlers_flags.TestHandlersFlags.test_handle_flag_check_global_flags_file_missing)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_handle_flag_check_global_flags_json_error (tests.test_handlers_flags.TestHandlersFlags.test_handle_flag_check_global_flags_json_error)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_handle_flag_check_global_flags_not_found (tests.test_handlers_flags.TestHandlersFlags.test_handle_flag_check_global_flags_not_found)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_handle_flag_check_global_flags_success (tests.test_handlers_flags.TestHandlersFlags.test_handle_flag_check_global_flags_success)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_handle_flag_check_invalid_format (tests.test_handlers_flags.TestHandlersFlags.test_handle_flag_check_invalid_format)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_handle_flag_check_no_flag (tests.test_handlers_flags.TestHandlersFlags.test_handle_flag_check_no_flag)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

### tests\test_handlers_misc.py
**ERROR**: `test_ask_confirm (tests.test_handlers_misc.TestMiscFunctions.test_ask_confirm)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_clear_chat_db_calls_clear (tests.test_handlers_misc.TestMiscFunctions.test_clear_chat_db_calls_clear)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_clear_chat_db_handles_exception (tests.test_handlers_misc.TestMiscFunctions.test_clear_chat_db_handles_exception)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_extract_json_block_empty (tests.test_handlers_misc.TestMiscFunctions.test_extract_json_block_empty)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_handlers_misc.py", line 37, in test_extract_json_block_empty
    from handlers.misc import extract_json_block
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\__init__.py", line 14, in <module>
    from .core import (  # основной диспетчер
        handle_commands,
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\core.py", line 30, in <module>
    from .misc import (
    ...<25 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\misc.py", line 15, in <module>
    from generators import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\generators.py", line 8, in <module>
    from knowledge import get_relevant_docs
  File "M:\Cyber_Teacher\Cyber_Teacher\knowledge.py", line 9, in <module>
    from langchain.text_splitter import RecursiveCharacterTextSplitter
ModuleNotFoundError: No module named 'langchain.text_splitter'

```

**ERROR**: `test_extract_json_block_nested (tests.test_handlers_misc.TestMiscFunctions.test_extract_json_block_nested)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_handlers_misc.py", line 30, in test_extract_json_block_nested
    from handlers.misc import extract_json_block
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\__init__.py", line 14, in <module>
    from .core import (  # основной диспетчер
        handle_commands,
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\core.py", line 30, in <module>
    from .misc import (
    ...<25 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\misc.py", line 15, in <module>
    from generators import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\generators.py", line 8, in <module>
    from knowledge import get_relevant_docs
  File "M:\Cyber_Teacher\Cyber_Teacher\knowledge.py", line 9, in <module>
    from langchain.text_splitter import RecursiveCharacterTextSplitter
ModuleNotFoundError: No module named 'langchain.text_splitter'

```

**ERROR**: `test_extract_json_block_no_backticks (tests.test_handlers_misc.TestMiscFunctions.test_extract_json_block_no_backticks)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_handlers_misc.py", line 23, in test_extract_json_block_no_backticks
    from handlers.misc import extract_json_block
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\__init__.py", line 14, in <module>
    from .core import (  # основной диспетчер
        handle_commands,
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\core.py", line 30, in <module>
    from .misc import (
    ...<25 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\misc.py", line 15, in <module>
    from generators import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\generators.py", line 8, in <module>
    from knowledge import get_relevant_docs
  File "M:\Cyber_Teacher\Cyber_Teacher\knowledge.py", line 9, in <module>
    from langchain.text_splitter import RecursiveCharacterTextSplitter
ModuleNotFoundError: No module named 'langchain.text_splitter'

```

**ERROR**: `test_extract_json_block_simple (tests.test_handlers_misc.TestMiscFunctions.test_extract_json_block_simple)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_handlers_misc.py", line 16, in test_extract_json_block_simple
    from handlers.misc import extract_json_block
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\__init__.py", line 14, in <module>
    from .core import (  # основной диспетчер
        handle_commands,
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\core.py", line 30, in <module>
    from .misc import (
    ...<25 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\misc.py", line 15, in <module>
    from generators import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\generators.py", line 8, in <module>
    from knowledge import get_relevant_docs
  File "M:\Cyber_Teacher\Cyber_Teacher\knowledge.py", line 9, in <module>
    from langchain.text_splitter import RecursiveCharacterTextSplitter
ModuleNotFoundError: No module named 'langchain.text_splitter'

```

**ERROR**: `test_handle_add_book_file_not_found (tests.test_handlers_misc.TestMiscFunctions.test_handle_add_book_file_not_found)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_handle_add_book_missing_args (tests.test_handlers_misc.TestMiscFunctions.test_handle_add_book_missing_args)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_handle_add_book_not_pdf (tests.test_handlers_misc.TestMiscFunctions.test_handle_add_book_not_pdf)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_handle_add_book_outside_knowledge_dir (tests.test_handlers_misc.TestMiscFunctions.test_handle_add_book_outside_knowledge_dir)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_handle_add_book_success (tests.test_handlers_misc.TestMiscFunctions.test_handle_add_book_success)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_handle_course_details (tests.test_handlers_misc.TestMiscFunctions.test_handle_course_details)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_handle_course_lists_courses (tests.test_handlers_misc.TestMiscFunctions.test_handle_course_lists_courses)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_handle_history_no_conn (tests.test_handlers_misc.TestMiscFunctions.test_handle_history_no_conn)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_handle_history_with_entries (tests.test_handlers_misc.TestMiscFunctions.test_handle_history_with_entries)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_handle_model_set (tests.test_handlers_misc.TestMiscFunctions.test_handle_model_set)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_handle_model_show_current (tests.test_handlers_misc.TestMiscFunctions.test_handle_model_show_current)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_handle_provider_invalid (tests.test_handlers_misc.TestMiscFunctions.test_handle_provider_invalid)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_handle_provider_show_current (tests.test_handlers_misc.TestMiscFunctions.test_handle_provider_show_current)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_handle_repeat_no_due (tests.test_handlers_misc.TestMiscFunctions.test_handle_repeat_no_due)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_handle_repeat_with_due (tests.test_handlers_misc.TestMiscFunctions.test_handle_repeat_with_due)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_handle_risk_display (tests.test_handlers_misc.TestMiscFunctions.test_handle_risk_display)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_handle_set_api_key_invalid_usage (tests.test_handlers_misc.TestMiscFunctions.test_handle_set_api_key_invalid_usage)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_handle_set_api_key_openrouter (tests.test_handlers_misc.TestMiscFunctions.test_handle_set_api_key_openrouter)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_handle_story_mode_list (tests.test_handlers_misc.TestMiscFunctions.test_handle_story_mode_list)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_handle_terminal_log_no_action (tests.test_handlers_misc.TestMiscFunctions.test_handle_terminal_log_no_action)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_handle_terminal_log_with_action (tests.test_handlers_misc.TestMiscFunctions.test_handle_terminal_log_with_action)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_handle_version (tests.test_handlers_misc.TestMiscFunctions.test_handle_version)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_handle_writeup_shows_template (tests.test_handlers_misc.TestMiscFunctions.test_handle_writeup_shows_template)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

### tests\test_handlers_news.py
**ERROR**: `test_get_last_news (tests.test_handlers_news.TestHandlersNews.test_get_last_news)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_handle_security_news_achievements_checked (tests.test_handlers_news.TestHandlersNews.test_handle_security_news_achievements_checked)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_handle_security_news_llm_exception_fallback (tests.test_handlers_news.TestHandlersNews.test_handle_security_news_llm_exception_fallback)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_handle_security_news_no_news (tests.test_handlers_news.TestHandlersNews.test_handle_security_news_no_news)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_handle_security_news_with_llm_success (tests.test_handlers_news.TestHandlersNews.test_handle_security_news_with_llm_success)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_handle_security_news_without_llm (tests.test_handlers_news.TestHandlersNews.test_handle_security_news_without_llm)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

### tests\test_handlers_practice.py
**ERROR**: `test_handle_container_check_no_labs (tests.test_handlers_practice.TestHandlersPractice.test_handle_container_check_no_labs)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_handle_container_check_with_labs (tests.test_handlers_practice.TestHandlersPractice.test_handle_container_check_with_labs)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_handle_practice_list (tests.test_handlers_practice.TestHandlersPractice.test_handle_practice_list)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1510, in __enter__
    original, local = self.get_original()
                      ~~~~~~~~~~~~~~~~~^^
  File "C:\Python314\Lib\unittest\mock.py", line 1480, in get_original
    raise AttributeError(
        "%s does not have the attribute %r" % (target, name)
    )
AttributeEr
```

**ERROR**: `test_handle_practice_start (tests.test_handlers_practice.TestHandlersPractice.test_handle_practice_start)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1510, in __enter__
    original, local = self.get_original()
                      ~~~~~~~~~~~~~~~~~^^
  File "C:\Python314\Lib\unittest\mock.py", line 1480, in get_original
    raise AttributeError(
        "%s does not have the attribute %r" % (target, name)
    )
AttributeEr
```

**ERROR**: `test_handle_practice_status_no_labs (tests.test_handlers_practice.TestHandlersPractice.test_handle_practice_status_no_labs)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_handle_practice_status_with_labs (tests.test_handlers_practice.TestHandlersPractice.test_handle_practice_status_with_labs)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_handle_practice_stop (tests.test_handlers_practice.TestHandlersPractice.test_handle_practice_stop)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1510, in __enter__
    original, local = self.get_original()
                      ~~~~~~~~~~~~~~~~~^^
  File "C:\Python314\Lib\unittest\mock.py", line 1480, in get_original
    raise AttributeError(
        "%s does not have the attribute %r" % (target, name)
    )
AttributeEr
```

**ERROR**: `test_handle_practice_usage (tests.test_handlers_practice.TestHandlersPractice.test_handle_practice_usage)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

### tests\test_handlers_quiz.py
**ERROR**: `test_check_open_answer_contains_correctly (tests.test_handlers_quiz.TestCheckOpenAnswer.test_check_open_answer_contains_correctly)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_handlers_quiz.py", line 605, in test_check_open_answer_contains_correctly
    from handlers.misc import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\__init__.py", line 14, in <module>
    from .core import (  # основной диспетчер
        handle_commands,
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\core.py", line 30, in <module>
    from .misc import (
    ...<25 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\misc.py", line 15, in <module>
    from generators import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\generators.py", line 8, in <module>
    from knowledge import get_relevant_docs
  File "M:\Cyber_Teacher\Cyber_Teacher\knowledge.py", line 9, in <module>
    from langchain.text_splitter import RecursiveCharacterTextSplitter
ModuleNotFoundError: No module named 'langchain.text_splitter'

```

**ERROR**: `test_check_open_answer_empty (tests.test_handlers_quiz.TestCheckOpenAnswer.test_check_open_answer_empty)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_handlers_quiz.py", line 593, in test_check_open_answer_empty
    from handlers.misc import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\__init__.py", line 14, in <module>
    from .core import (  # основной диспетчер
        handle_commands,
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\core.py", line 30, in <module>
    from .misc import (
    ...<25 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\misc.py", line 15, in <module>
    from generators import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\generators.py", line 8, in <module>
    from knowledge import get_relevant_docs
  File "M:\Cyber_Teacher\Cyber_Teacher\knowledge.py", line 9, in <module>
    from langchain.text_splitter import RecursiveCharacterTextSplitter
ModuleNotFoundError: No module named 'langchain.text_splitter'

```

**ERROR**: `test_check_open_answer_key_points (tests.test_handlers_quiz.TestCheckOpenAnswer.test_check_open_answer_key_points)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_handlers_quiz.py", line 612, in test_check_open_answer_key_points
    from handlers.misc import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\__init__.py", line 14, in <module>
    from .core import (  # основной диспетчер
        handle_commands,
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\core.py", line 30, in <module>
    from .misc import (
    ...<25 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\misc.py", line 15, in <module>
    from generators import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\generators.py", line 8, in <module>
    from knowledge import get_relevant_docs
  File "M:\Cyber_Teacher\Cyber_Teacher\knowledge.py", line 9, in <module>
    from langchain.text_splitter import RecursiveCharacterTextSplitter
ModuleNotFoundError: No module named 'langchain.text_splitter'

```

**ERROR**: `test_check_open_answer_non_empty (tests.test_handlers_quiz.TestCheckOpenAnswer.test_check_open_answer_non_empty)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_handlers_quiz.py", line 599, in test_check_open_answer_non_empty
    from handlers.misc import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\__init__.py", line 14, in <module>
    from .core import (  # основной диспетчер
        handle_commands,
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\core.py", line 30, in <module>
    from .misc import (
    ...<25 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\misc.py", line 15, in <module>
    from generators import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\generators.py", line 8, in <module>
    from knowledge import get_relevant_docs
  File "M:\Cyber_Teacher\Cyber_Teacher\knowledge.py", line 9, in <module>
    from langchain.text_splitter import RecursiveCharacterTextSplitter
ModuleNotFoundError: No module named 'langchain.text_splitter'

```

**ERROR**: `test_handle_code_review_stub (tests.test_handlers_quiz.TestHandlersQuiz.test_handle_code_review_stub)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_handle_quiz_action_multiple_choice_success (tests.test_handlers_quiz.TestHandlersQuiz.test_handle_quiz_action_multiple_choice_success)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_handle_quiz_action_no_generators (tests.test_handlers_quiz.TestHandlersQuiz.test_handle_quiz_action_no_generators)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_handle_quiz_action_no_questions_generated (tests.test_handlers_quiz.TestHandlersQuiz.test_handle_quiz_action_no_questions_generated)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_handle_quiz_action_open_ended (tests.test_handlers_quiz.TestHandlersQuiz.test_handle_quiz_action_open_ended)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_handle_quiz_action_risk_adjustment_low_score (tests.test_handlers_quiz.TestHandlersQuiz.test_handle_quiz_action_risk_adjustment_low_score)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_handle_quiz_action_stealth_ops_low_risk (tests.test_handlers_quiz.TestHandlersQuiz.test_handle_quiz_action_stealth_ops_low_risk)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_handle_quiz_action_with_skips_and_exit (tests.test_handlers_quiz.TestHandlersQuiz.test_handle_quiz_action_with_skips_and_exit)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_handle_quiz_action_with_weak_topic_focus (tests.test_handlers_quiz.TestHandlersQuiz.test_handle_quiz_action_with_weak_topic_focus)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_handle_quiz_generation_no_generators (tests.test_handlers_quiz.TestHandlersQuiz.test_handle_quiz_generation_no_generators)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_handle_quiz_generation_with_generators (tests.test_handlers_quiz.TestHandlersQuiz.test_handle_quiz_generation_with_generators)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_handle_task_action_no_generators (tests.test_handlers_quiz.TestHandlersQuiz.test_handle_task_action_no_generators)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_handle_task_action_skip (tests.test_handlers_quiz.TestHandlersQuiz.test_handle_task_action_skip)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_handle_task_action_success (tests.test_handlers_quiz.TestHandlersQuiz.test_handle_task_action_success)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

### tests\test_handlers_sandbox.py
**ERROR**: `test_handle_sandbox_execution_with_error (tests.test_handlers_sandbox.TestSandboxFunctions.test_handle_sandbox_execution_with_error)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_handle_sandbox_no_args (tests.test_handlers_sandbox.TestSandboxFunctions.test_handle_sandbox_no_args)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_handle_sandbox_no_output (tests.test_handlers_sandbox.TestSandboxFunctions.test_handle_sandbox_no_output)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_handle_sandbox_successful_execution (tests.test_handlers_sandbox.TestSandboxFunctions.test_handle_sandbox_successful_execution)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_handle_sandbox_validation_fails (tests.test_handlers_sandbox.TestSandboxFunctions.test_handle_sandbox_validation_fails)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_validate_code_bash_forbidden_etc (tests.test_handlers_sandbox.TestSandboxFunctions.test_validate_code_bash_forbidden_etc)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_handlers_sandbox.py", line 61, in test_validate_code_bash_forbidden_etc
    from handlers.sandbox import validate_code
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\__init__.py", line 14, in <module>
    from .core import (  # основной диспетчер
        handle_commands,
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\core.py", line 30, in <module>
    from .misc import (
    ...<25 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\misc.py", line 15, in <module>
    from generators import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\generators.py", line 8, in <module>
    from knowledge import get_relevant_docs
  File "M:\Cyber_Teacher\Cyber_Teacher\knowledge.py", line 9, in <module>
    from langchain.text_splitter import RecursiveCharacterTextSplitter
ModuleNotFoundError: No module named 'langchain.text_splitter'

```

**ERROR**: `test_validate_code_bash_forbidden_rm (tests.test_handlers_sandbox.TestSandboxFunctions.test_validate_code_bash_forbidden_rm)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_handlers_sandbox.py", line 47, in test_validate_code_bash_forbidden_rm
    from handlers.sandbox import validate_code
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\__init__.py", line 14, in <module>
    from .core import (  # основной диспетчер
        handle_commands,
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\core.py", line 30, in <module>
    from .misc import (
    ...<25 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\misc.py", line 15, in <module>
    from generators import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\generators.py", line 8, in <module>
    from knowledge import get_relevant_docs
  File "M:\Cyber_Teacher\Cyber_Teacher\knowledge.py", line 9, in <module>
    from langchain.text_splitter import RecursiveCharacterTextSplitter
ModuleNotFoundError: No module named 'langchain.text_splitter'

```

**ERROR**: `test_validate_code_bash_forbidden_sudo (tests.test_handlers_sandbox.TestSandboxFunctions.test_validate_code_bash_forbidden_sudo)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_handlers_sandbox.py", line 54, in test_validate_code_bash_forbidden_sudo
    from handlers.sandbox import validate_code
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\__init__.py", line 14, in <module>
    from .core import (  # основной диспетчер
        handle_commands,
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\core.py", line 30, in <module>
    from .misc import (
    ...<25 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\misc.py", line 15, in <module>
    from generators import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\generators.py", line 8, in <module>
    from knowledge import get_relevant_docs
  File "M:\Cyber_Teacher\Cyber_Teacher\knowledge.py", line 9, in <module>
    from langchain.text_splitter import RecursiveCharacterTextSplitter
ModuleNotFoundError: No module named 'langchain.text_splitter'

```

**ERROR**: `test_validate_code_python_forbidden_exec (tests.test_handlers_sandbox.TestSandboxFunctions.test_validate_code_python_forbidden_exec)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_handlers_sandbox.py", line 26, in test_validate_code_python_forbidden_exec
    from handlers.sandbox import validate_code
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\__init__.py", line 14, in <module>
    from .core import (  # основной диспетчер
        handle_commands,
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\core.py", line 30, in <module>
    from .misc import (
    ...<25 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\misc.py", line 15, in <module>
    from generators import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\generators.py", line 8, in <module>
    from knowledge import get_relevant_docs
  File "M:\Cyber_Teacher\Cyber_Teacher\knowledge.py", line 9, in <module>
    from langchain.text_splitter import RecursiveCharacterTextSplitter
ModuleNotFoundError: No module named 'langchain.text_splitter'

```

**ERROR**: `test_validate_code_python_forbidden_import (tests.test_handlers_sandbox.TestSandboxFunctions.test_validate_code_python_forbidden_import)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_handlers_sandbox.py", line 19, in test_validate_code_python_forbidden_import
    from handlers.sandbox import validate_code
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\__init__.py", line 14, in <module>
    from .core import (  # основной диспетчер
        handle_commands,
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\core.py", line 30, in <module>
    from .misc import (
    ...<25 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\misc.py", line 15, in <module>
    from generators import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\generators.py", line 8, in <module>
    from knowledge import get_relevant_docs
  File "M:\Cyber_Teacher\Cyber_Teacher\knowledge.py", line 9, in <module>
    from langchain.text_splitter import RecursiveCharacterTextSplitter
ModuleNotFoundError: No module named 'langchain.text_splitter'

```

**ERROR**: `test_validate_code_python_forbidden_open (tests.test_handlers_sandbox.TestSandboxFunctions.test_validate_code_python_forbidden_open)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_handlers_sandbox.py", line 33, in test_validate_code_python_forbidden_open
    from handlers.sandbox import validate_code
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\__init__.py", line 14, in <module>
    from .core import (  # основной диспетчер
        handle_commands,
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\core.py", line 30, in <module>
    from .misc import (
    ...<25 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\misc.py", line 15, in <module>
    from generators import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\generators.py", line 8, in <module>
    from knowledge import get_relevant_docs
  File "M:\Cyber_Teacher\Cyber_Teacher\knowledge.py", line 9, in <module>
    from langchain.text_splitter import RecursiveCharacterTextSplitter
ModuleNotFoundError: No module named 'langchain.text_splitter'

```

**ERROR**: `test_validate_code_python_forbidden_subprocess (tests.test_handlers_sandbox.TestSandboxFunctions.test_validate_code_python_forbidden_subprocess)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_handlers_sandbox.py", line 40, in test_validate_code_python_forbidden_subprocess
    from handlers.sandbox import validate_code
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\__init__.py", line 14, in <module>
    from .core import (  # основной диспетчер
        handle_commands,
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\core.py", line 30, in <module>
    from .misc import (
    ...<25 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\misc.py", line 15, in <module>
    from generators import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\generators.py", line 8, in <module>
    from knowledge import get_relevant_docs
  File "M:\Cyber_Teacher\Cyber_Teacher\knowledge.py", line 9, in <module>
    from langchain.text_splitter import RecursiveCharacterTextSplitter
ModuleNotFoundError: No module named 'langchain.text_splitter'

```

**ERROR**: `test_validate_code_safe_bash (tests.test_handlers_sandbox.TestSandboxFunctions.test_validate_code_safe_bash)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_handlers_sandbox.py", line 75, in test_validate_code_safe_bash
    from handlers.sandbox import validate_code
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\__init__.py", line 14, in <module>
    from .core import (  # основной диспетчер
        handle_commands,
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\core.py", line 30, in <module>
    from .misc import (
    ...<25 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\misc.py", line 15, in <module>
    from generators import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\generators.py", line 8, in <module>
    from knowledge import get_relevant_docs
  File "M:\Cyber_Teacher\Cyber_Teacher\knowledge.py", line 9, in <module>
    from langchain.text_splitter import RecursiveCharacterTextSplitter
ModuleNotFoundError: No module named 'langchain.text_splitter'

```

**ERROR**: `test_validate_code_safe_python (tests.test_handlers_sandbox.TestSandboxFunctions.test_validate_code_safe_python)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_handlers_sandbox.py", line 68, in test_validate_code_safe_python
    from handlers.sandbox import validate_code
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\__init__.py", line 14, in <module>
    from .core import (  # основной диспетчер
        handle_commands,
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\core.py", line 30, in <module>
    from .misc import (
    ...<25 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\misc.py", line 15, in <module>
    from generators import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\generators.py", line 8, in <module>
    from knowledge import get_relevant_docs
  File "M:\Cyber_Teacher\Cyber_Teacher\knowledge.py", line 9, in <module>
    from langchain.text_splitter import RecursiveCharacterTextSplitter
ModuleNotFoundError: No module named 'langchain.text_splitter'

```

**ERROR**: `test_validate_code_unsupported_language (tests.test_handlers_sandbox.TestSandboxFunctions.test_validate_code_unsupported_language)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_handlers_sandbox.py", line 13, in test_validate_code_unsupported_language
    from handlers.sandbox import validate_code
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\__init__.py", line 14, in <module>
    from .core import (  # основной диспетчер
        handle_commands,
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\core.py", line 30, in <module>
    from .misc import (
    ...<25 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\misc.py", line 15, in <module>
    from generators import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\generators.py", line 8, in <module>
    from knowledge import get_relevant_docs
  File "M:\Cyber_Teacher\Cyber_Teacher\knowledge.py", line 9, in <module>
    from langchain.text_splitter import RecursiveCharacterTextSplitter
ModuleNotFoundError: No module named 'langchain.text_splitter'

```

### tests\test_handlers_writeup_auto.py
**ERROR**: `test_handle_auto_writeup_activity_without_topic (tests.test_handlers_writeup_auto.TestHandlersWriteupAuto.test_handle_auto_writeup_activity_without_topic)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_handle_auto_writeup_llm_exception (tests.test_handlers_writeup_auto.TestHandlersWriteupAuto.test_handle_auto_writeup_llm_exception)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_handle_auto_writeup_no_activity (tests.test_handlers_writeup_auto.TestHandlersWriteupAuto.test_handle_auto_writeup_no_activity)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_handle_auto_writeup_no_vectordb (tests.test_handlers_writeup_auto.TestHandlersWriteupAuto.test_handle_auto_writeup_no_vectordb)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_handle_auto_writeup_quiz_success (tests.test_handlers_writeup_auto.TestHandlersWriteupAuto.test_handle_auto_writeup_quiz_success)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_handle_auto_writeup_saves_to_file (tests.test_handlers_writeup_auto.TestHandlersWriteupAuto.test_handle_auto_writeup_saves_to_file)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

### tests\test_health_handler.py
**ERROR**: `test_health_returns_success (tests.test_health_handler.TestHealthHandler.test_health_returns_success)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_health_uptime_calculation (tests.test_health_handler.TestHealthHandler.test_health_uptime_calculation)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_health_zero_cache_division (tests.test_health_handler.TestHealthHandler.test_health_zero_cache_division)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

### IMPORT ERROR: tests\test_hints_handler.py
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\run_all_tests.py", line 76, in run_test_file
    module = importlib.import_module(module_name)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1406, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 938, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 759, in exec_module
  File "<frozen importlib._bootstrap>", line 491, in _call_with_frames_removed
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_hints_handler.py", line 8, in <module>
    from handlers.hints import (
    ...<4 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\__init__.py", line 14, in <module>
    from .core import (  # основной диспетчер
        handle_commands,
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\core.py", line 30, in <module>
    from .misc import (
    ...<25 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\misc.py", line 15, in <module>
    from generators import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\generators.py", line 8, in <module>
    from knowledge import get_relevant_docs
  File "M:\Cyber_Teacher\Cyber_Teacher\knowledge.py", line 9, in <module>
    from langchain.text_splitter import RecursiveCharacterTextSplitter
ModuleNotFoundError: No module named 'langchain.text_splitter'

```

### IMPORT ERROR: tests\test_history.py
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\run_all_tests.py", line 76, in run_test_file
    module = importlib.import_module(module_name)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1406, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 938, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 759, in exec_module
  File "<frozen importlib._bootstrap>", line 491, in _call_with_frames_removed
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_history.py", line 6, in <module>
    from handlers.history import (
    ...<5 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\__init__.py", line 14, in <module>
    from .core import (  # основной диспетчер
        handle_commands,
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\core.py", line 30, in <module>
    from .misc import (
    ...<25 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\misc.py", line 15, in <module>
    from generators import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\generators.py", line 8, in <module>
    from knowledge import get_relevant_docs
  File "M:\Cyber_Teacher\Cyber_Teacher\knowledge.py", line 9, in <module>
    from langchain.text_splitter import RecursiveCharacterTextSplitter
ModuleNotFoundError: No module named 'langchain.text_splitter'

```

### tests\test_htb.py
**ERROR**: `test_htb_dispatches_login (tests.test_htb.TestHTBDispatcher.test_htb_dispatches_login)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_htb_no_args_shows_help (tests.test_htb.TestHTBDispatcher.test_htb_no_args_shows_help)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_htb_unknown_command (tests.test_htb.TestHTBDispatcher.test_htb_unknown_command)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_login_missing_password (tests.test_htb.TestHTBLogin.test_login_missing_password)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_login_wrong_args (tests.test_htb.TestHTBLogin.test_login_wrong_args)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_successful_login (tests.test_htb.TestHTBLogin.test_successful_login)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_machine_detail (tests.test_htb.TestHTBMachineDetail.test_machine_detail)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_machine_invalid_id (tests.test_htb.TestHTBMachineDetail.test_machine_invalid_id)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_machine_missing_id (tests.test_htb.TestHTBMachineDetail.test_machine_missing_id)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_list_machines (tests.test_htb.TestHTBMachines.test_list_machines)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_machines_auth_error (tests.test_htb.TestHTBMachines.test_machines_auth_error)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_machines_invalid_type (tests.test_htb.TestHTBMachines.test_machines_invalid_type)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_status_no_auth (tests.test_htb.TestHTBStatus.test_status_no_auth)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_status_with_progress (tests.test_htb.TestHTBStatus.test_status_with_progress)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_submit_invalid_id (tests.test_htb.TestHTBSubmit.test_submit_invalid_id)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_submit_missing_args (tests.test_htb.TestHTBSubmit.test_submit_missing_args)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_successful_submit (tests.test_htb.TestHTBSubmit.test_successful_submit)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

### tests\test_integration.py
**ERROR**: `test_full_learning_cycle (tests.test_integration.TestE2ELearningCycle.test_full_learning_cycle)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_integration.py", line 215, in test_full_learning_cycle
    self.state.set_course("web-security")
    ^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'AppState' object has no attribute 'set_course'

```

### tests\test_integration_achievements.py
**ERROR**: `test_earn_achievement (tests.test_integration_achievements.TestAchievementsIntegration.test_earn_achievement)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_integration_achievements.py", line 21, in setUp
    self.mock_get_context = self.state_patch.start()
                            ~~~~~~~~~~~~~~~~~~~~~~^^
  File "C:\Python314\Lib\unittest\mock.py", line 1667, in start
    result = self.__enter__()
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1406, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
  File "<fro
```

**ERROR**: `test_list_achievements (tests.test_integration_achievements.TestAchievementsIntegration.test_list_achievements)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_integration_achievements.py", line 21, in setUp
    self.mock_get_context = self.state_patch.start()
                            ~~~~~~~~~~~~~~~~~~~~~~^^
  File "C:\Python314\Lib\unittest\mock.py", line 1667, in start
    result = self.__enter__()
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1406, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
  File "<fro
```

### IMPORT ERROR: tests\test_integration_analytics.py
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\run_all_tests.py", line 76, in run_test_file
    module = importlib.import_module(module_name)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1406, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 938, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 759, in exec_module
  File "<frozen importlib._bootstrap>", line 491, in _call_with_frames_removed
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_integration_analytics.py", line 10, in <module>
    from handlers.analytics import handle_analytics, _compute_learning_metrics
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\__init__.py", line 14, in <module>
    from .core import (  # основной диспетчер
        handle_commands,
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\core.py", line 30, in <module>
    from .misc import (
    ...<25 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\misc.py", line 15, in <module>
    from generators import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\generators.py", line 8, in <module>
    from knowledge import get_relevant_docs
  File "M:\Cyber_Teacher\Cyber_Teacher\knowledge.py", line 9, in <module>
    from langchain.text_splitter import RecursiveCharacterTextSplitter
ModuleNotFoundError: No module named 'langchain.text_splitter'

```

### IMPORT ERROR: tests\test_integration_daily.py
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\run_all_tests.py", line 76, in run_test_file
    module = importlib.import_module(module_name)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1406, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 938, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 759, in exec_module
  File "<frozen importlib._bootstrap>", line 491, in _call_with_frames_removed
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_integration_daily.py", line 10, in <module>
    from handlers.daily import handle_daily
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\__init__.py", line 14, in <module>
    from .core import (  # основной диспетчер
        handle_commands,
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\core.py", line 30, in <module>
    from .misc import (
    ...<25 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\misc.py", line 15, in <module>
    from generators import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\generators.py", line 8, in <module>
    from knowledge import get_relevant_docs
  File "M:\Cyber_Teacher\Cyber_Teacher\knowledge.py", line 9, in <module>
    from langchain.text_splitter import RecursiveCharacterTextSplitter
ModuleNotFoundError: No module named 'langchain.text_splitter'

```

### tests\test_integration_flag.py
**ERROR**: `test_flag_already_used (tests.test_integration_flag.TestFlagIntegration.test_flag_already_used)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_integration_flag.py", line 21, in setUp
    self.mock_get_context = self.state_patch.start()
                            ~~~~~~~~~~~~~~~~~~~~~~^^
  File "C:\Python314\Lib\unittest\mock.py", line 1667, in start
    result = self.__enter__()
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1406, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
  File "<frozen impo
```

**ERROR**: `test_flag_found (tests.test_integration_flag.TestFlagIntegration.test_flag_found)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_integration_flag.py", line 21, in setUp
    self.mock_get_context = self.state_patch.start()
                            ~~~~~~~~~~~~~~~~~~~~~~^^
  File "C:\Python314\Lib\unittest\mock.py", line 1667, in start
    result = self.__enter__()
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1406, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
  File "<frozen impo
```

**ERROR**: `test_flag_not_found (tests.test_integration_flag.TestFlagIntegration.test_flag_not_found)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_integration_flag.py", line 21, in setUp
    self.mock_get_context = self.state_patch.start()
                            ~~~~~~~~~~~~~~~~~~~~~~^^
  File "C:\Python314\Lib\unittest\mock.py", line 1667, in start
    result = self.__enter__()
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1406, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
  File "<frozen impo
```

### IMPORT ERROR: tests\test_investigation.py
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\run_all_tests.py", line 76, in run_test_file
    module = importlib.import_module(module_name)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1406, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 938, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 759, in exec_module
  File "<frozen importlib._bootstrap>", line 491, in _call_with_frames_removed
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_investigation.py", line 6, in <module>
    from handlers.investigation import (
    ...<5 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\__init__.py", line 14, in <module>
    from .core import (  # основной диспетчер
        handle_commands,
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\core.py", line 30, in <module>
    from .misc import (
    ...<25 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\misc.py", line 15, in <module>
    from generators import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\generators.py", line 8, in <module>
    from knowledge import get_relevant_docs
  File "M:\Cyber_Teacher\Cyber_Teacher\knowledge.py", line 9, in <module>
    from langchain.text_splitter import RecursiveCharacterTextSplitter
ModuleNotFoundError: No module named 'langchain.text_splitter'

```

### IMPORT ERROR: tests\test_jupyter.py
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\run_all_tests.py", line 76, in run_test_file
    module = importlib.import_module(module_name)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1406, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 938, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 759, in exec_module
  File "<frozen importlib._bootstrap>", line 491, in _call_with_frames_removed
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_jupyter.py", line 6, in <module>
    from handlers.jupyter import (
    ...<5 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\__init__.py", line 14, in <module>
    from .core import (  # основной диспетчер
        handle_commands,
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\core.py", line 30, in <module>
    from .misc import (
    ...<25 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\misc.py", line 15, in <module>
    from generators import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\generators.py", line 8, in <module>
    from knowledge import get_relevant_docs
  File "M:\Cyber_Teacher\Cyber_Teacher\knowledge.py", line 9, in <module>
    from langchain.text_splitter import RecursiveCharacterTextSplitter
ModuleNotFoundError: No module named 'langchain.text_splitter'

```

### IMPORT ERROR: tests\test_knowledge.py
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\run_all_tests.py", line 76, in run_test_file
    module = importlib.import_module(module_name)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1406, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 938, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 759, in exec_module
  File "<frozen importlib._bootstrap>", line 491, in _call_with_frames_removed
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_knowledge.py", line 6, in <module>
    from knowledge import get_knowledge_status, get_relevant_docs
  File "M:\Cyber_Teacher\Cyber_Teacher\knowledge.py", line 9, in <module>
    from langchain.text_splitter import RecursiveCharacterTextSplitter
ModuleNotFoundError: No module named 'langchain.text_splitter'

```

### IMPORT ERROR: tests\test_lang_handler.py
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\run_all_tests.py", line 76, in run_test_file
    module = importlib.import_module(module_name)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1406, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 938, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 759, in exec_module
  File "<frozen importlib._bootstrap>", line 491, in _call_with_frames_removed
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_lang_handler.py", line 8, in <module>
    from handlers.lang import handle_lang
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\__init__.py", line 14, in <module>
    from .core import (  # основной диспетчер
        handle_commands,
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\core.py", line 30, in <module>
    from .misc import (
    ...<25 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\misc.py", line 15, in <module>
    from generators import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\generators.py", line 8, in <module>
    from knowledge import get_relevant_docs
  File "M:\Cyber_Teacher\Cyber_Teacher\knowledge.py", line 9, in <module>
    from langchain.text_splitter import RecursiveCharacterTextSplitter
ModuleNotFoundError: No module named 'langchain.text_splitter'

```

### IMPORT ERROR: tests\test_malware_analysis.py
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\run_all_tests.py", line 76, in run_test_file
    module = importlib.import_module(module_name)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1406, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 938, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 759, in exec_module
  File "<frozen importlib._bootstrap>", line 491, in _call_with_frames_removed
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_malware_analysis.py", line 6, in <module>
    from handlers.malware_analysis import (
    ...<7 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\__init__.py", line 14, in <module>
    from .core import (  # основной диспетчер
        handle_commands,
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\core.py", line 30, in <module>
    from .misc import (
    ...<25 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\misc.py", line 15, in <module>
    from generators import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\generators.py", line 8, in <module>
    from knowledge import get_relevant_docs
  File "M:\Cyber_Teacher\Cyber_Teacher\knowledge.py", line 9, in <module>
    from langchain.text_splitter import RecursiveCharacterTextSplitter
ModuleNotFoundError: No module named 'langchain.text_splitter'

```

### IMPORT ERROR: tests\test_media.py
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\run_all_tests.py", line 76, in run_test_file
    module = importlib.import_module(module_name)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1406, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 938, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 759, in exec_module
  File "<frozen importlib._bootstrap>", line 491, in _call_with_frames_removed
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_media.py", line 6, in <module>
    from handlers.media import (
    ...<4 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\__init__.py", line 14, in <module>
    from .core import (  # основной диспетчер
        handle_commands,
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\core.py", line 30, in <module>
    from .misc import (
    ...<25 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\misc.py", line 15, in <module>
    from generators import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\generators.py", line 8, in <module>
    from knowledge import get_relevant_docs
  File "M:\Cyber_Teacher\Cyber_Teacher\knowledge.py", line 9, in <module>
    from langchain.text_splitter import RecursiveCharacterTextSplitter
ModuleNotFoundError: No module named 'langchain.text_splitter'

```

### tests\test_memory.py
**FAIL**: `test_sanitize_log_removes_sensitive (tests.test_memory.TestMemory.test_sanitize_log_removes_sensitive)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_memory.py", line 132, in test_sanitize_log_removes_sensitive
    self.assertNotIn("12345", sanitized)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^
AssertionError: '12345' unexpectedly found in 'password="12345"'

```

### tests\test_metasploit.py
**ERROR**: `test_msf_info_no_client (tests.test_metasploit.TestMetasploitAction.test_msf_info_no_client)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_msf_no_args_shows_help (tests.test_metasploit.TestMetasploitAction.test_msf_no_args_shows_help)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_msf_search_no_client (tests.test_metasploit.TestMetasploitAction.test_msf_search_no_client)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_msf_sessions_no_client (tests.test_metasploit.TestMetasploitAction.test_msf_sessions_no_client)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_msf_unknown_command (tests.test_metasploit.TestMetasploitAction.test_msf_unknown_command)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

**ERROR**: `test_client_not_installed (tests.test_metasploit.TestMetasploitClient.test_client_not_installed)`
```
Traceback (most recent call last):
  File "C:\Python314\Lib\unittest\mock.py", line 1436, in patched
    with self.decoration_helper(patched,
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
                                args,
                                ^^^^^
                                keywargs) as (newargs, newkeywargs):
                                ^^^^^^^^^
  File "C:\Python314\Lib\contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "C:\Python314\Lib\unittest\mock.py", line 1418, in decoration_helper
    arg = exit_stack.enter_context(patching)
  File "C:\Python314\Lib\contextlib.py", line 530, in enter_context
    result = _enter(cm)
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _b
```

### IMPORT ERROR: tests\test_missions_handler.py
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\run_all_tests.py", line 76, in run_test_file
    module = importlib.import_module(module_name)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1406, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 938, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 759, in exec_module
  File "<frozen importlib._bootstrap>", line 491, in _call_with_frames_removed
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_missions_handler.py", line 11, in <module>
    from handlers.missions import (
    ...<5 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\__init__.py", line 14, in <module>
    from .core import (  # основной диспетчер
        handle_commands,
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\core.py", line 30, in <module>
    from .misc import (
    ...<25 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\misc.py", line 15, in <module>
    from generators import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\generators.py", line 8, in <module>
    from knowledge import get_relevant_docs
  File "M:\Cyber_Teacher\Cyber_Teacher\knowledge.py", line 9, in <module>
    from langchain.text_splitter import RecursiveCharacterTextSplitter
ModuleNotFoundError: No module named 'langchain.text_splitter'

```

### IMPORT ERROR: tests\test_new_features.py
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\run_all_tests.py", line 76, in run_test_file
    module = importlib.import_module(module_name)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1406, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 938, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 759, in exec_module
  File "<frozen importlib._bootstrap>", line 491, in _call_with_frames_removed
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_new_features.py", line 6, in <module>
    from handlers.mindmap import TOPIC_TREE, handle_mindmap
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\__init__.py", line 14, in <module>
    from .core import (  # основной диспетчер
        handle_commands,
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\core.py", line 30, in <module>
    from .misc import (
    ...<25 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\misc.py", line 15, in <module>
    from generators import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\generators.py", line 8, in <module>
    from knowledge import get_relevant_docs
  File "M:\Cyber_Teacher\Cyber_Teacher\knowledge.py", line 9, in <module>
    from langchain.text_splitter import RecursiveCharacterTextSplitter
ModuleNotFoundError: No module named 'langchain.text_splitter'

```

### IMPORT ERROR: tests\test_numeric_menu_fix.py
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\run_all_tests.py", line 76, in run_test_file
    module = importlib.import_module(module_name)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1406, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 938, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 759, in exec_module
  File "<frozen importlib._bootstrap>", line 491, in _call_with_frames_removed
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_numeric_menu_fix.py", line 12, in <module>
    from handlers.core import handle_commands
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\__init__.py", line 14, in <module>
    from .core import (  # основной диспетчер
        handle_commands,
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\core.py", line 30, in <module>
    from .misc import (
    ...<25 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\misc.py", line 15, in <module>
    from generators import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\generators.py", line 8, in <module>
    from knowledge import get_relevant_docs
  File "M:\Cyber_Teacher\Cyber_Teacher\knowledge.py", line 9, in <module>
    from langchain.text_splitter import RecursiveCharacterTextSplitter
ModuleNotFoundError: No module named 'langchain.text_splitter'

```

### IMPORT ERROR: tests\test_osint.py
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\run_all_tests.py", line 76, in run_test_file
    module = importlib.import_module(module_name)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1406, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 938, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 759, in exec_module
  File "<frozen importlib._bootstrap>", line 491, in _call_with_frames_removed
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_osint.py", line 6, in <module>
    from handlers.osint import (
    ...<7 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\__init__.py", line 14, in <module>
    from .core import (  # основной диспетчер
        handle_commands,
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\core.py", line 30, in <module>
    from .misc import (
    ...<25 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\misc.py", line 15, in <module>
    from generators import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\generators.py", line 8, in <module>
    from knowledge import get_relevant_docs
  File "M:\Cyber_Teacher\Cyber_Teacher\knowledge.py", line 9, in <module>
    from langchain.text_splitter import RecursiveCharacterTextSplitter
ModuleNotFoundError: No module named 'langchain.text_splitter'

```

### IMPORT ERROR: tests\test_pcap_analyzer.py
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\run_all_tests.py", line 76, in run_test_file
    module = importlib.import_module(module_name)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1406, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 938, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 759, in exec_module
  File "<frozen importlib._bootstrap>", line 491, in _call_with_frames_removed
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_pcap_analyzer.py", line 14, in <module>
    from handlers.pcap_analyzer import (
    ...<3 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\__init__.py", line 14, in <module>
    from .core import (  # основной диспетчер
        handle_commands,
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\core.py", line 30, in <module>
    from .misc import (
    ...<25 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\misc.py", line 15, in <module>
    from generators import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\generators.py", line 8, in <module>
    from knowledge import get_relevant_docs
  File "M:\Cyber_Teacher\Cyber_Teacher\knowledge.py", line 9, in <module>
    from langchain.text_splitter import RecursiveCharacterTextSplitter
ModuleNotFoundError: No module named 'langchain.text_splitter'

```

### IMPORT ERROR: tests\test_phishing_handler.py
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\run_all_tests.py", line 76, in run_test_file
    module = importlib.import_module(module_name)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1406, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 938, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 759, in exec_module
  File "<frozen importlib._bootstrap>", line 491, in _call_with_frames_removed
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_phishing_handler.py", line 8, in <module>
    from handlers.phishing import (
    ...<5 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\__init__.py", line 14, in <module>
    from .core import (  # основной диспетчер
        handle_commands,
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\core.py", line 30, in <module>
    from .misc import (
    ...<25 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\misc.py", line 15, in <module>
    from generators import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\generators.py", line 8, in <module>
    from knowledge import get_relevant_docs
  File "M:\Cyber_Teacher\Cyber_Teacher\knowledge.py", line 9, in <module>
    from langchain.text_splitter import RecursiveCharacterTextSplitter
ModuleNotFoundError: No module named 'langchain.text_splitter'

```

### IMPORT ERROR: tests\test_profile_handler.py
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\run_all_tests.py", line 76, in run_test_file
    module = importlib.import_module(module_name)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1406, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 938, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 759, in exec_module
  File "<frozen importlib._bootstrap>", line 491, in _call_with_frames_removed
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_profile_handler.py", line 9, in <module>
    from handlers.profile import (
    ...<5 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\__init__.py", line 14, in <module>
    from .core import (  # основной диспетчер
        handle_commands,
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\core.py", line 30, in <module>
    from .misc import (
    ...<25 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\misc.py", line 15, in <module>
    from generators import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\generators.py", line 8, in <module>
    from knowledge import get_relevant_docs
  File "M:\Cyber_Teacher\Cyber_Teacher\knowledge.py", line 9, in <module>
    from langchain.text_splitter import RecursiveCharacterTextSplitter
ModuleNotFoundError: No module named 'langchain.text_splitter'

```

### IMPORT ERROR: tests\test_pwa.py
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\run_all_tests.py", line 76, in run_test_file
    module = importlib.import_module(module_name)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1406, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 938, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 759, in exec_module
  File "<frozen importlib._bootstrap>", line 491, in _call_with_frames_removed
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_pwa.py", line 6, in <module>
    from handlers.pwa import handle_pwa
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\__init__.py", line 14, in <module>
    from .core import (  # основной диспетчер
        handle_commands,
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\core.py", line 30, in <module>
    from .misc import (
    ...<25 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\misc.py", line 15, in <module>
    from generators import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\generators.py", line 8, in <module>
    from knowledge import get_relevant_docs
  File "M:\Cyber_Teacher\Cyber_Teacher\knowledge.py", line 9, in <module>
    from langchain.text_splitter import RecursiveCharacterTextSplitter
ModuleNotFoundError: No module named 'langchain.text_splitter'

```

### IMPORT ERROR: tests\test_remaining_features.py
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\run_all_tests.py", line 76, in run_test_file
    module = importlib.import_module(module_name)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1406, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 938, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 759, in exec_module
  File "<frozen importlib._bootstrap>", line 491, in _call_with_frames_removed
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_remaining_features.py", line 6, in <module>
    from handlers.kb_manager import _get_kb_status, handle_kb
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\__init__.py", line 14, in <module>
    from .core import (  # основной диспетчер
        handle_commands,
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\core.py", line 30, in <module>
    from .misc import (
    ...<25 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\misc.py", line 15, in <module>
    from generators import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\generators.py", line 8, in <module>
    from knowledge import get_relevant_docs
  File "M:\Cyber_Teacher\Cyber_Teacher\knowledge.py", line 9, in <module>
    from langchain.text_splitter import RecursiveCharacterTextSplitter
ModuleNotFoundError: No module named 'langchain.text_splitter'

```

### IMPORT ERROR: tests\test_risk_integration.py
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\run_all_tests.py", line 76, in run_test_file
    module = importlib.import_module(module_name)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1406, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 938, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 759, in exec_module
  File "<frozen importlib._bootstrap>", line 491, in _call_with_frames_removed
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_risk_integration.py", line 14, in <module>
    from handlers.misc import handle_risk, handle_story_mode
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\__init__.py", line 14, in <module>
    from .core import (  # основной диспетчер
        handle_commands,
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\core.py", line 30, in <module>
    from .misc import (
    ...<25 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\misc.py", line 15, in <module>
    from generators import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\generators.py", line 8, in <module>
    from knowledge import get_relevant_docs
  File "M:\Cyber_Teacher\Cyber_Teacher\knowledge.py", line 9, in <module>
    from langchain.text_splitter import RecursiveCharacterTextSplitter
ModuleNotFoundError: No module named 'langchain.text_splitter'

```

### IMPORT ERROR: tests\test_sandbox.py
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\run_all_tests.py", line 76, in run_test_file
    module = importlib.import_module(module_name)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1406, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 938, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 759, in exec_module
  File "<frozen importlib._bootstrap>", line 491, in _call_with_frames_removed
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_sandbox.py", line 13, in <module>
    from handlers.sandbox import run_code_in_sandbox, validate_code
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\__init__.py", line 14, in <module>
    from .core import (  # основной диспетчер
        handle_commands,
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\core.py", line 30, in <module>
    from .misc import (
    ...<25 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\misc.py", line 15, in <module>
    from generators import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\generators.py", line 8, in <module>
    from knowledge import get_relevant_docs
  File "M:\Cyber_Teacher\Cyber_Teacher\knowledge.py", line 9, in <module>
    from langchain.text_splitter import RecursiveCharacterTextSplitter
ModuleNotFoundError: No module named 'langchain.text_splitter'

```

### IMPORT ERROR: tests\test_shodan_censys.py
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\run_all_tests.py", line 76, in run_test_file
    module = importlib.import_module(module_name)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1406, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 938, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 759, in exec_module
  File "<frozen importlib._bootstrap>", line 491, in _call_with_frames_removed
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_shodan_censys.py", line 6, in <module>
    from handlers.shodan_censys import (
    ...<5 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\__init__.py", line 14, in <module>
    from .core import (  # основной диспетчер
        handle_commands,
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\core.py", line 30, in <module>
    from .misc import (
    ...<25 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\misc.py", line 15, in <module>
    from generators import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\generators.py", line 8, in <module>
    from knowledge import get_relevant_docs
  File "M:\Cyber_Teacher\Cyber_Teacher\knowledge.py", line 9, in <module>
    from langchain.text_splitter import RecursiveCharacterTextSplitter
ModuleNotFoundError: No module named 'langchain.text_splitter'

```

### IMPORT ERROR: tests\test_shop.py
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\run_all_tests.py", line 76, in run_test_file
    module = importlib.import_module(module_name)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1406, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 938, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 759, in exec_module
  File "<frozen importlib._bootstrap>", line 491, in _call_with_frames_removed
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_shop.py", line 8, in <module>
    from handlers import shop as shop_handler
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\__init__.py", line 14, in <module>
    from .core import (  # основной диспетчер
        handle_commands,
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\core.py", line 30, in <module>
    from .misc import (
    ...<25 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\misc.py", line 15, in <module>
    from generators import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\generators.py", line 8, in <module>
    from knowledge import get_relevant_docs
  File "M:\Cyber_Teacher\Cyber_Teacher\knowledge.py", line 9, in <module>
    from langchain.text_splitter import RecursiveCharacterTextSplitter
ModuleNotFoundError: No module named 'langchain.text_splitter'

```

### IMPORT ERROR: tests\test_skills_handler.py
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\run_all_tests.py", line 76, in run_test_file
    module = importlib.import_module(module_name)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1406, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 938, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 759, in exec_module
  File "<frozen importlib._bootstrap>", line 491, in _call_with_frames_removed
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_skills_handler.py", line 8, in <module>
    from handlers.skills import (
    ...<6 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\__init__.py", line 14, in <module>
    from .core import (  # основной диспетчер
        handle_commands,
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\core.py", line 30, in <module>
    from .misc import (
    ...<25 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\misc.py", line 15, in <module>
    from generators import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\generators.py", line 8, in <module>
    from knowledge import get_relevant_docs
  File "M:\Cyber_Teacher\Cyber_Teacher\knowledge.py", line 9, in <module>
    from langchain.text_splitter import RecursiveCharacterTextSplitter
ModuleNotFoundError: No module named 'langchain.text_splitter'

```

### IMPORT ERROR: tests\test_social.py
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\run_all_tests.py", line 76, in run_test_file
    module = importlib.import_module(module_name)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1406, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 938, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 759, in exec_module
  File "<frozen importlib._bootstrap>", line 491, in _call_with_frames_removed
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_social.py", line 7, in <module>
    from handlers.social import SCENARIOS, handle_social
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\__init__.py", line 14, in <module>
    from .core import (  # основной диспетчер
        handle_commands,
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\core.py", line 30, in <module>
    from .misc import (
    ...<25 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\misc.py", line 15, in <module>
    from generators import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\generators.py", line 8, in <module>
    from knowledge import get_relevant_docs
  File "M:\Cyber_Teacher\Cyber_Teacher\knowledge.py", line 9, in <module>
    from langchain.text_splitter import RecursiveCharacterTextSplitter
ModuleNotFoundError: No module named 'langchain.text_splitter'

```

### tests\test_spaced_repetition.py
**ERROR**: `test_quiz_updates_review_schedule (tests.test_spaced_repetition.TestReviewIntegration.test_quiz_updates_review_schedule)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_spaced_repetition.py", line 168, in test_quiz_updates_review_schedule
    initial_count = len(state.review_schedule)
                        ^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'AppState' object has no attribute 'review_schedule'

```

**ERROR**: `test_weak_topics_and_review_coexist (tests.test_spaced_repetition.TestReviewIntegration.test_weak_topics_and_review_coexist)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_spaced_repetition.py", line 180, in test_weak_topics_and_review_coexist
    state.clear_weak_topics()
    ^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'AppState' object has no attribute 'clear_weak_topics'. Did you mean: 'get_weak_topics'?

```

**ERROR**: `test_clear_review_schedule (tests.test_spaced_repetition.TestSpacedRepetition.test_clear_review_schedule)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_spaced_repetition.py", line 123, in test_clear_review_schedule
    self.state.clear_review_schedule()
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'AppState' object has no attribute 'clear_review_schedule'. Did you mean: 'review_schedule'?

```

**ERROR**: `test_ef_not_below_1_3 (tests.test_spaced_repetition.TestSpacedRepetition.test_ef_not_below_1_3)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_spaced_repetition.py", line 152, in test_ef_not_below_1_3
    self.state.schedule_review("sql", 2.0, 10.0)  # quality 1
    ~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^
TypeError: AppState.schedule_review() takes 3 positional arguments but 4 were given

```

**FAIL**: `test_get_due_reviews_returns_due (tests.test_spaced_repetition.TestSpacedRepetition.test_get_due_reviews_returns_due)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_spaced_repetition.py", line 99, in test_get_due_reviews_returns_due
    self.assertEqual(len(due), 1)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
AssertionError: 0 != 1

```

**FAIL**: `test_get_due_reviews_sorted_by_date (tests.test_spaced_repetition.TestSpacedRepetition.test_get_due_reviews_sorted_by_date)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_spaced_repetition.py", line 113, in test_get_due_reviews_sorted_by_date
    self.assertEqual(len(due), 1)  # Only network is due
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
AssertionError: 0 != 1

```

**ERROR**: `test_interval_increases_with_ef (tests.test_spaced_repetition.TestSpacedRepetition.test_interval_increases_with_ef)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_spaced_repetition.py", line 52, in test_interval_increases_with_ef
    self.state.schedule_review("sql", 10.0, 10.0)  # quality 5
    ~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
TypeError: AppState.schedule_review() takes 3 positional arguments but 4 were given

```

**ERROR**: `test_mark_reviewed_alias (tests.test_spaced_repetition.TestSpacedRepetition.test_mark_reviewed_alias)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_spaced_repetition.py", line 73, in test_mark_reviewed_alias
    self.state.mark_reviewed("sql", 8.0, 10.0)
    ^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'AppState' object has no attribute 'mark_reviewed'

```

**ERROR**: `test_review_schedule_initial_empty (tests.test_spaced_repetition.TestSpacedRepetition.test_review_schedule_initial_empty)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_spaced_repetition.py", line 159, in test_review_schedule_initial_empty
    self.assertEqual(fresh_state.review_schedule, {})
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'AppState' object has no attribute 'review_schedule'

```

**ERROR**: `test_save_and_load_review_schedule (tests.test_spaced_repetition.TestSpacedRepetition.test_save_and_load_review_schedule)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_spaced_repetition.py", line 136, in test_save_and_load_review_schedule
    self.state.schedule_review("sql", 8.0, 10.0)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^
TypeError: AppState.schedule_review() takes 3 positional arguments but 4 were given

```

**ERROR**: `test_schedule_review_first_time (tests.test_spaced_repetition.TestSpacedRepetition.test_schedule_review_first_time)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_spaced_repetition.py", line 17, in test_schedule_review_first_time
    self.state.schedule_review("sql", 8.0, 10.0)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^
TypeError: AppState.schedule_review() takes 3 positional arguments but 4 were given

```

**ERROR**: `test_schedule_review_quality_bad_resets (tests.test_spaced_repetition.TestSpacedRepetition.test_schedule_review_quality_bad_resets)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_spaced_repetition.py", line 29, in test_schedule_review_quality_bad_resets
    self.state.schedule_review("sql", 8.0, 10.0)  # First, quality 4
    ~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^
TypeError: AppState.schedule_review() takes 3 positional arguments but 4 were given

```

**ERROR**: `test_schedule_review_quality_good_increments (tests.test_spaced_repetition.TestSpacedRepetition.test_schedule_review_quality_good_increments)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_spaced_repetition.py", line 41, in test_schedule_review_quality_good_increments
    self.state.schedule_review("sql", 8.0, 10.0)  # quality 4
    ~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^
TypeError: AppState.schedule_review() takes 3 positional arguments but 4 were given

```

### tests\test_state.py
**ERROR**: `test_increment_labs_started (tests.test_state.TestIncrementMethods.test_increment_labs_started)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_state.py", line 287, in test_increment_labs_started
    state.increment_labs_started()
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'AppState' object has no attribute 'increment_labs_started'

```

**ERROR**: `test_increment_messages_sent (tests.test_state.TestIncrementMethods.test_increment_messages_sent)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_state.py", line 305, in test_increment_messages_sent
    state.increment_messages_sent()
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'AppState' object has no attribute 'increment_messages_sent'

```

**ERROR**: `test_increment_news_checked (tests.test_state.TestIncrementMethods.test_increment_news_checked)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_state.py", line 299, in test_increment_news_checked
    state.increment_news_checked()
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'AppState' object has no attribute 'increment_news_checked'

```

**ERROR**: `test_increment_quizzes_taken (tests.test_state.TestIncrementMethods.test_increment_quizzes_taken)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_state.py", line 293, in test_increment_quizzes_taken
    state.increment_quizzes_taken()
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'AppState' object has no attribute 'increment_quizzes_taken'

```

**ERROR**: `test_increment_social_success (tests.test_state.TestIncrementMethods.test_increment_social_success)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_state.py", line 311, in test_increment_social_success
    state.increment_social_success()
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'AppState' object has no attribute 'increment_social_success'

```

**ERROR**: `test_save_and_load_all_fields (tests.test_state.TestPersistence.test_save_and_load_all_fields)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_state.py", line 441, in test_save_and_load_all_fields
    self.assertEqual(new_state.review_schedule, state.review_schedule)
                     ^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'AppState' object has no attribute 'review_schedule'

```

**FAIL**: `test_get_due_reviews_returns_due_items (tests.test_state.TestSpacedRepetition.test_get_due_reviews_returns_due_items)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_state.py", line 189, in test_get_due_reviews_returns_due_items
    self.assertEqual(len(due), 1)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
AssertionError: 0 != 1

```

**ERROR**: `test_schedule_review_first_time (tests.test_state.TestSpacedRepetition.test_schedule_review_first_time)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_state.py", line 131, in test_schedule_review_first_time
    state.schedule_review(
    ~~~~~~~~~~~~~~~~~~~~~^
        "SQLi", 8.0, 10.0
        ^^^^^^^^^^^^^^^^^
    )  # first review always repetitions=0 regardless of quality
    ^
TypeError: AppState.schedule_review() takes 3 positional arguments but 4 were given

```

**ERROR**: `test_schedule_review_quality_bad_resets (tests.test_state.TestSpacedRepetition.test_schedule_review_quality_bad_resets)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_state.py", line 144, in test_schedule_review_quality_bad_resets
    state.schedule_review("XSS", 2.0, 10.0)
    ~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^
TypeError: AppState.schedule_review() takes 3 positional arguments but 4 were given

```

**ERROR**: `test_schedule_review_quality_good_increments (tests.test_state.TestSpacedRepetition.test_schedule_review_quality_good_increments)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_state.py", line 152, in test_schedule_review_quality_good_increments
    state.schedule_review("XSS", 7.0, 10.0)
    ~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^
TypeError: AppState.schedule_review() takes 3 positional arguments but 4 were given

```

**ERROR**: `test_clear_weak_topics (tests.test_state.TestWeakTopics.test_clear_weak_topics)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_state.py", line 122, in test_clear_weak_topics
    state.clear_weak_topics()
    ^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'AppState' object has no attribute 'clear_weak_topics'. Did you mean: 'get_weak_topics'?

```

**ERROR**: `test_update_weak_topic_creates_new (tests.test_state.TestWeakTopics.test_update_weak_topic_creates_new)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_state.py", line 17, in test_update_weak_topic_creates_new
    state.update_weak_topic("SQLi", 5.0, 10.0)
    ~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
TypeError: AppState.update_weak_topic() takes 3 positional arguments but 4 were given

```

**ERROR**: `test_update_weak_topic_updates_existing (tests.test_state.TestWeakTopics.test_update_weak_topic_updates_existing)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_state.py", line 28, in test_update_weak_topic_updates_existing
    state.update_weak_topic("XSS", 8.0, 10.0)  # 80%
    ~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^
TypeError: AppState.update_weak_topic() takes 3 positional arguments but 4 were given

```

### IMPORT ERROR: tests\test_summary.py
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\run_all_tests.py", line 76, in run_test_file
    module = importlib.import_module(module_name)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1406, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 938, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 759, in exec_module
  File "<frozen importlib._bootstrap>", line 491, in _call_with_frames_removed
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_summary.py", line 4, in <module>
    from handlers.summary import handle_summary
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\__init__.py", line 14, in <module>
    from .core import (  # основной диспетчер
        handle_commands,
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\core.py", line 30, in <module>
    from .misc import (
    ...<25 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\misc.py", line 15, in <module>
    from generators import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\generators.py", line 8, in <module>
    from knowledge import get_relevant_docs
  File "M:\Cyber_Teacher\Cyber_Teacher\knowledge.py", line 9, in <module>
    from langchain.text_splitter import RecursiveCharacterTextSplitter
ModuleNotFoundError: No module named 'langchain.text_splitter'

```

### IMPORT ERROR: tests\test_sync.py
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\run_all_tests.py", line 76, in run_test_file
    module = importlib.import_module(module_name)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1406, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 938, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 759, in exec_module
  File "<frozen importlib._bootstrap>", line 491, in _call_with_frames_removed
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_sync.py", line 8, in <module>
    from handlers.sync import (
    ...<4 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\__init__.py", line 14, in <module>
    from .core import (  # основной диспетчер
        handle_commands,
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\core.py", line 30, in <module>
    from .misc import (
    ...<25 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\misc.py", line 15, in <module>
    from generators import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\generators.py", line 8, in <module>
    from knowledge import get_relevant_docs
  File "M:\Cyber_Teacher\Cyber_Teacher\knowledge.py", line 9, in <module>
    from langchain.text_splitter import RecursiveCharacterTextSplitter
ModuleNotFoundError: No module named 'langchain.text_splitter'

```

### IMPORT ERROR: tests\test_theme_handler.py
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\run_all_tests.py", line 76, in run_test_file
    module = importlib.import_module(module_name)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1406, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 938, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 759, in exec_module
  File "<frozen importlib._bootstrap>", line 491, in _call_with_frames_removed
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_theme_handler.py", line 9, in <module>
    from handlers.theme import THEMES, get_theme_colors, handle_theme
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\__init__.py", line 14, in <module>
    from .core import (  # основной диспетчер
        handle_commands,
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\core.py", line 30, in <module>
    from .misc import (
    ...<25 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\misc.py", line 15, in <module>
    from generators import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\generators.py", line 8, in <module>
    from knowledge import get_relevant_docs
  File "M:\Cyber_Teacher\Cyber_Teacher\knowledge.py", line 9, in <module>
    from langchain.text_splitter import RecursiveCharacterTextSplitter
ModuleNotFoundError: No module named 'langchain.text_splitter'

```

### IMPORT ERROR: tests\test_threats_groups.py
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\run_all_tests.py", line 76, in run_test_file
    module = importlib.import_module(module_name)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1406, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 938, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 759, in exec_module
  File "<frozen importlib._bootstrap>", line 491, in _call_with_frames_removed
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_threats_groups.py", line 9, in <module>
    from handlers.threats import THREATS_DIR, handle_groups, handle_threats
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\__init__.py", line 14, in <module>
    from .core import (  # основной диспетчер
        handle_commands,
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\core.py", line 30, in <module>
    from .misc import (
    ...<25 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\misc.py", line 15, in <module>
    from generators import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\generators.py", line 8, in <module>
    from knowledge import get_relevant_docs
  File "M:\Cyber_Teacher\Cyber_Teacher\knowledge.py", line 9, in <module>
    from langchain.text_splitter import RecursiveCharacterTextSplitter
ModuleNotFoundError: No module named 'langchain.text_splitter'

```

### IMPORT ERROR: tests\test_threat_summary.py
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\run_all_tests.py", line 76, in run_test_file
    module = importlib.import_module(module_name)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1406, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 938, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 759, in exec_module
  File "<frozen importlib._bootstrap>", line 491, in _call_with_frames_removed
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_threat_summary.py", line 7, in <module>
    from handlers.threats import handle_threat_summary
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\__init__.py", line 14, in <module>
    from .core import (  # основной диспетчер
        handle_commands,
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\core.py", line 30, in <module>
    from .misc import (
    ...<25 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\misc.py", line 15, in <module>
    from generators import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\generators.py", line 8, in <module>
    from knowledge import get_relevant_docs
  File "M:\Cyber_Teacher\Cyber_Teacher\knowledge.py", line 9, in <module>
    from langchain.text_splitter import RecursiveCharacterTextSplitter
ModuleNotFoundError: No module named 'langchain.text_splitter'

```

### IMPORT ERROR: tests\test_timeloop.py
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\run_all_tests.py", line 76, in run_test_file
    module = importlib.import_module(module_name)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1406, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 938, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 759, in exec_module
  File "<frozen importlib._bootstrap>", line 491, in _call_with_frames_removed
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_timeloop.py", line 6, in <module>
    from handlers.timeloop import (
    ...<5 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\__init__.py", line 14, in <module>
    from .core import (  # основной диспетчер
        handle_commands,
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\core.py", line 30, in <module>
    from .misc import (
    ...<25 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\misc.py", line 15, in <module>
    from generators import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\generators.py", line 8, in <module>
    from knowledge import get_relevant_docs
  File "M:\Cyber_Teacher\Cyber_Teacher\knowledge.py", line 9, in <module>
    from langchain.text_splitter import RecursiveCharacterTextSplitter
ModuleNotFoundError: No module named 'langchain.text_splitter'

```

### tests\test_tracks.py
**ERROR**: `test_cmd_track_complete_topic_updates_progress (tests.test_tracks.TestHandlersTracks.test_cmd_track_complete_topic_updates_progress)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_tracks.py", line 265, in setUp
    self.mock_get_context = self.context_patcher.start()
                            ~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "C:\Python314\Lib\unittest\mock.py", line 1667, in start
    result = self.__enter__()
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1406, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
  File "<frozen impor
```

**ERROR**: `test_cmd_track_next_returns_first_topic (tests.test_tracks.TestHandlersTracks.test_cmd_track_next_returns_first_topic)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_tracks.py", line 265, in setUp
    self.mock_get_context = self.context_patcher.start()
                            ~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "C:\Python314\Lib\unittest\mock.py", line 1667, in start
    result = self.__enter__()
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1406, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
  File "<frozen impor
```

**ERROR**: `test_cmd_track_next_skips_completed (tests.test_tracks.TestHandlersTracks.test_cmd_track_next_skips_completed)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_tracks.py", line 265, in setUp
    self.mock_get_context = self.context_patcher.start()
                            ~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "C:\Python314\Lib\unittest\mock.py", line 1667, in start
    result = self.__enter__()
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1406, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
  File "<frozen impor
```

**ERROR**: `test_cmd_track_progress_no_enrolled (tests.test_tracks.TestHandlersTracks.test_cmd_track_progress_no_enrolled)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_tracks.py", line 265, in setUp
    self.mock_get_context = self.context_patcher.start()
                            ~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "C:\Python314\Lib\unittest\mock.py", line 1667, in start
    result = self.__enter__()
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1406, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
  File "<frozen impor
```

**ERROR**: `test_cmd_track_progress_summary (tests.test_tracks.TestHandlersTracks.test_cmd_track_progress_summary)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_tracks.py", line 265, in setUp
    self.mock_get_context = self.context_patcher.start()
                            ~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "C:\Python314\Lib\unittest\mock.py", line 1667, in start
    result = self.__enter__()
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1406, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
  File "<frozen impor
```

**ERROR**: `test_cmd_track_recommend (tests.test_tracks.TestHandlersTracks.test_cmd_track_recommend)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_tracks.py", line 265, in setUp
    self.mock_get_context = self.context_patcher.start()
                            ~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "C:\Python314\Lib\unittest\mock.py", line 1667, in start
    result = self.__enter__()
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1406, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
  File "<frozen impor
```

**ERROR**: `test_cmd_track_reset_removes_progress (tests.test_tracks.TestHandlersTracks.test_cmd_track_reset_removes_progress)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_tracks.py", line 265, in setUp
    self.mock_get_context = self.context_patcher.start()
                            ~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "C:\Python314\Lib\unittest\mock.py", line 1667, in start
    result = self.__enter__()
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1406, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
  File "<frozen impor
```

**ERROR**: `test_cmd_track_start_already_enrolled (tests.test_tracks.TestHandlersTracks.test_cmd_track_start_already_enrolled)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_tracks.py", line 265, in setUp
    self.mock_get_context = self.context_patcher.start()
                            ~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "C:\Python314\Lib\unittest\mock.py", line 1667, in start
    result = self.__enter__()
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1406, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
  File "<frozen impor
```

**ERROR**: `test_cmd_track_start_missing_id (tests.test_tracks.TestHandlersTracks.test_cmd_track_start_missing_id)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_tracks.py", line 265, in setUp
    self.mock_get_context = self.context_patcher.start()
                            ~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "C:\Python314\Lib\unittest\mock.py", line 1667, in start
    result = self.__enter__()
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1406, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
  File "<frozen impor
```

**ERROR**: `test_cmd_track_start_prereqs_missing (tests.test_tracks.TestHandlersTracks.test_cmd_track_start_prereqs_missing)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_tracks.py", line 265, in setUp
    self.mock_get_context = self.context_patcher.start()
                            ~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "C:\Python314\Lib\unittest\mock.py", line 1667, in start
    result = self.__enter__()
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1406, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
  File "<frozen impor
```

**ERROR**: `test_cmd_track_start_success (tests.test_tracks.TestHandlersTracks.test_cmd_track_start_success)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_tracks.py", line 265, in setUp
    self.mock_get_context = self.context_patcher.start()
                            ~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "C:\Python314\Lib\unittest\mock.py", line 1667, in start
    result = self.__enter__()
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1406, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
  File "<frozen impor
```

**ERROR**: `test_cmd_track_start_unknown (tests.test_tracks.TestHandlersTracks.test_cmd_track_start_unknown)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_tracks.py", line 265, in setUp
    self.mock_get_context = self.context_patcher.start()
                            ~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "C:\Python314\Lib\unittest\mock.py", line 1667, in start
    result = self.__enter__()
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1406, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
  File "<frozen impor
```

**ERROR**: `test_cmd_track_status_no_active (tests.test_tracks.TestHandlersTracks.test_cmd_track_status_no_active)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_tracks.py", line 265, in setUp
    self.mock_get_context = self.context_patcher.start()
                            ~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "C:\Python314\Lib\unittest\mock.py", line 1667, in start
    result = self.__enter__()
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1406, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
  File "<frozen impor
```

**ERROR**: `test_cmd_track_status_shows_current (tests.test_tracks.TestHandlersTracks.test_cmd_track_status_shows_current)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_tracks.py", line 265, in setUp
    self.mock_get_context = self.context_patcher.start()
                            ~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "C:\Python314\Lib\unittest\mock.py", line 1667, in start
    result = self.__enter__()
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1406, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
  File "<frozen impor
```

**ERROR**: `test_cmd_tracks_list_empty (tests.test_tracks.TestHandlersTracks.test_cmd_tracks_list_empty)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_tracks.py", line 265, in setUp
    self.mock_get_context = self.context_patcher.start()
                            ~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "C:\Python314\Lib\unittest\mock.py", line 1667, in start
    result = self.__enter__()
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1406, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
  File "<frozen impor
```

**ERROR**: `test_cmd_tracks_list_shows_tracks (tests.test_tracks.TestHandlersTracks.test_cmd_tracks_list_shows_tracks)`
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_tracks.py", line 265, in setUp
    self.mock_get_context = self.context_patcher.start()
                            ~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "C:\Python314\Lib\unittest\mock.py", line 1667, in start
    result = self.__enter__()
  File "C:\Python314\Lib\unittest\mock.py", line 1494, in __enter__
    self.target = self.getter()
                  ~~~~~~~~~~~^^
  File "C:\Python314\Lib\pkgutil.py", line 458, in resolve_name
    mod = importlib.import_module(modname)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1406, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
  File "<frozen impor
```

### IMPORT ERROR: tests\test_tryhackme.py
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\run_all_tests.py", line 76, in run_test_file
    module = importlib.import_module(module_name)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1406, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 938, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 759, in exec_module
  File "<frozen importlib._bootstrap>", line 491, in _call_with_frames_removed
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_tryhackme.py", line 14, in <module>
    from handlers.tryhackme import (
    ...<2 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\__init__.py", line 14, in <module>
    from .core import (  # основной диспетчер
        handle_commands,
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\core.py", line 30, in <module>
    from .misc import (
    ...<25 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\misc.py", line 15, in <module>
    from generators import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\generators.py", line 8, in <module>
    from knowledge import get_relevant_docs
  File "M:\Cyber_Teacher\Cyber_Teacher\knowledge.py", line 9, in <module>
    from langchain.text_splitter import RecursiveCharacterTextSplitter
ModuleNotFoundError: No module named 'langchain.text_splitter'

```

### IMPORT ERROR: tests\test_voice.py
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\run_all_tests.py", line 76, in run_test_file
    module = importlib.import_module(module_name)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1406, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 938, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 759, in exec_module
  File "<frozen importlib._bootstrap>", line 491, in _call_with_frames_removed
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_voice.py", line 6, in <module>
    from handlers.voice import _speak, handle_voice
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\__init__.py", line 14, in <module>
    from .core import (  # основной диспетчер
        handle_commands,
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\core.py", line 30, in <module>
    from .misc import (
    ...<25 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\misc.py", line 15, in <module>
    from generators import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\generators.py", line 8, in <module>
    from knowledge import get_relevant_docs
  File "M:\Cyber_Teacher\Cyber_Teacher\knowledge.py", line 9, in <module>
    from langchain.text_splitter import RecursiveCharacterTextSplitter
ModuleNotFoundError: No module named 'langchain.text_splitter'

```

### IMPORT ERROR: tests\test_voice_stt.py
```
Traceback (most recent call last):
  File "M:\Cyber_Teacher\Cyber_Teacher\run_all_tests.py", line 76, in run_test_file
    module = importlib.import_module(module_name)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1406, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 938, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 759, in exec_module
  File "<frozen importlib._bootstrap>", line 491, in _call_with_frames_removed
  File "M:\Cyber_Teacher\Cyber_Teacher\tests\test_voice_stt.py", line 6, in <module>
    from handlers.voice import (
    ...<4 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\__init__.py", line 14, in <module>
    from .core import (  # основной диспетчер
        handle_commands,
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\core.py", line 30, in <module>
    from .misc import (
    ...<25 lines>...
    )
  File "M:\Cyber_Teacher\Cyber_Teacher\handlers\misc.py", line 15, in <module>
    from generators import check_open_answer
  File "M:\Cyber_Teacher\Cyber_Teacher\generators.py", line 8, in <module>
    from knowledge import get_relevant_docs
  File "M:\Cyber_Teacher\Cyber_Teacher\knowledge.py", line 9, in <module>
    from langchain.text_splitter import RecursiveCharacterTextSplitter
ModuleNotFoundError: No module named 'langchain.text_splitter'

```
