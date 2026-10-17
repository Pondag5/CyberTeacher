"""
Push Notifications (MF-05) — APScheduler + Web Push (VAPID).
24/48/72h re-engagement notifications.
"""

import os
import json
import time
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta

from state import get_state
from settings import get_settings

# Try to import optional dependencies
try:
    import pywebpush
    from pywebpush import webpush, WebPushException
    PYWEBPUSH_AVAILABLE = True
except ImportError:
    PYWEBPUSH_AVAILABLE = False

try:
    from apscheduler.schedulers.background import BackgroundScheduler
    from apscheduler.triggers.interval import IntervalTrigger
    APSCHEDULER_AVAILABLE = True
except ImportError:
    APSCHEDULER_AVAILABLE = False


# VAPID keys file
VAPID_KEYS_FILE = "./memory/vapid_keys.json"
PUSH_SUBSCRIPTIONS_FILE = "./memory/push_subscriptions.json"

# Notification templates
NOTIFICATION_TEMPLATES = {
    "24h": {
        "title": "CyberTeacher: Вернись в систему",
        "body": "24 часа тишины. Твои флаги ждут. /story",
        "tag": "reengage_24h",
    },
    "48h": {
        "title": "CyberTeacher: Шум нарастает",
        "body": "48 часов без активности. Watchers заметили. /noise",
        "tag": "reengage_48h",
    },
    "72h": {
        "title": "CyberTeacher: Последний звонок",
        "body": "72 часа. Долги накапливаются. Эхо зовёт. /phantom",
        "tag": "reengage_72h",
    },
}

# Global scheduler
_scheduler = None


def _load_vapid_keys() -> Dict[str, str]:
    """Load or generate VAPID keys."""
    if os.path.exists(VAPID_KEYS_FILE):
        try:
            with open(VAPID_KEYS_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    
    # Generate new keys
    from pywebpush import Vapid
    v = Vapid()
    v.generate_keys()
    
    # Convert to base64 strings
    import base64
    from cryptography.hazmat.primitives import serialization
    
    private_bytes = v.private_key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_bytes = v.public_key.public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    
    keys = {
        "public_key": base64.urlsafe_b64encode(public_bytes).decode(),
        "private_key": base64.urlsafe_b64encode(private_bytes).decode(),
    }
    
    _save_vapid_keys(keys)
    return keys


def _save_vapid_keys(keys: Dict[str, str]) -> None:
    """Save VAPID keys to file."""
    os.makedirs(os.path.dirname(VAPID_KEYS_FILE), exist_ok=True)
    with open(VAPID_KEYS_FILE, "w") as f:
        json.dump(keys, f)


def get_vapid_public_key() -> str:
    """Get VAPID public key for client subscription."""
    keys = _load_vapid_keys()
    return keys.get("public_key", "")


def _load_subscriptions() -> List[Dict[str, Any]]:
    """Load push subscriptions from file."""
    if os.path.exists(PUSH_SUBSCRIPTIONS_FILE):
        try:
            with open(PUSH_SUBSCRIPTIONS_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return []


def _save_subscriptions(subscriptions: List[Dict[str, Any]]) -> None:
    """Save push subscriptions to file."""
    os.makedirs(os.path.dirname(PUSH_SUBSCRIPTIONS_FILE), exist_ok=True)
    with open(PUSH_SUBSCRIPTIONS_FILE, "w") as f:
        json.dump(subscriptions, f)


def subscribe_push(subscription: Dict[str, Any]) -> bool:
    """Subscribe a user to push notifications."""
    subscriptions = _load_subscriptions()
    
    # Check if already subscribed (by endpoint)
    endpoint = subscription.get("endpoint", "")
    for i, sub in enumerate(subscriptions):
        if sub.get("endpoint") == endpoint:
            # Update existing
            subscriptions[i] = subscription
            subscriptions[i]["updated_at"] = time.time()
            _save_subscriptions(subscriptions)
            return True
    
    # Add new
    subscription["created_at"] = time.time()
    subscription["updated_at"] = time.time()
    subscriptions.append(subscription)
    _save_subscriptions(subscriptions)
    return True


def unsubscribe_push(endpoint: str) -> bool:
    """Unsubscribe a user from push notifications."""
    subscriptions = _load_subscriptions()
    original_len = len(subscriptions)
    subscriptions = [s for s in subscriptions if s.get("endpoint") != endpoint]
    if len(subscriptions) < original_len:
        _save_subscriptions(subscriptions)
        return True
    return False


def get_subscriptions() -> List[Dict[str, Any]]:
    """Get all push subscriptions."""
    return _load_subscriptions()


def send_push_notification(
    subscription: Dict[str, Any],
    payload: Dict[str, Any],
    vapid_private_key: str = None,
    vapid_claims: Dict[str, str] = None
) -> bool:
    """Send a push notification to a single subscription."""
    if not PYWEBPUSH_AVAILABLE:
        logging.warning("pywebpush not available, cannot send push")
        return False
    
    keys = _load_vapid_keys()
    private_key = vapid_private_key or keys.get("private_key", "")
    
    if not private_key:
        logging.warning("No VAPID private key available")
        return False
    
    default_claims = {
        "sub": f"mailto:admin@{get_settings().cors_origins.split(',')[0].replace('http://', '').replace('https://', '')}",
        "aud": subscription.get("endpoint", "").split("/")[2] if subscription.get("endpoint") else "",
    }
    claims = vapid_claims or default_claims
    
    try:
        webpush(
            subscription_info=subscription,
            data=json.dumps(payload),
            vapid_private_key=private_key,
            vapid_claims=claims,
            timeout=10,
        )
        return True
    except WebPushException as e:
        logging.error(f"WebPush failed: {e}")
        # If subscription expired/invalid, we might want to remove it
        if e.response and e.response.status_code in (404, 410):
            unsubscribe_push(subscription.get("endpoint", ""))
        return False
    except Exception as e:
        logging.error(f"Push notification error: {e}")
        return False


def send_notification_to_all(template_key: str, custom_payload: Dict[str, Any] = None) -> int:
    """Send a notification to all subscribers using a template."""
    template = NOTIFICATION_TEMPLATES.get(template_key)
    if not template:
        return 0
    
    payload = {
        "title": template["title"],
        "body": template["body"],
        "tag": template["tag"],
        "icon": "/static/icons/icon-192.png",
        "badge": "/static/icons/badge-72.png",
        "requireInteraction": True,
        "actions": [
            {"action": "open", "title": "Открыть"},
            {"action": "dismiss", "title": "Отложить"},
        ],
        "data": {"url": "/"},
    }
    if custom_payload:
        payload.update(custom_payload)
    
    subscriptions = _load_subscriptions()
    sent = 0
    
    for sub in subscriptions:
        if send_push_notification(sub, payload):
            sent += 1
    
    return sent


def schedule_reengagement_notifications():
    """Schedule 24h, 48h, 72h re-engagement notifications."""
    if not APSCHEDULER_AVAILABLE:
        logging.warning("APScheduler not available, cannot schedule notifications")
        return
    
    global _scheduler
    if _scheduler is None:
        _scheduler = BackgroundScheduler()
        _scheduler.start()
    
    # Remove existing re-engagement jobs
    for job in _scheduler.get_jobs():
        if job.id.startswith("reengage_"):
            _scheduler.remove_job(job.id)
    
    # Schedule 24h, 48h, 72h notifications
    intervals = [
        ("24h", 24),
        ("48h", 48),
        ("72h", 72),
    ]
    
    for tag, hours in intervals:
        _scheduler.add_job(
            send_notification_to_all,
            trigger=IntervalTrigger(hours=hours),
            args=[tag],
            id=f"reengage_{tag}",
            replace_existing=True,
            max_instances=1,
            coalesce=True,
        )


def start_push_scheduler():
    """Start the push notification scheduler."""
    if not APSCHEDULER_AVAILABLE:
        logging.warning("APScheduler not installed, push scheduler not started")
        return
    
    global _scheduler
    if _scheduler is None:
        _scheduler = BackgroundScheduler()
        _scheduler.start()
        logging.info("Push notification scheduler started")
    
    # Schedule re-engagement notifications
    schedule_reengagement_notifications()
    
    # Also schedule daily cleanup of invalid subscriptions
    _scheduler.add_job(
        _cleanup_invalid_subscriptions,
        trigger=IntervalTrigger(days=1),
        id="push_cleanup",
        replace_existing=True,
    )


def _cleanup_invalid_subscriptions():
    """Remove subscriptions that consistently fail."""
    # This would track failed deliveries and remove after N failures
    # For now, just a placeholder
    pass


def stop_push_scheduler():
    """Stop the push notification scheduler."""
    global _scheduler
    if _scheduler:
        _scheduler.shutdown()
        _scheduler = None
        logging.info("Push notification scheduler stopped")


# CLI handler
def handle_push_subscribe(action: str) -> tuple:
    """Handle /push [subscribe|unsubscribe|status|test|vapid] command."""
    from ui import console
    from rich.panel import Panel
    
    state = get_state()
    parts = action.split()
    sub = parts[1].lower() if len(parts) > 1 else "status"
    
    if sub == "vapid":
        # Show VAPID public key for client
        public_key = get_vapid_public_key()
        console.print(Panel(
            f"VAPID Public Key:\n[bold]{public_key}[/bold]\n\n"
            f"Use this in client:\n"
            f"navigator.serviceWorker.register('/sw.js').then(reg =>\n"
            f"  reg.pushManager.subscribe({{{{\n"
            f"    userVisibleOnly: true,\n"
            f"    applicationServerKey: urlBase64ToUint8Array('{public_key}')\n"
            f"  }}}})\n"
            f")",
            title="VAPID Public Key",
            border_style="cyan",
        ))
        return True, None, None, True
    
    if sub == "status":
        subs = _load_subscriptions()
        vapid_key = get_vapid_public_key()
        console.print(Panel(
            f"Подписчики: [bold]{len(subs)}[/bold]\n"
            f"VAPID ключ: {'✅' if vapid_key else '❌'}\n"
            f"pywebpush: {'✅' if PYWEBPUSH_AVAILABLE else '❌'}\n"
            f"APScheduler: {'✅' if APSCHEDULER_AVAILABLE else '❌'}",
            title="🔔 Push Notifications Status",
            border_style="cyan",
        ))
        return True, None, None, True
    
    if sub == "test":
        # Send test notification
        sent = send_notification_to_all("24h")
        console.print(f"[green]Тестовое уведомление отправлено {sent} подписчикам[/green]")
        return True, None, None, True
    
    if sub == "schedule":
        schedule_reengagement_notifications()
        console.print("[green]Расписание уведомлений обновлено (24h/48h/72h)[/green]")
        return True, None, None, True
    
    if sub == "clear":
        # Clear all subscriptions
        _save_subscriptions([])
        console.print("[yellow]Все подписки удалены[/yellow]")
        return True, None, None, True
    
    console.print("[yellow]Использование:[/yellow]")
    console.print("  /push vapid      — показать VAPID публичный ключ")
    console.print("  /push status     — статус подписок")
    console.print("  /push test       — тестовое уведомление")
    console.print("  /push schedule   — настроить расписание 24/48/72h")
    console.print("  /push clear      — удалить все подписки")
    return True, None, None, True