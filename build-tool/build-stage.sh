# !/bin/bash
export APP_HOME="$(cd "`dirname "$0"`"/..; pwd)"

. "${APP_HOME}/etc/build.conf"


function usage ()
{
    echo "[Installation]
    Usage: `basename $0` [OPTIONS] ENV (dev|ut|prod)
     e.g. `basename $0` -p dev
    OPTIONS:
       -h|--help                             Show this message
       -a|--all                              Install all
       -b|--build                            Install Python
       -c|--clean                            Clean last build result
    "
}

args=`getopt -o habc --long all,build,clean,help \
     -n 'build-stage' -- "$@"`

if [ $? != 0 ] ; then
  echo "terminating..." >&2 ;
  exit 1 ;
fi
eval set -- "$args"


while true ; do
  case "$1" in
    -a|--all)
        ALL_OPT="true" 
        shift
        ;;
    -b|--build )
        BUILD_OPT="true" 
        shift
        ;;
    -c|--clean )
        CLEAN_OPT="true"
        shift
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
if [[ -z ${ENV} ]] || [[ ! -d ${APP_HOME}/etc/${ENV} ]] ; then
  echo "$(basename $0): missing ENV : ${ENV}"
  usage
  exit 1
fi

function build_py_project ()
{
    cd "${APP_HOME}"
    echo "[info] mkdir $BUILD_RUNTIME_DIR"
    mkdir -p $BUILD_RUNTIME_DIR
    mkdir -p $BUILD_RUNTIME_DIR/etc
    # src
    rsync -az etc/${ENV}/* $BUILD_RUNTIME_DIR/etc
    
    rsync -az build-tool bin lib src README.md VERSION requirements.txt example $BUILD_RUNTIME_DIR
    cd "${APP_HOME}"
}

function clean ()
{
    if [ -d "$APP_HOME/$BUILD_DIR" ]; then
        echo "[CLEAN]Clean root project $APP_NAME, delete dir $APP_HOME/$BUILD_DIR"
        rm -rf "$APP_HOME/$BUILD_DIR"
    fi
}



# call function
if [[ -n $ALL_OPT ]]; then
    build_py_project
fi

if [[ -n $BUILD_OPT ]]; then
    build_py_project
fi

if [[ -n $CLEAN_OPT ]]; then
    clean
fi