# !/bin/bash
if [[ -z "${APP_HOME}" ]]; then
    export APP_HOME="$(cd "`dirname "$0"`"/..; pwd)"
fi

function build_py_project ()
{
    cd "${APP_HOME}"
    echo "[info] mkdir $BUILD_RUNTIME_DIR"
    mkdir -p $BUILD_RUNTIME_DIR
    mkdir -p $BUILD_RUNTIME_DIR/etc
    # src
    echo "[info] copy etc/${ENV} to $BUILD_RUNTIME_DIR/etc"
    rsync -az etc/${ENV}/* $BUILD_RUNTIME_DIR/etc

    echo "[info] copy bin lib src README.md VERSION requirements.txt example to $BUILD_RUNTIME_DIR"
    rsync -az bin lib src README.md VERSION requirements.txt example $BUILD_RUNTIME_DIR
}

function clean ()
{
    if [ -d "$APP_HOME/$BUILD_DIR" ]; then
        echo "[info] clean root project $APP_NAME, delete dir $APP_HOME/$BUILD_DIR"
        rm -rf "$APP_HOME/$BUILD_DIR"
    fi
}



