FROM python:3.8

RUN apt update && \
    apt install -y build-essential git vim && \
    rm -rf /var/lib/apt/lists/*
RUN pip install ipython

ENV PRIWO_PATH=/software/priwo
RUN mkdir -p ${PRIWO_PATH}
WORKDIR ${PRIWO_PATH}
COPY . ${PRIWO_PATH}
RUN python -m pip install -e .

RUN echo "\"\e[B\":history-search-forward"  >> ~/.inputrc && \
    echo "\"\e[A\":history-search-backward" >> ~/.inputrc

RUN echo "filetype plugin indent on" >> ~/.vimrc && \
    echo "set tabstop=4"             >> ~/.vimrc && \
    echo "set shiftwidth=4"          >> ~/.vimrc && \
    echo "set expandtab"             >> ~/.vimrc && \
    echo "set pastetoggle=<F2>"      >> ~/.vimrc && \
    echo "set hlsearch"              >> ~/.vimrc && \
    echo "syntax on"                 >> ~/.vimrc

ENTRYPOINT [ "/bin/bash" ]
