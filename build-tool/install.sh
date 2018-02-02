# !/bin/bash

export APP_HOME="$(cd "`dirname "$0"`"/..; pwd)"
requirments_file="${APP_HOME}"/etc/requirements.txt


function install_py()
{
    echo "[info] install pip rsync"
    os=$(uname -s)
    if [ $os == "Linux" ]; then
        if [ ${ENV} == "dev" ]; then
            # redhat 
            if [ -f /etc/redhat-release ]; then
                sudo yum install epel-release
                sudo yum install python-pip
                sudo yum -y install rsync
            fi
            # centos 
            if [ -f /etc/lsb-release ]; then
                sudo apt-get install python-pip
                sudo apt-get install python-setuptools
            fi
        fi
    elif [ $os == "Darwin" ]; then
        echo ""
    fi

    pip install --upgrade pip setuptools wheel

}

function install_virtualenv()
{
    py_venv=$1
    echo "[info] mkdir $py_venv"
    mkdir -p $py_venv
    echo "[info] install virtualenv"
    pip install virtualenv
    echo "[info] create python2.7 venv"
    virtualenv -p python2.7 ${py_venv}
    echo "[info] install pip2.7 setuptools in venv"
    $py_venv/bin/pip install --upgrade pip setuptools ${PROXY}
    echo "[info] install requirments in venv"
    $py_venv/bin/pip install -r ${requirments_file} ${PROXY}
}

function install_cli_env()
{   
    
    . "${APP_HOME}/etc/env.conf"
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
    if [ ${ENV} == "dev" ]; then
        sudo ln -sf ${APP_HOME}/cli/hippo /usr/local/bin/hippo
    fi
    # export HIPPO_CLI_HOME=${APP_HOME}
    # export PATH=$PATH:${HIPPO_CLI_HOME}
    # echo ${HIPPO_CLI_HOME}
}
function usage ()
{
    echo "[Installation]
    Usage: `basename $0` [OPTIONS] ENV
     e.g. `basename $0` -p dev
    OPTIONS:
       -h|--help                             Show this message
       -a|--all                              Install all
       -p|--install-py                       Install Python
       -c|--install-cli-env                  Install Python Env for cli
       -t|--install-template-env             Install Python Env for template
       -v|--export-var                       Set up variable
       
       
    "
}

args=`getopt -o havepct --long export-var,all,install-py,install-cli-env,install-template-env,help \
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
         ALL_OPT="true" 
        #  install_cli_env
        #  install_template_env
        #  export_variable
         ;;
    -p|--install-py)
         INSTALL_PY_OPT="true" 
         shift
        #  install_py
          ;;
    -c|--install-cli-env)
         INSTALL_CLI_ENV_OPT="true" 
         shift
        #  install_cli_env
          ;;
    -t|--install-template-env)
         INSTALL_TEMPLATE_ENV_OPT="true" 
         shift
        #  install_template_env
          ;;
    -v|--export_variable)
         EXPORT_VARIABLE_OPT="true" 
         shift
        #  export_variable
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

for arg do
    ENV=$arg
done

# check for required args
if [[ -z ${ENV} ]] || [[ ! -f ${APP_HOME}/etc/${ENV}-env.conf ]] ; then
  echo "$(basename $0): missing ENV : ${ENV}"
  usage
  exit 1
fi

# read config

. "${APP_HOME}/etc/default.conf"
. "${APP_HOME}/etc/${ENV}-env.conf"


# call function
if [[ -n $ALL_OPT ]]; then
    install_cli_env
    install_template_env
    export_variable
fi

if [[ -n $INSTALL_PY_OPT ]]; then
    install_py
fi

if [[ -n $INSTALL_CLI_ENV_OPT ]]; then
    install_cli_env
fi

if [[ -n $INSTALL_TEMPLATE_ENV_OPT ]]; then
    install_template_env
fi

if [[ -n $EXPORT_VARIABLE_OPT ]]; then
    export_variable
fi