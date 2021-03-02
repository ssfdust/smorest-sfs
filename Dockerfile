FROM python3:latest

ENV FLASK_ENV="production" \
      FLASK_APP="/Application/smorest_sfs/app.py" \
      HOST="0.0.0.0" \
      PYTHONPYCACHEPREFIX="/pycache" \
      LOGURU_LEVEL=INFO \
      PUID=1000 \
      PGID=1000 \
      APP="web"

COPY requirements.txt /

RUN apt-get update && apt-get install --assume-yes --no-install-recommends \
        wget \
        zlibc \
        libjpeg-dev \
        libfreetype6 \
        libfreetype6-dev \
        gcc \
    && pip install --no-cache-dir -r requirements.txt \
    && wget https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh -O /usr/bin/wait-for-it \
    && chmod 755 /usr/bin/wait-for-it \
    && mkdir Application \
    && apt-get purge --assume-yes --auto-remove -o APT::AutoRemove::RecommendsImportant=false gcc \
	&& rm -rf /var/lib/apt/lists/*

RUN addgroup --gid ${PGID} webapp && \
    useradd -d /Application/ --uid ${PUID} --gid ${PGID} webapp

WORKDIR /Application/

USER webapp

ENV PATH "$PATH:/python/bin"

CMD ["/bin/sh", "scripts/initapp.sh"]
