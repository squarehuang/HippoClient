# !/usr/bin/env bash

export APP_HOME="$(cd "`dirname "$0"`"/..; pwd)"
requirments_file="${APP_HOME}"/etc/requirements.txt
. "${APP_HOME}/etc/env.conf"



function env_install ()
{
    echo "[info] mkdir $PY_VENV"
    mkdir -p $PY_VENV
    echo "[info] create python2.7 venv"
    virtualenv -p python2.7 $PY_VENV
    echo "[info] install pip2.7 setuptools in venv"
    $PY_VENV/bin/pip install --upgrade pip setuptools
    echo "[info] install requirments in venv"
    $PY_VENV/bin/pip install -r $requirments_file

}

function export_variable()
{
    os=$(uname -s)
    sudo ln -sf ${APP_HOME}/cli/hippo /usr/local/bin/hippo
}
function usage ()
{
    echo "[build-service]
    Usage: `basename $0` [OPTIONS] 
    OPTIONS:
       -h|--help                             Show this message
       -a|--all                              Install all
       -e|--env-install                      Install Python Env
       -v|--export-var                       Set up variable
    "
}

args=`getopt -o have --long env-install,export-var,all,help \
     -n 'build' -- "$@"`

if [ $? != 0 ] ; then
  echo "terminating..." >&2 ;
  exit 1 ;
fi
eval set -- "$args"



while true ; do
  case "$1" in
    -i|--all)
         shift
         env_install
         export_variable
         ;;
    -e|--env-install)
         shift
         env_install
          ;;
    -v|--export_variable)
         shift
         export_variable
          ;;
    -h|--help )
        usage
        exit
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
