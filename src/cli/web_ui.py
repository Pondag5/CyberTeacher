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


# в”Ђв”Ђ Helper functions (testable without streamlit) в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ


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


# в”Ђв”Ђ Streamlit UI (only runs when executed directly) в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ


def run_dashboard():
    """Run the Streamlit dashboard."""
    import streamlit as st

    st.set_page_config(
        page_title="CyberTeacher Dashboard",
        page_icon="рџ›ЎпёЏ",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    state = load_state()

    # в”Ђв”Ђ Sidebar в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
    st.sidebar.title("рџ›ЎпёЏ CyberTeacher")
    st.sidebar.markdown("---")

    username = state.get("username", "РђРЅРѕРЅРёРј")
    avatar = state.get("avatar", "рџ§‘вЂЌрџ’»")
    st.sidebar.markdown(f"### {avatar} {username}")

    st.sidebar.metric("XP", f"{state.get('points', 0):.0f}")
    st.sidebar.metric("Р РµРїСѓС‚Р°С†РёСЏ", state.get("reputation", 0))
    st.sidebar.metric("Р РµР¶РёРј", state.get("current_mode", "вЂ”"))

    refresh = st.sidebar.checkbox("РђРІС‚Рѕ-РѕР±РЅРѕРІР»РµРЅРёРµ (5СЃ)", value=False)
    if refresh:
        time.sleep(5)
        st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.info("Р”Р»СЏ РёРЅС‚РµСЂР°РєС‚РёРІР° РёСЃРїРѕР»СЊР·СѓР№С‚Рµ CLI: `python main.py`")

    # в”Ђв”Ђ Main content в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
    st.title("рџ“Љ CyberTeacher Dashboard")

    tabs = st.tabs(
        [
            "рџ“€ РџСЂРѕРіСЂРµСЃСЃ",
            "рџ”Ґ РђРєС‚РёРІРЅРѕСЃС‚СЊ",
            "рџЋЇ РќР°РІС‹РєРё",
            "рџ“љ РћР±СѓС‡РµРЅРёРµ",
            "рџ“– РСЃС‚РѕСЂРёСЏ",
            "рџ›¤пёЏ РўСЂРµРєРё",
            "рџљ© CTF",
            "рџђі Р›Р°Р±РѕСЂР°С‚РѕСЂРёРё",
            "рџ”Ќ OSINT",
            "рџ’» Scanner",
            "рџ›’ РњР°РіР°Р·РёРЅ",
            "рџЏ† Р”РѕСЃС‚РёР¶РµРЅРёСЏ",
            "вљ™пёЏ РќР°СЃС‚СЂРѕР№РєРё",
        ]
    )

    # в”Ђв”Ђ Tab 1: Progress в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
    with tabs[0]:
        st.header("рџ“€ РџСЂРѕРіСЂРµСЃСЃ РѕР±СѓС‡РµРЅРёСЏ")

        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("XP", f"{state.get('points', 0):.0f}")
        with col2:
            st.metric("РљРІРёР·РѕРІ", state.get("quizzes_taken", 0))
        with col3:
            st.metric("Р¤Р»Р°РіРѕРІ", state.get("total_flags_collected", 0))
        with col4:
            st.metric("Р›Р°Р±", state.get("labs_started", 0))
        with col5:
            st.metric("РЈСЂРѕРІРµРЅСЊ", state.get("level", 1))

        st.markdown("---")

        st.subheader("рџ“Љ XP Р·Р° РїРѕСЃР»РµРґРЅРёРµ 30 РґРЅРµР№")
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
            st.info("РќРµС‚ РґР°РЅРЅС‹С… РѕР± XP. РќР°С‡РЅРёС‚Рµ РѕР±СѓС‡РµРЅРёРµ РґР»СЏ РѕС‚РѕР±СЂР°Р¶РµРЅРёСЏ РіСЂР°С„РёРєР°.")

        st.subheader("рџ”ґ РЎР»Р°Р±С‹Рµ С‚РµРјС‹")
        weak_topics = state.get("weak_topics", [])
        if weak_topics:
            for topic in weak_topics[:5]:
                score = topic.get("max_score", 0)
                st.progress(
                    score / 100, text=f"{topic.get('name', 'Unknown')}: {score:.0f}%"
                )
        else:
            st.success("РќРµС‚ СЃР»Р°Р±С‹С… С‚РµРј! РћС‚Р»РёС‡РЅР°СЏ СЂР°Р±РѕС‚Р°.")

    # в”Ђв”Ђ Tab 2: Activity Heatmap в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
    with tabs[1]:
        st.header("рџ”Ґ РљР°СЂС‚Р° Р°РєС‚РёРІРЅРѕСЃС‚Рё")

        heatmap = generate_activity_heatmap(state)
        days = ["РџРЅ", "Р’С‚", "РЎСЂ", "Р§С‚", "РџС‚", "РЎР±", "Р’СЃ"]

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

        st.caption("рџџў Р—РµР»С‘РЅС‹Р№ = РІС‹СЃРѕРєР°СЏ Р°РєС‚РёРІРЅРѕСЃС‚СЊ | РџРѕРєР°Р·Р°РЅС‹ РїРѕСЃР»РµРґРЅРёРµ 4 РЅРµРґРµР»Рё")

        st.markdown("---")
        st.subheader("рџ“Љ РЎС‚Р°С‚РёСЃС‚РёРєР° Р°РєС‚РёРІРЅРѕСЃС‚Рё")
        col1, col2, col3 = st.columns(3)
        with col1:
            total_actions = sum(sum(w) for w in heatmap)
            st.metric("Р”РµР№СЃС‚РІРёР№ (4 РЅРµРґРµР»Рё)", total_actions)
        with col2:
            active_days = sum(1 for w in heatmap for v in w if v > 0)
            st.metric("РђРєС‚РёРІРЅС‹С… РґРЅРµР№", active_days)
        with col3:
            streak = state.get("daily_streak", 0)
            st.metric("рџ”Ґ РЎС‚СЂРёРє", f"{streak} РґРЅРµР№")

    # в”Ђв”Ђ Tab 3: Skills в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
    with tabs[2]:
        st.header("рџЋЇ РќР°РІС‹РєРё")

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
                    st.progress(min(level / 5, 1.0), text=f"{skill_name} вЂ” L{level}")
                with col2:
                    st.metric("XP", f"{xp:.0f}")
                    st.caption(f"РЈСЃРїРµС…: {success_rate:.0f}% ({attempts} РїРѕРїС‹С‚РѕРє)")
        else:
            st.info(
                "РќРµС‚ Р·Р°РїРёСЃР°РЅРЅС‹С… РЅР°РІС‹РєРѕРІ. РСЃРїРѕР»СЊР·СѓР№С‚Рµ /skills track РґР»СЏ РѕС‚СЃР»РµР¶РёРІР°РЅРёСЏ."
            )

    # в”Ђв”Ђ Tab 4: Learning в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
    with tabs[3]:
        st.header("рџ“љ РћР±СѓС‡РµРЅРёРµ")

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("РљСѓСЂСЃС‹")
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
                            "Р’С‹Р±РµСЂРёС‚Рµ РєСѓСЂСЃ",
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
                                st.write(f"РўРµРєСѓС‰РёР№ РєСѓСЂСЃ: **{selected_course['name']}**")
                                st.write(f"РџСЂРѕРіСЂРµСЃСЃ: {selected_course['progress']}%")
                                st.write(f"РўРµРј: {selected_course['topics_count']}")
                                if st.button("РќР°С‡Р°С‚СЊ РєСѓСЂСЃ"):
                                    # Select course via API
                                    try:
                                        requests.post(
                                            f"http://localhost:8000/api/courses/{selected_course_id}/select"
                                        )
                                        st.success(
                                            f"РљСѓСЂСЃ '{selected_course['name']}' РІС‹Р±СЂР°РЅ!"
                                        )
                                        st.rerun()
                                    except:
                                        st.error("РќРµ СѓРґР°Р»РѕСЃСЊ РІС‹Р±СЂР°С‚СЊ РєСѓСЂСЃ")
                        else:
                            st.info("РљСѓСЂСЃС‹ РЅРµ РЅР°Р№РґРµРЅС‹")
                    else:
                        st.warning("API РЅРµРґРѕСЃС‚СѓРїРµРЅ")
            except:
                # Fallback to current state
                current_course = state.get("current_course", "РќРµ РІС‹Р±СЂР°РЅ")
                current_topic = state.get("current_topic", "вЂ”")
                st.write(f"РўРµРєСѓС‰РёР№ РєСѓСЂСЃ: **{current_course}**")
                st.write(f"РўРµРєСѓС‰Р°СЏ С‚РµРјР°: **{current_topic}**")

        with col2:
            st.subheader("РџРѕРІС‚РѕСЂРµРЅРёСЏ")
            review_schedule = state.get("review_schedule", {})
            if review_schedule:
                due = sum(
                    1
                    for r in review_schedule.values()
                    if r.get("next_review", 0) < time.time()
                )
                st.metric("РџСЂРѕСЃСЂРѕС‡РµРЅРѕ", due)
                st.metric("Р’СЃРµРіРѕ РІ СЂР°СЃРїРёСЃР°РЅРёРё", len(review_schedule))
            else:
                st.info("РќРµС‚ Р·Р°РїР»Р°РЅРёСЂРѕРІР°РЅРЅС‹С… РїРѕРІС‚РѕСЂРµРЅРёР№.")

        st.markdown("---")

        st.subheader("рџЋ® РњРёСЃСЃРёРё")
        missions_completed = state.get("missions_completed", [])
        st.metric("РџСЂРѕР№РґРµРЅРѕ РјРёСЃСЃРёР№", len(missions_completed))

        if missions_completed:
            st.write(", ".join(missions_completed[:10]))
            if len(missions_completed) > 10:
                st.caption(f"...Рё РµС‰С‘ {len(missions_completed) - 10}")

    # в”Ђв”Ђ Tab 5: History (Story Mode) в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
    with tabs[4]:
        st.header("рџ“– РСЃС‚РѕСЂРёСЏ")

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
                        "Р’С‹Р±РµСЂРёС‚Рµ СЌРїРёР·РѕРґ",
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
                                st.success("вњ… Р­РїРёР·РѕРґ Р·Р°РІРµСЂС€РµРЅ")
                            elif selected_episode.get("started", False):
                                st.info("в–¶пёЏ Р­РїРёР·РѕРґ РІ РїСЂРѕРіСЂРµСЃСЃРµ")
                                # Answer input
                                user_answer = st.text_input(
                                    "Р’Р°С€ РѕС‚РІРµС‚ РёР»Рё С„Р»Р°Рі:",
                                    key=f"answer_{selected_episode_id}",
                                )
                                if st.button(
                                    "РћС‚РїСЂР°РІРёС‚СЊ РѕС‚РІРµС‚",
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
                                                        "вњ… РџСЂР°РІРёР»СЊРЅРѕ! Р­РїРёР·РѕРґ Р·Р°РІРµСЂС€РµРЅ."
                                                    )
                                                    st.rerun()
                                                else:
                                                    st.error(
                                                        "вќЊ РќРµРїСЂР°РІРёР»СЊРЅРѕ. РџРѕРїСЂРѕР±СѓР№С‚Рµ РµС‰Рµ СЂР°Р·."
                                                    )
                                                    # Show hint if available
                                                    if result.get("hint"):
                                                        st.info(
                                                            f"рџ’Ў РџРѕРґСЃРєР°Р·РєР°: {result['hint']}"
                                                        )
                                        except Exception as e:
                                            st.error(f"РћС€РёР±РєР° РѕС‚РїСЂР°РІРєРё: {str(e)}")
                                    else:
                                        st.warning("РџРѕР¶Р°Р»СѓР№СЃС‚Р°, РІРІРµРґРёС‚Рµ РѕС‚РІРµС‚")
                            else:
                                st.write("РќР°Р¶РјРёС‚Рµ 'РќР°С‡Р°С‚СЊ СЌРїРёР·РѕРґ', С‡С‚РѕР±С‹ РЅР°С‡Р°С‚СЊ")
                                if st.button(
                                    "РќР°С‡Р°С‚СЊ СЌРїРёР·РѕРґ", key=f"start_{selected_episode_id}"
                                ):
                                    try:
                                        resp = requests.post(
                                            f"http://localhost:8000/api/story/start/{selected_episode_id}",
                                            timeout=5,
                                        )
                                        if resp.status_code == 200:
                                            st.success("Р­РїРёР·РѕРґ РЅР°С‡Р°Р»СЃСЏ!")
                                            st.rerun()
                                        else:
                                            st.error("РќРµ СѓРґР°Р»РѕСЃСЊ РЅР°С‡Р°С‚СЊ СЌРїРёР·РѕРґ")
                                    except Exception as e:
                                        st.error(f"РћС€РёР±РєР°: {str(e)}")
                        else:
                            st.info("Р’С‹Р±РµСЂРёС‚Рµ СЌРїРёР·РѕРґ РёР· СЃРїРёСЃРєР° РІС‹С€Рµ")
                else:
                    st.info("Р­РїРёР·РѕРґС‹ РёСЃС‚РѕСЂРёРё РЅРµ РЅР°Р№РґРµРЅС‹")
            else:
                st.warning("API РёСЃС‚РѕСЂРёРё РЅРµРґРѕСЃС‚СѓРїРµРЅ")
        except Exception as e:
            st.error(f"РќРµ СѓРґР°Р»РѕСЃСЊ Р·Р°РіСЂСѓР·РёС‚СЊ РґР°РЅРЅС‹Рµ РёСЃС‚РѕСЂРёРё: {e}")

    # в”Ђв”Ђ Tab 6: Tracks в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
    with tabs[5]:
        st.header("рџ›¤пёЏ РўСЂРµРєРё РѕР±СѓС‡РµРЅРёСЏ")

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
                        "Р’С‹Р±РµСЂРёС‚Рµ С‚СЂРµРє",
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
                            st.progress(progress / 100, text=f"РџСЂРѕРіСЂРµСЃСЃ: {progress}%")

                            # Show current topic/step
                            current_step = selected_track.get(
                                "current_step", "РќРµ РЅР°С‡Р°С‚Рѕ"
                            )
                            st.write(f"РўРµРєСѓС‰РёР№ С€Р°Рі: {current_step}")

                            if st.button(
                                "РќР°С‡Р°С‚СЊ С‚СЂРµРє", key=f"start_track_{selected_track_id}"
                            ):
                                try:
                                    resp = requests.post(
                                        f"http://localhost:8000/api/tracks/start/{selected_track_id}",
                                        timeout=5,
                                    )
                                    if resp.status_code == 200:
                                        st.success("РўСЂРµРє РЅР°С‡Р°С‚!")
                                        st.rerun()
                                    else:
                                        st.error("РќРµ СѓРґР°Р»РѕСЃСЊ РЅР°С‡Р°С‚СЊ С‚СЂРµРє")
                                except Exception as e:
                                    st.error(f"РћС€РёР±РєР°: {str(e)}")
                        else:
                            st.info("Р’С‹Р±РµСЂРёС‚Рµ С‚СЂРµРє РёР· СЃРїРёСЃРєР° РІС‹С€Рµ")
                else:
                    st.info("РўСЂРµРєРё РѕР±СѓС‡РµРЅРёСЏ РЅРµ РЅР°Р№РґРµРЅС‹")
            else:
                st.warning("API С‚СЂРµРєРѕРІ РЅРµРґРѕСЃС‚СѓРїРµРЅ")
        except Exception as e:
            st.error(f"РќРµ СѓРґР°Р»РѕСЃСЊ Р·Р°РіСЂСѓР·РёС‚СЊ РґР°РЅРЅС‹Рµ С‚СЂРµРєРѕРІ: {e}")

    # в”Ђв”Ђ Tab 7: CTF в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
    with tabs[6]:
        st.header("рџљ© CTF Р¦РµРЅС‚СЂ")

        # Load CTF status from API
        import requests

        try:
            response = requests.get("http://localhost:8000/api/ctf/status", timeout=2)
            if response.status_code == 200:
                ctf_data = response.json()

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Р¤Р»Р°РіРѕРІ СЃРѕР±СЂР°РЅРѕ", ctf_data.get("flags_collected", 0))
                with col2:
                    st.metric("РђРєС‚РёРІРЅС‹С… РјРёСЃСЃРёР№", ctf_data.get("active_missions", 0))
                with col3:
                    st.metric("Р РµРїСѓС‚Р°С†РёРё", ctf_data.get("reputation", 0))

                st.markdown("---")

                # Recent flags
                recent_flags = ctf_data.get("recent_flags", [])
                if recent_flags:
                    st.subheader("РџРѕСЃР»РµРґРЅРёРµ С„Р»Р°РіРё")
                    for flag in recent_flags[:5]:
                        status_icon = "вњ…" if flag.get("verified") else "вЏі"
                        st.write(
                            f"{status_icon} {flag.get('name', 'РќРµРёР·РІРµСЃС‚РЅС‹Р№ С„Р»Р°Рі')} - {flag.get('points', 0)} XP"
                        )
                else:
                    st.info("РџРѕРєР° РЅРµС‚ СЃРѕР±СЂР°РЅРЅС‹С… С„Р»Р°РіРѕРІ")

                # Available missions
                missions = ctf_data.get("missions", [])
                if missions:
                    st.subheader("Р”РѕСЃС‚СѓРїРЅС‹Рµ РјРёСЃСЃРёРё")
                    for mission in missions[:3]:
                        with st.expander(
                            f"{mission.get('name', 'РњРёСЃСЃРёСЏ')} - {mission.get('difficulty', '???')}"
                        ):
                            st.write(mission.get("description", ""))
                            if st.button(
                                f"РќР°С‡Р°С‚СЊ РјРёСЃСЃРёСЋ",
                                key=f"start_mission_{mission.get('id', '')}",
                            ):
                                try:
                                    resp = requests.post(
                                        f"http://localhost:8000/api/missions/start/{mission.get('id')}",
                                        timeout=5,
                                    )
                                    if resp.status_code == 200:
                                        st.success("РњРёСЃСЃРёСЏ РЅР°С‡Р°С‚Р°!")
                                        st.rerun()
                                    else:
                                        st.error("РќРµ СѓРґР°Р»РѕСЃСЊ РЅР°С‡Р°С‚СЊ РјРёСЃСЃРёСЋ")
                                except Exception as e:
                                    st.error(f"РћС€РёР±РєР°: {str(e)}")
                else:
                    st.info("РњРёСЃСЃРёРё РЅРµ РЅР°Р№РґРµРЅС‹")
            else:
                st.warning("API CTF РЅРµРґРѕСЃС‚СѓРїРµРЅ")
        except Exception as e:
            st.error(f"РќРµ СѓРґР°Р»РѕСЃСЊ Р·Р°РіСЂСѓР·РёС‚СЊ РґР°РЅРЅС‹Рµ CTF: {e}")

    # в”Ђв”Ђ Tab 8: Laboratories в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
    with tabs[7]:
        st.header("рџђі Docker Р›Р°Р±РѕСЂР°С‚РѕСЂРёРё")

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
                            f"{lab.get('name', 'Р›Р°Р±РѕСЂР°С‚РѕСЂРёСЏ')} [{lab.get('difficulty', '???').title()}]"
                        ):
                            st.write(lab.get("description", ""))

                            status = (
                                "рџџў Р—Р°РїСѓС‰РµРЅР°"
                                if lab.get("running")
                                else "вљЄ РћСЃС‚Р°РЅРѕРІР»РµРЅР°"
                            )
                            st.write(f"РЎС‚Р°С‚СѓСЃ: {status}")

                            cols = st.columns(2)
                            with cols[0]:
                                if not lab.get("running"):
                                    if st.button(
                                        "Р—Р°РїСѓСЃС‚РёС‚СЊ", key=f"start_lab_{lab.get('id')}"
                                    ):
                                        try:
                                            resp = requests.post(
                                                f"http://localhost:8000/api/labs/{lab.get('id')}/start",
                                                timeout=10,
                                            )
                                            if resp.status_code == 200:
                                                st.success("Р›Р°Р±РѕСЂР°С‚РѕСЂРёСЏ Р·Р°РїСѓС‰РµРЅР°!")
                                                st.rerun()
                                            else:
                                                st.error(
                                                    "РќРµ СѓРґР°Р»РѕСЃСЊ Р·Р°РїСѓСЃС‚РёС‚СЊ Р»Р°Р±РѕСЂР°С‚РѕСЂРёСЋ"
                                                )
                                        except Exception as e:
                                            st.error(f"РћС€РёР±РєР°: {str(e)}")
                                else:
                                    if st.button(
                                        "РћСЃС‚Р°РЅРѕРІРёС‚СЊ", key=f"stop_lab_{lab.get('id')}"
                                    ):
                                        try:
                                            resp = requests.post(
                                                f"http://localhost:8000/api/labs/{lab.get('id')}/stop",
                                                timeout=10,
                                            )
                                            if resp.status_code == 200:
                                                st.success("Р›Р°Р±РѕСЂР°С‚РѕСЂРёСЏ РѕСЃС‚Р°РЅРѕРІР»РµРЅР°!")
                                                st.rerun()
                                            else:
                                                st.error(
                                                    "РќРµ СѓРґР°Р»РѕСЃСЊ РѕСЃС‚Р°РЅРѕРІРёС‚СЊ Р»Р°Р±РѕСЂР°С‚РѕСЂРёСЋ"
                                                )
                                        except Exception as e:
                                            st.error(f"РћС€РёР±РєР°: {str(e)}")

                            with cols[1]:
                                if lab.get("ports"):
                                    st.write("Р”РѕСЃС‚СѓРїРЅРѕ РїРѕ РїРѕСЂС‚Р°Рј:")
                                    for port in lab.get("ports", []):
                                        st.code(f"http://localhost:{port}")
                else:
                    st.info("Р›Р°Р±РѕСЂР°С‚РѕСЂРёРё РЅРµ РЅР°Р№РґРµРЅС‹")
            else:
                st.warning("API Р»Р°Р±РѕСЂР°С‚РѕСЂРёР№ РЅРµРґРѕСЃС‚СѓРїРµРЅ")
        except Exception as e:
            st.error(f"РќРµ СѓРґР°Р»РѕСЃСЊ Р·Р°РіСЂСѓР·РёС‚СЊ РґР°РЅРЅС‹Рµ Р»Р°Р±РѕСЂР°С‚РѕСЂРёР№: {e}")

    # в”Ђв”Ђ Tab 9: OSINT в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
    with tabs[8]:
        st.header("рџ”Ќ OSINT Р¦РµРЅС‚СЂ")

        # Load threats (APT groups) from API
        import requests

        try:
            threats_response = requests.get(
                "http://localhost:8000/api/threats", timeout=2
            )
            news_response = requests.get("http://localhost:8000/api/news", timeout=2)

            col1, col2 = st.columns([1, 1])

            with col1:
                st.subheader("APT Р“СЂСѓРїРїС‹")
                if threats_response.status_code == 200:
                    threats_data = threats_response.json()
                    groups = threats_data.get("groups", [])
                    if groups:
                        for group in groups[:5]:  # Show top 5
                            with st.expander(
                                f"{group.get('name', 'Р“СЂСѓРїРїР°')} ({group.get('country', '???')})"
                            ):
                                st.write(
                                    f"РЎРїРµС†РёР°Р»РёР·Р°С†РёСЏ: {group.get('specialization', 'РќРµ СѓРєР°Р·Р°РЅР°')}"
                                )
                                st.write(
                                    f"РЈСЂРѕРІРµРЅСЊ СѓРіСЂРѕР·С‹: {group.get('threat_level', '???')}/10"
                                )
                                if st.button(
                                    f"РџРѕРґСЂРѕР±РЅРµРµ",
                                    key=f"apt_detail_{group.get('id', '')}",
                                ):
                                    st.info(
                                        group.get("description", "РћРїРёСЃР°РЅРёРµ РЅРµРґРѕСЃС‚СѓРїРЅРѕ")
                                    )
                    else:
                        st.info("APT РіСЂСѓРїРїС‹ РЅРµ РЅР°Р№РґРµРЅС‹")
                else:
                    st.warning("API СѓРіСЂРѕР· РЅРµРґРѕСЃС‚СѓРїРµРЅ")

            with col2:
                st.subheader("РџРѕСЃР»РµРґРЅРёРµ РЅРѕРІРѕСЃС‚Рё")
                if news_response.status_code == 200:
                    news_data = news_response.json()
                    articles = news_data.get("articles", [])
                    if articles:
                        for article in articles[:5]:  # Show top 5
                            with st.expander(
                                f"{article.get('title', 'РќРѕРІРѕСЃС‚СЊ')} - {article.get('source', '???')}"
                            ):
                                st.write(article.get("summary", ""))
                                if article.get("url"):
                                    st.link_button("Р§РёС‚Р°С‚СЊ РїРѕР»РЅРѕСЃС‚СЊСЋ", article["url"])
                    else:
                        st.info("РќРѕРІРѕСЃС‚Рё РЅРµ РЅР°Р№РґРµРЅС‹")
                else:
                    st.warning("API РЅРѕРІРѕСЃС‚РµР№ РЅРµРґРѕСЃС‚СѓРїРµРЅ")

            st.markdown("---")

            # CVE Search
            st.subheader("РџРѕРёСЃРє CVE")
            cve_id = st.text_input(
                "Р’РІРµРґРёС‚Рµ ID CVE (РЅР°РїСЂРёРјРµСЂ, CVE-2023-12345)", placeholder="CVE-2023-..."
            )
            if st.button("РќР°Р№С‚Рё CVE") and cve_id:
                try:
                    resp = requests.get(
                        f"http://localhost:8000/api/cve/{cve_id.upper()}", timeout=5
                    )
                    if resp.status_code == 200:
                        cve_data = resp.json()
                        st.subheader(f"CVE: {cve_data.get('id', '')}")
                        st.write(f"**РћРїРёСЃР°РЅРёРµ:** {cve_data.get('description', '')}")
                        st.write(f"**РЎРµСЂСЊРµР·РЅРѕСЃС‚СЊ:** {cve_data.get('severity', '???')}")
                        st.write(f"**CVSS Score:** {cve_data.get('cvss_score', '???')}")
                        if cve_data.get("references"):
                            st.write("**РЎСЃС‹Р»РєРё:**")
                            for ref in cve_data["references"][:3]:
                                st.write(f"- {ref}")
                    elif resp.status_code == 404:
                        st.error("CVE РЅРµ РЅР°Р№РґРµРЅ")
                    else:
                        st.error("РћС€РёР±РєР° РїСЂРё РїРѕРёСЃРєРµ CVE")
                except Exception as e:
                    st.error(f"РћС€РёР±РєР°: {str(e)}")
        except Exception as e:
            st.error(f"РќРµ СѓРґР°Р»РѕСЃСЊ Р·Р°РіСЂСѓР·РёС‚СЊ РґР°РЅРЅС‹Рµ OSINT: {e}")

    # в”Ђв”Ђ Tab 10: Scanner в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
    with tabs[9]:
        st.header("рџ”Ќ Scanner (РЎРєР°РЅРµСЂ РєРѕРґР°)")

        st.subheader("РЎС‚Р°С‚РёС‡РµСЃРєРёР№ Р°РЅР°Р»РёР· РєРѕРґР°")

        # File upload
        uploaded_file = st.file_uploader(
            "Р—Р°РіСЂСѓР·РёС‚Рµ С„Р°Р№Р» РґР»СЏ Р°РЅР°Р»РёР·Р°",
            type=["py", "js", "java", "cpp", "c", "php", "rb", "go", "rs"],
            help="РџРѕРґРґРµСЂР¶РёРІР°РµРјС‹Рµ С„РѕСЂРјР°С‚С‹: Python, JavaScript, Java, C/C++, PHP, Ruby, Go, Rust",
        )

        if uploaded_file is not None:
            # Display file info
            st.write(f"РРјСЏ С„Р°Р№Р»Р°: {uploaded_file.name}")
            st.write(f"Р Р°Р·РјРµСЂ: {uploaded_file.size} Р±Р°Р№С‚")

            # Read file content
            try:
                content = uploaded_file.read().decode("utf-8")
                st.text_area("РЎРѕРґРµСЂР¶РёРјРѕРµ С„Р°Р№Р»Р°:", content, height=200, disabled=True)

                # Reset file pointer for upload
                uploaded_file.seek(0)

                if st.button("РџСЂРѕР°РЅР°Р»РёР·РёСЂРѕРІР°С‚СЊ РєРѕРґ"):
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

                            st.subheader("Р РµР·СѓР»СЊС‚Р°С‚С‹ Р°РЅР°Р»РёР·Р°")

                            # Summary
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric(
                                    "Р’СЃРµРіРѕ РїСЂРѕР±Р»РµРј", results.get("total_issues", 0)
                                )
                            with col2:
                                st.metric(
                                    "РљСЂРёС‚РёС‡РЅС‹С…", results.get("critical_issues", 0)
                                )
                            with col3:
                                st.metric(
                                    "РџСЂРµРґСѓРїСЂРµР¶РґРµРЅРёР№", results.get("warning_issues", 0)
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
                                                    f"Р¤Р°Р№Р»: {issue.get('file', '')}:{issue.get('line', '')}"
                                                )
                            else:
                                st.success("вќЊ РџСЂРѕР±Р»РµРјС‹ РЅРµ РЅР°Р№РґРµРЅС‹! РћС‚Р»РёС‡РЅС‹Р№ РєРѕРґ.")
                        else:
                            st.error("РћС€РёР±РєР° РїСЂРё Р°РЅР°Р»РёР·Рµ РєРѕРґР°")
                    except Exception as e:
                        st.error(f"РћС€РёР±РєР°: {str(e)}")
            except Exception as e:
                st.error(f"РќРµ СѓРґР°Р»РѕСЃСЊ РїСЂРѕС‡РёС‚Р°С‚СЊ С„Р°Р№Р»: {str(e)}")
        else:
            st.info("Р—Р°РіСЂСѓР·РёС‚Рµ С„Р°Р№Р» РґР»СЏ Р°РЅР°Р»РёР·Р° РєРѕРґР°")

        st.markdown("---")

        # Quick scan examples
        st.subheader("Р‘С‹СЃС‚СЂР°СЏ РїСЂРѕРІРµСЂРєР° РїСЂРёРјРµСЂРѕРІ")
        example_code = st.selectbox(
            "Р’С‹Р±РµСЂРёС‚Рµ РїСЂРёРјРµСЂ РґР»СЏ РїСЂРѕРІРµСЂРєРё:",
            [
                "Р‘РµР·РѕРїР°СЃРЅС‹Р№ РєРѕРґ",
                "SQL Injection СѓСЏР·РІРёРјРѕСЃС‚СЊ",
                "XSS СѓСЏР·РІРёРјРѕСЃС‚СЊ",
                "Hardcoded СЃРµРєСЂРµС‚",
                "РќРµР±РµР·РѕРїР°СЃРЅР°СЏ СЂР°Р·СЂСЏРґРєР°",
            ],
        )

        if st.button("РџСЂРѕРІРµСЂРёС‚СЊ РїСЂРёРјРµСЂ"):
            # Define example snippets
            examples = {
                "Р‘РµР·РѕРїР°СЃРЅС‹Р№ РєРѕРґ": "def add(a, b):\n    return a + b\n\nresult = add(2, 3)\nprint(result)",
                "SQL Injection СѓСЏР·РІРёРјРѕСЃС‚СЊ": 'def get_user(user_id):\n    query = f"SELECT * FROM users WHERE id = {user_id}"\n    return execute_query(query)',
                "XSS СѓСЏР·РІРёРјРѕСЃС‚СЊ": "def render_comment(comment):\n    return f'<div>{comment}</div>'  # Unsafely renders user input",
                "Hardcoded СЃРµРєСЂРµС‚": "API_KEY = 'sk_live_REPLACE_WITH_YOUR_KEY'\nDB_PASSWORD = 'admin123'",
                "РќРµР±РµР·РѕРїР°СЃРЅР°СЏ СЂР°Р·СЂСЏРґРєР°": "import os\nos.system(user_input)  # Direct command execution",
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
                            st.error(f"вљ пёЏ РќР°Р№РґРµРЅРѕ РїСЂРѕР±Р»РµРј: {results['total_issues']}")
                            for issue in results.get("issues", [])[:3]:  # Show first 3
                                st.write(
                                    f"рџ”ґ {issue.get('rule_id', '')}: {issue.get('message', '')}"
                                )
                        else:
                            st.success("вњ… РџСЂРѕР±Р»РµРјС‹ РЅРµ РѕР±РЅР°СЂСѓР¶РµРЅС‹")
                    else:
                        st.error("РћС€РёР±РєР° РїСЂРё СЃРєР°РЅРёСЂРѕРІР°РЅРёРё")
                except Exception as e:
                    st.error(f"РћС€РёР±РєР°: {str(e)}")

    # в”Ђв”Ђ Tab 11: Shop в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
    with tabs[10]:
        st.header("рџ›’ РњР°РіР°Р·РёРЅ CyberTeacher")

        # Load shop items from API
        import requests

        try:
            response = requests.get("http://localhost:8000/api/shop", timeout=2)
            if response.status_code == 200:
                shop_data = response.json()
                items = shop_data.get("items", [])
                user_xp = state.get("points", 0)

                st.write(f"Р’Р°С€ Р±Р°Р»Р°РЅСЃ: **{user_xp} XP**")

                if items:
                    # Group items by category
                    categories = {}
                    for item in items:
                        category = item.get("category", "РџСЂРѕС‡РµРµ")
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
                                    st.markdown(f"### {item.get('name', 'РџСЂРµРґРјРµС‚')}")
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
                                        st.success("вњ… РџСЂРёРѕР±СЂРµС‚РµРЅРѕ")
                                    elif st.button(
                                        "РљСѓРїРёС‚СЊ",
                                        key=f"buy_{item.get('id', idx)}",
                                        disabled=not affordable,
                                    ):
                                        try:
                                            resp = requests.post(
                                                f"http://localhost:8000/api/shop/purchase/{item.get('id')}",
                                                timeout=5,
                                            )
                                            if resp.status_code == 200:
                                                st.success("РџРѕРєСѓРїРєР° Р·Р°РІРµСЂС€РµРЅР°!")
                                                st.rerun()
                                            else:
                                                error_msg = resp.json().get(
                                                    "detail", "РќРµРёР·РІРµСЃС‚РЅР°СЏ РѕС€РёР±РєР°"
                                                )
                                                st.error(f"РћС€РёР±РєР° РїРѕРєСѓРїРєРё: {error_msg}")
                                        except Exception as e:
                                            st.error(f"РћС€РёР±РєР°: {str(e)}")

                                    if not affordable and not owned:
                                        if user_xp < cost:
                                            st.caption(
                                                f"РќРµРґРѕСЃС‚Р°С‚РѕС‡РЅРѕ XP (РЅСѓР¶РЅРѕ: {cost - user_xp})"
                                            )
                                        else:
                                            st.caption("РЈР¶Рµ РїСЂРёРѕР±СЂРµС‚РµРЅРѕ")
                else:
                    st.info("РўРѕРІР°СЂС‹ РІ РјР°РіР°Р·РёРЅРµ РЅРµ РЅР°Р№РґРµРЅС‹")
            else:
                st.warning("API РјР°РіР°Р·РёРЅР° РЅРµРґРѕСЃС‚СѓРїРµРЅ")
        except Exception as e:
            st.error(f"РќРµ СѓРґР°Р»РѕСЃСЊ Р·Р°РіСЂСѓР·РёС‚СЊ РґР°РЅРЅС‹Рµ РјР°РіР°Р·РёРЅР°: {e}")

    # в”Ђв”Ђ Tab 12: Achievements в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ

    # в”Ђв”Ђ Tab 5: Achievements в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
    with tabs[4]:
        st.header("рџЏ† Р”РѕСЃС‚РёР¶РµРЅРёСЏ")

        achievements = state.get("achievements", {})
        if achievements:
            cols = st.columns(3)
            for idx, (ach_id, ach_data) in enumerate(achievements.items()):
                with cols[idx % 3]:
                    earned = ach_data.get("earned", False)
                    icon = "вњ…" if earned else "рџ”’"
                    st.markdown(f"### {icon} {ach_data.get('name', ach_id)}")
                    st.caption(ach_data.get("description", ""))
                    if ach_data.get("xp_bonus", 0) > 0:
                        st.caption(f"+{ach_data['xp_bonus']} XP")
        else:
            st.info("РќРµС‚ РґР°РЅРЅС‹С… Рѕ РґРѕСЃС‚РёР¶РµРЅРёСЏС….")

    # в”Ђв”Ђ Tab 6: Settings в”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђв”Ђ
    with tabs[5]:
        st.header("вљ™пёЏ РќР°СЃС‚СЂРѕР№РєРё")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("РЇР·С‹Рє")
            current_lang = state.get("language", "ru")
            new_lang = st.selectbox(
                "Р’С‹Р±РµСЂРёС‚Рµ СЏР·С‹Рє",
                options=["ru", "en"],
                index=0 if current_lang == "ru" else 1,
                format_func=lambda x: "Р СѓСЃСЃРєРёР№" if x == "ru" else "English",
            )
            if new_lang != current_lang:
                state["language"] = new_lang
                with open(STATE_PATH, "w", encoding="utf-8") as f:
                    json.dump(state, f, ensure_ascii=False, indent=2)
                st.success(
                    f"РЇР·С‹Рє РёР·РјРµРЅС‘РЅ РЅР° {'Р СѓСЃСЃРєРёР№' if new_lang == 'ru' else 'English'}"
                )
                st.rerun()

        with col2:
            st.subheader("Р РµР¶РёРј")
            current_mode = state.get("current_mode", "teacher")
            modes = ["teacher", "expert", "ctf", "review"]
            new_mode = st.selectbox(
                "Р РµР¶РёРј РѕР±СѓС‡РµРЅРёСЏ",
                options=modes,
                index=modes.index(current_mode) if current_mode in modes else 0,
            )
            if new_mode != current_mode:
                state["current_mode"] = new_mode
                with open(STATE_PATH, "w", encoding="utf-8") as f:
                    json.dump(state, f, ensure_ascii=False, indent=2)
                st.success(f"Р РµР¶РёРј РёР·РјРµРЅС‘РЅ РЅР° {new_mode}")
                st.rerun()

        st.markdown("---")

        st.subheader("рџ–ҐпёЏ РЎРёСЃС‚РµРјРЅР°СЏ РёРЅС„РѕСЂРјР°С†РёСЏ")
        st.write(f"Р’РµСЂСЃРёСЏ Python: {os.sys.version}")
        st.write(f"РџСѓС‚СЊ Рє state: {STATE_PATH.absolute()}")
        st.write(
            f"Р Р°Р·РјРµСЂ state: {STATE_PATH.stat().st_size if STATE_PATH.exists() else 0} bytes"
        )

        st.subheader("рџ¤– LLM")
        llm_provider = state.get("llm_provider", "ollama")
        st.write(f"РџСЂРѕРІР°Р№РґРµСЂ: **{llm_provider}**")
        st.write(f"Р—Р°РїСЂРѕСЃРѕРІ: **{state.get('llm_call_count', 0)}**")
        st.write(f"РўРѕРєРµРЅРѕРІ: **{state.get('llm_total_tokens', 0)}**")


if __name__ == "__main__":
    run_dashboard()
