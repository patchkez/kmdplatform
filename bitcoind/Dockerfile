FROM ubuntu:16.04
LABEL maintainer="Emmanux <infra@komodo.rocks>"

ENV BITCOIN_HOME /home/bitcoin

RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 8842ce5e && \
    echo "deb http://ppa.launchpad.net/bitcoin/bitcoin/ubuntu xenial main" \
    > /etc/apt/sources.list.d/bitcoin.list
RUN apt-get update && \
    apt-get install -y bitcoind curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
RUN useradd -u 3001 -m bitcoin

# Add confd files as root
COPY confd/ /etc/confd
ADD entrypoint.sh /usr/local/bin
ADD start-bitcoind.sh /usr/local/bin

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
# CMD ["bitcoind"]

EXPOSE 8332 8333
