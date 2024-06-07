#!/bin/bash
set -e

host="$1"
port="$2"
shift 2
cmd="$@"

until pg_isready -h localhost -p 5433; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"
exec $cmd
