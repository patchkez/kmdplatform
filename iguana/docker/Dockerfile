FROM ubuntu:16.04
MAINTAINER emmanux
LABEL version="0.5c"

# prepare system to build things
COPY *.patch /
COPY x-cli.sh /

ENV BUILD_PACKAGES="git build-essential cmake libssl-dev clang libcurl4-openssl-dev"

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

# get iguana code
RUN git clone https://github.com/jl777/SuperNET && \
    echo "trying jl777 branch" && \
    cd SuperNET/iguana && \
    git checkout jl777 && \
    git apply -v /*.patch

# build secp256k1
RUN cd SuperNET/iguana/secp256k1 && \
    gcc -c -o secp256k1.o -I. -I./src  -I./include \
    -O3 -W -std=c89 -pedantic -Wall -Wextra -Wcast-align -Wnested-externs -Wshadow -Wstrict-prototypes \
    -Wno-unused-function -Wno-long-long -Wno-overlength-strings -fvisibility=hidden -DHAVE_CONFIG_H \
    src/secp256k1.c

# build crypto777
RUN cd SuperNET/crypto777 && \
    gcc -c -DLIQUIDITY_PROVIDER=1 -O2 *.c jpeg/*.c jpeg/unix/*.c \
    -I/usr/include/curl && \
    ar rc ../agents/libcrypto777.a *.o

# build iguana
RUN cd SuperNET/iguana && \
    cp -rp secp256k1/* . && \
    clang -g -Wno-deprecated -c -O2 -DISNOTARYNODE=1 -DLIQUIDITY_PROVIDER=1 \
        *.c ../basilisk/basilisk.c ../gecko/gecko.c ../datachain/datachain.c && \
    clang -g  -Wno-deprecated -c -DISNOTARYNODE=1 -DLIQUIDITY_PROVIDER=1  \
        main.c iguana777.c iguana_bundles.c ../basilisk/basilisk.c && \
    clang -g -o ../agents/iguana *.o ../agents/libcrypto777.a \
        -lnanomsg -lcurl -lssl -lcrypto -lpthread -lz -lm

# remove unnecessary packages and install useful tools
RUN apt remove --purge -y $BUILD_PACKAGES $(apt-mark showauto) && \
    apt install -y curl libcurl4-openssl-dev telnet net-tools redir screen && \
    rm -rf /var/lib/apt/lists/* 

# install x-cli.sh wrapper
RUN ln -s /x-cli.sh /usr/bin/bitcoin-cli && \
    ln -s /x-cli.sh /usr/bin/komodo-cli && \
    ln -s /x-cli.sh /SuperNET/agents/komodo-cli

# initialize things
RUN useradd -u 3004 -m iguana
ENV PATH="/SuperNET/iguana:${PATH}"
USER iguana
WORKDIR /home/iguana
ENV HOME=/home/iguana

# get testnet file
RUN curl -so /home/iguana/testnet https://raw.githubusercontent.com/KomodoPlatform/vote2018/master/testnet/testnet.json

ENTRYPOINT ["/SuperNET/agents/iguana"]

