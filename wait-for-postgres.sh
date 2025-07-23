#!/bin/bash
set -e

host="$1"
shift
cmd="$@"

echo "Waiting for postgres at $host..."

until pg_isready -h "$host" -p 5432 > /dev/null 2>&1; do
  sleep 1
done

echo "Postgres is ready. Running command..."
exec $cmd
