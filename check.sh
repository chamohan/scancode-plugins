mkdir Containers/Docker/plugins
export PWD=`pwd`
for d in ${PWD}/Containers/Docker/amd-scancode/scancode-*/;do
      cd "${d}";/bin/bash -c "(python3 setup.py bdist_wheel)"
      sleep 2
      /usr/bin/cp -R ${d}/dist/* ${PWD}/Containers/Docker/plugins
done

ls -ltr ${PWD}/Containers/Docker/plugins/
