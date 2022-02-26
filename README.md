# Fail2Ban-exporter


Fail2ban exporter is an exporter for Prometheus.

## Requirements 

- Python 3: Only required if you execute the script. 

# Installation

## Python script

TODO

## Python executable

TODO




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

