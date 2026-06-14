"""Story and chapter API routes."""


def register_story_routes(app, _if_app, HTTPException, get_state):
    @_if_app("get", "/api/story")
    def get_story_episodes():
        try:
            from story_mode import STORY_EPISODES, CHAPTERS

            state = get_state()
            completed = getattr(state, "story_completed", [])
            result = []
            for ep in STORY_EPISODES:
                ep_id = ep["id"]
                prev_completed = ep_id == 1 or (ep_id - 1) in completed
                ch_id = next(
                    (ch["id"] for ch in CHAPTERS if ep_id in ch["episode_ids"]), None
                )
                result.append(
                    {
                        "id": ep_id,
                        "title": ep["title"],
                        "desc": ep["desc"],
                        "category": ep.get("cat", "general"),
                        "difficulty": ep.get("diff", 1),
                        "xp": ep.get("xp", 100),
                        "chapter_id": ch_id,
                        "completed": ep_id in completed,
                        "locked": not prev_completed and ep_id not in completed,
                    }
                )
            return {"episodes": result}
        except Exception as e:
            return {"episodes": [], "error": "Internal error"}

    @_if_app("post", "/api/story/start")
    def start_story_episode(episode_id: int):
        try:
            from story_mode import STORY_EPISODES

            ep = next((e for e in STORY_EPISODES if e["id"] == episode_id), None)
            if not ep:
                raise HTTPException(status_code=404, detail="Episode not found")
            state = get_state()
            completed = getattr(state, "story_completed", [])
            if (
                episode_id not in completed
                and episode_id > 1
                and (episode_id - 1) not in completed
            ):
                raise HTTPException(
                    status_code=400,
                    detail=f"Episode {episode_id - 1} must be completed first",
                )
            state.current_story_episode = episode_id
            return {
                "status": "ok",
                "episode": ep,
                "prompt": f"Эпизод {ep['id']}: {ep['title']}. {ep['desc']}",
            }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail="Internal server error")

    @_if_app("post", "/api/story/submit")
    def submit_story_answer(answer: str):
        try:
            from story_mode import STORY_EPISODES

            state = get_state()
            ep_id = getattr(state, "current_story_episode", None)
            if not ep_id:
                raise HTTPException(status_code=400, detail="No active episode")
            ep = next((e for e in STORY_EPISODES if e["id"] == ep_id), None)
            if not ep:
                raise HTTPException(status_code=404, detail="Episode not found")

            flag = ep.get("flag", "")
            correct = flag.lower() in answer.lower() if flag else False

            if correct:
                completed = getattr(state, "story_completed", [])
                if ep_id not in completed:
                    completed.append(ep_id)
                    state.story_completed = completed
                    state.xp = getattr(state, "xp", 0) + ep.get("xp", 100)

            return {
                "correct": correct,
                "xp_earned": ep.get("xp", 100) if correct else 0,
                "hint": ep.get("hint", [""])[0] if not correct else "",
            }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail="Internal server error")

    @_if_app("get", "/api/chapters")
    def get_chapters_api():
        try:
            from story_mode import get_chapters

            return {"chapters": get_chapters()}
        except Exception as e:
            return {"chapters": [], "error": "Internal error"}

    @_if_app("post", "/api/chapter/start")
    def start_chapter_api(chapter_id: int):
        try:
            from story_mode import start_chapter

            result = start_chapter(chapter_id)
            if result.startswith("❌"):
                raise HTTPException(status_code=400, detail=result)
            return {"status": "ok", "chapter_id": chapter_id, "intro": result}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail="Internal server error")

    @_if_app("post", "/api/story/final")
    def final_choice_api(path: str):
        try:
            from story_mode import final_choice

            result = final_choice(path)
            if result.startswith("❌"):
                return {"status": "error", "message": result}
            return {"status": "ok", "path": path, "message": result}
        except Exception as e:
            return {"status": "error", "message": str(e)}
