FROM ssfdust/alpine-python-poetry:latest

ENV FLASK_ENV="production" \
      FLASK_APP="/Application/smorest_sfs/app.py" \
      HOST="0.0.0.0" \
      PYTHONPYCACHEPREFIX="/pycache" \
      LOGURU_LEVEL=INFO \
      PUID=1000 \
      PGID=1000 \
      APP="web"

COPY pyproject.toml poetry.lock /

RUN /entrypoint.sh \
        -a zlib \
        -a libjpeg \
        -a freetype \
        -a postgresql-libs \
        -b zlib-dev \
        -b libffi-dev \
        -b jpeg-dev \
        -b freetype-dev \
        -b postgresql-dev \
    && wget https://raw.githubusercontent.com/eficode/wait-for/master/wait-for -O /usr/bin/waitfor \
    && chmod 755 /usr/bin/waitfor \
    && mkdir Application

RUN addgroup -g ${PGID} webapp && \
    adduser -D -u ${PUID} -G webapp webapp

WORKDIR /Application/

USER webapp

CMD ["/bin/sh", "scripts/initapp.sh"]
