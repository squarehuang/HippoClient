#!/bin/bash
export APP_HOME="$(cd "`dirname "$0"`"/../..; pwd)"
SRC_DIR="${APP_HOME}/src"
CONF_DIR="${APP_HOME}/etc"


# include log manipulation script start
. "${APP_HOME}"/lib/log.sh
# include log manipulation script end

. "${CONF_DIR}"/env.conf
. "${SRC_DIR}"/plugin/plugin-utils.sh


example_path="$(cd "`dirname "$APP_HOME"`"/../..; pwd)"/test_project
function usage ()
{
    echo "[plugin-installer]
    Usage: `basename $0` [OPTIONS] PROJECT_HOME
    e.g. `basename $0` --install $example_path
    OPTIONS:
       -h|--help                             Show this message
       -i|--install                          Install Hippo Plugin to PROJECT_PATH
       -u|--uninstall                        Uninstall Hippo Plugin from PROJECT_PATH
       --check-install                       Check Plugin install on PROJECT_PATH
       -c|--create-service=SERVICE           Create a service
       -d|--delete-service=SERVICE           Delete a service
       -l|--list-services                    List services
       --check-service=SERVICE               Check service existed by SERVICE
       --cmd=\"CMD\"                         Command to run to service (py, jar, sh...) , you can use \"{PROJECT_HOME}\" variable (e.g. $example_path) to build command
    "
}
args=`getopt -o ilhuc:d: --long create-service:,delete-service:,check-service:,cmd:,list-services,install,uninstall,check-install,help \
     -n 'plugin-installer' -- "$@"`

if [ $? != 0 ] ; then
  echo "terminating..." >&2 ;
  exit 1 ;
fi
eval set -- "$args"



while true ; do
  case "$1" in
    -i|--install)
         IS_INSTALL="true"
         shift
          ;;
    -u|--uninstall)
         IS_UNINSTALL="true"
         shift
          ;;
    -l|--list-services)
         IS_LIST_SERVICES="true"
         shift
          ;;
    -c|--create-service)
         IS_CREATE_SERVICE="true"
         SERVICE_NAME="$2";
         shift 2
         if [[ -z $SERVICE_NAME ]] ; then
           echo "$(basename $0): missing SERVICE_NAME"
           usage
           exit 1
         fi
         ;;
    -d|--delete-service)
        IS_DELETE_SERVICE="true"
        SERVICE_NAME="$2";
        shift 2
        if [[ -z $SERVICE_NAME ]] ; then
          echo "$(basename $0): missing SERVICE_NAME"
          usage
          exit 1
        fi
        ;;
    -h|--help )
        usage
        exit
        ;;
    --check-install )
        IS_CHECK_INSTALL="true"
        shift
        ;;
    --check-service )
        IS_CHECK_SERVICE="true"
        SERVICE_NAME="$2";
        shift 2
        if [[ -z $SERVICE_NAME ]] ; then
          echo "$(basename $0): missing SERVICE_NAME"
          usage
          exit 1
        fi
        ;;
    --cmd)
        CMD=$2;
        shift 2
        if [[ $CMD =~ '{PROJECT_HOME}' ]] ; then
          # echo cmd: "$CMD"
          CMD=`echo $CMD | sed 's/{PROJECT_HOME}/\${PROJECT_HOME}/g'`
        fi
        # CMD=\"$CMD\"
        echo cmd: "$CMD"
        ;;
    --)
        shift ;
        break
        ;;
    *)
        echo "internal error!" ;
        exit 1
        ;;
  esac
done


for arg do
    PROJECT_HOME=$arg
done

# check for required args
if [[ -z $PROJECT_HOME ]] ; then
  echo "$(basename $0): missing PROJECT_HOME"
  usage
  exit 1
fi
export PROJECT_NAME="$(basename ${PROJECT_HOME})"

function check_installed(){
    check_exists_plugin_func
    RETVAL=$?
    return "$RETVAL"
}

function check_service(){
   check_installed
   retval_is_install=$?
    if [[ $retval_is_install == 1 ]] ; then
      RETVAL=1
      exit "$RETVAL"
    fi

  check_service_func $SERVICE_NAME
}

function install(){
    check_installed
    retval_is_install=$?
    if [[ $retval_is_install == 0 ]] ; then
      exit
    fi
    log_info "Install Plugin on $PROJECT_HOME"
    install_plugin_func "basic"
    log_info "Install Python VirtaulEnv for plugin"
    install_plugin_venv
}

function uninstall(){
    check_installed
    retval_is_install=$?
    if [[ $retval_is_install == 0 ]] ; then
      log_info " Uninstall Plugin on $PROJECT_HOME"
      uninstall_plugin_func
    fi


}

function create_service(){
    check_installed
    retval_is_install=$?
    if [[ $retval_is_install == 1 ]] ; then
      install
    fi

    if [[ -n $CMD ]] ; then
      create_service_func "basic" $SERVICE_NAME "$CMD"
    else
      create_service_func "basic" $SERVICE_NAME
    fi
}
function delete_service(){
  check_installed
  retval_is_install=$?
  if [[ $retval_is_install == 1 ]] ; then
    install
  fi
  delete_service_func $SERVICE_NAME
}
function list_services(){
  check_installed
  retval_is_install=$?
  if [[ $retval_is_install == 1 ]] ; then
    RETVAL=1
    exit "$RETVAL"
  fi

  list_services_func
}

# call function
if [[ -n $IS_CHECK_INSTALL ]]; then
  check_installed
  exit $RETVAL
fi

if [[ -n $IS_CHECK_SERVICE ]]; then
  check_service
  exit $RETVAL
fi


if [[ -n $IS_LIST_SERVICES ]]; then
  list_services
fi

if [[ -n $IS_INSTALL ]]; then
  install
fi

if [[ -n $IS_UNINSTALL ]]; then
  uninstall
  exit $RETVAL
fi

if [[ -n $IS_CREATE_SERVICE ]]; then
  create_service
fi

if [[ -n $IS_DELETE_SERVICE ]]; then
  delete_service
fi
