#!/usr/bin/env bash

export PROJECT_HOME="$(cd "`dirname "$0"`"/../../..; pwd)"

# project folder name 
PROJECT_NAME="$(basename ${PROJECT_HOME})"
# auto generate service name
SERVICE_NAME="recommender-evaluation"
HIPPO_DIR=${PROJECT_HOME}/hippo
HIPPO_BIN_DIR=${HIPPO_DIR}/bin
HIPPO_SBIN_DIR=${HIPPO_DIR}/sbin
HIPPO_CONF_DIR=${HIPPO_DIR}/etc
HIPPO_LOG_DIR=${HIPPO_DIR}/var/logs


. "${HIPPO_CONF_DIR}/env.conf"
. "${HIPPO_BIN_DIR}/runtime-env-info.sh"
. "${HIPPO_CONF_DIR}/${SERVICE_NAME}/${SERVICE_NAME}-env.conf"

while read assignment; do
  if [[ $assignment != *"#"* ]] ; then
    if [ ! -z "$assignment" -a "$assignment" != " " ]; then
      export "$assignment"
    fi
  fi
done < ${HIPPO_CONF_DIR}/env.conf

function start() {
  cmd=$EXECUTE_CMD
  sh ${HIPPO_SBIN_DIR}/daemon.sh ${SERVICE_NAME} start 1 $cmd
}

function stop() {
  sh ${HIPPO_SBIN_DIR}/daemon.sh ${SERVICE_NAME} stop 1
}

function status() {
  sh ${HIPPO_SBIN_DIR}/daemon.sh ${SERVICE_NAME} status 1
}

function restart() {
  stop ${SERVICE_NAME}
  start ${SERVICE_NAME}
}

function usage ()
{
    echo "[${SERVICE_NAME}]
    Usage: `basename $0` {arg}
    e.g. `basename $0` --start
    --start
    --stop
    --status
    --restart
    -h, --help
    "
}

if [ ! -n "$1" ];then
    usage
    exit 1
fi

case "$1" in
    --start)
      start
      ;;
    --stop)
      stop
      ;;
    --status)
      status
      ;;
    --restart)
      restart
      ;;
    -h | --help)
      usage
      exit
      ;;
    *)
      usage
      exit 1
      ;;
esac
