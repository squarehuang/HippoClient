#!/usr/bin/env bash

if [ -z "${PROJECT_HOME}" ]; then
  export PROJECT_HOME="$(cd "`dirname "$0"`"/../..; pwd)"
fi


if [ -z "$HIPPO_DIR" ]; then
  export HIPPO_DIR="${PROJECT_HOME}/hippo"
fi

if [ -z "$HIPPO_LOG_DIR" ]; then
  export HIPPO_LOG_DIR="${HIPPO_DIR}/var/logs"
fi

if [ -z "$HIPPO_PID_DIR" ]; then
    export HIPPO_PID_DIR="${HIPPO_DIR}/var/run"
fi

if [ -z "$APP_IDENT_STRING" ]; then
  export APP_IDENT_STRING="$USER"
fi

usage="Usage: daemon.sh  (start) "

# get log directory

mkdir -p "$HIPPO_LOG_DIR"
touch "$HIPPO_LOG_DIR"/.app_test > /dev/null 2>&1
TEST_LOG_DIR=$?
if [ "${TEST_LOG_DIR}" = "0" ]; then
  rm -f "$HIPPO_LOG_DIR"/.app_test
else
  chown "$APP_IDENT_STRING" "$HIPPO_LOG_DIR"
fi

rotate_log ()
{
    log=$1;
    num=5;
    if [ -n "$2" ]; then
	     num=$2
    fi
    if [ -f "$log" ]; then # rotate logs
  	  while [ $num -gt 1 ]; do
  	      prev=`expr $num - 1`
  	      [ -f "$log.$prev" ] && mv "$log.$prev" "$log.$num"
  	      num=$prev
  	  done
      mv "$log" "$log.$num";
    fi
}

service_type=$1
shift
option=$1
shift
instance=$1
shift
command=$@

log="$HIPPO_LOG_DIR/$APP_IDENT_STRING-$service_type-$instance.out"
pid="$HIPPO_PID_DIR/$APP_IDENT_STRING-$service_type-$instance.pid"

run_command() {
  mkdir -p "$HIPPO_PID_DIR"

  # check exists process
  if [ -f "$pid" ]; then
    TARGET_ID="$(cat "$pid")"
    if kill -0 $TARGET_ID > /dev/null 2>&1; then
      echo "$command running as process $TARGET_ID.  Stop it first."
      exit 2
    fi
  fi

  rotate_log "$log"
  #echo "starting $PROJECT_NAME, logging to $log"

  $command >> $log 2>&1 &
  #$command > /dev/null 2>&1 &
  newpid="$!"

  echo "$newpid" > "$pid"
  sleep 2
  # Check if the process has died; in that case we'll tail the log so the user can see
  TARGET_ID="$(cat "$pid")"
  if ! kill -0 $TARGET_ID > /dev/null 2>&1; then
    echo "failed to launch $command:"
    tail -2 "$log" | sed 's/^/  /'
    echo "full log in $log"
    exit 1
  fi
  echo $service_type pid : $TARGET_ID
}

stop() {
  if [ -f $pid ]; then
    TARGET_ID="$(cat "$pid")"
    # 檢查PID是否存在於PIDFILE中
    if [ -z $TARGET_ID ]; then
      echo "PIDFILE $pid is empty !"
      ## TODO
      rm -f "$pid"
      exit 1
    fi
     # 檢查該進程是否存在
    if kill -0 $TARGET_ID > /dev/null 2>&1; then
      kill -9 "$TARGET_ID" && rm -f "$pid"
      echo "Stopping $service_type successfully , whose pid is $TARGET_ID"
    else
      rm -f "$pid"
      echo "no $service_type to stop"
      echo "Delete file $pid"

    fi
  else
    echo "no $service_type to stop"
    echo "File $pid does NOT exist!"
    exit 2
  fi
}

restart() {
  stop
  start
}

status() {
  if [ -f $pid ]; then
    TARGET_ID="$(cat "$pid")"
    # 檢查PID是否存在於PIDFILE中
    if [ -z $TARGET_ID ]; then
      echo "$service_type No effective pid but pidfile exists!"
      exit 1
    fi
     # 檢查pid對應的進程是否還存在
    if [ -z "`ps aux | grep $TARGET_ID | grep -v grep`" ]; then
      echo "$service_type Process dead but pidfile exist"
      exit 1
    else
      echo "$service_type is running : $TARGET_ID "
    fi
  else
    echo "$service_type not running"
    exit 1
  fi
}
case $option in
    start)
      run_command
      ;;
    stop)
      stop
      ;;
    restart)
      restart
      ;;
    status)
      status
      ;;
  (*)
    $usage
    exit 1
    ;;

esac
