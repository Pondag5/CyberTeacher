#!/usr/bin/env python3
"""Enhanced Streamlit Web UI for CyberTeacher with analytics dashboard."""

import json
import os
import time
from datetime import datetime, timedelta
from pathlib import Path

STATE_PATH = Path("./memory/app_state.json")
METRICS_PATH = Path("./memory/metrics.json")


# ── Helper functions (testable without streamlit) ─────────────────

def load_state() -> dict:
    """Load application state from JSON file."""
    if STATE_PATH.exists():
        try:
            with open(STATE_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def load_metrics() -> dict:
    """Load metrics history if available."""
    if METRICS_PATH.exists():
        try:
            with open(METRICS_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def generate_xp_history(state: dict) -> list[dict]:
    """Generate XP history from state (simulated if no history stored)."""
    xp_history = state.get("xp_history", [])
    if not xp_history:
        current = state.get("points", 0)
        if current > 0:
            days = 30
            xp_history = [
                {
                    "date": (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d"),
                    "xp": max(0, current * (1 - i / days) + (current * 0.1 * (days - i) / days)),
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
            date_str = (datetime.now() - timedelta(days=(3 - week) * 7 + (6 - day))).strftime("%Y-%m-%d")
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

    tabs = st.tabs([
        "📈 Прогресс",
        "🔥 Активность",
        "🎯 Навыки",
        "📚 Обучение",
        "🏆 Достижения",
        "⚙️ Настройки",
    ])

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
                st.progress(score / 100, text=f"{topic.get('name', 'Unknown')}: {score:.0f}%")
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
            max_val = max(max(row) for row in heatmap) if any(any(v > 0 for v in row) for row in heatmap) else 1

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
            for skill_name, skill_data in sorted(skill_tracker.items(), key=lambda x: x[1].get("level", 0), reverse=True):
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
            st.info("Нет записанных навыков. Используйте /skills track для отслеживания.")

    # ── Tab 4: Learning ──────────────────────────────────────────
    with tabs[3]:
        st.header("📚 Обучение")

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Курсы")
            current_course = state.get("current_course", "Не выбран")
            current_topic = state.get("current_topic", "—")
            st.write(f"Текущий курс: **{current_course}**")
            st.write(f"Текущая тема: **{current_topic}**")

        with col2:
            st.subheader("Повторения")
            review_schedule = state.get("review_schedule", {})
            if review_schedule:
                due = sum(1 for r in review_schedule.values() if r.get("next_review", 0) < time.time())
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
                st.success(f"Язык изменён на {'Русский' if new_lang == 'ru' else 'English'}")
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
        st.write(f"Размер state: {STATE_PATH.stat().st_size if STATE_PATH.exists() else 0} bytes")

        st.subheader("🤖 LLM")
        llm_provider = state.get("llm_provider", "ollama")
        st.write(f"Провайдер: **{llm_provider}**")
        st.write(f"Запросов: **{state.get('llm_call_count', 0)}**")
        st.write(f"Токенов: **{state.get('llm_total_tokens', 0)}**")


if __name__ == "__main__":
    run_dashboard()
