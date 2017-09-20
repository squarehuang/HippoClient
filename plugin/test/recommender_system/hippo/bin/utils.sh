
function log_info (){
    now=$(date +"%Y-%m-%d %H:%M:%S")
    echo "[$now] [INFO] $*"
}

function log_warn (){
    now=$(date +"%Y-%m-%d %H:%M:%S")
    echo "[$now] [WARN] $*"
}

function log_error (){
    now=$(date +"%Y-%m-%d %H:%M:%S")
    echo
    echo "[$now] [ERROR] $*"
    echo
    #exit 1
}
