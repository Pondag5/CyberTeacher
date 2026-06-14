"""Faction system API routes (factions, echo, memory)."""


def register_faction_routes(app, _if_app, HTTPException, get_state):
    @_if_app("get", "/api/factions")
    def get_factions_api():
        try:
            from handlers.faction import get_factions

            return get_factions()
        except Exception as e:
            return {"rick": 0, "ghost": 0, "chosen": None}

    @_if_app("post", "/api/faction/choose")
    def choose_faction_api(faction: str):
        try:
            from handlers.faction import choose_faction

            result = choose_faction(faction)
            return {
                "status": "ok" if result.startswith("✅") else "error",
                "message": result,
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @_if_app("get", "/api/echo")
    def get_echo_api():
        try:
            from handlers.echo import get_echo_message

            msg = get_echo_message(force=True)
            return {"message": msg}
        except Exception as e:
            return {"message": ""}

    @_if_app("get", "/api/memory")
    def get_memory_api():
        try:
            from handlers.memory import get_random_memory

            state = get_state()
            memories = getattr(state, "student_memories", [])
            return {"memories": memories[-10:], "random": get_random_memory()}
        except Exception as e:
            return {"memories": [], "random": None}
