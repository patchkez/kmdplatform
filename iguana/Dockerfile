#FROM komodo-base:latest
FROM ubuntu:16.04

LABEL maintainer="Emmanux <infra@komodo.rocks>"

#ARG BUILD_PACKAGES

ENV USER_ID ${USER_ID:-3004}
ENV GROUP_ID ${GROUP_ID:-3004}
ENV SHARED_GROUP_ID ${SHARED_GROUP_ID:-3005}

RUN groupadd -g ${GROUP_ID} iguana && \
    groupadd -g ${SHARED_GROUP_ID} shared && \
    useradd -u ${USER_ID} -g iguana -G shared -s /bin/bash -m -d /home/iguana iguana

ENV BUILD_PACKAGES="git libcurl4-openssl-dev build-essential libnanomsg-dev cmake libssl-dev"
RUN apt update && \
     apt install -y $BUILD_PACKAGES && \
     apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


RUN git clone https://github.com/nanomsg/nanomsg && \
    cd nanomsg && \
    cmake . && \
    make && \
    make install && \
    ldconfig

USER iguana
WORKDIR /home/iguana
RUN mkdir -p /home/iguana/.shared
RUN mkdir -p /home/iguana/.komodo

RUN whoami && ls -ltrh /home && touch /home/iguana/test && ls -ltrh /home/iguana/test

RUN git clone https://github.com/jl777/SuperNET && \
    cd SuperNET/iguana && \
    git checkout beta && \
    ./m_LP
# OR????
#git clone https://github.com/jl777/SuperNET; cd SuperNET; ./m_onetime m_unix;



#RUN apt remove --purge -y $BUILD_PACKAGES $(apt-mark showauto) && \
#    rm -rf /var/lib/apt/lists/* && \
#    rm -rf /komodo/depends

#RUN useradd -u 3003 -m komodod && \
#RUN mv /root/.zcash-params /home/komodod/ && \
#    chown -R komodod:komodod /home/komodod/.zcash-params

#ENV PATH="/komodo/src/:${PATH}"
#USER iguana
#WORKDIR /home/iguana
#RUN mkdir ~/.komodo 

VOLUME ["/home/iguana/.iguana"] 

# We need to mount it in order to share pubkey with komodo and bitcoin
VOLUME ["/home/iguana/.shared"] 

# We need access to komodo coins
VOLUME ["/home/iguana/.komodo"]

ADD ./bin /usr/local/bin
COPY docker-entrypoint.sh /usr/local/bin/
#ENTRYPOINT ["docker-entrypoint.sh"]

#CMD ["/komodo/src/komodod"]
#CMD ["komodo_oneshot"]
USER root
RUN apt update &&  apt install -y curl
USER iguana

# RUN cd ~/SuperNET/iguana && ln -s /home/iguana/.iguana/wp wp

#CMD ["/home/iguana/SuperNET/agents/iguana"]

ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["iguana_oneshot"]


EXPOSE 7776 7778
