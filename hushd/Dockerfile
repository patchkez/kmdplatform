FROM ubuntu:16.04 as hush_builder
LABEL maintainer="Emmanux <infra@komodo.rocks>"

ARG HUSH_BRANCH
ENV HUSH_HOME /home/hush

ENV BUILD_PACKAGES="build-essential pkg-config libcurl3-gnutls-dev libc6-dev libevent-dev m4 g++-multilib autoconf libtool ncurses-dev unzip git python zlib1g-dev wget bsdmainutils automake libboost-all-dev libssl-dev libprotobuf-dev protobuf-compiler libqt4-dev libqrencode-dev libdb++-dev curl libcurl3-gnutls-dev libgomp1"

RUN apt update && \
    apt install -y $BUILD_PACKAGES

RUN useradd -u 3010 -m hush

USER hush
WORKDIR ${HUSH_HOME}

COPY *.patch /tmp/

RUN git clone https://github.com/MyHush/hush && \
    cd hush && \
    git checkout ${HUSH_BRANCH}
    # git apply -v /tmp/*.patch
RUN cd hush && ./zcutil/fetch-params.sh
RUN cd hush && ./zcutil/build.sh -j$(nproc)

USER root
RUN apt remove --purge -y $BUILD_PACKAGES $(apt-mark showauto) && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf ${KOMODO_HOME}/depends

RUN apt update && \
    apt install -y curl libcurl3-gnutls-dev libgomp1


FROM ubuntu:16.04 as hush_minimal
RUN useradd -u 3010 -m hush
ENV HUSH_HOME /home/hush

COPY --from=hush_builder  /home/hush/hush/src/hushd /bin
COPY --from=hush_builder  /home/hush/hush/src/hush-cli /bin
COPY --from=hush_builder  /home/hush/.zcash-params /home/hush/.zcash-params

RUN apt update && \
    apt install -y libcurl3-gnutls-dev curl libgomp1

# confd
RUN curl -L -o /usr/local/bin/confd https://github.com/kelseyhightower/confd/releases/download/v0.15.0/confd-0.15.0-linux-amd64 && \
    chmod +x /usr/local/bin/confd

ADD entrypoint.sh /usr/local/bin
ADD start-hushd.sh /usr/local/bin
COPY confd/ "${HUSH_HOME}"/confd
RUN chown -R hush:hush "${HUSH_HOME}"/confd

ENV PATH="~/hush/src/:${PATH}"

USER hush
WORKDIR "${HUSH_HOME}"
RUN mkdir ${HUSH_HOME}/.hush && \
    mkdir ${HUSH_HOME}/.komodo && \
    mkdir ${HUSH_HOME}/.bitcoin && \
    touch ${HUSH_HOME}/.komodo/komodo.conf && \
    chown hush:hush "${HUSH_HOME}"/.komodo/komodo.conf

VOLUME ["/home/hush/.hush"]

ENTRYPOINT ["entrypoint.sh"]
CMD ["start-hushd.sh"]
