FROM debian_wps:base
ARG DEBIAN_FRONTEND noninteractive
WORKDIR /wps2pdf
ADD fonts  /usr/share/fonts
ADD entrypoint.sh  /
ADD sources.list  /etc/apt
ADD dummy.conf /etc/X11/xorg.conf.d
RUN apt update -y  && apt install libqt5xml5 python3 python3-pip   xserver-xorg-video-dummy locales procps  -y
RUN python3 -m pip --no-cache-dir  install pywpsrpc flask -i https://pypi.tuna.tsinghua.edu.cn/simple/  \
    && fc-cache -v \
    && chmod +x /entrypoint.sh \
    && echo "zh_CN.UTF-8 UTF-8"  >/etc/locale.gen  \
    && locale-gen \
    && update-locale LANG=zh_CN.UTF-8 \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean -y
ADD converter.py   ./
EXPOSE 9000
ENV LANG=zh_CN.UTF-8 \
    LANGUAGE zh_CN:zh \
    LC_ALL zh_CN.UTF-8 \
    DISPLAY=:0
ENTRYPOINT [ "/entrypoint.sh" ]
