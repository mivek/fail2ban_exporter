FROM python:alpine3.16

RUN pip install prometheus-client

COPY ./src/fail2ban_exporter /fail2ban_exporter

ENTRYPOINT [ "python", "-m", "fail2ban_exporter" ]

EXPOSE 9921/tcp
VOLUME [ "/var/run/fail2ban" ]