FROM ubuntu:16.04
LABEL maintainer="Emmanux <infra@komodo.rocks>"

RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 8842ce5e && \
    echo "deb http://ppa.launchpad.net/bitcoin/bitcoin/ubuntu xenial main" \
    > /etc/apt/sources.list.d/bitcoin.list
RUN apt-get update && \
    apt-get install -y bitcoind && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
RUN useradd -u 3001 -m bitcoind
USER bitcoind
WORKDIR /home/bitcoind

CMD /usr/bin/bitcoind -daemon && \
  tail -f /home/bitcoind/.bitcoin/debug.log

EXPOSE 8332 8333
