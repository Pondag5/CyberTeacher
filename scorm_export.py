"""SCORM 1.2 package export for CyberTeacher courses.

Generates a SCORM-compliant .zip package that can be imported into
any LMS (Moodle, Canvas, Blackboard, etc.).

Usage:
    from scorm_export import export_scorm_package
    zip_path = export_scorm_package("web-basics")
"""

import html
import io
import os
import time
import zipfile
from xml.etree.ElementTree import Element, SubElement, tostring

from courses import COURSES

SCORM_CSS = """
body { font-family: 'Segoe UI', sans-serif; margin: 0; padding: 20px; background: #f5f5f5; color: #333; }
.container { max-width: 800px; margin: 0 auto; background: #fff; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,.1); padding: 32px; }
h1 { color: #00B4D8; border-bottom: 2px solid #00B4D8; padding-bottom: 8px; }
h2 { color: #2a2a3c; margin-top: 24px; }
.topic { margin: 16px 0; padding: 16px; background: #f0f8ff; border-left: 4px solid #00B4D8; border-radius: 4px; }
.quiz-option { display: block; margin: 8px 0; padding: 10px 16px; background: #e8e8e8; border-radius: 4px; cursor: pointer; border: 2px solid transparent; }
.quiz-option:hover { background: #d0e8ff; border-color: #00B4D8; }
.quiz-option.correct { background: #d4edda; border-color: #28a745; }
.quiz-option.wrong { background: #f8d7da; border-color: #dc3545; }
.quiz-result { margin-top: 16px; padding: 12px; border-radius: 4px; font-weight: bold; text-align: center; }
.quiz-result.pass { background: #d4edda; color: #155724; }
.quiz-result.fail { background: #f8d7da; color: #721c24; }
.nav-buttons { margin-top: 24px; display: flex; justify-content: space-between; }
.nav-buttons a { display: inline-block; padding: 10px 24px; background: #00B4D8; color: #fff; text-decoration: none; border-radius: 4px; font-weight: 600; }
.nav-buttons a:hover { background: #0096b8; }
.nav-buttons a.disabled { background: #ccc; pointer-events: none; }
.badge { display: inline-block; padding: 4px 12px; background: #00B4D8; color: #fff; border-radius: 12px; font-size: 0.85rem; }
.progress-bar { width: 100%; height: 8px; background: #e0e0e0; border-radius: 4px; margin: 8px 0; }
.progress-fill { height: 100%; background: #00B4D8; border-radius: 4px; transition: width .3s; }
"""

SCORM_API_JS = """
var API = null;
function scormInit() {
    try { API = window.parent.API; } catch(e) {}
    if (!API) { try { API = parent.API; } catch(e) {} }
    if (API) { API.LMSInitialize(""); }
}
function scormSetValue(name, value) {
    if (API) { API.LMSSetValue(name, value); }
}
function scormCommit() {
    if (API) { API.LMSCommit(""); }
}
function scormFinish() {
    if (API) {
        API.LMSSetValue("cmi.core.lesson_status", "completed");
        API.LMSFinish("");
    }
}
function scormSetScore(score, maxScore) {
    if (API) {
        API.LMSSetValue("cmi.core.score.raw", String(score));
        API.LMSSetValue("cmi.core.score.max", String(maxScore));
        API.LMSSetValue("cmi.core.score.min", "0");
        API.LMSSetValue("cmi.core.lesson_status", score >= maxScore * 0.7 ? "passed" : "failed");
        API.LMSCommit("");
    }
}
window.addEventListener("load", scormInit);
window.addEventListener("beforeunload", scormFinish);
"""


def _esc(text: str) -> str:
    return html.escape(text)


def _make_manifest(course_id: str, course: dict, sco_items: list[dict]) -> str:
    org_id = f"ORG_{course_id.upper().replace('-', '_')}"
    manifest = f"""<?xml version="1.0" encoding="UTF-8"?>
<manifest identifier="CyberTeacher_{_esc(course_id)}"
          xmlns="http://www.imsproject.org/xsd/imscp_rootv1p1p2"
          xmlns:adlcp="http://www.adlnet.org/xsd/adlcp_rootv1p2"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:schemaLocation="http://www.imsproject.org/xsd/imscp_rootv1p1p2 imscp_rootv1p1p2.xsd">
  <metadata>
    <schema>ADL SCORM</schema>
    <schemaversion>1.2</schemaversion>
  </metadata>
  <organizations default="{org_id}">
    <organization identifier="{org_id}">
      <title>{_esc(course.get("name", course_id))}</title>
"""
    for i, sco in enumerate(sco_items):
        manifest += f'      <item identifier="{sco["item_id"]}" identifierref="{sco["res_id"]}">\n'
        manifest += f"        <title>{_esc(sco['title'])}</title>\n"
        manifest += f"      </item>\n"

    manifest += f"""    </organization>
  </organizations>
  <resources>
"""
    manifest += f'    <resource identifier="RES_INDEX" type="webcontent" adlcp:scormtype="sco" href="index.html">\n'
    manifest += f'      <file href="index.html"/>\n'
    manifest += f'      <file href="css/style.css"/>\n'
    manifest += f'      <file href="js/scorm_api.js"/>\n'
    manifest += f"    </resource>\n"

    for sco in sco_items:
        manifest += f'    <resource identifier="{sco["res_id"]}" type="webcontent" adlcp:scormtype="sco" href="{sco["href"]}">\n'
        manifest += f'      <file href="{sco["href"]}"/>\n'
        manifest += f"    </resource>\n"

    manifest += """  </resources>
</manifest>"""
    return manifest


def _make_index_html(course_id: str, course: dict, sco_items: list[dict]) -> str:
    topics_html = ""
    for sco in sco_items:
        icon = "📖" if sco["type"] == "lesson" else "📝"
        topics_html += f"""
        <div class="topic">
            <a href="{_esc(sco["href"])}" style="text-decoration:none;color:inherit;">
                {icon} <strong>{_esc(sco["title"])}</strong>
            </a>
        </div>"""

    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{_esc(course.get("name", course_id))}</title>
    <link rel="stylesheet" href="css/style.css">
    <script src="js/scorm_api.js"></script>
</head>
<body>
<div class="container">
    <h1>{_esc(course.get("name", course_id))}</h1>
    <p>{_esc(course.get("desc", course.get("description", "")))}</p>
    <span class="badge">{_esc(course.get("level", "beginner"))}</span>
    <div class="progress-bar"><div class="progress-fill" style="width:0%"></div></div>
    <h2>Содержание</h2>
    {topics_html}
    <div class="nav-buttons" style="margin-top:32px;">
        <a class="disabled">Назад</a>
        <a href="{_esc(sco_items[0]["href"]) if sco_items else "#"}">Начать</a>
    </div>
</div>
</body>
</html>"""


def _make_lesson_html(
    course_id: str,
    topic_name: str,
    topic_desc: str,
    prev_href: str | None,
    next_href: str | None,
    res_id: str,
) -> str:
    prev_btn = (
        f'<a href="{_esc(prev_href)}">Назад</a>'
        if prev_href
        else '<a class="disabled">Назад</a>'
    )
    next_btn = (
        f'<a href="{_esc(next_href)}">Далее</a>'
        if next_href
        else f'<a href="quiz_{_esc(course_id)}_{_esc(topic_name)}.html">Квиз</a>'
    )

    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{_esc(topic_name)}</title>
    <link rel="stylesheet" href="css/style.css">
    <script src="js/scorm_api.js"></script>
</head>
<body>
<div class="container">
    <h1>{_esc(topic_name)}</h1>
    <div class="topic">
        <p>{_esc(topic_desc)}</p>
    </div>
    <div class="nav-buttons">
        {prev_btn}
        {next_btn}
    </div>
</div>
</body>
</html>"""


def _make_quiz_html(
    course_id: str,
    topic_name: str,
    quiz_questions: list[dict],
    next_href: str | None,
    res_id: str,
) -> str:
    questions_html = ""
    for i, q in enumerate(quiz_questions):
        options_html = ""
        for j, opt in enumerate(q.get("options", [])):
            options_html += f"""
            <div class="quiz-option" data-question="{i}" data-answer="{j}"
                 onclick="checkAnswer({i}, {j})">{_esc(opt)}</div>"""

        questions_html += f"""
        <div class="question" id="q{i}">
            <h3>Вопрос {i + 1}: {_esc(q.get("question", ""))}</h3>
            {options_html}
            <div class="quiz-result" id="result{i}"></div>
        </div>"""

    next_btn = (
        f'<a href="{_esc(next_href)}">Далее</a>'
        if next_href
        else '<a href="index.html">Завершить</a>'
    )
    total = len(quiz_questions)

    questions_json = str(
        [
            {k: v for k, v in q.items() if k in ("question", "correct_answer")}
            for q in quiz_questions
        ]
    ).replace("'", '"')

    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Квиз: {_esc(topic_name)}</title>
    <link rel="stylesheet" href="css/style.css">
    <script src="js/scorm_api.js"></script>
</head>
<body>
<div class="container">
    <h1>📝 Квиз: {_esc(topic_name)}</h1>
    <p>Вопросов: {total} | Для прохождения: 70%</p>
    {questions_html}
    <div id="finalResult" style="display:none;" class="quiz-result"></div>
    <div class="nav-buttons">
        <a class="disabled">Назад</a>
        {next_btn}
    </div>
</div>
<script>
var totalQ = {total};
var answers = {questions_json};
var correct = 0;
function checkAnswer(q, a) {{
    var opts = document.querySelectorAll('[data-question="'+q+'"]');
    opts.forEach(function(o) {{ o.style.pointerEvents = 'none'; }});
    if (a === answers[q].correct_answer) {{
        opts[a].classList.add('correct');
        document.getElementById('result'+q).innerHTML = '✅ Правильно!';
        document.getElementById('result'+q).style.color = '#155724';
        correct++;
    }} else {{
        opts[a].classList.add('wrong');
        opts[answers[q].correct_answer].classList.add('correct');
        document.getElementById('result'+q).innerHTML = '❌ Неправильно. Правильный ответ: ' + answers[q].correct_answer;
        document.getElementById('result'+q).style.color = '#721c24';
    }}
    if (document.querySelectorAll('.correct, .wrong').length >= totalQ * 2) {{
        var pct = Math.round(correct / totalQ * 100);
        var res = document.getElementById('finalResult');
        res.style.display = 'block';
        res.className = 'quiz-result ' + (pct >= 70 ? 'pass' : 'fail');
        res.innerHTML = 'Результат: ' + correct + '/' + totalQ + ' (' + pct + '%)';
        scormSetScore(correct, totalQ);
    }}
}}
</script>
</body>
</html>"""


def export_scorm_package(course_id: str, output_dir: str = "./") -> str:
    """Generate a SCORM 1.2 .zip package for a course.

    Args:
        course_id: Course identifier (e.g., "web-basics").
        output_dir: Directory to write the .zip file.

    Returns:
        Path to the generated .zip file.

    Raises:
        ValueError: If course_id not found.
    """
    if course_id not in COURSES:
        available = ", ".join(COURSES.keys())
        raise ValueError(f"Unknown course: {course_id}. Available: {available}")

    course = COURSES[course_id]
    course_name = course.get("name", course_id)

    sco_items: list[dict] = []
    zip_buffer = io.BytesIO()

    topics = course.get("topics", [])

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for i, topic in enumerate(topics):
            topic_name = topic.name if hasattr(topic, "name") else str(topic)
            topic_desc = topic.description if hasattr(topic, "description") else ""
            safe_name = topic_name.replace(" ", "_").replace("/", "_")

            lesson_href = f"lesson_{safe_name}.html"
            quiz_href = f"quiz_{safe_name}.html"

            prev_href = sco_items[-1]["href"] if sco_items else None

            lesson_id = f"ITEM_LESSON_{i + 1}_{safe_name.upper()}"
            lesson_res_id = f"RES_LESSON_{i + 1}_{safe_name.upper()}"
            quiz_id = f"ITEM_QUIZ_{i + 1}_{safe_name.upper()}"
            quiz_res_id = f"RES_QUIZ_{i + 1}_{safe_name.upper()}"

            lesson_html = _make_lesson_html(
                course_id,
                topic_name,
                topic_desc,
                prev_href,
                quiz_href,
                lesson_res_id,
            )
            zf.writestr(lesson_href, lesson_html)
            sco_items.append(
                {
                    "item_id": lesson_id,
                    "res_id": lesson_res_id,
                    "href": lesson_href,
                    "title": topic_name,
                    "type": "lesson",
                }
            )

            quiz_questions = []
            quiz_topics = topic.quiz_topics if hasattr(topic, "quiz_topics") else []
            for qt in quiz_topics:
                quiz_questions.append(
                    {
                        "question": f"Проверьте понимание темы: {qt}",
                        "options": [
                            f"Я изучил основы {qt}",
                            f"Мне нужно повторить {qt}",
                            f"Я могу применить {qt} на практике",
                        ],
                        "correct_answer": 2,
                    }
                )

            if not quiz_questions:
                quiz_questions = [
                    {
                        "question": f"Вы изучили тему «{topic_name}»?",
                        "options": ["Да", "Частично", "Нет"],
                        "correct_answer": 0,
                    },
                ]

            next_href = sco_items[-1]["href"] if len(sco_items) > 0 else None
            quiz_html = _make_quiz_html(
                course_id,
                topic_name,
                quiz_questions,
                None,
                quiz_res_id,
            )
            zf.writestr(quiz_href, quiz_html)
            sco_items.append(
                {
                    "item_id": quiz_id,
                    "res_id": quiz_res_id,
                    "href": quiz_href,
                    "title": f"Квиз: {topic_name}",
                    "type": "quiz",
                }
            )

        if not sco_items:
            sco_items.append(
                {
                    "item_id": "ITEM_INTRO",
                    "res_id": "RES_INTRO",
                    "href": "index.html",
                    "title": course_name,
                    "type": "lesson",
                }
            )

        manifest = _make_manifest(course_id, course, sco_items)
        zf.writestr("imsmanifest.xml", manifest)
        zf.writestr("index.html", _make_index_html(course_id, course, sco_items))
        zf.writestr("css/style.css", SCORM_CSS)
        zf.writestr("js/scorm_api.js", SCORM_API_JS)

    os.makedirs(output_dir, exist_ok=True)
    ts = int(time.time())
    filename = f"scorm_{course_id}_{ts}.zip"
    filepath = os.path.join(output_dir, filename)
    with open(filepath, "wb") as f:
        f.write(zip_buffer.getvalue())

    return filepath


def export_scorm_package_bytes(course_id: str) -> bytes:
    """Generate a SCORM 1.2 .zip package and return as bytes.

    Args:
        course_id: Course identifier (e.g., "web-basics").

    Returns:
        ZIP file contents as bytes.

    Raises:
        ValueError: If course_id not found.
    """
    if course_id not in COURSES:
        available = ", ".join(COURSES.keys())
        raise ValueError(f"Unknown course: {course_id}. Available: {available}")

    course = COURSES[course_id]
    sco_items: list[dict] = []
    zip_buffer = io.BytesIO()
    topics = course.get("topics", [])

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for i, topic in enumerate(topics):
            topic_name = topic.name if hasattr(topic, "name") else str(topic)
            topic_desc = topic.description if hasattr(topic, "description") else ""
            safe_name = topic_name.replace(" ", "_").replace("/", "_")
            lesson_href = f"lesson_{safe_name}.html"
            quiz_href = f"quiz_{safe_name}.html"
            prev_href = sco_items[-1]["href"] if sco_items else None
            lesson_id = f"ITEM_LESSON_{i + 1}_{safe_name.upper()}"
            lesson_res_id = f"RES_LESSON_{i + 1}_{safe_name.upper()}"
            quiz_id = f"ITEM_QUIZ_{i + 1}_{safe_name.upper()}"
            quiz_res_id = f"RES_QUIZ_{i + 1}_{safe_name.upper()}"

            zf.writestr(
                lesson_href,
                _make_lesson_html(
                    course_id,
                    topic_name,
                    topic_desc,
                    prev_href,
                    quiz_href,
                    lesson_res_id,
                ),
            )
            sco_items.append(
                {
                    "item_id": lesson_id,
                    "res_id": lesson_res_id,
                    "href": lesson_href,
                    "title": topic_name,
                    "type": "lesson",
                }
            )

            quiz_questions = []
            quiz_topics = topic.quiz_topics if hasattr(topic, "quiz_topics") else []
            for qt in quiz_topics:
                quiz_questions.append(
                    {
                        "question": f"Проверьте понимание темы: {qt}",
                        "options": [
                            f"Я изучил основы {qt}",
                            f"Мне нужно повторить {qt}",
                            f"Я могу применить {qt} на практике",
                        ],
                        "correct_answer": 2,
                    }
                )
            if not quiz_questions:
                quiz_questions = [
                    {
                        "question": f"Вы изучили тему «{topic_name}»?",
                        "options": ["Да", "Частично", "Нет"],
                        "correct_answer": 0,
                    }
                ]

            zf.writestr(
                quiz_href,
                _make_quiz_html(
                    course_id, topic_name, quiz_questions, None, quiz_res_id
                ),
            )
            sco_items.append(
                {
                    "item_id": quiz_id,
                    "res_id": quiz_res_id,
                    "href": quiz_href,
                    "title": f"Квиз: {topic_name}",
                    "type": "quiz",
                }
            )

        if not sco_items:
            sco_items.append(
                {
                    "item_id": "ITEM_INTRO",
                    "res_id": "RES_INTRO",
                    "href": "index.html",
                    "title": course.get("name", course_id),
                    "type": "lesson",
                }
            )

        zf.writestr("imsmanifest.xml", _make_manifest(course_id, course, sco_items))
        zf.writestr("index.html", _make_index_html(course_id, course, sco_items))
        zf.writestr("css/style.css", SCORM_CSS)
        zf.writestr("js/scorm_api.js", SCORM_API_JS)

    return zip_buffer.getvalue()


def list_exportable_courses() -> list[dict[str, str]]:
    """List all courses available for SCORM export."""
    result = []
    for cid, course in COURSES.items():
        topics = course.get("topics", [])
        result.append(
            {
                "id": cid,
                "name": course.get("name", cid),
                "description": course.get("desc", ""),
                "level": course.get("level", "beginner"),
                "topics_count": str(len(topics)),
            }
        )
    return result
