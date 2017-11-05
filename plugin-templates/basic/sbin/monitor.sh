#!/bin/bash


export PROJECT_HOME="$(cd "`dirname "$0"`"/../..; pwd)"

PROJECT_NAME="$(basename ${PROJECT_HOME})"
HIPPO_DIR=${PROJECT_HOME}/hippo
HIPPO_BIN_DIR=${HIPPO_DIR}/bin
HIPPO_CONF_DIR=${HIPPO_DIR}/etc

. "${HIPPO_BIN_DIR}/utils.sh"

function usage ()
{
    echo "[monitor]
    Usage: `basename $0` -i <interval> SERVICE_NAME
    OPTIONS:
       -h|--help                          Show this message
       -i|--interval <interval>           Monitor interval seconds, (default: 5)
       -c|--coordAddress <coordAddress>   Coordinate Address
       -u|--user <user>                   User
       

    "
}

args=`getopt -o hi:c:u: --long interval:coordAddress:user:,help \
     -n 'monitor' -- "$@"`

if [ $? != 0 ] ; then
  echo "terminating..." >&2 ;
  exit 1 ;
fi

eval set -- "$args"

while true; do
  case $1 in
    -i|--interval)
      INTERVAL=$2
      shift 2
      ;;
    -c|--coordAddress)
      COORD_ADDRESS=$2
      shift 2
      ;;
    -u|--user)
      USERNAME=$2
      shift 2
      ;;
    -h|--help)
      usage
      exit
      ;;
    --)
      shift;
      break
      ;;
  esac
done

for arg do
   SERVICE_NAME=$arg
done

# check for required args
if [[ -z $SERVICE_NAME ]] ; then
  echo "$(basename $0): missing SERVICE"
  usage
  exit 1
fi


if [[ -z $INTERVAL ]] ; then
  INTERVAL=5000
fi
log_info "INTERVAL is $INTERVAL"
log_info "coordAddress is $COORD_ADDRESS"
log_info "USERNAME is $USERNAME"

err_cnt=1
is_success=0

# convert to seconds
INTERVAL_SEC=$(($INTERVAL/1000))

while [[ True ]]; do
  sleep $INTERVAL_SEC
  # sleep $INTERVAL
  error_msg=''
  # start monitor
  status_retout=$(${HIPPO_BIN_DIR}/${SERVICE_NAME}/run-${SERVICE_NAME}.sh --status)
  status_retcode=$?
  if [[ $status_retcode -eq 1 ]]; then
   log_warn "restart service..."
   restart_retout=$(${HIPPO_BIN_DIR}/${SERVICE_NAME}/run-${SERVICE_NAME}.sh --restart)
   restart_retcode=$?
   log_warn "restart_retout : $restart_retout"
   log_warn "restart_retcode : $restart_retcode"


    if [[ $restart_retcode -eq 1 ]]; then
     is_success=0
     error_msg=$restart_retout
    else
     is_success=1
    fi

  else
    is_success=1
    # parse pid ,e.g. hippos.service.test1 is running : 8880
    service_pid=$(echo $status_retout | awk -F ":" '{print $2}' | awk 'gsub(/^[[:blank:]]+|[[:blank:]]+$/,"")')
    # get detailed service information
    #TODO
  fi

  # send message to kafka
  own_pid=$$
  path=$PROJECT_HOME
  exec_time=`date +%s`
  exec_timems=$((exec_time*1000+`date "+%N"`/1000000))

  # get client ip 
  client_ip=`ifconfig | sed -En 's/127.0.0.1//;s/.*inet (addr:)?(([0-9]*\.){3}[0-9]*).*/\2/p'`
  message="{\"clientIP\": \"$client_ip\",\"path\":\"$path\",\"service_name\":\"$SERVICE_NAME\",\"monitor_pid\":$own_pid,\"service_pid\":$service_pid,\"exec_time\":$exec_timems,\"is_success\":$is_success,\"error_msg\":\"$error_msg\",\"coordAddress\":\"$COORD_ADDRESS\",\"interval\":$INTERVAL,\"user\":\"$USERNAME\"}"
  producer_cmd="$KAFKA_PRODUCER --broker-list ${KAFKA_HOST} --topic ${HEALTH_TOPIC}"
  #echo ${message} "|" ${producer_cmd}

  log_info "${message} | ${producer_cmd}"
  send_msg_retout=$(echo ${message} | ${producer_cmd})

done
echo "Finished."
