#!/bin/bash
set -e

cd ${SCRIPTS_DIR}
python3 setup.py

if [ "${1#-}" != "${1}" ] || [ -z "$(command -v "${1}")" ]; then
  set -- python3 "$@"
fi

exec "$@"