#/usr/bin/env bash
set -e

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

/usr/local/bin/jtd-validate ${SCRIPT_DIR}/wow_messages/intermediate_representation_schema.json ${SCRIPT_DIR}/wow_messages/intermediate_representation.json
/usr/local/bin/jtd-codegen --python-out ${SCRIPT_DIR} ${SCRIPT_DIR}/wow_messages/intermediate_representation_schema.json
mv ${SCRIPT_DIR}/__init__.py ${SCRIPT_DIR}/model.py

python3 ${SCRIPT_DIR}/main.py

