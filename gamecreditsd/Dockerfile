FROM ubuntu:16.04
LABEL maintainer="Dragon Riders <infra@komodo.rocks>"

ARG GAME_BRANCH

ENV USER_ID ${USER_ID:-3008}
ENV GROUP_ID ${GROUP_ID:-3008}
ENV GAMECREDITS_HOME /home/gamecredits

RUN useradd -u ${USER_ID} -s /bin/bash -m -d /home/gamecredits gamecredits

ENV BUILD_PACKAGES="build-essential pkg-config libcurl3-gnutls-dev libc6-dev libevent-dev m4 g++-multilib autoconf libtool git python zlib1g-dev bsdmainutils automake libboost-all-dev libssl-dev libprotobuf-dev protobuf-compiler libqrencode-dev libdb++-dev curl"

RUN apt update && \
    apt install -y $BUILD_PACKAGES && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

USER gamecredits
WORKDIR ${GAMECREDITS_HOME}
# ENV GAMECREDITS "${GAMECREDITS_HOME}/GameCredits"
ENV BDB_PREFIX "${GAMECREDITS_HOME}/db4"
ENV SSL_PREFIX "${GAMECREDITS_HOME}/openssl"

# Build Berkly DB 4.8
RUN cd ${GAMECREDITS_HOME} && \
    mkdir -p $BDB_PREFIX && \
    curl -L -O 'http://download.oracle.com/berkeley-db/db-4.8.30.NC.tar.gz' && \
    echo '12edc0df75bf9abd7f82f821795bcee50f42cb2e5f76a6a281b85732798364ef  db-4.8.30.NC.tar.gz' | sha256sum -c && \
    tar -xzvf db-4.8.30.NC.tar.gz && cd db-4.8.30.NC/build_unix/ && \
    ../dist/configure -enable-cxx -disable-shared -with-pic -prefix=$BDB_PREFIX && \
    make -j$(nproc) && \
    make install


# Build OpenSSL (libssl-dev) 1.0.x

RUN cd ${GAMECREDITS_HOME} && \
    mkdir -p ${SSL_PREFIX} && \
    curl -L -O http://www.openssl.org/source/openssl-1.0.2o.tar.gz && \
    echo 'ec3f5c9714ba0fd45cb4e087301eb1336c317e0d20b575a125050470e8089e4d  openssl-1.0.2o.tar.gz' | sha256sum -c && \
    tar -xvzf openssl-1.0.2o.tar.gz && cd openssl-1.0.2o && export CFLAGS=-fPIC && \
        ./config no-shared --prefix=${SSL_PREFIX} && make -j$(nproc) && make install && cd ..

# export PKG_CONFIG_PATH="${SSL_PREFIX}/pkgconfig"
# export CXXFLAGS+=" -I${SSL_PREFIX}/include/ -I${GAMECREDITS_PREFIX}/include/"
# export LDFLAGS+=" -L${SSL_PREFIX}/lib -L${SSL_PREFIX}/lib/ -static"
# export LIBS+="-ldl"

# Build GameCredits
RUN cd ${GAMECREDITS_HOME} && \
    # git clone https://github.com/jl777/GameCredits && \
    git clone https://github.com/gamecredits-project/GameCredits && \
    cd GameCredits && git checkout ${GAME_BRANCH} && ./autogen.sh && \
   ./configure LIBS="-ldl" PKG_CONFIG_PATH="${SSL_PREFIX}/pkgconfig" LDFLAGS="-L${SSL_PREFIX}/lib -L${BDB_PREFIX}/lib/ -static" CXXFLAGS="-I${SSL_PREFIX}/include -I${BDB_PREFIX}/include/" \
       -without-gui -without-miniupnpc --disable-tests --disable-bench --enable-static --disable-shared && \
   make -j$(nproc)

USER root

RUN rm -rf /var/lib/apt/lists/*

# Add confd files
COPY confd/ /etc/confd

USER gamecredits
ENV PATH="${GAMECREDITS_HOME}/GameCredits/src:${GAMECREDITS_HOME}:${PATH}"

RUN mkdir ${GAMECREDITS_HOME}/.gamecredits && \
    mkdir ${GAMECREDITS_HOME}/.komodo && \
    chmod 0750 ${GAMECREDITS_HOME}/.gamecredits && \
    chown gamecredits:gamecredits -R ${GAMECREDITS_HOME}/.gamecredits

VOLUME ["/home/gamecredits/.gamecredits"]

# confd
ADD entrypoint.sh "${GAMECREDITS_HOME}"
ADD start-gamecreditsd.sh "${GAMECREDITS_HOME}"
RUN curl -L -o confd https://github.com/kelseyhightower/confd/releases/download/v0.15.0/confd-0.15.0-linux-amd64 && \
    chmod +x confd


ENTRYPOINT ["entrypoint.sh"]
CMD ["start-gamecreditsd.sh"]
