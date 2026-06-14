"""Rewind (time machine) API routes."""


def register_rewind_routes(app, _if_app, HTTPException, get_state):
    @_if_app("get", "/api/rewind")
    def get_rewind_api():
        try:
            state = get_state()
            chapters = getattr(state, "chapter_completed", [])
            from story_mode import CHAPTERS

            available = [
                {"id": c["id"], "title": c["title"]}
                for c in CHAPTERS
                if c["id"] in chapters
            ]
            return {
                "available_chapters": available,
                "current_chapter": getattr(state, "current_chapter", 1),
            }
        except ImportError:
            return {"available_chapters": [], "current_chapter": 1}

    @_if_app("post", "/api/rewind")
    def post_rewind_api():
        try:
            import json as _json

            body = _json.loads(app.request.body)
            chapter_id = body.get("chapter", 0)
            if not chapter_id:
                from di import get_context

                ctx = get_context()
                chapters = getattr(ctx.state, "chapter_completed", [])
                return {
                    "success": False,
                    "message": "Missing chapter field",
                    "available": chapters,
                }

            from handlers.rewind import handle_rewind

            result = handle_rewind(f"rewind {chapter_id}")
            return {"success": result[0], "message": "Rewind executed"}
        except Exception as e:
            return {"success": False, "message": f"Error: {e}"}
