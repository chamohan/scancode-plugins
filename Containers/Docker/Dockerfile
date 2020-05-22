FROM python:3.6

RUN pip install scancode-toolkit

ADD ./Containers/Docker/amd-scancode /amd-scancode
ADD ./Containers/Docker/plugins /plugins

WORKDIR /amd-scancode

# RUN Loop through all whl files in the directory and run pip install
RUN for files in /plugins/*.whl; do pip install ${files}; done

ENTRYPOINT ["/bin/bash", "/amd-scancode/scansourcecode.sh"]
