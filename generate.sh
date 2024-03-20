#!/usr/bin/env bash
set -e

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
GENERATOR_DIR="${SCRIPT_DIR}/generator"

jtd-validate ${GENERATOR_DIR}/wow_messages/intermediate_representation_schema.json ${SCRIPT_DIR}/generator/wow_messages/intermediate_representation.json
jtd-codegen --python-out ${GENERATOR_DIR} ${GENERATOR_DIR}/wow_messages/intermediate_representation_schema.json
mv ${GENERATOR_DIR}/__init__.py ${GENERATOR_DIR}/model.py

mypy ${GENERATOR_DIR}

python3 ${GENERATOR_DIR}/main.py

