FROM ubuntu:16.04
LABEL maintainer="Emmanux <infra@komodo.rocks>"

ENV BITCOIN_HOME /home/bitcoin
# RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 8842ce5e && \
#    echo "deb http://ppa.launchpad.net/bitcoin/bitcoin/ubuntu xenial main" \
#    > /etc/apt/sources.list.d/bitcoin.list
# RUN apt-get update && \
#    apt-get install -y bitcoind curl && \
#    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN apt-get update && \
    apt-get install -y build-essential pkg-config git libc6-dev m4 \
    g++-multilib autoconf libtool ncurses-dev unzip python zlib1g-dev \
    curl bsdmainutils automake libssl-dev libprotobuf-dev protobuf-compiler \
    libqrencode-dev ntp ntpdate software-properties-common libcurl4-gnutls-dev \
    cmake clang libevent-dev libboost-all-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN useradd -u 3001 -m bitcoin
USER bitcoin
WORKDIR "${BITCOIN_HOME}"



RUN cd ${BITCOIN_HOME} && pwd && ls -ltr /home &&\
    git clone https://github.com/bitcoin/bitcoin.git && cd bitcoin && \
    git checkout 0.15 

#BDB 4.8 for bitcoin
ENV BDB_PREFIX "${BITCOIN_HOME}/db4"

RUN mkdir -p ${BDB_PREFIX} && pwd && ls -ltr && \
    curl -O 'http://download.oracle.com/berkeley-db/db-4.8.30.NC.tar.gz' && \
    echo '12edc0df75bf9abd7f82f821795bcee50f42cb2e5f76a6a281b85732798364ef  db-4.8.30.NC.tar.gz' | sha256sum -c && \
    tar -xzvf db-4.8.30.NC.tar.gz

RUN cd db-4.8.30.NC/build_unix/ && \
    ../dist/configure -enable-cxx -disable-shared -with-pic -prefix=$BDB_PREFIX && \
    make -j$(nproc) && \
    make install 

RUN cd ${BITCOIN_HOME}/bitcoin && \
    ./autogen.sh && \
    ./configure LDFLAGS="-L${BDB_PREFIX}/lib/" CPPFLAGS="-I${BDB_PREFIX}/include/" -without-gui -without-miniupnpc && \
    make -j$(nproc)

USER root
# Add confd files as root
COPY confd/ /etc/confd
ADD entrypoint.sh /usr/local/bin
ADD start-bitcoind.sh /usr/local/bin
RUN ls -ltr ${BITCOIN_HOME}/bitcoin/src
RUN cp "${BITCOIN_HOME}/bitcoin/src/bitcoin-cli" /usr/local/bin
RUN cp "${BITCOIN_HOME}/bitcoin/src/bitcoind" /usr/local/bin

# confd
RUN curl -L -o /usr/local/bin/confd https://github.com/kelseyhightower/confd/releases/download/v0.15.0/confd-0.15.0-linux-amd64 && \
    chmod +x /usr/local/bin/confd

USER bitcoin
WORKDIR "${BITCOIN_HOME}"

RUN mkdir ${BITCOIN_HOME}/.bitcoin && \
    chmod 0750 ${BITCOIN_HOME}/.bitcoin && \
    chown bitcoin:bitcoin -R ${BITCOIN_HOME}/.bitcoin

VOLUME ["/home/bitcoin"] 

ENTRYPOINT ["entrypoint.sh"]
CMD ["start-bitcoind.sh"]

EXPOSE 8332 8333
