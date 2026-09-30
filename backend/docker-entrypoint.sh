#!/bin/sh
set -eu

mkdir -p /app/data /app/codex-home
chown -R app:app /app/data /app/codex-home
exec setpriv --reuid=10001 --regid=10001 --init-groups "$@"
