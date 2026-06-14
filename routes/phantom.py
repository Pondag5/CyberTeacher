"""Phantom Labs API routes."""


def register_phantom_routes(app, _if_app, HTTPException, get_state):
    @_if_app("get", "/api/phantom")
    def get_phantom_api():
        try:
            from handlers.phantom_lab import get_phantom_labs

            return get_phantom_labs()
        except Exception as e:
            return []

    @_if_app("get", "/api/secret")
    def get_secret_room_api():
        try:
            from handlers.secret_room import get_secret_room_status

            return get_secret_room_status()
        except ImportError:
            return {"unlocked": False}

    @_if_app("post", "/api/secret/enter")
    def enter_secret_room_api():
        try:
            from handlers.secret_room import enter_secret_room

            msg = enter_secret_room()
            return {"visited": True, "message": msg}
        except ImportError:
            return {"visited": False, "message": "Error"}

    @_if_app("post", "/api/phantom/complete")
    def complete_phantom_api():
        try:
            from handlers.phantom_lab import complete_phantom_lab
            import json as _json

            body = _json.loads(app.request.body)
            lab_id = body.get("lab_id", "")
            msg = complete_phantom_lab(lab_id)
            if msg:
                return {"success": True, "message": msg}
            return {"success": False, "message": "Lab not found"}
        except Exception as e:
            return {"success": False, "message": "Error"}
