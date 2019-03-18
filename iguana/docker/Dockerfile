FROM ubuntu:16.04
MAINTAINER emmanux
LABEL version="0.5c"

ARG IGUANA_BRANCH
ENV IGUANA_HOME /home/iguana
# prepare system to build things
COPY *.patch /tmp/
COPY sha256hwaccel/*.patch /tmp/sha256hwaccel/
COPY x-cli.sh /tmp/

ENV BUILD_PACKAGES="git build-essential cmake libssl-dev clang libcurl4-openssl-dev libsodium-dev"
# ENV BUILD_PACKAGES="git build-essential cmake libssl-dev clang libcurl4-gnutls-dev"
# apt-get install git libcurl4-openssl-dev build-essential libnanomsg-dev

RUN apt update && \
    apt install -y $BUILD_PACKAGES

# build nanomsg
RUN git clone https://github.com/nanomsg/nanomsg && \
    cd nanomsg && \
    cmake . && \
    make && \
    make install && \
    ldconfig && \
    cd .. && rm -rf nanomsg

# initialize things
RUN useradd -u 3004 -m iguana

USER iguana
WORKDIR ${IGUANA_HOME}
# get iguana code
# RUN  git config --global  http.sslVerify false && \
    # git config --global http.postBuffer 1048576000 && \
    # mkdir ~/.ssh/ && \
    # ssh-keyscan -t rsa github.com >> ~/.ssh/known_hosts && \
RUN git config --global http.postBuffer 2M && git config --global http.maxRequestBuffer 100M && git config --global core.compression 4 && export GIT_CURL_VERBOSE=1 && export GIT_TRACE=1 && export GIT_TRACE_PACKET=1 && git clone https://github.com/jl777/SuperNET && \
    # cd SuperNET && git fetch --unshallow && \
    cd SuperNET/iguana && \
    git checkout ${IGUANA_BRANCH} && \
    git apply -v /tmp/sha256hwaccel/*.patch && \
    # git apply -v /tmp/0001-fix-iguana-autosplit-acsplit-issue.patch && \
    # git apply -v /tmp/*.patch && \
    # git apply -v /tmp/listen_to_all.patch && \
    # git apply -v /tmp/disable_ip_list_autoupdate.patch && \
    cd secp256k1; ./m_unix; cd .. && \
    cd ../crypto777; ./m_LP; cd ../iguana && \
    clang -g -Wno-deprecated -c -O2 -DISNOTARYNODE=1 -DLIQUIDITY_PROVIDER=1 *.c ../basilisk/basilisk.c ../gecko/gecko.c ../datachain/datachain.c && \
    clang -g  -Wno-deprecated -c -DISNOTARYNODE=1 -DLIQUIDITY_PROVIDER=1  main.c iguana777.c iguana_bundles.c ../basilisk/basilisk.c && \
    clang -g -o ../agents/iguana *.o ../agents/libcrypto777.a -lnanomsg -lcurl -lssl -lcrypto -lpthread -lz -lm -lsodium
	
# # build secp256k1
# RUN cd SuperNET/iguana/secp256k1 && \
#     gcc -c -o secp256k1.o -I. -I./src  -I./include \
#     -O3 -W -std=c89 -pedantic -Wall -Wextra -Wcast-align -Wnested-externs -Wshadow -Wstrict-prototypes \
#     -Wno-unused-function -Wno-long-long -Wno-overlength-strings -fvisibility=hidden -DHAVE_CONFIG_H \
#     src/secp256k1.c
# 
# # build crypto777
# RUN cd SuperNET/crypto777 && \
#     gcc -c -DLIQUIDITY_PROVIDER=1 -O2 *.c jpeg/*.c jpeg/unix/*.c \
#     -I/usr/include/curl && \
#     ar rc ../agents/libcrypto777.a *.o
# 
# # build iguana
# RUN cd SuperNET/iguana && \
#     cp -rp secp256k1/* . && \
#     clang -g -Wno-deprecated -c -O2 -DISNOTARYNODE=1 -DLIQUIDITY_PROVIDER=1 \
#         *.c ../basilisk/basilisk.c ../gecko/gecko.c ../datachain/datachain.c && \
#     clang -g  -Wno-deprecated -c -DISNOTARYNODE=1 -DLIQUIDITY_PROVIDER=1  \
#         main.c iguana777.c iguana_bundles.c ../basilisk/basilisk.c && \
#     clang -g -o ../agents/iguana *.o ../agents/libcrypto777.a \
#         -lnanomsg -lcurl -lssl -lcrypto -lpthread -lz -lm

USER root
# remove unnecessary packages and install useful tools
# RUN apt remove --purge -y $BUILD_PACKAGES $(apt-mark showauto) && \
RUN apt update && apt install -y curl libcurl4-openssl-dev telnet net-tools redir screen python3-pip git && \
    pip3 install virtualenv && \
    rm -rf /var/lib/apt/lists/*


# install x-cli.sh wrapper
RUN ln -s /x-cli.sh /usr/bin/bitcoin-cli && \
    ln -s /x-cli.sh /usr/bin/komodo-cli && \
    ln -s /x-cli.sh ${IGUANA_HOME}/SuperNET/agents/komodo-cli

# confd
RUN curl -L -o /usr/local/bin/confd https://github.com/kelseyhightower/confd/releases/download/v0.15.0/confd-0.15.0-linux-amd64 && \
    chmod +x /usr/local/bin/confd

ADD entrypoint.sh /usr/local/bin
COPY confd/ "${IGUANA_HOME}"/confd
RUN chown -R iguana:iguana "${IGUANA_HOME}"/confd

ENV PATH="~/SuperNET/agents/:~/SuperNET/iguana:${PATH}"
USER iguana
WORKDIR /home/iguana

# Create directories for configs, it seems confd cannot create them
RUN mkdir ${IGUANA_HOME}/.bitcoin && \
    mkdir ${IGUANA_HOME}/.komodo && \
    mkdir ${IGUANA_HOME}/.komodo/VRSC && \
    mkdir ${IGUANA_HOME}/.chips && \
    mkdir ${IGUANA_HOME}/.gamecredits && \
    mkdir ${IGUANA_HOME}/.hush && \
    mkdir ${IGUANA_HOME}/.einsteinium && \
    mkdir ${IGUANA_HOME}/.gincoincore

# Create python3 venv
RUN virtualenv komodotools-venv && \
    # Export needed variables for Python3
    echo 'export LC_ALL=C.UTF-8' >> ~/.bashrc && \
    echo 'export LANG=C.UTF-8' >> ~/.bashrc && \
    # Acivate environment on container startup
    echo 'source ~/komodotools-venv/bin/activate' >> ~/.bashrc && \
    # Activate env now
    . ~/komodotools-venv/bin/activate && \
    # Clone komodotools repo
    echo "" && \
    git clone https://github.com/KomodoPlatform/komodotools && \
    # Install needed requirements
    cd komodotools/dragonriders && pip install -Ur requirements.txt && \
    # Install this repo as pip package
    pip install --editable .


ENTRYPOINT ["entrypoint.sh"]
CMD ["~/SuperNET/agents/iguana"]
#ENTRYPOINT ["/SuperNET/agents/iguana"]
