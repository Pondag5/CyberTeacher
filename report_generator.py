"""PDF Report Generator — training report export.

Uses HTML-to-print approach (CSS @media print) for PDF generation.
No external dependencies needed — uses browser print dialog.
"""

from typing import Any, Dict, Optional
import time


def generate_report_html(state: Any, conn: Any = None) -> str:
    """Generate a printable HTML report of the user's training progress."""
    from datetime import datetime

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    handle = getattr(state, "handle", "Новичок")
    level = getattr(state, "level", 1)
    xp = getattr(state, "xp", 0)
    points = getattr(state, "points", 0)
    reputation = getattr(state, "reputation", 0)
    quizzes = getattr(state, "quizzes_taken", 0)
    labs = getattr(state, "labs_started", 0)
    flags = getattr(state, "total_flags_collected", 0)
    skills = getattr(state, "skills", {})
    achievements = getattr(state, "earned_achievements", [])
    weak = getattr(state, "weak_topics", [])

    skills_html = ""
    if skills:
        for name, data in skills.items():
            skill_level = data.get("level", 0) if isinstance(data, dict) else 0
            skill_xp = data.get("xp", 0) if isinstance(data, dict) else 0
            pct = min(100, skill_level * 20)
            skills_html += f"""
            <tr>
                <td>{name}</td>
                <td>{skill_level}</td>
                <td>{skill_xp}</td>
                <td><div style="background:#e0e0e0;height:8px;border-radius:4px;width:100px;">
                    <div style="background:#00B4D8;height:100%;width:{pct}%;border-radius:4px;"></div>
                </div></td>
            </tr>"""

    weak_html = ""
    if weak:
        for w in weak:
            topic = w.get("topic", "") if isinstance(w, dict) else str(w)
            rate = w.get("success_rate", 0) if isinstance(w, dict) else 0
            weak_html += f"<li>{topic} ({rate:.0f}%)</li>"

    achievements_html = ""
    for a in achievements:
        achievements_html += f'<span style="display:inline-block;background:#f0f0f0;padding:2px 8px;border-radius:12px;margin:2px;font-size:12px;">✅ {a}</span>'

    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<title>CyberTeacher — Training Report</title>
<style>
body {{ font-family: Arial, sans-serif; margin: 40px; color: #333; line-height: 1.5; }}
h1 {{ color: #1a1a2e; border-bottom: 3px solid #00B4D8; padding-bottom: 10px; }}
h2 {{ color: #1a1a2e; margin-top: 30px; }}
table {{ width: 100%; border-collapse: collapse; margin: 10px 0; }}
th, td {{ border: 1px solid #ddd; padding: 8px 12px; text-align: left; }}
th {{ background: #f5f5f5; }}
.metric {{ display: inline-block; text-align: center; padding: 15px 25px; margin: 5px; border: 1px solid #ddd; border-radius: 8px; }}
.metric .value {{ font-size: 24px; font-weight: bold; color: #00B4D8; }}
.metric .label {{ font-size: 12px; color: #666; }}
.footer {{ margin-top: 40px; padding-top: 10px; border-top: 1px solid #ddd; font-size: 11px; color: #999; }}
@media print {{ body {{ margin: 20px; }} }}
</style>
</head>
<body>
<h1>🎓 CyberTeacher — Training Report</h1>
<p><strong>Generated:</strong> {now}</p>

<div style="text-align:center; margin: 20px 0;">
    <div class="metric"><div class="value">{xp}</div><div class="label">XP</div></div>
    <div class="metric"><div class="value">Lvl {level}</div><div class="label">Level</div></div>
    <div class="metric"><div class="value">{handle}</div><div class="label">Rank</div></div>
    <div class="metric"><div class="value">{reputation}</div><div class="label">Reputation</div></div>
    <div class="metric"><div class="value">{quizzes}</div><div class="label">Quizzes</div></div>
    <div class="metric"><div class="value">{labs}</div><div class="label">Labs</div></div>
    <div class="metric"><div class="value">{flags}</div><div class="label">Flags</div></div>
</div>

<h2>📊 Skills</h2>
{"<table><tr><th>Skill</th><th>Level</th><th>XP</th><th>Progress</th></tr>" + skills_html + "</table>" if skills_html else "<p>No skills tracked yet.</p>"}

<h2>⚠️ Weak Topics</h2>
{"<ul>" + weak_html + "</ul>" if weak_html else "<p>No weak topics identified.</p>"}

<h2>🏆 Achievements ({len(achievements)})</h2>
{achievements_html if achievements_html else "<p>No achievements yet.</p>"}

<div class="footer">
    CyberTeacher — AI Cybersecurity Tutor v5.13<br>
    Report generated automatically. For educational use only.
</div>
</body>
</html>"""


def generate_report_from_state(state: Any) -> str:
    """Generate report directly from state object."""
    return generate_report_html(state)
