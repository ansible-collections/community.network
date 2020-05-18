#!/usr/bin/env bash

set -o pipefail -eux

declare -a args
IFS='/:' read -ra args <<< "$1"

group="${args[1]}"

if [ "${BASE_BRANCH:-}" ]; then
    base_branch="origin/${BASE_BRANCH}"
else
    base_branch=""
fi

if [ "${group}" == "extra" ]; then
    # we need git checkout until 0.2.0 has been released; then we can install from galaxy
    git clone https://github.com/ansible-collections/community.internal_test_tools.git ../internal_test_tools

    ../internal_test_tools/tools/run.py --color
    exit
fi

case "${group}" in
    1) options=(--skip-test pylint --skip-test ansible-doc --skip-test validate-modules) ;;
    2) options=(                   --test      ansible-doc                             ) ;;
    3) options=(                                                --test validate-modules) ;;
    4) options=(--test pylint --exclude tests/unit/ --exclude plugins/module_utils/) ;;
    5) options=(--test pylint           tests/unit/           plugins/module_utils/) ;;
esac

# allow collection migration sanity tests for groups 3 and 4 to pass without updating this script during migration
network_path="lib/ansible/modules/network/"

if [ -d "${network_path}" ]; then
    if [ "${group}" -eq 3 ]; then
        options+=(--exclude "${network_path}")
    elif [ "${group}" -eq 4 ]; then
        options+=("${network_path}")
    fi
fi

# shellcheck disable=SC2086
ansible-test sanity --color -v --junit ${COVERAGE:+"$COVERAGE"} ${CHANGED:+"$CHANGED"} \
    --docker --base-branch "${base_branch}" \
    "${options[@]}" --allow-disabled
