---
name: deploy
description: Deploy Rmzn Tutor to production (rmzn.net) after the owner approved it, and open an SSH tunnel to the production Piston for local checking/verification. Use for «выкатывай», «задеплой», «обнови прод», or when Verify.java / local checks need Piston.
---

# Deploy to rmzn.net

Only after the owner said so («выкатывай», «делай и выкатывай»). The frontend is built into the backend image (Dockerfile),
so every deploy = rebuild the `backend` service.

1. Locally: full backend suite and frontend build must pass.
   ```sh
   cd backend && export JAVA_HOME=/Users/ramzankibiev/Library/Java/JavaVirtualMachines/corretto-21.0.5/Contents/Home && mvn -q -o test
   cd ../frontend && npm run build
   ```
2. Commit (message ends with the Co-Authored-By line) and `git push origin master`.
3. If the change adds a Flyway migration or otherwise writes production data, back up the database first:
   ```sh
   ssh root@rmzn.net 'D=/var/lib/docker/volumes/adaptive-course_adaptive-data/_data/adaptive-tutor.db
   B=/root/adaptive-course-backups/adaptive-tutor-$(date -u +%Y%m%d-%H%M%S)-pre-<what>.db
   python3 -c "import sqlite3,sys; s=sqlite3.connect(sys.argv[1]); d=sqlite3.connect(sys.argv[2]); s.backup(d); d.close(); print(\"backup ok\", sys.argv[2])" $D $B'
   ```
4. Build first (the old container keeps serving), then swap — the restart takes ~5 s:
   ```sh
   ssh root@rmzn.net 'set -e; cd /root/adaptive-course && git pull -q --ff-only && git log --oneline -1
   docker compose build backend 2>&1 | tail -1
   docker compose up -d --no-deps --no-build backend 2>&1 | tail -1
   for k in $(seq 1 40); do docker compose logs --since 2m backend 2>&1 | grep -q "Started .* in " && break; sleep 3; done
   docker compose logs --since 2m backend 2>&1 | grep -E "Migrating schema|Started .* in |ERROR|Exception" | head'
   ```
   Students may be in a lesson; the owner normally wants the deploy right away. If unsure, check open lessons
   (`select count(*) from lessons where finished_at is null`, read-only) and say how many will see a short blip.
5. Report: commit hash, migration applied (if any), backup path, «errors: 0» from the logs.

Never touch the other services on the VPS (adlantgbot, bjj-sync-db, remnanode, openclaw, caddy-selfsteal); never
`docker compose down`; `--no-deps` keeps Piston running.

## Tunnel to the production Piston (for Verify.java or a local backend)
```sh
ssh root@rmzn.net 'docker inspect adaptive-course-piston-1 --format "{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}"'   # usually 172.20.0.2
# keep it open in the background (the connection sometimes drops):
while true; do ssh -o ConnectTimeout=15 -o ServerAliveInterval=15 -o ExitOnForwardFailure=yes -N -L 2779:172.20.0.2:2000 root@rmzn.net; sleep 1; done
curl -s http://127.0.0.1:2779/api/v2/runtimes   # java 15.0.2, python 3.12.0
```
Stop the tunnel when done.
