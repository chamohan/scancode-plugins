#!/usr/bin/env bash
export PWD=`pwd`
export MKDIR=`which mkdir`
export PYTHON3=`which python3`
export CP=`which cp`
export pluginDir="${PWD}/Containers/Docker/plugins"
export PIP=`which pip`


function buildPlugins {

    ${MKDIR} -p ${PWD}/Containers/Docker/plugins

    type -P python3 >/dev/null 2>&1 && echo Python 3 is installed

    if [ $? -eq 1 ];then
        echo "python3 not installed or change the environment to python3"
        exit 1
    fi
    ${PIP} install wheel
    for d in ${PWD}/plugins/scancode-*/;do
        cd "${d}";/bin/bash -c "(python3 setup.py bdist_wheel)"
        sleep 2
        ${CP} -R ${d}/dist/* ${pluginDir}
    done
}


buildPlugins
