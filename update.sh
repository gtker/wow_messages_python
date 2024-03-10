#!/usr/bin/env bash
set -e

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

if ! command -v git &> /dev/null
then
    echo "Unable to find 'git' command."
    exit 1
fi

if ! command -v /usr/local/bin/jtd-validate &> /dev/null
then
    echo "Unable to find 'jtd-validate' command."
    exit 1
fi

if ! command -v /usr/local/bin/jtd-codegen &> /dev/null
then
    echo "Unable to find 'jtd-codegen' command."
    exit 1
fi

echo "Running as $(whoami)"

cd ${SCRIPT_DIR}
git fetch && git reset --hard origin/main

git submodule update --init --recursive

cd ${SCRIPT_DIR}/generator/wow_messages
git fetch && git reset --hard origin/main

${SCRIPT_DIR}/generator/generate.sh

if [[ $(git status --porcelain | grep -v generator/wow_messages | wc -l) -ne "0" ]]; then
    DIFF="$(git diff --stat HEAD)"
    git diff --stat HEAD

    git commit --all --message "Auto update wow_messages version"
    git push

    /usr/local/bin/send-email "wow_messages_python auto updated" "The wow_messages_python repo has been updated.\n\n${DIFF}"
fi

