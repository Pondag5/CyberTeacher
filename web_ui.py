#!/usr/bin/env python3
"""Streamlit Web UI for CyberTeacher monitoring."""

import json
import subprocess
import time
from datetime import datetime
from pathlib import Path

import streamlit as st

STATE_PATH = Path("./memory/app_state.json")
DOCKER_LABS = {
    # Web уязвимости
    "dvwa": {
        "name": "DVWA",
        "desc": "Damn Vulnerable Web App — классическая платформа для веб-пентеста",
        "image": "vulnerables/web-dvwa",
        "ports": {8080: 80},
        "db": "dvwa-db",
    },
    "bwapp": {
        "name": "bWAPP",
        "desc": "Ещё одна уязвимая веб-приложения",
        "image": "raesene/bwapp",
        "ports": {8081: 80},
        "db": "bwapp-db",
    },
    "juiceshop": {
        "name": "OWASP Juice Shop",
        "desc": "Современное уязвимое приложение",
        "image": "bkimminich/juice-shop",
        "ports": {3000: 3000},
    },
}

st.set_page_config(page_title="CyberTeacher Web UI", layout="wide")
st.title("🛡️ CyberTeacher Web UI")


# Load state
def load_state():
    if STATE_PATH.exists():
        with open(STATE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


state = load_state()

# Tabs
tabs = st.tabs(["Обзор", "Сеть", "Лаборатории", "Сканер", "Миссии"])

with tabs[0]:
    st.header("Системная статистика")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Режим", state.get("current_mode", "—"))
    with col2:
        st.metric("Очки", state.get("points", 0))
    with col3:
        st.metric("LLM запросов", state.get("llm_call_count", 0))
    with col4:
        total_cache = state.get("cache_hits", 0) + state.get("cache_misses", 0)
        hit_rate = (
            (state.get("cache_hits", 0) / total_cache * 100) if total_cache else 0.0
        )
        st.metric("Кэш hit rate", f"{hit_rate:.1f}%")

    st.subheader("Информация о LLM")
    calls = state.get("llm_call_count", 0)
    avg_time = (state.get("llm_total_time", 0) / calls) if calls else 0.0
    st.write(f"Среднее время ответа: **{avg_time:.3f} сек**")
    st.write(f"Всего токенов: **{state.get('llm_total_tokens', 0)}**")

    st.subheader("Rate Limiting")
    timestamps = state.get("request_timestamps", [])
    now = time.time()
    recent = [t for t in timestamps if now - t < 60]
    st.progress(
        min(len(recent), 10) / 10,
        text=f"Запросов за последнюю минуту: {len(recent)}/10",
    )

with tabs[1]:
    st.header("Визуализация сети (ASCII)")
    try:
        import subprocess

        from practice import DOCKER_LABS as DL

        lines = ["Host (CyberTeacher)"]
        for key, lab in DL.items():
            container_name = f"{key}-web"
            try:
                res = subprocess.run(
                    [
                        "docker",
                        "ps",
                        "--filter",
                        f"name={container_name}",
                        "--format",
                        "{{.Status}}",
                    ],
                    capture_output=True,
                    text=True,
                    timeout=2,
                    check=False,
                )
                running = "Up" in res.stdout
                if running:
                    lines.append(f"  └─ [green]{key}[/green] ({lab['name']}) - running")
                else:
                    lines.append(f"  └─ [red]{key}[/red] ({lab['name']}) - stopped")
            except Exception:
                lines.append(f"  └─ {key} (docker unavailable)")
        st.code("\n".join(lines), language="")
    except Exception as e:
        st.error(f"Ошибка загрузки лабораторий: {e}")

with tabs[2]:
    st.header("Лаборатории Docker")
    try:
        import subprocess

        labs = DOCKER_LABS
        cols = st.columns(len(labs))
        for idx, (key, lab) in enumerate(labs.items()):
            with cols[idx]:
                st.subheader(lab["name"])
                st.write(lab["desc"])
                st.code(f"Порты: {lab['ports']}")
                container = f"{key}-web"
                if st.button(f"Запустить {key}", key=f"start_{key}"):
                    subprocess.run(
                        [
                            "docker",
                            "run",
                            "-d",
                            "--name",
                            container,
                            "--network",
                            f"{key}-net",
                            *[f"-p{p}:{c}" for p, c in lab["ports"].items()],
                            lab["image"],
                        ],
                        check=False,
                    )
                    st.rerun()
                if st.button(f"Остановить {key}", key=f"stop_{key}"):
                    subprocess.run(["docker", "stop", container], check=False)
                    st.rerun()
    except Exception as e:
        st.error(e)

with tabs[3]:
    st.header("Сканирование уязвимостей (CVE)")
    cve_id = st.text_input("CVE ID (например, CVE-2024-1234)").strip()
    if cve_id:
        import time as _time

        import requests

        cached = st.session_state.get("cve_cache", {})
        if cve_id in cached and (_time.time() - cached[cve_id][0] < 3600):
            data = cached[cve_id][1]
        else:
            r = requests.get(
                f"https://services.nvd.nist.gov/rest/json/cves/2.0?cveId={cve_id}",
                timeout=10,
            )
            if r.status_code == 200:
                vulns = r.json().get("vulnerabilities", [])
                data = vulns[0]["cve"] if vulns else None
                if data:
                    st.session_state.setdefault("cve_cache", {})[cve_id] = (
                        _time.time(),
                        data,
                    )
        if data:
            desc = next(
                (d["value"] for d in data.get("descriptions", []) if d["lang"] == "en"),
                "N/A",
            )
            st.write(f"**Описание:** {desc}")
            refs = [ref["url"] for ref in data.get("references", []) if ref.get("url")]
            for url in refs[:5]:
                st.write(f"- {url}")
        else:
            st.error("CVE не найден")

with tabs[4]:
    st.header("Миссии")
    missions_path = Path("./missions")
    if missions_path.exists():
        files = list(missions_path.glob("*.json"))
        for f in files:
            with open(f, "r", encoding="utf-8") as fp:
                data = json.load(fp)
            mid = data.get("id", f.stem)
            st.subheader(f"{mid}: {data.get('title')}")
            st.write(data.get("description"))
            st.write(
                f"XP: {data.get('xp_reward')} | Сложность: {'★' * data.get('difficulty', 1)}"
            )
            completed = mid in state.get("missions_completed", [])
            st.write("Статус:", "✅ Пройдена" if completed else "⬜ Не начата")
            if st.button(f"Запустить миссию {mid}", key=f"mission_{mid}"):
                st.session_state["active_mission"] = mid
                st.success(
                    f"Миссия {mid} активирована. Используйте CLI для выполнения."
                )
    else:
        st.info("Нет доступных миссий.")

st.sidebar.title("CyberTeacher")
st.sidebar.info("Это мониторинговая панель. Для интерактива используйте CLI.")
