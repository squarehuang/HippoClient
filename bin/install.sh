# !/bin/bash

export APP_HOME="$(cd "`dirname "$0"`"/..; pwd)"
requirments_file="${APP_HOME}"/requirements.txt
. "${APP_HOME}/etc/env.conf"
. "${APP_HOME}/bin/runtime-env-info.sh"



function install_virtualenv()
{
    py_venv=$1
    echo "[info] mkdir $py_venv"
    mkdir -p $py_venv
    echo "[info] install virtualenv"
    pip install virtualenv
    echo "[info] create python2.7 venv"
    virtualenv -p python2.7 $py_venv
    echo "[info] install pip2.7 setuptools in venv"
    $py_venv/bin/pip install --upgrade pip setuptools ${PROXY}
    echo "[info] install requirments in venv"
    $py_venv/bin/pip install -r $requirments_file ${PROXY}
}

function install_cli_env()
{   
    install_virtualenv ${PY_VENV}
}

function install_template_env()
{   
    # install python env to plugin-templates/basic
    template_pyvenv="${APP_HOME}"/plugin-templates/basic/venv
    requirments_file="${APP_HOME}"/plugin-templates/basic/etc/requirements.txt
    install_virtualenv $template_pyvenv
    # copy lib folder to plugin-templates
    echo "[info] copy lib folder ${APP_HOME}/lib/* to ${APP_HOME}/plugin-templates/basic/lib"
    rsync -az "${APP_HOME}"/lib/* "${APP_HOME}"/plugin-templates/basic/lib
}

function export_variable()
{
    if [[ ${ENV} == "dev" ]]; then
        sudo ln -sf ${APP_HOME}/cli/hippo /usr/local/bin/hippo
    fi
}
function usage ()
{
    echo "[Installation]
    Usage: `basename $0` [OPTIONS] 
    OPTIONS:
       -h|--help                             Show this message
       -a|--all                              Install all
       -c|--install-cli-env                  Install Python Env for cli
       -t|--install-template-env             Install Python Env for template
       -v|--export-var                       Set up variable
       
       
    "
}

args=`getopt -o havect --long export-var,all,install-cli-env,install-template-env,help \
     -n 'build' -- "$@"`

if [ $? != 0 ] ; then
  echo "terminating..." >&2 ;
  exit 1 ;
fi
eval set -- "$args"



while true ; do
  case "$1" in
    -a|--all)
         shift
         install_cli_env
         install_template_env
         export_variable
         ;;
    -c|--install-cli-env)
         shift
         install_cli_env
          ;;
    -t|--install-template-env)
         shift
         install_template_env
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
        usage
        break
        ;;
    *)
        echo "internal error!" ;
        exit 1
        ;;
  esac
done