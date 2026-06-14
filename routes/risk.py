"""Risk mechanics API routes (noise, stealth, trace, debts, logs)."""


def register_risk_routes(app, _if_app, HTTPException, get_state):
    @_if_app("get", "/api/noise")
    def get_noise_api():
        try:
            from handlers.noise import get_noise_level

            return get_noise_level()
        except Exception as e:
            return {"level": 0, "status": "unknown"}

    @_if_app("post", "/api/stealth/toggle")
    def toggle_stealth_api():
        try:
            from handlers.noise import toggle_stealth

            return toggle_stealth()
        except Exception as e:
            return {"active": False, "message": "Error"}

    @_if_app("get", "/api/trace")
    def get_trace_api():
        try:
            from handlers.trace import get_trace_status

            return get_trace_status()
        except Exception as e:
            return {"active": False}

    @_if_app("get", "/api/debts")
    def get_debts_api():
        try:
            from handlers.debt import get_debts

            return get_debts()
        except Exception as e:
            return {"total": 0, "details": [], "status": "clean"}

    @_if_app("get", "/api/logs")
    def get_logs_api():
        try:
            from handlers.logs import check_logs

            return check_logs()
        except Exception as e:
            return {"count": 0, "logs": []}

    @_if_app("post", "/api/logs/wipe")
    def wipe_logs_api():
        try:
            from handlers.logs import wipe_logs

            return {"message": wipe_logs()}
        except Exception as e:
            return {"message": "Error"}

    @_if_app("get", "/api/watchers")
    def get_watchers_api():
        try:
            from handlers.watchers import get_watchers_status

            return get_watchers_status()
        except Exception as e:
            return {"attack_active": False}

    @_if_app("post", "/api/watchers/trigger")
    def trigger_watchers_api():
        try:
            from handlers.watchers import trigger_counterattack

            msg = trigger_counterattack()
            if msg:
                return {"triggered": True, "message": msg}
            return {"triggered": False, "message": "Conditions not met or on cooldown"}
        except Exception as e:
            return {"triggered": False, "message": "Error"}
