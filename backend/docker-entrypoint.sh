#!/bin/sh
set -eu

mkdir -p /app/data /app/codex-home
# Keep host-side credentials in auth.json, while the application owns the
# permission profile required by every App Server process.
cp /app/codex-config.toml /app/codex-home/config.toml
chmod 600 /app/codex-home/config.toml
chown -R app:app /app/data /app/codex-home
exec setpriv --reuid=10001 --regid=10001 --init-groups "$@"
