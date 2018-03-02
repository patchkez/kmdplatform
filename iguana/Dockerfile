FROM ubuntu:16.04
MAINTAINER emmanux
LABEL version="0.3"

# prepare system to build things
ENV BUILD_PACKAGES="git build-essential cmake libcurl4-openssl-dev libssl-dev"
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
RUN git clone https://github.com/Emmanux/SuperNET && \
    cd SuperNET/iguana && \
    git checkout beta

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
    gcc -g -Wno-aggressive-loop-optimizations -Wno-deprecated -c -O2 -DLIQUIDITY_PROVIDER=1 \
        *.c ../basilisk/basilisk.c ../gecko/gecko.c ../datachain/datachain.c && \
    gcc -g -Wno-aggressive-loop-optimizations -Wno-deprecated -c -DLIQUIDITY_PROVIDER=1 \
        main.c iguana777.c iguana_bundles.c ../basilisk/basilisk.c iguana_ramchain.c && \
    gcc -g -o ../agents/iguana *.o ./secp256k1/*.o ../agents/libcrypto777.a /usr/local/lib/libnanomsg.so \
        -lcurl -lssl -lcrypto -lpthread -lz -lm

# remove unnecessary packages
RUN apt remove --purge -y $BUILD_PACKAGES $(apt-mark showauto) && \
    apt install -y curl libcurl4-openssl-dev telnet net-tools && \
    rm -rf /var/lib/apt/lists/* 

# initialize things
RUN useradd -u 3004 -m iguana
ENV PATH="/SuperNET/iguana:${PATH}"
USER iguana
WORKDIR /home/iguana

ENTRYPOINT ["/SuperNET/agents/iguana"]
