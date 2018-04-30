FROM ubuntu:16.04
LABEL maintainer="Dragon Riders <infra@komodo.rocks>"

ARG CHIPS_BRANCH

ENV USER_ID ${USER_ID:-3007}
ENV GROUP_ID ${GROUP_ID:-3007}
ENV CHIPS_HOME /home/chips

RUN useradd -u ${USER_ID} -s /bin/bash -m -d /home/chips chips

ENV BUILD_PACKAGES="build-essential pkg-config libcurl3-gnutls-dev libc6-dev libevent-dev m4 g++-multilib autoconf libtool git python zlib1g-dev bsdmainutils automake libboost-all-dev libssl-dev libprotobuf-dev protobuf-compiler libqrencode-dev libdb++-dev curl"

RUN apt update && \
    apt install -y $BUILD_PACKAGES && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

USER chips
WORKDIR ${CHIPS_HOME}
ENV CHIPS "${CHIPS_HOME}/chips3"  
ENV BDB_PREFIX "${CHIPS_HOME}/db4"

# Clone CHIPS repository
RUN cd ${CHIPS_HOME} && \
    git clone https://github.com/jl777/chips3.git && \
    cd chips3 && git checkout ${CHIPS_BRANCH}

# Build Berkly DB 4.8
RUN cd ${CHIPS_HOME} && \
    mkdir -p $BDB_PREFIX && \
    curl -O 'http://download.oracle.com/berkeley-db/db-4.8.30.NC.tar.gz' && \
    echo '12edc0df75bf9abd7f82f821795bcee50f42cb2e5f76a6a281b85732798364ef  db-4.8.30.NC.tar.gz' | sha256sum -c && \
    tar -xzvf db-4.8.30.NC.tar.gz && cd db-4.8.30.NC/build_unix/ && \
    ../dist/configure -enable-cxx -disable-shared -with-pic -prefix=$BDB_PREFIX && \
    make -j$(nproc) && \
    make install 

# Build Chips:
RUN cd ${CHIPS} && \
    ./autogen.sh && \
    ./configure LDFLAGS="-L${BDB_PREFIX}/lib/" CPPFLAGS="-I${BDB_PREFIX}/include/" -without-gui -without-miniupnpc && \
    make -j$(nproc)

USER root

RUN rm -rf /var/lib/apt/lists/*

# Add confd files
COPY confd/ /etc/confd

USER chips
ENV PATH="${CHIPS_HOME}:${CHIPS}/src:${PATH}"

RUN mkdir ${CHIPS_HOME}/.chips && \
    mkdir ${CHIPS_HOME}/.komodo && \
    chmod 0750 ${CHIPS_HOME}/.chips && \
    chown chips:chips -R ${CHIPS_HOME}/.chips

VOLUME ["/home/chips/.chips"] 


# confd
ADD entrypoint.sh "${CHIPS_HOME}"
RUN curl -L -o confd https://github.com/kelseyhightower/confd/releases/download/v0.15.0/confd-0.15.0-linux-amd64 && \
    chmod +x confd


ENTRYPOINT ["entrypoint.sh"]
CMD ["chipsd"]

EXPOSE 57776 57777
