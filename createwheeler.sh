#!/usr/bin/env bash
export PWD=`pwd`
export MKDIR=`which mkdir`
export PYTHON3=`which python3`
export CP=`which cp`
export pluginDir="${PWD}/Containers/Docker/plugins"
export PIP=`which pip`
export BASH=`which bash`


trap cleanup 3 6 15

function cleanup {

  echo "Caught Signal ... cleaning up." >>${LOGS}/$(date "+%Y.%m.%d-%H.%M.%S")-cleanup
  echo "Done cleanup ... quitting. process id $$ " >>${LOGS}/$(date "+%Y.%m.%d-%H.%M.%S")-create-wheelercleanup
  exit 1
}

# Compile the plugin code into wheel package and copy them to installation directory of plugins
function buildPlugins {

    ${MKDIR} -p ${PWD}/Containers/Docker/plugins

    type -P python3 >/dev/null 2>&1 && echo Python 3 is installed

    if [ $? -eq 1 ];then
        echo "please install python3  or change the environment to python3"
        exit 1
    fi
    ${PIP} install wheel
    for dir in ${PWD}/plugins/scancode-*/;do
        cd "${dir}";${BASH} -c "(${PYTHON3} setup.py bdist_wheel)"
        #sleep 2
        ${CP} -R ${dir}/dist/* ${pluginDir}
    done
}

buildPlugins
