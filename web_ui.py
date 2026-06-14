#!/usr/bin/env python3
"""Enhanced Streamlit Web UI for CyberTeacher with analytics dashboard."""

import json
import os
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

STATE_PATH = Path("./memory/app_state.json")
METRICS_PATH = Path("./memory/metrics.json")


# ── Helper functions (testable without streamlit) ─────────────────


def load_state() -> dict[Any, Any]:
    """Load application state from JSON file."""
    if STATE_PATH.exists():
        try:
            with open(STATE_PATH, "r", encoding="utf-8") as f:
                result: dict[Any, Any] = json.load(f)
                return result
        except (OSError, IOError, json.JSONDecodeError):
            return {}
    return {}


def load_metrics() -> dict[Any, Any]:
    """Load metrics history if available."""
    if METRICS_PATH.exists():
        try:
            with open(METRICS_PATH, "r", encoding="utf-8") as f:
                result: dict[Any, Any] = json.load(f)
                return result
        except (OSError, IOError, json.JSONDecodeError):
            return {}
    return {}


def generate_xp_history(state: dict) -> list[dict[Any, Any]]:
    """Generate XP history from state (simulated if no history stored)."""
    xp_history: list[dict[Any, Any]] = state.get("xp_history", [])
    if not xp_history:
        current = state.get("points", 0)
        if current > 0:
            days = 30
            xp_history = [
                {
                    "date": (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d"),
                    "xp": max(
                        0,
                        current * (1 - i / days) + (current * 0.1 * (days - i) / days),
                    ),
                }
                for i in range(days, 0, -1)
            ]
    return xp_history


def generate_activity_heatmap(state: dict) -> list[list[int]]:
    """Generate 7x4 activity heatmap (last 4 weeks)."""
    activity = state.get("activity_log", {})
    heatmap = []
    for week in range(4):
        week_data = []
        for day in range(7):
            date_str = (
                datetime.now() - timedelta(days=(3 - week) * 7 + (6 - day))
            ).strftime("%Y-%m-%d")
            count = activity.get(date_str, 0)
            week_data.append(count)
        heatmap.append(week_data)
    return heatmap


# ── Streamlit UI (only runs when executed directly) ───────────────


def run_dashboard():
    """Run the Streamlit dashboard."""
    import streamlit as st

    st.set_page_config(
        page_title="CyberTeacher Dashboard",
        page_icon="🛡️",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    state = load_state()

    # ── Sidebar ───────────────────────────────────────────────────
    st.sidebar.title("🛡️ CyberTeacher")
    st.sidebar.markdown("---")

    username = state.get("username", "Аноним")
    avatar = state.get("avatar", "🧑‍💻")
    st.sidebar.markdown(f"### {avatar} {username}")

    st.sidebar.metric("XP", f"{state.get('points', 0):.0f}")
    st.sidebar.metric("Репутация", state.get("reputation", 0))
    st.sidebar.metric("Режим", state.get("current_mode", "—"))

    refresh = st.sidebar.checkbox("Авто-обновление (5с)", value=False)
    if refresh:
        time.sleep(5)
        st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.info("Для интерактива используйте CLI: `python main.py`")

    # ── Main content ──────────────────────────────────────────────
    st.title("📊 CyberTeacher Dashboard")

    tabs = st.tabs(
        [
            "📈 Прогресс",
            "🔥 Активность",
            "🎯 Навыки",
            "📚 Обучение",
            "📖 История",
            "🛤️ Треки",
            "🚩 CTF",
            "🐳 Лаборатории",
            "🔍 OSINT",
            "💻 Scanner",
            "🛒 Магазин",
            "🏆 Достижения",
            "⚙️ Настройки",
        ]
    )

    # ── Tab 1: Progress ──────────────────────────────────────────
    with tabs[0]:
        st.header("📈 Прогресс обучения")

        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("XP", f"{state.get('points', 0):.0f}")
        with col2:
            st.metric("Квизов", state.get("quizzes_taken", 0))
        with col3:
            st.metric("Флагов", state.get("total_flags_collected", 0))
        with col4:
            st.metric("Лаб", state.get("labs_started", 0))
        with col5:
            st.metric("Уровень", state.get("level", 1))

        st.markdown("---")

        st.subheader("📊 XP за последние 30 дней")
        xp_history = generate_xp_history(state)

        if xp_history:
            try:
                import pandas as pd

                df = pd.DataFrame(xp_history)
                df["date"] = pd.to_datetime(df["date"])
                st.line_chart(df.set_index("date")["xp"], use_container_width=True)
            except ImportError:
                values = [h["xp"] for h in xp_history]
                st.line_chart({"XP": values}, use_container_width=True)
        else:
            st.info("Нет данных об XP. Начните обучение для отображения графика.")

        st.subheader("🔴 Слабые темы")
        weak_topics = state.get("weak_topics", [])
        if weak_topics:
            for topic in weak_topics[:5]:
                score = topic.get("max_score", 0)
                st.progress(
                    score / 100, text=f"{topic.get('name', 'Unknown')}: {score:.0f}%"
                )
        else:
            st.success("Нет слабых тем! Отличная работа.")

    # ── Tab 2: Activity Heatmap ──────────────────────────────────
    with tabs[1]:
        st.header("🔥 Карта активности")

        heatmap = generate_activity_heatmap(state)
        days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]

        col_labels, col_heatmap = st.columns([1, 10])

        with col_labels:
            st.write("")
            for day in days:
                st.write(day)

        with col_heatmap:
            max_val = (
                max(max(row) for row in heatmap)
                if any(any(v > 0 for v in row) for row in heatmap)
                else 1
            )

            for week_idx, week in enumerate(heatmap):
                cols = st.columns(7)
                for day_idx, count in enumerate(week):
                    intensity = count / max_val if max_val > 0 else 0
                    color = f"rgba(0, {100 + int(intensity * 155)}, 0, {0.2 + intensity * 0.8})"
                    with cols[day_idx]:
                        st.markdown(
                            f"<div style='background:{color};padding:10px;text-align:center;border-radius:4px;margin:2px;'>"
                            f"{count}</div>",
                            unsafe_allow_html=True,
                        )

        st.caption("🟢 Зелёный = высокая активность | Показаны последние 4 недели")

        st.markdown("---")
        st.subheader("📊 Статистика активности")
        col1, col2, col3 = st.columns(3)
        with col1:
            total_actions = sum(sum(w) for w in heatmap)
            st.metric("Действий (4 недели)", total_actions)
        with col2:
            active_days = sum(1 for w in heatmap for v in w if v > 0)
            st.metric("Активных дней", active_days)
        with col3:
            streak = state.get("daily_streak", 0)
            st.metric("🔥 Стрик", f"{streak} дней")

    # ── Tab 3: Skills ────────────────────────────────────────────
    with tabs[2]:
        st.header("🎯 Навыки")

        skill_tracker = state.get("skill_tracker", {})
        if skill_tracker:
            for skill_name, skill_data in sorted(
                skill_tracker.items(), key=lambda x: x[1].get("level", 0), reverse=True
            ):
                level = skill_data.get("level", 0)
                xp = skill_data.get("xp", 0)
                success_rate = skill_data.get("success_rate", 0)
                attempts = skill_data.get("attempts", 0)

                col1, col2 = st.columns([3, 1])
                with col1:
                    st.progress(min(level / 5, 1.0), text=f"{skill_name} — L{level}")
                with col2:
                    st.metric("XP", f"{xp:.0f}")
                    st.caption(f"Успех: {success_rate:.0f}% ({attempts} попыток)")
        else:
            st.info(
                "Нет записанных навыков. Используйте /skills track для отслеживания."
            )

    # ── Tab 4: Learning ──────────────────────────────────────────
    with tabs[3]:
        st.header("📚 Обучение")

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Курсы")
            # Load courses from API
            import requests

            try:
                response = requests.get("http://localhost:8000/api/courses", timeout=2)
                if response.status_code == 200:
                    courses_data = response.json().get("courses", [])
                    if courses_data:
                        # Create course selection
                        course_options = {
                            course["name"]: course["id"] for course in courses_data
                        }
                        selected_course_name = st.selectbox(
                            "Выберите курс",
                            options=list(course_options.keys()),
                            index=0 if course_options else None,
                        )
                        if selected_course_name:
                            selected_course_id = course_options[selected_course_name]
                            # Find selected course details
                            selected_course = next(
                                (
                                    c
                                    for c in courses_data
                                    if c["id"] == selected_course_id
                                ),
                                None,
                            )
                            if selected_course:
                                st.write(f"Текущий курс: **{selected_course['name']}**")
                                st.write(f"Прогресс: {selected_course['progress']}%")
                                st.write(f"Тем: {selected_course['topics_count']}")
                                if st.button("Начать курс"):
                                    # Select course via API
                                    try:
                                        requests.post(
                                            f"http://localhost:8000/api/courses/{selected_course_id}/select"
                                        )
                                        st.success(
                                            f"Курс '{selected_course['name']}' выбран!"
                                        )
                                        st.rerun()
                                    except:
                                        st.error("Не удалось выбрать курс")
                        else:
                            st.info("Курсы не найдены")
                    else:
                        st.warning("API недоступен")
            except:
                # Fallback to current state
                current_course = state.get("current_course", "Не выбран")
                current_topic = state.get("current_topic", "—")
                st.write(f"Текущий курс: **{current_course}**")
                st.write(f"Текущая тема: **{current_topic}**")

        with col2:
            st.subheader("Повторения")
            review_schedule = state.get("review_schedule", {})
            if review_schedule:
                due = sum(
                    1
                    for r in review_schedule.values()
                    if r.get("next_review", 0) < time.time()
                )
                st.metric("Просрочено", due)
                st.metric("Всего в расписании", len(review_schedule))
            else:
                st.info("Нет запланированных повторений.")

        st.markdown("---")

        st.subheader("🎮 Миссии")
        missions_completed = state.get("missions_completed", [])
        st.metric("Пройдено миссий", len(missions_completed))

        if missions_completed:
            st.write(", ".join(missions_completed[:10]))
            if len(missions_completed) > 10:
                st.caption(f"...и ещё {len(missions_completed) - 10}")

    # ── Tab 5: History (Story Mode) ─────────────────────────────────────
    with tabs[4]:
        st.header("📖 История")

        # Load story episodes from API
        import requests

        try:
            response = requests.get("http://localhost:8000/api/story", timeout=2)
            if response.status_code == 200:
                story_data = response.json()
                episodes = story_data.get("episodes", [])
                if episodes:
                    # Create episode selection
                    episode_options = {ep["title"]: ep["id"] for ep in episodes}
                    selected_episode_title = st.selectbox(
                        "Выберите эпизод",
                        options=list(episode_options.keys()),
                        index=0 if episode_options else None,
                    )
                    if selected_episode_title:
                        selected_episode_id = episode_options[selected_episode_title]
                        # Find selected episode details
                        selected_episode = next(
                            (ep for ep in episodes if ep["id"] == selected_episode_id),
                            None,
                        )
                        if selected_episode:
                            st.subheader(selected_episode["title"])
                            st.write(selected_episode["description"])

                            # Check if episode is started/completed
                            if selected_episode.get("completed", False):
                                st.success("✅ Эпизод завершен")
                            elif selected_episode.get("started", False):
                                st.info("▶️ Эпизод в прогрессе")
                                # Answer input
                                user_answer = st.text_input(
                                    "Ваш ответ или флаг:",
                                    key=f"answer_{selected_episode_id}",
                                )
                                if st.button(
                                    "Отправить ответ",
                                    key=f"submit_{selected_episode_id}",
                                ):
                                    if user_answer:
                                        try:
                                            # Submit answer via API
                                            resp = requests.post(
                                                "http://localhost:8000/api/story/submit",
                                                json={
                                                    "episode_id": selected_episode_id,
                                                    "answer": user_answer,
                                                },
                                                timeout=5,
                                            )
                                            if resp.status_code == 200:
                                                result = resp.json()
                                                if result.get("correct"):
                                                    st.success(
                                                        "✅ Правильно! Эпизод завершен."
                                                    )
                                                    st.rerun()
                                                else:
                                                    st.error(
                                                        "❌ Неправильно. Попробуйте еще раз."
                                                    )
                                                    # Show hint if available
                                                    if result.get("hint"):
                                                        st.info(
                                                            f"💡 Подсказка: {result['hint']}"
                                                        )
                                        except Exception as e:
                                            st.error(f"Ошибка отправки: {str(e)}")
                                    else:
                                        st.warning("Пожалуйста, введите ответ")
                            else:
                                st.write("Нажмите 'Начать эпизод', чтобы начать")
                                if st.button(
                                    "Начать эпизод", key=f"start_{selected_episode_id}"
                                ):
                                    try:
                                        resp = requests.post(
                                            f"http://localhost:8000/api/story/start/{selected_episode_id}",
                                            timeout=5,
                                        )
                                        if resp.status_code == 200:
                                            st.success("Эпизод начался!")
                                            st.rerun()
                                        else:
                                            st.error("Не удалось начать эпизод")
                                    except Exception as e:
                                        st.error(f"Ошибка: {str(e)}")
                        else:
                            st.info("Выберите эпизод из списка выше")
                else:
                    st.info("Эпизоды истории не найдены")
            else:
                st.warning("API истории недоступен")
        except:
            st.error("Не удалось загрузить данные истории")

    # ── Tab 6: Tracks ───────────────────────────────────────────────────
    with tabs[5]:
        st.header("🛤️ Треки обучения")

        # Load tracks from API
        import requests

        try:
            response = requests.get("http://localhost:8000/api/tracks", timeout=2)
            if response.status_code == 200:
                tracks_data = response.json().get("tracks", [])
                if tracks_data:
                    # Create track selection
                    track_options = {
                        track["name"]: track["id"] for track in tracks_data
                    }
                    selected_track_name = st.selectbox(
                        "Выберите трек",
                        options=list(track_options.keys()),
                        index=0 if track_options else None,
                    )
                    if selected_track_name:
                        selected_track_id = track_options[selected_track_name]
                        # Find selected track details
                        selected_track = next(
                            (t for t in tracks_data if t["id"] == selected_track_id),
                            None,
                        )
                        if selected_track:
                            st.subheader(selected_track["name"])
                            st.write(selected_track["description"])

                            progress = selected_track.get("progress", 0)
                            st.progress(progress / 100, text=f"Прогресс: {progress}%")

                            # Show current topic/step
                            current_step = selected_track.get(
                                "current_step", "Не начато"
                            )
                            st.write(f"Текущий шаг: {current_step}")

                            if st.button(
                                "Начать трек", key=f"start_track_{selected_track_id}"
                            ):
                                try:
                                    resp = requests.post(
                                        f"http://localhost:8000/api/tracks/start/{selected_track_id}",
                                        timeout=5,
                                    )
                                    if resp.status_code == 200:
                                        st.success("Трек начат!")
                                        st.rerun()
                                    else:
                                        st.error("Не удалось начать трек")
                                except Exception as e:
                                    st.error(f"Ошибка: {str(e)}")
                        else:
                            st.info("Выберите трек из списка выше")
                else:
                    st.info("Треки обучения не найдены")
            else:
                st.warning("API треков недоступен")
        except:
            st.error("Не удалось загрузить данные треков")

    # ── Tab 7: CTF ──────────────────────────────────────────────────────
    with tabs[6]:
        st.header("🚩 CTF Центр")

        # Load CTF status from API
        import requests

        try:
            response = requests.get("http://localhost:8000/api/ctf/status", timeout=2)
            if response.status_code == 200:
                ctf_data = response.json()

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Флагов собрано", ctf_data.get("flags_collected", 0))
                with col2:
                    st.metric("Активных миссий", ctf_data.get("active_missions", 0))
                with col3:
                    st.metric("Репутации", ctf_data.get("reputation", 0))

                st.markdown("---")

                # Recent flags
                recent_flags = ctf_data.get("recent_flags", [])
                if recent_flags:
                    st.subheader("Последние флаги")
                    for flag in recent_flags[:5]:
                        status_icon = "✅" if flag.get("verified") else "⏳"
                        st.write(
                            f"{status_icon} {flag.get('name', 'Неизвестный флаг')} - {flag.get('points', 0)} XP"
                        )
                else:
                    st.info("Пока нет собранных флагов")

                # Available missions
                missions = ctf_data.get("missions", [])
                if missions:
                    st.subheader("Доступные миссии")
                    for mission in missions[:3]:
                        with st.expander(
                            f"{mission.get('name', 'Миссия')} - {mission.get('difficulty', '???')}"
                        ):
                            st.write(mission.get("description", ""))
                            if st.button(
                                f"Начать миссию",
                                key=f"start_mission_{mission.get('id', '')}",
                            ):
                                try:
                                    resp = requests.post(
                                        f"http://localhost:8000/api/missions/start/{mission.get('id')}",
                                        timeout=5,
                                    )
                                    if resp.status_code == 200:
                                        st.success("Миссия начата!")
                                        st.rerun()
                                    else:
                                        st.error("Не удалось начать миссию")
                                except Exception as e:
                                    st.error(f"Ошибка: {str(e)}")
                else:
                    st.info("Миссии не найдены")
            else:
                st.warning("API CTF недоступен")
        except:
            st.error("Не удалось загрузить данные CTF")

    # ── Tab 8: Laboratories ─────────────────────────────────────────────
    with tabs[7]:
        st.header("🐳 Docker Лаборатории")

        # Load labs from API
        import requests

        try:
            response = requests.get("http://localhost:8000/api/labs", timeout=2)
            if response.status_code == 200:
                labs_data = response.json().get("labs", [])
                if labs_data:
                    # Filter and display labs
                    for lab in labs_data:
                        with st.expander(
                            f"{lab.get('name', 'Лаборатория')} [{lab.get('difficulty', '???').title()}]"
                        ):
                            st.write(lab.get("description", ""))

                            status = (
                                "🟢 Запущена"
                                if lab.get("running")
                                else "⚪ Остановлена"
                            )
                            st.write(f"Статус: {status}")

                            cols = st.columns(2)
                            with cols[0]:
                                if not lab.get("running"):
                                    if st.button(
                                        "Запустить", key=f"start_lab_{lab.get('id')}"
                                    ):
                                        try:
                                            resp = requests.post(
                                                f"http://localhost:8000/api/labs/{lab.get('id')}/start",
                                                timeout=10,
                                            )
                                            if resp.status_code == 200:
                                                st.success("Лаборатория запущена!")
                                                st.rerun()
                                            else:
                                                st.error(
                                                    "Не удалось запустить лабораторию"
                                                )
                                        except Exception as e:
                                            st.error(f"Ошибка: {str(e)}")
                                else:
                                    if st.button(
                                        "Остановить", key=f"stop_lab_{lab.get('id')}"
                                    ):
                                        try:
                                            resp = requests.post(
                                                f"http://localhost:8000/api/labs/{lab.get('id')}/stop",
                                                timeout=10,
                                            )
                                            if resp.status_code == 200:
                                                st.success("Лаборатория остановлена!")
                                                st.rerun()
                                            else:
                                                st.error(
                                                    "Не удалось остановить лабораторию"
                                                )
                                        except Exception as e:
                                            st.error(f"Ошибка: {str(e)}")

                            with cols[1]:
                                if lab.get("ports"):
                                    st.write("Доступно по портам:")
                                    for port in lab.get("ports", []):
                                        st.code(f"http://localhost:{port}")
                else:
                    st.info("Лаборатории не найдены")
            else:
                st.warning("API лабораторий недоступен")
        except:
            st.error("Не удалось загрузить данные лабораторий")

    # ── Tab 9: OSINT ────────────────────────────────────────────────────
    with tabs[8]:
        st.header("🔍 OSINT Центр")

        # Load threats (APT groups) from API
        import requests

        try:
            threats_response = requests.get(
                "http://localhost:8000/api/threats", timeout=2
            )
            news_response = requests.get("http://localhost:8000/api/news", timeout=2)

            col1, col2 = st.columns([1, 1])

            with col1:
                st.subheader("APT Группы")
                if threats_response.status_code == 200:
                    threats_data = threats_response.json()
                    groups = threats_data.get("groups", [])
                    if groups:
                        for group in groups[:5]:  # Show top 5
                            with st.expander(
                                f"{group.get('name', 'Группа')} ({group.get('country', '???')})"
                            ):
                                st.write(
                                    f"Специализация: {group.get('specialization', 'Не указана')}"
                                )
                                st.write(
                                    f"Уровень угрозы: {group.get('threat_level', '???')}/10"
                                )
                                if st.button(
                                    f"Подробнее",
                                    key=f"apt_detail_{group.get('id', '')}",
                                ):
                                    st.info(
                                        group.get("description", "Описание недоступно")
                                    )
                    else:
                        st.info("APT группы не найдены")
                else:
                    st.warning("API угроз недоступен")

            with col2:
                st.subheader("Последние новости")
                if news_response.status_code == 200:
                    news_data = news_response.json()
                    articles = news_data.get("articles", [])
                    if articles:
                        for article in articles[:5]:  # Show top 5
                            with st.expander(
                                f"{article.get('title', 'Новость')} - {article.get('source', '???')}"
                            ):
                                st.write(article.get("summary", ""))
                                if article.get("url"):
                                    st.link_button("Читать полностью", article["url"])
                    else:
                        st.info("Новости не найдены")
                else:
                    st.warning("API новостей недоступен")

            st.markdown("---")

            # CVE Search
            st.subheader("Поиск CVE")
            cve_id = st.text_input(
                "Введите ID CVE (например, CVE-2023-12345)", placeholder="CVE-2023-..."
            )
            if st.button("Найти CVE") and cve_id:
                try:
                    resp = requests.get(
                        f"http://localhost:8000/api/cve/{cve_id.upper()}", timeout=5
                    )
                    if resp.status_code == 200:
                        cve_data = resp.json()
                        st.subheader(f"CVE: {cve_data.get('id', '')}")
                        st.write(f"**Описание:** {cve_data.get('description', '')}")
                        st.write(f"**Серьезность:** {cve_data.get('severity', '???')}")
                        st.write(f"**CVSS Score:** {cve_data.get('cvss_score', '???')}")
                        if cve_data.get("references"):
                            st.write("**Ссылки:**")
                            for ref in cve_data["references"][:3]:
                                st.write(f"- {ref}")
                    elif resp.status_code == 404:
                        st.error("CVE не найден")
                    else:
                        st.error("Ошибка при поиске CVE")
                except Exception as e:
                    st.error(f"Ошибка: {str(e)}")
        except:
            st.error("Не удалось загрузить данные OSINT")

    # ── Tab 10: Scanner ─────────────────────────────────────────────────
    with tabs[9]:
        st.header("🔍 Scanner (Сканер кода)")

        st.subheader("Статический анализ кода")

        # File upload
        uploaded_file = st.file_uploader(
            "Загрузите файл для анализа",
            type=["py", "js", "java", "cpp", "c", "php", "rb", "go", "rs"],
            help="Поддерживаемые форматы: Python, JavaScript, Java, C/C++, PHP, Ruby, Go, Rust",
        )

        if uploaded_file is not None:
            # Display file info
            st.write(f"Имя файла: {uploaded_file.name}")
            st.write(f"Размер: {uploaded_file.size} байт")

            # Read file content
            try:
                content = uploaded_file.read().decode("utf-8")
                st.text_area("Содержимое файла:", content, height=200, disabled=True)

                # Reset file pointer for upload
                uploaded_file.seek(0)

                if st.button("Проанализировать код"):
                    try:
                        # Prepare file for upload
                        files = {
                            "file": (
                                uploaded_file.name,
                                uploaded_file,
                                uploaded_file.type,
                            )
                        }
                        resp = requests.post(
                            "http://localhost:8000/api/scanv2", files=files, timeout=10
                        )
                        if resp.status_code == 200:
                            results = resp.json()

                            st.subheader("Результаты анализа")

                            # Summary
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric(
                                    "Всего проблем", results.get("total_issues", 0)
                                )
                            with col2:
                                st.metric(
                                    "Критичных", results.get("critical_issues", 0)
                                )
                            with col3:
                                st.metric(
                                    "Предупреждений", results.get("warning_issues", 0)
                                )

                            # Details by severity
                            if results.get("issues"):
                                for severity in ["critical", "high", "medium", "low"]:
                                    issues = [
                                        issue
                                        for issue in results["issues"]
                                        if issue.get("severity") == severity
                                    ]
                                    if issues:
                                        with st.expander(
                                            f"{severity.title()} ({len(issues)})"
                                        ):
                                            for issue in issues:
                                                st.write(
                                                    f"**{issue.get('rule_id', '')}**: {issue.get('message', '')}"
                                                )
                                                st.caption(
                                                    f"Файл: {issue.get('file', '')}:{issue.get('line', '')}"
                                                )
                            else:
                                st.success("❌ Проблемы не найдены! Отличный код.")
                        else:
                            st.error("Ошибка при анализе кода")
                    except Exception as e:
                        st.error(f"Ошибка: {str(e)}")
            except Exception as e:
                st.error(f"Не удалось прочитать файл: {str(e)}")
        else:
            st.info("Загрузите файл для анализа кода")

        st.markdown("---")

        # Quick scan examples
        st.subheader("Быстрая проверка примеров")
        example_code = st.selectbox(
            "Выберите пример для проверки:",
            [
                "Безопасный код",
                "SQL Injection уязвимость",
                "XSS уязвимость",
                "Hardcoded секрет",
                "Небезопасная разрядка",
            ],
        )

        if st.button("Проверить пример"):
            # Define example snippets
            examples = {
                "Безопасный код": "def add(a, b):\n    return a + b\n\nresult = add(2, 3)\nprint(result)",
                "SQL Injection уязвимость": 'def get_user(user_id):\n    query = f"SELECT * FROM users WHERE id = {user_id}"\n    return execute_query(query)',
                "XSS уязвимость": "def render_comment(comment):\n    return f'<div>{comment}</div>'  # Unsafely renders user input",
                "Hardcoded секрет": "API_KEY = 'sk_live_REPLACE_WITH_YOUR_KEY'\nDB_PASSWORD = 'admin123'",
                "Небезопасная разрядка": "import os\nos.system(user_input)  # Direct command execution",
            }

            if example_code in examples:
                code_to_scan = examples[example_code]
                st.code(code_to_scan, language="python")

                # Create temporary file-like object for scanning
                import io

                file_obj = io.BytesIO(code_to_scan.encode("utf-8"))
                file_obj.name = "example.py"

                try:
                    files = {"file": (file_obj.name, file_obj, "text/plain")}
                    resp = requests.post(
                        "http://localhost:8000/api/scanv2", files=files, timeout=10
                    )
                    if resp.status_code == 200:
                        results = resp.json()

                        if results.get("total_issues", 0) > 0:
                            st.error(f"⚠️ Найдено проблем: {results['total_issues']}")
                            for issue in results.get("issues", [])[:3]:  # Show first 3
                                st.write(
                                    f"🔴 {issue.get('rule_id', '')}: {issue.get('message', '')}"
                                )
                        else:
                            st.success("✅ Проблемы не обнаружены")
                    else:
                        st.error("Ошибка при сканировании")
                except Exception as e:
                    st.error(f"Ошибка: {str(e)}")

    # ── Tab 11: Shop ────────────────────────────────────────────────────
    with tabs[10]:
        st.header("🛒 Магазин CyberTeacher")

        # Load shop items from API
        import requests

        try:
            response = requests.get("http://localhost:8000/api/shop", timeout=2)
            if response.status_code == 200:
                shop_data = response.json()
                items = shop_data.get("items", [])
                user_xp = state.get("points", 0)

                st.write(f"Ваш баланс: **{user_xp} XP**")

                if items:
                    # Group items by category
                    categories = {}
                    for item in items:
                        category = item.get("category", "Прочее")
                        if category not in categories:
                            categories[category] = []
                        categories[category].append(item)

                    # Display items by category
                    for category, category_items in categories.items():
                        st.subheader(f"{category}")

                        cols = st.columns(min(3, len(category_items)))
                        for idx, item in enumerate(category_items):
                            with cols[idx % 3]:
                                # Item card
                                with st.container():
                                    st.markdown(f"### {item.get('name', 'Предмет')}")
                                    st.write(item.get("description", ""))

                                    cost = item.get("cost", 0)
                                    original_cost = item.get("original_cost", cost)
                                    discount = item.get("discount", 0)

                                    if discount > 0:
                                        st.markdown(
                                            f"~~{original_cost}~~ XP **{cost} XP** (-{discount}%)"
                                        )
                                    else:
                                        st.write(f"**{cost} XP**")

                                    # Check if affordable and not already owned
                                    owned = item.get("owned", False)
                                    affordable = user_xp >= cost and not owned

                                    if owned:
                                        st.success("✅ Приобретено")
                                    elif st.button(
                                        "Купить",
                                        key=f"buy_{item.get('id', idx)}",
                                        disabled=not affordable,
                                    ):
                                        try:
                                            resp = requests.post(
                                                f"http://localhost:8000/api/shop/purchase/{item.get('id')}",
                                                timeout=5,
                                            )
                                            if resp.status_code == 200:
                                                st.success("Покупка завершена!")
                                                st.rerun()
                                            else:
                                                error_msg = resp.json().get(
                                                    "detail", "Неизвестная ошибка"
                                                )
                                                st.error(f"Ошибка покупки: {error_msg}")
                                        except Exception as e:
                                            st.error(f"Ошибка: {str(e)}")

                                    if not affordable and not owned:
                                        if user_xp < cost:
                                            st.caption(
                                                f"Недостаточно XP (нужно: {cost - user_xp})"
                                            )
                                        else:
                                            st.caption("Уже приобретено")
                else:
                    st.info("Товары в магазине не найдены")
            else:
                st.warning("API магазина недоступен")
        except:
            st.error("Не удалось загрузить данные магазина")

    # ── Tab 12: Achievements ────────────────────────────────────────────

    # ── Tab 5: Achievements ──────────────────────────────────────
    with tabs[4]:
        st.header("🏆 Достижения")

        achievements = state.get("achievements", {})
        if achievements:
            cols = st.columns(3)
            for idx, (ach_id, ach_data) in enumerate(achievements.items()):
                with cols[idx % 3]:
                    earned = ach_data.get("earned", False)
                    icon = "✅" if earned else "🔒"
                    st.markdown(f"### {icon} {ach_data.get('name', ach_id)}")
                    st.caption(ach_data.get("description", ""))
                    if ach_data.get("xp_bonus", 0) > 0:
                        st.caption(f"+{ach_data['xp_bonus']} XP")
        else:
            st.info("Нет данных о достижениях.")

    # ── Tab 6: Settings ──────────────────────────────────────────
    with tabs[5]:
        st.header("⚙️ Настройки")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Язык")
            current_lang = state.get("language", "ru")
            new_lang = st.selectbox(
                "Выберите язык",
                options=["ru", "en"],
                index=0 if current_lang == "ru" else 1,
                format_func=lambda x: "Русский" if x == "ru" else "English",
            )
            if new_lang != current_lang:
                state["language"] = new_lang
                with open(STATE_PATH, "w", encoding="utf-8") as f:
                    json.dump(state, f, ensure_ascii=False, indent=2)
                st.success(
                    f"Язык изменён на {'Русский' if new_lang == 'ru' else 'English'}"
                )
                st.rerun()

        with col2:
            st.subheader("Режим")
            current_mode = state.get("current_mode", "teacher")
            modes = ["teacher", "expert", "ctf", "review"]
            new_mode = st.selectbox(
                "Режим обучения",
                options=modes,
                index=modes.index(current_mode) if current_mode in modes else 0,
            )
            if new_mode != current_mode:
                state["current_mode"] = new_mode
                with open(STATE_PATH, "w", encoding="utf-8") as f:
                    json.dump(state, f, ensure_ascii=False, indent=2)
                st.success(f"Режим изменён на {new_mode}")
                st.rerun()

        st.markdown("---")

        st.subheader("🖥️ Системная информация")
        st.write(f"Версия Python: {os.sys.version}")
        st.write(f"Путь к state: {STATE_PATH.absolute()}")
        st.write(
            f"Размер state: {STATE_PATH.stat().st_size if STATE_PATH.exists() else 0} bytes"
        )

        st.subheader("🤖 LLM")
        llm_provider = state.get("llm_provider", "ollama")
        st.write(f"Провайдер: **{llm_provider}**")
        st.write(f"Запросов: **{state.get('llm_call_count', 0)}**")
        st.write(f"Токенов: **{state.get('llm_total_tokens', 0)}**")


if __name__ == "__main__":
    run_dashboard()
