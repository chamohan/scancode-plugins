FROM python:3.6

RUN pip install scancode

ADD ./amd-scancode /
ADD ./plugins /

WORKDIR /plugins

# RUN Loop through all whl files in the directory and run pip install

CMD ["/bin/bash", "/amd-scancode/scansourcecode.sh"]
