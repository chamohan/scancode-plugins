export SCANCODE=`which scancode`
export PYTHON=`which python`

type -P python3 >/dev/null 2>&1 && echo Python 3 is installed


${SCANCODE}  -clpeui  --package --processes `expr $(nproc --all) - 1` --classify --keywordsscan --verbose --full-root --json-pp /artifacts/$(date "+%Y.%m.%d-%H.%M.%S")-licenses.json /src --license-policy /amd-scancode/amd_licence_policy.yml --summary --summary-with-details --license-text --license-text-diagnostics --is-license-text  --license-diag  --no-licenses  --licence-modifications --custom-output /artifacts/$(date "+%Y.%m.%d-%H.%M.%S")-license-modification-report.html --custom-template /amd-scancode/license-modification-template.html >>/logs/$(date "+%Y.%m.%d-%H.%M.%S")-logfile 2>&1

# running analysis

${PYTHON} /amd-scancode/scancodestatus.py >/statistics/$(date "+%Y.%m.%d-%H.%M.%S")-logfile 2>&1
