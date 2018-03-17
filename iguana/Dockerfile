#FROM komodo-base:latest
FROM ubuntu:16.04

LABEL maintainer="Emmanux <infra@komodo.rocks>"

#ARG BUILD_PACKAGES

ARG IGUANA_BRANCH
# ENV IGUANA_BRANCH=${IGUANA_BRANCH}


ENV USER_ID ${USER_ID:-3004}
ENV GROUP_ID ${GROUP_ID:-3004}
ENV SHARED_GROUP_ID ${SHARED_GROUP_ID:-3005}

RUN groupadd -g ${GROUP_ID} iguana && \
    groupadd -g ${SHARED_GROUP_ID} shared && \
    useradd -u ${USER_ID} -g iguana -G shared -s /bin/bash -m -d /home/iguana iguana

ENV BUILD_PACKAGES="git libcurl4-openssl-dev build-essential libnanomsg-dev cmake libssl-dev clang"
RUN apt update && \
     apt install -y $BUILD_PACKAGES && \
     apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


RUN git clone https://github.com/nanomsg/nanomsg && \
    cd nanomsg && \
    cmake . && \
    make && \
    make install && \
    ldconfig

USER iguana
WORKDIR /home/iguana
RUN mkdir -p /home/iguana/.iguana
RUN mkdir -p /home/iguana/.shared
RUN mkdir -p /home/iguana/.komodo

RUN whoami && ls -ltrh /home && touch /home/iguana/test && ls -ltrh /home/iguana/test

RUN git clone https://github.com/jl777/SuperNET && \
    cd SuperNET/iguana && \
    git checkout ${IGUANA_BRANCH}
    # ./m_LP
# OR????
#git clone https://github.com/jl777/SuperNET; cd SuperNET; ./m_onetime m_unix;



# TEST

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
    # gcc -g -o ../agents/iguana *.o ./secp256k1/*.o ../agents/libcrypto777.a /usr/local/lib/libnanomsg.so \
    gcc -g -o ../agents/iguana *.o ./secp256k1/*.o ../agents/libcrypto777.a \
        -lnanomsg -lcurl -lssl -lcrypto -lpthread -lz -lm

# RUN cd SuperNET/iguana && \
#    clang -g -Wno-deprecated -c -O2 -DISNOTARYNODE=1 -DLIQUIDITY_PROVIDER=1 *.c ../basilisk/basilisk.c ../gecko/gecko.c ../datachain/datachain.c && \
#    clang -g  -Wno-deprecated -c -DISNOTARYNODE=1 -DLIQUIDITY_PROVIDER=1  main.c iguana777.c iguana_bundles.c ../basilisk/basilisk.c && \
#    clang -g -o ../agents/iguana *.o ../agents/libcrypto777.a -lnanomsg -lcurl -lssl -lcrypto -lpthread -lz -lm


USER root
RUN apt update && \
    apt install -y strace && \
    rm -rf /var/lib/apt/lists/*
# remove unnecessary packages
# RUN apt remove --purge -y $BUILD_PACKAGES $(apt-mark showauto) && \
#    apt install -y curl libcurl4-openssl-dev telnet net-tools && \
# rm -rf /var/lib/apt/lists/* 
USER iguana

#RUN apt remove --purge -y $BUILD_PACKAGES $(apt-mark showauto) && \
#    rm -rf /var/lib/apt/lists/* && \
#    rm -rf /komodo/depends

#RUN useradd -u 3003 -m komodod && \
#RUN mv /root/.zcash-params /home/komodod/ && \
#    chown -R komodod:komodod /home/komodod/.zcash-params

#ENV PATH="/komodo/src/:${PATH}"
#USER iguana
#WORKDIR /home/iguana
#RUN mkdir ~/.komodo 

VOLUME ["/home/iguana/.iguana"] 

# We need to mount it in order to share pubkey with komodo and bitcoin
VOLUME ["/home/iguana/.shared"] 

# We need access to komodo coins
VOLUME ["/home/iguana/.komodo"]

ADD ./bin /usr/local/bin
COPY docker-entrypoint.sh /usr/local/bin/
#ENTRYPOINT ["docker-entrypoint.sh"]

#CMD ["/komodo/src/komodod"]
#CMD ["komodo_oneshot"]
USER root
RUN apt update &&  apt install -y curl
USER iguana

# RUN cd ~/SuperNET/iguana && ln -s /home/iguana/.iguana/wp wp

#CMD ["/home/iguana/SuperNET/agents/iguana"]

ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["iguana_oneshot"]


EXPOSE 7776 7778
