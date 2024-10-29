FROM debian:bullseye-slim
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Shanghai
WORKDIR /root
RUN apt update && \
    apt-get install -y wget bsdmainutils xdg-utils libxslt1.1 xvfb libqt5gui5 && \
    apt-get clean -y && rm -rf /var/lib/apt/lists/*
RUN apt update && \
    wget https://wdl1.cache.wps.cn/wps/download/ep/Linux2019/10920/wps-office_11.1.0.10920_amd64.deb && \
    apt install -y ./wps-office_11.1.0.10920_amd64.deb && \
    rm -rf ./wps-office_11.1.0.10920_amd64.deb && \
    mkdir -p /root/.config/Kingsoft/ && \
    apt-get clean -y && rm -rf /var/lib/apt/lists/*  && \
    echo '[6.0]' >>  /root/.config/Kingsoft/Office.conf && \
    echo 'wpsoffice\Application%20Settings\AppComponentMode=prome_independ'  >>  /root/.config/Kingsoft/Office.conf && \
    echo 'wpsoffice\Application%20Settings\AppComponentModeInstall=prome_independ'  >>  /root/.config/Kingsoft/Office.conf && \
    echo 'common\AcceptedEULA=true'   >>  /root/.config/Kingsoft/Office.conf
