# API Endpoint Index — CyberTeacher
# Source: /workspace/app/api_server.py + routes/

## Core
GET  /api/health
GET  /api/doctor
GET/POST /api/offline
GET  /api/progress
GET  /api/achievements
GET  /api/weak-topics
GET  /api/courses
POST /api/courses/{id}/select
POST /api/courses/select
POST /api/quiz/result
POST /api/chat
POST /api/quiz/generate
GET  /api/courses-alt
POST /api/courses-alt/select
GET  /api/labs
POST /api/labs/{id}/start
POST /api/labs/start
POST /api/labs/{id}/stop
POST /api/labs/stop
GET  /api/docker/status
POST /api/docker/start
POST /api/docker/stop
GET  /api/docker/containers
GET  /api/achievements/list
GET  /api/stats
GET/POST /api/versus/scenarios, /start, /move, /status, /stop
POST /api/scan
GET  /api/scan/rules
GET  /api/modes
POST /api/modes/set
GET  /api/profile
POST /api/profile/update
GET  /api/behavior-profile
GET  /api/daily
POST /api/daily/submit
POST /api/knowledge/reindex          <-- NEW (alpha readiness)
GET  /api/learning/weak-topics
GET  /api/learning/similar-errors
GET  /api/learning/events
GET  /api/skills
GET  /api/shop
POST /api/shop/purchase
GET  /api/heatmap
GET  /api/history
GET  /api/history/eras
POST /api/history/study
GET  /api/history/progress
GET  /api/config
GET  /api/writeups
GET  /api/writeups/{name}
POST /api/provider/set
POST /api/provider/key
GET  /api/providers
GET  /api/provider/lmstudio/check
POST /api/provider/set_url
POST /api/features/toggle
POST /api/settings/lang
GET  /api/context/budget
POST /api/context/budget
GET  /api/context/history
GET  /api/tracks
POST /api/tracks/start
POST /api/tracks/progress
GET  /api/ctf/status
POST /api/ctf/flag
GET  /api/missions
POST /api/missions/start
POST /api/missions/submit
GET  /api/threats
GET  /api/cve/{id}
GET  /api/shodan
GET  /api/shodan/host
GET  /api/censys
GET  /api/htb/machines
GET  /api/htb/machine/{id}
GET  /api/htb/status
GET  /api/thm/rooms
GET  /api/thm/room/{id}
GET  /api/thm/status
GET  /api/news
POST /api/scanv2
POST /api/malware
GET  /api/scorm/courses
POST /api/scorm/export
POST /api/auth/register
POST /api/auth/login
GET  /api/auth/verify
GET  /api/users
POST /api/users/role
GET  /api/report
POST /api/feedback
POST /api/courses/create
POST /api/courses/update
POST /api/courses/delete
POST /api/courses/topic
GET  /api/gdpr/export
POST /api/gdpr/import
GET  /api/personality
GET  /api/context
GET  /api/world
GET  /api/episodes
GET  /api/cyberpsychosis
GET  /api/social/scenarios
GET  /api/phishing/templates
POST /api/phishing/generate
POST /api/sandbox/run
GET  /api/network/status
GET  /api/noise
GET  /api/trace
GET  /api/debts
POST /api/stealth/toggle
POST /api/knowledge/reindex
GET  /api/targets
GET  /api/targets/{id}/status
GET  /api/mood
POST /api/mood/set
GET  /api/emotions
POST /api/summary
GET  /api/dockergen/images
POST /api/dockergen/generate
GET  /api/equipment
POST /api/equipment/toggle
GET  /api/timeloop
POST /api/timeloop/start
POST /api/timeloop/choice
GET  /api/sync/id
GET  /api/sync/export
GET  /api/exploit/challenges
GET  /api/analytics
GET  /api/mermaid/generate
GET  /api/bounty/scenarios
GET  /api/media
GET  /api/walkthroughs
POST /api/save
GET  /api/ws/stats

## Routes modules (routes/)
risk.py:      /api/noise, /api/stealth/toggle, /api/trace, /api/debts,
              /api/logs, /api/logs/wipe, /api/watchers, /api/watchers/trigger
story.py:     /api/story, /api/story/start, /api/story/submit, /api/chapters,
              /api/chapter/start, /api/story/final
phantom.py:   /api/secret, /api/secret/enter
rewind.py:    /api/rewind, /api/rewind (POST)
faction.py:   faction routes

## PWA static API path map (static/js/utils.js API_PATH_MAP)
Maps frontend shorthand -> /api/* endpoints (e.g. /get_progress -> /api/progress,
/get_story_episodes -> /api/story, /start_story_episode -> /api/story/start,
/submit_flag -> /api/ctf/flag, /save -> /api/save)
