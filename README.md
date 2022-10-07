# Fail2Ban-exporter


Fail2ban exporter is an exporter for Prometheus.
The exporter exposes metrics on port 9921.

## Requirements 

- Python 3: Only required if you execute the script. 

# Installation

## Python script

Check the latest version.

Download the latest version.

Unarchive it

```
wget https://github.com/mivek/fail2ban_exporter/releases/download/{{version}}/fail2ban_exporter-{{version}}.tar.gz
tar -xzf fail2ban_exporter-{{version}}.tar.gz
```

Install the dependencies
Launch the script

```
python -m pip install prometheus_client
python fail2ban_exporter-0.0.2/src/fail2ban_exporter &
```



## Python executable

Check the latest version

Download the latest version of the executable

Unarchive it.

```
wget https://github.com/mivek/fail2ban_exporter/releases/download/{{ version }}/fail2ban_exporter_executable-{{ version }}.tar.gz
tar -xzf fail2ban_exporter_executable-{{version}}.tar.gz
```

Set the execution mod to the executable and run it as the user running fail2ban-client.

```
chmod ug+x fail2ban_exporter_executable-{{ version }}/fail2ban_exporter
./fail2ban_exporter &
```

## Docker image

It is possible to run the exporter as a docker container.
The parent folder of the fail2ban socket needs to be mapped.

**Note**: Do not map the socket itself as it is destroyed whenever fail2ban is stopped.

### Docker run

```
docker run -d \
--name "fail2ban_exporter" \
-v /var/run/fail2ban:/var/run/fail2ban:ro
- p "9921:9921"
ghcr.io/mivek/fail2ban_exporter:latest
```

### Docker compose

```(yaml)
services:
    fail2ban_exporter:
        image: ghcr.io/mivek/fail2ban_exporter:latest
        ports:
            - "9921:9921"
        volumes:
            - /var/run/fail2ban:/var/run/fail2ban:ro
```

# Metrics

The following metrics are exposed:

| Name                      | Type    |  Description                                                 |
|-----------------------    |-------  |--------------------------------------------------------------|
| fail2ban_jail_count       | Gauge   | Number of active jails                                       |
| fail2ban_failed_total     | Counter | Total number of failures. Labelled by the name of the jail   |
| fail2ban_currently_failed | Gauge   | Current number of failures. Labelled by the name of the jail |
| fail2ban_currently_banned | Gauge   | Current number of bans. Labelled by the name of the jail     |
| fail2ban_banned_total     | Counter | Total number of bans. Labelled by the name of the jail       |


# Environment variable

- FAIL2BAN_EXPORTER_PORT . If specified the exporter will run on this port.

