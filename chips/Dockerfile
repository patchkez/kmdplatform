#FROM: komodo-base:latest
FROM ubuntu:16.04
LABEL maintainer="Dragon Riders <infra@komodo.rocks>"

ARG CHIPS_BRANCH

ENV USER_ID ${USER_ID:-3007}
ENV GROUP_ID ${GROUP_ID:-3007}
ENV SHARED_GROUP_ID ${SHARED_GROUP_ID:-3005}
ENV CHIPS_HOME /home/chips

RUN groupadd -g ${GROUP_ID} chips && \
    groupadd -g ${SHARED_GROUP_ID} shared && \
    useradd -u ${USER_ID} -g chips -G shared -s /bin/bash -m -d /home/chips chips

ENV BUILD_PACKAGES="build-essential pkg-config libcurl3-gnutls-dev libc6-dev libevent-dev m4 g++-multilib autoconf libtool git python zlib1g-dev bsdmainutils automake libboost-all-dev libssl-dev libprotobuf-dev protobuf-compiler libqrencode-dev libdb++-dev curl"
# ENV BUILD_PACKAGES="build-essential pkg-config libcurl3-gnutls-dev libc6-dev libevent-dev m4 g++-multilib autoconf libtool ncurses-dev unzip git python zlib1g-dev wget bsdmainutils automake libboost-all-dev libssl-dev libprotobuf-dev protobuf-compiler libqt4-dev libqrencode-dev libdb++-dev"

RUN apt update && \
    apt install -y $BUILD_PACKAGES && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

USER chips
WORKDIR /home/chips

ENV CHIPS "${CHIPS_HOME}/chips3"  
ENV BDB_PREFIX "${CHIPS_HOME}/db4"


RUN cd ${CHIPS_HOME} && \
    git clone https://github.com/jl777/chips3.git
#Build Berkly DB 4.8
# CHIPS_ROOT=$(pwd)
# BDB_PREFIX="${CHIPS_ROOT}/db4"
RUN cd ${CHIPS_HOME} && \
    mkdir -p $BDB_PREFIX && \
    curl -O 'http://download.oracle.com/berkeley-db/db-4.8.30.NC.tar.gz' && \
    echo '12edc0df75bf9abd7f82f821795bcee50f42cb2e5f76a6a281b85732798364ef  db-4.8.30.NC.tar.gz' | sha256sum -c && \
    tar -xzvf db-4.8.30.NC.tar.gz && cd db-4.8.30.NC/build_unix/ && \
    ../dist/configure -enable-cxx -disable-shared -with-pic -prefix=$BDB_PREFIX && \
    make -j$(nproc) && \
    make install 

#Install Chips:
RUN cd ${CHIPS} && \
    ./autogen.sh && \
    ./configure LDFLAGS="-L${BDB_PREFIX}/lib/" CPPFLAGS="-I${BDB_PREFIX}/include/" -without-gui -without-miniupnpc && \
    make -j$(nproc)

USER root
# RUN apt remove --purge -y $BUILD_PACKAGES $(apt-mark showauto) && \
#    rm -rf /var/lib/apt/lists/* && \
#    rm -rf ${KOMODO_HOME}/komodo/depends

# RUN apt update && apt install -y libcurl3-gnutls-dev libgomp1 telnet curl

# Workaround - do not want to redownload params
RUN usermod -g shared chips

USER chips

#RUN useradd -u 3003 -m komodod && \
#RUN mv /root/.zcash-params /home/komodo/ && \
#    chown -R komodo:komodo /home/komodo/.zcash-params

ENV PATH="${CHIPS}/src:${PATH}"
# USER komodod
# WORKDIR /home/komodod
RUN mkdir ${CHIPS_HOME}/.chips && \
    mkdir ${CHIPS_HOME}/.shared && \
    chmod 0750 ${CHIPS_HOME}/.chips && \
    chown chips:shared -R ${CHIPS_HOME}/.chips

VOLUME ["/home/chips/.chips"] 
VOLUME ["/home/chips/.shared"] 

ADD ./bin /usr/local/bin
COPY docker-entrypoint.sh /usr/local/bin/
ENTRYPOINT ["docker-entrypoint.sh"]


CMD ["chips_oneshot"]

EXPOSE 57776 57777
