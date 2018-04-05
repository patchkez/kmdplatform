#FROM: komodo-base:latest
FROM ubuntu:16.04
LABEL maintainer="Emmanux <infra@komodo.rocks>"

ARG KOMODO_BRANCH

ENV USER_ID ${USER_ID:-3003}
ENV GROUP_ID ${GROUP_ID:-3003}
ENV SHARED_GROUP_ID ${SHARED_GROUP_ID:-3005}
ENV KOMODO_HOME /home/komodo

RUN groupadd -g ${GROUP_ID} komodo && \
    groupadd -g ${SHARED_GROUP_ID} shared && \
    useradd -u ${USER_ID} -g komodo -G shared -s /bin/bash -m -d /home/komodo komodo

ENV BUILD_PACKAGES="build-essential pkg-config libcurl3-gnutls-dev libc6-dev libevent-dev m4 g++-multilib autoconf libtool ncurses-dev unzip git python zlib1g-dev wget bsdmainutils automake libboost-all-dev libssl-dev libprotobuf-dev protobuf-compiler libqt4-dev libqrencode-dev libdb++-dev"

RUN apt update && \
     apt install -y $BUILD_PACKAGES && \
     apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

USER komodo
WORKDIR /home/komodo

RUN git clone https://github.com/jl777/komodo && \
    cd komodo && \
    git checkout ${KOMODO_BRANCH} && \
    ./zcutil/fetch-params.sh && \
    ./zcutil/build.sh -j$(nproc)
    
#RUN ln -s /home/komodo/.komodo/shared/pubkey.txt /komodo/src/pubkey.txt

USER root
RUN apt remove --purge -y $BUILD_PACKAGES $(apt-mark showauto) && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf ${KOMODO_HOME}/komodo/depends

RUN apt update && apt install -y libcurl3-gnutls-dev libgomp1 telnet curl

# Workaround - do not want to redownload params
RUN usermod -g shared komodo

USER komodo

#RUN useradd -u 3003 -m komodod && \
#RUN mv /root/.zcash-params /home/komodo/ && \
#    chown -R komodo:komodo /home/komodo/.zcash-params

ENV PATH="${KOMODO_HOME}/komodo/src/:${PATH}"
# USER komodod
# WORKDIR /home/komodod
RUN mkdir ${KOMODO_HOME}/.komodo && \
    mkdir ${KOMODO_HOME}/.shared && \
    chmod 0750 ${KOMODO_HOME}/.komodo && \
    chown komodo:shared -R ${KOMODO_HOME}/.komodo/

VOLUME ["/home/komodo/.komodo"] 
VOLUME ["/home/komodo/.shared"] 


#RUN echo 'if [ -f /home/komodo/.shared/pubkey.txt ]; then export $(cat /home/komodo/.shared/pubkey.txt); fi' >> ~/.bashrc

#RUN echo 'if [ -f /home/komodo/.shared/pubkey.txt ]; then source /home/komodo/.shared/pubkey.txt; fi' >> ~/.bashrc

ADD ./bin /usr/local/bin
COPY docker-entrypoint.sh /usr/local/bin/
ENTRYPOINT ["docker-entrypoint.sh"]


#CMD ["/komodo/src/komodod"]
CMD ["komodo_oneshot"]

EXPOSE 7770 7771
