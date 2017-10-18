#!/usr/bin/env bash

PROJECT_NAME="recommender_system"

export PROJECT_HOME="$(cd "`dirname "$0"`"/..; pwd)"

BIN_DIR=$(dirname "$0")
SBIN_DIR=${PROJECT_HOME}/sbin
CONF_DIR=${PROJECT_HOME}/etc

. "${CONF_DIR}/${PROJECT_NAME}-env.conf"
. "${BIN_DIR}/runtime-env-info.sh"

python ${SBIN_DIR}/kafka_app.py &
echo $!
