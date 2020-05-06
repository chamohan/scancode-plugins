FROM python:3.6

RUN pip install scancode-toolkit && mkdir scancode-toolkit
WORKDIR scancode-toolkit

RUN scancode --help 

ENV PATH=$HOME/scancode-toolkit:$PATH
ADD ./amd-plugin.sh /scancode-toolkit/
RUN chmod +x /scancode-toolkit/amd-plugin.sh;
RUN cd /scancode-toolkit
RUN bash -c "/scancode-toolkit/amd-plugin.sh"

CMD scancode  -clpeui  --package --processes `expr $(nproc --all) - 1` --classify --keywordsscan --verbose --full-root --json-pp /artifacts/$(date "+%Y.%m.%d-%H.%M.%S")-licenses.json /src --license-policy scancode-plugins/amd_licence_policy.yml --summary --summary-with-details --license-text --license-text-diagnostics --is-license-text  --license-diag  --no-licenses  --licence-modifications --custom-output /artifacts/$(date "+%Y.%m.%d-%H.%M.%S")-license-modification-report.html --custom-template scancode-plugins/license-modification-template.html >>/logs/$(date "+%Y.%m.%d-%H.%M.%S")-logfile 2>&1

