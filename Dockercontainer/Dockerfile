FROM python:3.6

RUN pip install scancode-toolkit && mkdir scancode-toolkit
WORKDIR scancode-toolkit

RUN scancode --help 

ENV PATH=$HOME/scancode-toolkit:$PATH
ADD ./amd-plugin.sh /scancode-toolkit/
RUN git clone https://github.com/chamohan/scancode-plugins.git
RUN cd /scancode-toolkit
RUN chmod +x /scancode-toolkit/scancode-plugins/amd-plugin.sh;
RUN bash -c "/scancode-toolkit/scancode-plugins/amd-plugin.sh"
CMD ["/bin/bash", "/scancode-toolkit/scancode-plugins/scansourcecode.sh"]
