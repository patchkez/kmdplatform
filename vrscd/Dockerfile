FROM ubuntu:16.04 as vrsc_builder
LABEL maintainer="Emmanux <infra@komodo.rocks>"

ARG VRSC_BRANCH
ENV VRSC_HOME /home/veruscoin

ENV BUILD_PACKAGES="build-essential pkg-config libcurl3-gnutls-dev libc6-dev libevent-dev m4 g++-multilib autoconf libtool ncurses-dev unzip git python zlib1g-dev wget bsdmainutils automake libboost-all-dev libssl-dev libprotobuf-dev protobuf-compiler libqt4-dev libqrencode-dev libdb++-dev curl libcurl3-gnutls-dev libgomp1"

RUN apt update && \
    apt install -y $BUILD_PACKAGES

RUN useradd -u 3009 -m veruscoin

USER veruscoin
WORKDIR ${VRSC_HOME}

RUN git clone https://github.com/VerusCoin/VerusCoin/ && \
    cd VerusCoin && \
    git checkout ${VRSC_BRANCH} 
RUN cd VerusCoin && ./zcutil/fetch-params.sh
RUN cd VerusCoin && ./zcutil/build.sh -j$(nproc)

USER root
RUN apt remove --purge -y $BUILD_PACKAGES $(apt-mark showauto) && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf ${VRSC_HOME}/depends

RUN apt update && \
    apt install -y curl libcurl3-gnutls-dev libgomp1


FROM ubuntu:16.04 as vrsc_minimal
RUN useradd -u 3009 -m veruscoin
ENV VRSC_HOME /home/veruscoin

COPY --from=vrsc_builder  /home/veruscoin/VerusCoin/src/komodod /bin
COPY --from=vrsc_builder  /home/veruscoin/VerusCoin/src/komodo-cli /bin
COPY --from=vrsc_builder  /home/veruscoin/.zcash-params /home/veruscoin/.zcash-params

RUN apt update && \
    apt install -y libcurl3-gnutls-dev curl libgomp1

# confd
RUN curl -L -o /usr/local/bin/confd https://github.com/kelseyhightower/confd/releases/download/v0.15.0/confd-0.15.0-linux-amd64 && \
    chmod +x /usr/local/bin/confd

ADD entrypoint.sh /usr/local/bin
ADD start-veruscoind.sh /usr/local/bin
COPY confd/ "${VRSC_HOME}"/confd
RUN chown -R veruscoin:veruscoin "${VRSC_HOME}"/confd

ENV PATH="~/veruscoin/src/:${PATH}"

USER veruscoin
WORKDIR "${VRSC_HOME}"
RUN mkdir ${VRSC_HOME}/.komodo && \
    mkdir ${VRSC_HOME}/.bitcoin && \
    touch ${VRSC_HOME}/.komodo/komodo.conf && \
    chown veruscoin:veruscoin "${VRSC_HOME}"/.komodo/komodo.conf

VOLUME ["/home/veruscoin/.komodo"]

ENTRYPOINT ["entrypoint.sh"]
CMD ["start-veruscoind.sh"]
