#!/bin/sh
# wait-for-postgres.sh

set -e

host="$1"
shift
cmd="$@"

>&2 echo "Postgres is up - executing command"
exec $cmd