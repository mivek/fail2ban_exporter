import re
import os
import subprocess
from time import sleep
from prometheus_client import start_http_server
from prometheus_client.core import (
    GaugeMetricFamily,
    CounterMetricFamily,
    REGISTRY
)

exec_path = os.path.join('/usr/bin/')
PORT = int(os.getenv('FAIL2BAN_EXPORTER_PORT', 9921))
BASE_COMMAND = os.path.join(os.getenv('EXEC_PATH',
                                      '/usr/bin/'), 'fail2ban-client')
STATUS = 'status'


class Fail2BanCollector(object):
    def collect(self):
        global_status = get_status()
        jail_count = int(get_jail_number(global_status))
        yield GaugeMetricFamily('fail2ban_jail_count',
                                'Number of active jails',
                                value=jail_count)
        counter_total_failed = CounterMetricFamily('fail2ban_failed',
                                                   'Total number of failures',
                                                   labels=['jail'])
        gauge_current_failed = GaugeMetricFamily('fail2ban_currently_failed',
                                                 'Current number of failures',
                                                 labels=['jail'])
        counter_total_banned = CounterMetricFamily('fail2ban_banned',
                                                   'Number of banned IPs',
                                                   labels=['jail'])
        gauge_current_banned = GaugeMetricFamily('fail2ban_currently_banned',
                                                 'Current number '
                                                 'of banned IPs',
                                                 labels=['jail'])

        for jail in get_jails(global_status):
            state = get_jail_state(jail)
            counter_total_failed.add_metric([clean_name(jail)],
                                            int(state['total_failed']))
            gauge_current_failed.add_metric([clean_name(jail)],
                                            int(state['currently_failed']))
            counter_total_banned.add_metric([clean_name(jail)],
                                            int(state['total_banned']))
            gauge_current_banned.add_metric([clean_name(jail)],
                                            int(state['currently_banned']))

        yield counter_total_failed
        yield gauge_current_failed
        yield counter_total_banned
        yield gauge_current_banned


def get_status(jail: str = None):
    cmd = [BASE_COMMAND, STATUS]
    if jail:
        cmd.append(jail)
    return execute_command(cmd)


def get_jail_number(status_result: str):
    p = re.compile(r'.*Number of jail: \s*(\d+)', flags=re.M)
    m = p.search(status_result)
    return m.group(1)


def get_jails(status_result: str):
    p = re.compile(r'.*Jail list: \s*(.*)\s', flags=re.M)
    m = p.search(status_result)
    jails = m.group(1)
    return jails.split(', ')


def get_jail_state(jail: str) -> dict:
    currently_failed_pattern = re.compile(r'Currently failed:\s*(\d+)',
                                          flags=re.M)
    total_failed_pattern = re.compile(r'Total failed:\s*(\d+)',
                                      flags=re.M)
    currently_banned_pattern = re.compile(r'Currently banned:\s*(\d+)',
                                          flags=re.M)
    total_banned_pattern = re.compile(r'Total banned:\s*(\d+)',
                                      flags=re.M)

    cmd = [BASE_COMMAND, STATUS, jail]
    output = execute_command(cmd)
    currently_failed_match = currently_failed_pattern.search(output)
    total_failed_match = total_failed_pattern.search(output)
    currently_banned_match = currently_banned_pattern.search(output)
    total_banned_match = total_banned_pattern.search(output)

    return {'currently_failed': currently_failed_match.group(1),
            'total_failed': total_failed_match.group(1),
            'currently_banned': currently_banned_match.group(1),
            'total_banned': total_banned_match.group(1)
            }


def clean_name(jail: str) -> str:
    return jail.strip().replace(' ', '_').replace('-', '_').lower()


def execute_command(cmd: list):
    return subprocess.run(cmd, text=True,
                          capture_output=True,
                          check=True,
                          encoding='utf-8').stdout \
                              .replace('\n', ' ') \
                              .replace('\t', ' ')


if __name__ == '__main__':
    start_http_server(PORT)
    print('The exporter is now running on port ', PORT)
    REGISTRY.register(Fail2BanCollector())
    while True:
        sleep(10)
