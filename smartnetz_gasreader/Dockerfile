ARG BUILD_FROM
FROM $BUILD_FROM

RUN apk add --no-cache python3 py3-pip
RUN pip3 install --no-cache-dir paho-mqtt

COPY run.sh /run.sh
COPY discovery.py /app/discovery.py
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
