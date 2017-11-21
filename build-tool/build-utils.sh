#!/bin/bash
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


# os=$(uname -s)
# if [ $os == "Linux" ]; then
#     sed_command="sed -i"
# elif [ $os == "Darwin" ]; then
#     sed_command="sed -i ''"
# fi

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
# TODO serving | ml_pipeline | streaming 
function gen_template_path () {
    service_type=$1
    if [[ $service_type == "basic" ]]; then
        export template_path=${APP_HOME}/plugin-templates/basic
    fi
}

function install_plugin_func (){
  service_type=$1
  shift
  gen_template_path $service_type
  # TODO check permission
  # clone hippo folder to target project
  mkdir -p ${PROJECT_HOME}/hippo
  chmod -R 755 ${PROJECT_HOME}/hippo

  rsync -az --exclude 'service' ${template_path}/* ${PROJECT_HOME}/hippo/
  [[ -d "${PROJECT_HOME}/hippo" ]] ; cp_issuccess=$?
  chmod -R 755 ${PROJECT_HOME}/hippo
  if [[ $cp_issuccess -ne 0 ]] ; then
    log_info " Hippo Plugin install failed on $BUILD_SERVER:${PROJECT_HOME}"
    exit 1    
  else
    log_info " Hippo Plugin successfully installed on $BUILD_SERVER:${PROJECT_HOME}"
  fi

}

function uninstall_plugin_func (){
  [[ -d "${PROJECT_HOME}/hippo" ]] ; is_exists=$?
  if [[ $is_exists -eq 0 ]] ; then
    rm -r ${PROJECT_HOME}/hippo
    [[ -d "${PROJECT_HOME}/hippo" ]] ; is_exists2=$?
    if [[ $is_exists2 -ne 0 ]] ; then
      log_info " Hippo Plugin was successfully uninstalled from $BUILD_SERVER:${PROJECT_HOME}"
    fi

  fi
}

function check_exists_plugin_func (){
  [[ -d "${PROJECT_HOME}/hippo" ]] ; is_exists=$?
  if [[ $is_exists -ne 0 ]] ; then
     log_info " Hippo Plugin not exists on $BUILD_SERVER:$PROJECT_HOME"
     return 1
  else
     log_info " Hippo Plugin already installed on $BUILD_SERVER:$PROJECT_HOME"
     return 0
  fi
}

function create_service_func (){
    service_type=$1
    shift
    service_name=$1
    shift
    cmd=$1
    ENV_PATH="${PROJECT_HOME}/hippo/etc/env.conf"
    gen_template_path $service_type
    eval $(cat ${PROJECT_HOME}/hippo/etc/env.conf)
    ## read service_name
    if [[ $SERVICE_LIST =~ $service_name ]]; then
        log_warn "a Service name \"${service_name}\" is already existed, please type another one"
        exit 1
    elif [[ -z ${service_name} ]]; then
        exit 1
    fi

    [[ -d "${PROJECT_HOME}/hippo/bin/${service_name}" ]] ; is_bin_exists=$?
    if [[ $is_bin_exists -eq 0 ]] ; then
        rm -r ${PROJECT_HOME}/hippo/bin/${service_name}
    fi
    [[ -d "${PROJECT_HOME}/hippo/etc/${service_name}" ]] ; is_etc_exists=$?
    if [[ $is_etc_exists -eq 0 ]] ; then
        rm -r ${PROJECT_HOME}/hippo/etc/${service_name}
    fi
    # get SERVICE_LIST values from env.conf
    if [[ -z ${SERVICE_LIST} ]] ; then
      service_value="$service_name"
    else
      service_value="${SERVICE_LIST},${service_name}"
    fi
    grep -q "^SERVICE_LIST" "$ENV_PATH" && sed_command "s/^SERVICE_LIST.*/SERVICE_LIST=\\\"${service_value}\\\"/" "$ENV_PATH" || echo "SERVICE_LIST=\\\"${service_value}\\\"" >> $ENV_PATH
    # generate service folder and run shell
    # folder path and filename pattern  : hippo/bin/${service_name}/run-${service_name}.conf
    mkdir -p "${PROJECT_HOME}/hippo/bin/${service_name}"
    log_info "[BUILD] create folder : $BUILD_SERVER:${PROJECT_HOME}/hippo/bin/${service_name}"
    rsync -az "${template_path}/bin/service/run-template.sh" ${PROJECT_HOME}/hippo/bin/${service_name}/run-${service_name}.sh
    # add service name into run script
    sed_command "s/^SERVICE_NAME=.*/SERVICE_NAME=\\\"${service_name}\\\"/" "${PROJECT_HOME}/hippo/bin/${service_name}/run-${service_name}.sh"
    chmod 755 "${PROJECT_HOME}/hippo/bin/${service_name}/run-${service_name}.sh"

    # generate service folder and env file
    # folder path and filename pattern  : hippo/etc/${service_name}/${service_name}-env.conf
    mkdir -p "${PROJECT_HOME}/hippo/etc/${service_name}"
    log_info "[BUILD] create folder : $BUILD_SERVER:${PROJECT_HOME}/hippo/etc/${service_name}"
    rsync -az "${template_path}/etc/service/template-env.conf" ${PROJECT_HOME}/hippo/etc/${service_name}/${service_name}-env.conf
    
    chmod 755 "${PROJECT_HOME}/hippo/etc/${service_name}/${service_name}-env.conf"

    if [[ -n $cmd ]] ; then
      log_info "[BUILD] add EXECUTE_CMD=\"${cmd}\" to ${PROJECT_HOME}/hippo/etc/${service_name}/${service_name}-env.conf"
      sed_command "/^EXECUTE_CMD/d" "${PROJECT_HOME}/hippo/etc/${service_name}/${service_name}-env.conf"
      # '' avoid ${PROJECT_HOME} convert to real value, \\\" for print EXECUTE_CMD=""
      echo "EXECUTE_CMD=\"${cmd}\"" >> "${PROJECT_HOME}/hippo/etc/${service_name}/${service_name}-env.conf"
    fi
    log_info "[BUILD] Service Name : ${service_name}"
    log_info "[BUILD] show ${PROJECT_HOME}/hippo/etc/${service_name}/${service_name}-env.conf"
    log_info "[BUILD] ================${service_name}-env.conf Header ====================="
    cat "${PROJECT_HOME}/hippo/etc/${service_name}/${service_name}-env.conf"
    log_info "[BUILD] ================${service_name}-env.conf Footer ====================="

}

function delete_service_func() {
    service_name=$1
    ENV_PATH="${PROJECT_HOME}/hippo/etc/env.conf"

    [[ -d "${PROJECT_HOME}/hippo/bin/${service_name}" ]] ; is_bin_exists=$?
    [[ -d "${PROJECT_HOME}/hippo/etc/${service_name}" ]] ; is_etc_exists=$?

    if [[ is_bin_exists -ne 0 ]] && [[ is_etc_exists -ne 0 ]]; then
        log_warn "Service name \"${service_name}\" is not existed"
        yn=""
    else
      # delete service_name folder and modify env.conf
        rm -r ${PROJECT_HOME}/hippo/bin/${service_name}
        rm -r ${PROJECT_HOME}/hippo/etc/${service_name}

        sed_command "s/\"${service_name},/\"/g" "$ENV_PATH"
        sed_command "s/,${service_name},/,/g" "$ENV_PATH"
        sed_command "s/,${service_name}\"/\"/g" "$ENV_PATH"
        log_info "[DELETE] Service Name : ${service_name}"
    fi
}
function list_services_func() {
    ENV_PATH="${PROJECT_HOME}/hippo/etc/env.conf"
    eval $(cat ${PROJECT_HOME}/hippo/etc/env.conf)

    echo "PROJECT_HOME: "${PROJECT_HOME}
    printf "%-40s %-40s %-40s \n" PROJECT_NAME SERVICE_NAME

    for element in ${SERVICE_LIST//,/ } ; do
      printf '%-40s %-40s %-40s \n' ${PROJECT_NAME} ${element}
    done
}

function check_service_func() {
    service_name=$1


    ENV_PATH="${PROJECT_HOME}/hippo/etc/env.conf"
    eval $(cat ${PROJECT_HOME}/hippo/etc/env.conf)
    ## read service_name
    if [[ $SERVICE_LIST =~ $service_name ]]; then
         exit 0
    else
        log_warn "a Service name \"${service_name}\" not exists"
        exit 1
    fi

}
