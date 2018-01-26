FROM ubuntu:16.04
MAINTAINER emmanux

ENV BUILD_PACKAGES="build-essential pkg-config libcurl3-gnutls-dev libc6-dev libevent-dev m4 g++-multilib autoconf libtool ncurses-dev unzip git python zlib1g-dev wget bsdmainutils automake libboost-all-dev libssl-dev libprotobuf-dev protobuf-compiler libqt4-dev libqrencode-dev libdb++-dev"

RUN apt update && \
    apt install -y $BUILD_PACKAGES

RUN git clone https://github.com/jl777/komodo && \
    cd komodo && \
    git checkout beta && \
    ./zcutil/fetch-params.sh && \
    ./zcutil/build.sh -j$(nproc)

RUN apt remove --purge -y $BUILD_PACKAGES $(apt-mark showauto) && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /komodo/depends

RUN apt update && apt install -y libcurl3-gnutls-dev libgomp1 telnet

RUN useradd -u 3003 -m komodod && \
    mv /root/.zcash-params /home/komodod/ && \
    chown -R komodod:komodod /home/komodod/.zcash-params

ENV PATH="/komodo/src/:${PATH}"
USER komodod
WORKDIR /home/komodod
RUN mkdir ~/.komodo && \
    touch ~/.komodo/komodo.conf

ENTRYPOINT ["/komodo/src/komodod"]

EXPOSE 7770 7771
