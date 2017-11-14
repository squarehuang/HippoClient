#echo "this script is for runtime environment check "

# TODO
# what might be interested:
# network
# memory
# build path
# dependency
# whoami
# service version, like Impala, Hive, HBase....
# language version, like Python, JDK, R, Scala


export PYTHONPATH=${PYTHONPATH}:${APP_HOME}/cli/app

# Setting the python virtual ENV path
# source /Users/square_huang/ENV/bin/activate
source $PY_VENV/bin/activate
