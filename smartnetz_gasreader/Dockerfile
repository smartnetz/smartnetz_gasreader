ARG BUILD_FROM
FROM $BUILD_FROM

# Python + paho-mqtt aus Alpine-Paketen installieren
RUN apk add --no-cache \
      python3 \
      py3-paho-mqtt

# Skripte kopieren
COPY run.sh /run.sh
COPY discovery.py /app/discovery.py
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
