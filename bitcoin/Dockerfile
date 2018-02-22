FROM ubuntu:16.04
LABEL maintainer="Emmanux <infra@komodo.rocks>"

ARG USER_ID
ARG GROUP_ID
ENV USER_ID ${BITCOIN_USER_ID:-3001}
ENV GROUP_ID ${BITCOIN_GROUP_ID:-3001}
ENV SHARED_GROUP_ID ${SHARED_GROUP_ID:-3005}
ENV HOME /home/bitcoin

RUN groupadd -g ${GROUP_ID} bitcoin && \
    groupadd -g ${SHARED_GROUP_ID} shared && \
    useradd -u ${USER_ID} -g bitcoin -G shared -s /bin/bash -m -d /home/bitcoin bitcoin

RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 8842ce5e && \
    echo "deb http://ppa.launchpad.net/bitcoin/bitcoin/ubuntu xenial main" \
    > /etc/apt/sources.list.d/bitcoin.list

RUN apt-get update && \
    apt-get install -y bitcoind && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
# RUN useradd -u 3001 -m bitcoind

USER bitcoin
RUN mkdir -p /home/bitcoin/.shared
WORKDIR /home/bitcoin
VOLUME ["/home/bitcoin"]
VOLUME ["/home/bitcoin/.shared"]


ADD ./bin /usr/local/bin
COPY docker-entrypoint.sh /usr/local/bin/

ENTRYPOINT ["docker-entrypoint.sh"]

CMD ["btc_oneshot"]

EXPOSE 8332 8333
