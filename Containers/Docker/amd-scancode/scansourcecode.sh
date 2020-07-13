#!/usr/bin/env bash
#For any issue please write to chamohan@amd.com

export SCANCODE=`which scancode`
export PYTHON=`which python`
export SOURCECODE='src'
export LOGS='logs'
export OUT='out'
export ARTIFACTS='artifacts'
export LICENSEPOLICY='/amd-scancode/amd_licence_policy.yml'
export LICENSETEMPLATE='/amd-scancode/license-modification-template.html'
export STATUSSCRIPT='/amd-scancode/scancodestatuscheck.py'
export KEYWORDSFILE='/amd-scancode/keywordsdata.yml'
export STATISTICS='statistics'

trap cleanup 3 6 15

function cleanup {

  echo "Caught Signal ... cleaning up." >>${LOGS}/$(date "+%Y.%m.%d-%H.%M.%S")-cleanup
  echo "Done cleanup ... quitting. process id $$ " >>${LOGS}/$(date "+%Y.%m.%d-%H.%M.%S")-cleanup
  exit 1
}


${SCANCODE}  -clpeui  --package --processes `expr $(nproc --all) - 1` --classify --keyword-scan ${KEYWORDSFILE} --verbose --full-root --json-pp /${STATISTICS}/$(date "+%Y.%m.%d-%H.%M.%S")-licenses.json /${SOURCECODE} --license-policy ${LICENSEPOLICY} --summary --summary-with-details --license-text --license-text-diagnostics --is-license-text  --license-diag  --no-licenses --licence-modifications >>/${LOGS}/$(date "+%Y.%m.%d-%H.%M.%S")-logfile 2>&1

# running analysis

${PYTHON} ${STATUSSCRIPT} --dirpath=/${STATISTICS} --jsonfilepath=/${ARTIFACTS}>>/${OUT}/$(date "+%Y.%m.%d-%H.%M.%S")-logfile 2>&1
