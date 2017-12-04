# !/bin/bash

export APP_HOME="$(cd "`dirname "$0"`"/..; pwd)"
requirments_file="${APP_HOME}"/etc/requirements.txt
. "${APP_HOME}/etc/env.conf"


function install_py()
{
    echo "[info] install pip rsync"
    os=$(uname -s)
    if [ $os == "Linux" ]; then
        if [ -f /etc/redhat-release ]; then
            sudo yum install epel-release
            sudo yum install python-pip
            sudo yum -y install rsync
        fi

        if [ -f /etc/lsb-release ]; then
            sudo apt-get install python-pip
            sudo apt-get install python-setuptools
        fi
    elif [ $os == "Darwin" ]; then
        echo ""
    fi
    pip install --upgrade pip setuptools wheel

}

function install_virtualenv()
{
    py_venv=${APP_HOME}/hippo/venv
    echo "[info] mkdir $py_venv"
    mkdir -p $py_venv
    echo "[info] install virtualenv"
    pip install virtualenv
    echo "[info] create python2.7 venv"
    virtualenv -p python2.7 $py_venv
    echo "[info] install pip2.7 setuptools in venv"
    $py_venv/bin/pip install --upgrade pip setuptools
    echo "[info] install requirments in venv"
    $py_venv/bin/pip install -r $requirments_file
}

function usage ()
{
    echo "[Installation]
    Usage: `basename $0` [OPTIONS] 
    OPTIONS:
       -h|--help                             Show this message
       -p|--install-py-env                   Install Python and Env
    "
}

args=`getopt -o hp --long install-py-env,help \
     -n 'build' -- "$@"`

if [ $? != 0 ] ; then
  echo "terminating..." >&2 ;
  exit 1 ;
fi
eval set -- "$args"



while true ; do
  case "$1" in
    -p|--install-py-env)
         shift
         install_py
         install_virtualenv
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
