function log_info (){
    echo "[INFO]$*"
}

function log_warn (){
    echo "[WARN]$*"
}

function log_error (){
    echo
    echo "[ERROR]$*"
    echo
    exit 1
}


os=$(uname -s)
if [ $os == "Linux" ]; then
    ssh_cmd="ssh -q"
    sed_command="sed -i"
elif [ $os == "Darwin" ]; then
    ssh_cmd="ssh -q"
    sed_command="sed -i '' "
fi

function sed_command (){
    # sed command is different in Linux and MacOS, so we need this function
    os=$(uname -s)
    if [ $os == "Linux" ]; then
        sed -i $1 $2
    elif [ $os == "Darwin" ]; then
        sed -i '' $1 $2
    fi
}

function stat_permission (){
    # stat command is different in Linux and MacOS, so we need this function
    os=$(uname -s)
    if [ $os == "Linux" ]; then
        stat -c %a $1
    elif [ $os == "Darwin" ]; then
        stat -f %Lp $1
    fi
}


function install_plugin_func (){
  # TODO check permission
  # clone hippo folder to target project
  $ssh_cmd $BUILD_ACCOUNT@$BUILD_SERVER mkdir -p ${PROJECT_HOME}/hippo
  $ssh_cmd $BUILD_ACCOUNT@$BUILD_SERVER chmod -R 755 ${PROJECT_HOME}/hippo

  rsync -avz --exclude 'service' --exclude 'build-tool' ${HIPPO_HOME}/build-tool/.template/* $BUILD_ACCOUNT@$BUILD_SERVER:${PROJECT_HOME}/hippo/
  $ssh_cmd $BUILD_ACCOUNT@$BUILD_SERVER [[ -d "${PROJECT_HOME}/hippo" ]] ; cp_issuccess=$?
  $ssh_cmd $BUILD_ACCOUNT@$BUILD_SERVER chmod -R 755 ${PROJECT_HOME}/hippo
  if [[ $cp_issuccess -ne 0 ]] ; then
    log_info " Hippo Plugin install failed on $BUILD_SERVER:${PROJECT_HOME}"
    exit 1    
  else
    log_info " Hippo Plugin successfully installed on $BUILD_SERVER:${PROJECT_HOME}"
  fi

}

function uninstall_plugin_func (){
  $ssh_cmd $BUILD_ACCOUNT@$BUILD_SERVER [[ -d "${PROJECT_HOME}/hippo" ]] ; is_exists=$?
  if [[ $is_exists -eq 0 ]] ; then
    $ssh_cmd $BUILD_ACCOUNT@$BUILD_SERVER rm -r ${PROJECT_HOME}/hippo
    $ssh_cmd $BUILD_ACCOUNT@$BUILD_SERVER [[ -d "${PROJECT_HOME}/hippo" ]] ; is_exists2=$?
    if [[ $is_exists2 -ne 0 ]] ; then
      log_info " Hippo Plugin was successfully uninstalled from $BUILD_SERVER:${PROJECT_HOME}"
    fi

  fi
}

function check_exists_plugin_func (){
  $ssh_cmd $BUILD_ACCOUNT@$BUILD_SERVER [[ -d "${PROJECT_HOME}/hippo" ]] ; is_exists=$?
  if [[ $is_exists -ne 0 ]] ; then
     log_info " Hippo Plugin not exists on $BUILD_SERVER:$PROJECT_HOME"
     return 1
  else
     log_info " Hippo Plugin already installed on $BUILD_SERVER:$PROJECT_HOME"
     return 0
  fi
}

function create_service_func (){
    service_name=$1
    shift
    cmd=$1
    ENV_PATH="${PROJECT_HOME}/hippo/etc/env.conf"
    eval $($ssh_cmd $BUILD_ACCOUNT@$BUILD_SERVER cat ${PROJECT_HOME}/hippo/etc/env.conf)
    ## read service_name
    if [[ $SERVICE_LIST =~ $service_name ]]; then
        log_warn "a Service name \"${service_name}\" is already existed, please type another one"
        exit 1
    elif [[ -z ${service_name} ]]; then
        exit 1
    fi

    $ssh_cmd $BUILD_ACCOUNT@$BUILD_SERVER [[ -d "${PROJECT_HOME}/hippo/bin/${service_name}" ]] ; is_bin_exists=$?
    if [[ $is_bin_exists -eq 0 ]] ; then
        $ssh_cmd $BUILD_ACCOUNT@$BUILD_SERVER rm -r ${PROJECT_HOME}/hippo/bin/${service_name}
    fi

    $ssh_cmd $BUILD_ACCOUNT@$BUILD_SERVER [[ -d "${PROJECT_HOME}/hippo/etc/${service_name}" ]] ; is_etc_exists=$?
    if [[ $is_etc_exists -eq 0 ]] ; then
        $ssh_cmd $BUILD_ACCOUNT@$BUILD_SERVER rm -r ${PROJECT_HOME}/hippo/etc/${service_name}
    fi

    # get SERVICE_LIST values from env.conf
    if [ -z ${SERVICE_LIST} ]; then
      service_value="$service_name"
    else
      service_value="${SERVICE_LIST},${service_name}"
    fi

    # substitute service value
    $ssh_cmd $BUILD_ACCOUNT@$BUILD_SERVER "grep -q "^SERVICE_LIST" "$ENV_PATH" && $sed_command "s/^SERVICE_LIST.*/SERVICE_LIST=\\\"${service_value}\\\"/" "$ENV_PATH" || echo "SERVICE_LIST=\\\"${service_value}\\\"" >> $ENV_PATH"

    # generate service folder and run shell
    # folder path and filename pattern  : hippo/bin/${service_name}/run-${service_name}.conf
    $ssh_cmd $BUILD_ACCOUNT@$BUILD_SERVER mkdir -p "${PROJECT_HOME}/hippo/bin/${service_name}"
    log_info "[BUILD] create folder : $BUILD_SERVER:${PROJECT_HOME}/hippo/bin/${service_name}"
    rsync -az "${HIPPO_HOME}/build-tool/.template/bin/service/run-template.sh" $BUILD_ACCOUNT@$BUILD_SERVER:${PROJECT_HOME}/hippo/bin/${service_name}/run-${service_name}.sh
    # add service name into run script
    $ssh_cmd $BUILD_ACCOUNT@$BUILD_SERVER $sed_command "s/^SERVICE_NAME=.*/SERVICE_NAME=\\\"${service_name}\\\"/" "${PROJECT_HOME}/hippo/bin/${service_name}/run-${service_name}.sh"
    $ssh_cmd $BUILD_ACCOUNT@$BUILD_SERVER chmod 755 "${PROJECT_HOME}/hippo/bin/${service_name}/run-${service_name}.sh"


    # generate service folder and env file
    # folder path and filename pattern  : hippo/etc/${service_name}/${service_name}-env.conf
    $ssh_cmd $BUILD_ACCOUNT@$BUILD_SERVER mkdir -p "${PROJECT_HOME}/hippo/etc/${service_name}"
    log_info "[BUILD] create folder : $BUILD_SERVER:${PROJECT_HOME}/hippo/etc/${service_name}"
    rsync -az "${HIPPO_HOME}/build-tool/.template/etc/service/template-env.conf" $BUILD_ACCOUNT@$BUILD_SERVER:${PROJECT_HOME}/hippo/etc/${service_name}/${service_name}-env.conf
    $ssh_cmd $BUILD_ACCOUNT@$BUILD_SERVER chmod 755 "${PROJECT_HOME}/hippo/etc/${service_name}/${service_name}-env.conf"

    if [[ -n $cmd ]] ; then
      log_info "[BUILD] add EXECUTE_CMD=\"${cmd}\" to ${PROJECT_HOME}/hippo/etc/${service_name}/${service_name}-env.conf"
      $ssh_cmd $BUILD_ACCOUNT@$BUILD_SERVER $sed_command "/^EXECUTE_CMD/d" "${PROJECT_HOME}/hippo/etc/${service_name}/${service_name}-env.conf"
      $ssh_cmd $BUILD_ACCOUNT@$BUILD_SERVER echo "EXECUTE_CMD=\"${cmd}\"" >> "${PROJECT_HOME}/hippo/etc/${service_name}/${service_name}-env.conf"
    fi
    log_info "[BUILD] Service Name : ${service_name}"
}

function delete_service_func() {
    service_name=$1
    ENV_PATH="${PROJECT_HOME}/hippo/etc/env.conf"

    $ssh_cmd $BUILD_ACCOUNT@$BUILD_SERVER [[ -d "${PROJECT_HOME}/hippo/bin/${service_name}" ]] ; is_bin_exists=$?
    $ssh_cmd $BUILD_ACCOUNT@$BUILD_SERVER [[ -d "${PROJECT_HOME}/hippo/etc/${service_name}" ]] ; is_etc_exists=$?

    if [[ is_bin_exists -ne 0 ]] && [[ is_etc_exists -ne 0 ]]; then
        log_warn "Service name \"${service_name}\" is not existed"
        yn=""
    else
      # delete service_name folder and modify env.conf
        $ssh_cmd $BUILD_ACCOUNT@$BUILD_SERVER rm -r ${PROJECT_HOME}/hippo/bin/${service_name}
        $ssh_cmd $BUILD_ACCOUNT@$BUILD_SERVER rm -r ${PROJECT_HOME}/hippo/etc/${service_name}

        $ssh_cmd $BUILD_ACCOUNT@$BUILD_SERVER $sed_command "s/\"${service_name},/\"/g" "$ENV_PATH"
        $ssh_cmd $BUILD_ACCOUNT@$BUILD_SERVER $sed_command "s/,${service_name},/,/g" "$ENV_PATH"
        $ssh_cmd $BUILD_ACCOUNT@$BUILD_SERVER $sed_command "s/,${service_name}\"/\"/g" "$ENV_PATH"
        log_info "[DELETE] Service Name : ${service_name}"
    fi
}
function list_services_func() {
    ENV_PATH="${PROJECT_HOME}/hippo/etc/env.conf"
    eval $($ssh_cmd $BUILD_ACCOUNT@$BUILD_SERVER cat ${PROJECT_HOME}/hippo/etc/env.conf)

    echo "PROJECT_HOME: "${PROJECT_HOME}
    printf "%-40s %-40s %-40s \n" PROJECT_NAME SERVICE_NAME

    for element in ${SERVICE_LIST//,/ } ; do
      printf '%-40s %-40s %-40s \n' ${PROJECT_NAME} ${element}
    done
}

function check_service_func() {
    service_name=$1


    ENV_PATH="${PROJECT_HOME}/hippo/etc/env.conf"
    eval $($ssh_cmd $BUILD_ACCOUNT@$BUILD_SERVER cat ${PROJECT_HOME}/hippo/etc/env.conf)
    ## read service_name
    if [[ $SERVICE_LIST =~ $service_name ]]; then
         exit 0
    else
        log_warn "a Service name \"${service_name}\" not exists"
        exit 1
    fi

}
