#!/usr/bin/env bash
export PWD=`pwd`
mkdir -p ${PWD}/Containers/Docker/plugins
pluginDir="${PWD}/Containers/Docker/plugins"


for d in ${PWD}/Containers/Docker/amd-scancode/scancode-*/;do
      cd "${d}";/bin/bash -c "(python3 setup.py bdist_wheel)"
      sleep 2
      cp -R ${d}/dist/* ${pluginDir}
done
