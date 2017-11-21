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

export PYTHONPATH=${PYTHONPATH}:${PROJECT_HOME}/hippo/lib
export PYTHONPATH=${PYTHONPATH}:${PROJECT_HOME}/hippo/app
source $PY_VENV/bin/activate
