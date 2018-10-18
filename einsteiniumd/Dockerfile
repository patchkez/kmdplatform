FROM ubuntu:16.04
LABEL maintainer="Dragon Riders <infra@komodo.rocks>"

ARG EMC2_BRANCH

ENV USER_ID ${USER_ID:-3011}
ENV GROUP_ID ${GROUP_ID:-3011}
ENV EMC2_HOME /home/einsteinium

RUN useradd -u ${USER_ID} -s /bin/bash -m -d /home/einsteinium einsteinium

ENV BUILD_PACKAGES="build-essential pkg-config libcurl3-gnutls-dev libc6-dev libevent-dev m4 g++-multilib autoconf libtool git python zlib1g-dev bsdmainutils automake libboost-all-dev libssl-dev libprotobuf-dev protobuf-compiler libqrencode-dev libdb++-dev curl"

RUN apt update && \
    apt install -y $BUILD_PACKAGES && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

USER einsteinium
WORKDIR ${EMC2_HOME}
ENV EMC2 "${EMC2_HOME}/einsteinium"  
ENV BDB_PREFIX "${EMC2_HOME}/db4"

# Clone CHIPS repository
RUN cd ${EMC2_HOME} && \
    # git clone https://github.com/jl777/chips3.git && \
    git clone https://github.com/emc2foundation/einsteinium.git && \
    cd einsteinium && git checkout ${EMC2_BRANCH}

# Build Berkly DB 4.8
RUN cd ${EMC2_HOME} && \
    mkdir -p $BDB_PREFIX && \
    curl -O 'http://download.oracle.com/berkeley-db/db-4.8.30.NC.tar.gz' && \
    echo '12edc0df75bf9abd7f82f821795bcee50f42cb2e5f76a6a281b85732798364ef  db-4.8.30.NC.tar.gz' | sha256sum -c && \
    tar -xzvf db-4.8.30.NC.tar.gz && cd db-4.8.30.NC/build_unix/ && \
    ../dist/configure -enable-cxx -disable-shared -with-pic -prefix=$BDB_PREFIX && \
    make -j$(nproc) && \
    make install 

# Build Chips:
RUN cd ${EMC2} && \
    ./autogen.sh && \
    ./configure LDFLAGS="-L${BDB_PREFIX}/lib/" CPPFLAGS="-I${BDB_PREFIX}/include/" -without-gui -without-miniupnpc -disable-bench && \
    make -j$(nproc)

USER root

RUN rm -rf /var/lib/apt/lists/*

# Add confd files
COPY confd/ /etc/confd

USER einsteinium
ENV PATH="${EMC2_HOME}:${EMC2}/src:${PATH}"

RUN mkdir ${EMC2_HOME}/.einsteinium && \
    mkdir ${EMC2_HOME}/.komodo && \
    chmod 0750 ${EMC2_HOME}/.einsteinium && \
    chown einsteinium:einsteinium -R ${EMC2_HOME}/.einsteinium

VOLUME ["/home/einsteinium/.einsteinium"] 


# confd
ADD entrypoint.sh "${EMC2_HOME}"
ADD start-einsteinium.sh /usr/local/bin
RUN curl -L -o confd https://github.com/kelseyhightower/confd/releases/download/v0.15.0/confd-0.15.0-linux-amd64 && \
    chmod +x confd


ENTRYPOINT ["entrypoint.sh"]
CMD ["start-einsteinium.sh"]

EXPOSE 41879
