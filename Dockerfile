FROM alpine:3.22.1
LABEL maintainer="Paul Bowen-Huggett <paulhuggett@mac.com>"

WORKDIR /app

# Install python
ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python

# Now the ktransfer tool
RUN mkdir /ktransfer
COPY ktransfer.py /app/ktransfer.py
COPY entry.py /app/entry.py
ENTRYPOINT [ "/app/entry.py" ]
