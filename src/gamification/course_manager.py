"""Course management — teacher/admin can create, edit, delete courses.

Provides CRUD for courses with topics, prerequisites, and difficulty levels.
Courses are stored in JSON file, not database.
"""

import json
import os
import time
from typing import Any, Dict, List, Optional


COURSES_FILE = "./memory/courses.json"

DEFAULT_COURSES: List[Dict[str, Any]] = [
    {
        "id": "web_security",
        "name": "Web Security",
        "description": "OWASP Top 10, XSS, SQLi, CSRF, authentication bypass",
        "icon": "\ud83c\udf10",
        "difficulty": "beginner",
        "topics": ["owasp_top10", "xss", "sqli", "csrf", "auth_bypass", "ssrf"],
        "progress": 0,
        "active": False,
        "created_by": "system",
        "is_default": True,
    },
    {
        "id": "network_security",
        "name": "Network Security",
        "description": "TCP/IP, firewalls, IDS/IPS, packet analysis, network attacks",
        "icon": "\ud83d\udd17",
        "difficulty": "beginner",
        "topics": [
            "tcp_ip",
            "firewall",
            "ids_ips",
            "packet_analysis",
            "arp_spoof",
            "dns_poison",
        ],
        "progress": 0,
        "active": False,
        "created_by": "system",
        "is_default": True,
    },
    {
        "id": "crypto",
        "name": "Cryptography",
        "description": "Symmetric, asymmetric, hashing, PKI, TLS, crypto attacks",
        "icon": "\ud83d\udd10",
        "difficulty": "intermediate",
        "topics": [
            "symmetric",
            "asymmetric",
            "hashing",
            "pki",
            "tls",
            "crypto_attacks",
        ],
        "progress": 0,
        "active": False,
        "created_by": "system",
        "is_default": True,
    },
    {
        "id": "malware_analysis",
        "name": "Malware Analysis",
        "description": "Static/dynamic analysis, reverse engineering, sandboxing",
        "icon": "\ud83e\udda0",
        "difficulty": "advanced",
        "topics": [
            "static_analysis",
            "dynamic_analysis",
            "reverse_engineering",
            "sandboxing",
            "yara",
        ],
        "progress": 0,
        "active": False,
        "created_by": "system",
        "is_default": True,
    },
    {
        "id": "pentesting",
        "name": "Penetration Testing",
        "description": "Recon, exploitation, post-exploitation, reporting",
        "icon": "\u2694\ufe0f",
        "difficulty": "advanced",
        "topics": [
            "recon",
            "exploitation",
            "post_exploitation",
            "privilege_escalation",
            "reporting",
        ],
        "progress": 0,
        "active": False,
        "created_by": "system",
        "is_default": True,
    },
    {
        "id": "social_engineering",
        "name": "Social Engineering",
        "description": "Phishing, pretexting, manipulation, OSINT",
        "icon": "\ud83c\udfa4",
        "difficulty": "intermediate",
        "topics": [
            "phishing",
            "pretexting",
            "manipulation",
            "osint_social",
            "awareness",
        ],
        "progress": 0,
        "active": False,
        "created_by": "system",
        "is_default": True,
    },
]


def _load_courses() -> List[Dict[str, Any]]:
    try:
        if os.path.exists(COURSES_FILE):
            with open(COURSES_FILE, "r", encoding="utf-8") as f:
                result: List[Dict[str, Any]] = json.load(f)
                return result
    except (OSError, IOError, json.JSONDecodeError):
        pass
    # Initialize with defaults
    _save_courses(DEFAULT_COURSES)
    return list(DEFAULT_COURSES)


def _save_courses(courses: List[Dict[str, Any]]) -> None:
    dir_path = os.path.dirname(COURSES_FILE)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)
    content = json.dumps(courses, ensure_ascii=True, indent=2)
    with open(COURSES_FILE, "w", encoding="utf-8") as f:
        f.write(content)


def get_courses() -> List[Dict[str, Any]]:
    """Get all courses."""
    return _load_courses()


def get_course(course_id: str) -> Optional[Dict[str, Any]]:
    """Get a single course by ID."""
    courses = _load_courses()
    return next((c for c in courses if c["id"] == course_id), None)


def create_course(
    name: str,
    description: str = "",
    icon: str = "\ud83d\udcda",
    difficulty: str = "beginner",
    topics: Optional[List[str]] = None,
    created_by: str = "teacher",
) -> Dict[str, Any]:
    """Create a new course."""
    courses = _load_courses()
    course_id = name.lower().replace(" ", "_").replace("-", "_")[:50]

    # Check duplicate
    if any(c["id"] == course_id for c in courses):
        return {"error": f"Course with id '{course_id}' already exists"}

    course = {
        "id": course_id,
        "name": name,
        "description": description,
        "icon": icon,
        "difficulty": difficulty,
        "topics": topics or [],
        "progress": 0,
        "active": False,
        "created_by": created_by,
        "created_at": time.time(),
        "is_default": False,
    }
    courses.append(course)
    _save_courses(courses)
    return course


def update_course(course_id: str, **kwargs: Any) -> Optional[Dict[str, Any]]:
    """Update course fields."""
    courses = _load_courses()
    for course in courses:
        if course["id"] == course_id:
            if course.get("is_default"):
                # Can only update non-structural fields for default courses
                allowed = {"description", "icon"}
                kwargs = {k: v for k, v in kwargs.items() if k in allowed}
            for k, v in kwargs.items():
                if k not in ("id", "is_default", "created_by", "created_at"):
                    course[k] = v
            _save_courses(courses)
            return course
    return None


def delete_course(course_id: str) -> bool:
    """Delete a course (only non-default)."""
    courses = _load_courses()
    course = next((c for c in courses if c["id"] == course_id), None)
    if not course:
        return False
    if course.get("is_default"):
        return False  # Cannot delete built-in courses
    courses = [c for c in courses if c["id"] != course_id]
    _save_courses(courses)
    return True


def add_topic(course_id: str, topic: str) -> bool:
    """Add a topic to a course."""
    courses = _load_courses()
    for course in courses:
        if course["id"] == course_id:
            if topic not in course.get("topics", []):
                course.setdefault("topics", []).append(topic)
                _save_courses(courses)
            return True
    return False


def remove_topic(course_id: str, topic: str) -> bool:
    """Remove a topic from a course."""
    courses = _load_courses()
    for course in courses:
        if course["id"] == course_id:
            topics = course.get("topics", [])
            if topic in topics:
                topics.remove(topic)
                _save_courses(courses)
            return True
    return False
