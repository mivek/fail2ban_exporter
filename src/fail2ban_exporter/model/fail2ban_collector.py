
from prometheus_client.core import (
    GaugeMetricFamily,
    CounterMetricFamily
)

from fail2ban_exporter.model.csocket import CSocket


class Fail2BanCollector(object):

    def __init__(self, socket_path) -> None:
        self._socket = CSocket(socket_path)

    def collect(self):
        status = self._socket.send(['status'])[1]
        jail_count = int(status[0][1])
        jail_list = status[1][1].split(', ')

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

        for jail in jail_list:
            state = get_jail_state(self._socket, jail)
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


def get_jail_state(socket: CSocket, jail: str) -> dict:
    jail_state = socket.send(['status', jail])[1]
    currently_failed = int(jail_state[0][1][0][1])
    total_failed = int(jail_state[0][1][1][1])
    currently_banned = int(jail_state[1][1][0][1])
    total_banned = int(jail_state[1][1][1][1])

    return {'currently_failed': currently_failed,
            'total_failed': total_failed,
            'currently_banned': currently_banned,
            'total_banned': total_banned
            }


def clean_name(jail: str) -> str:
    return jail.strip().replace(' ', '_').replace('-', '_').lower()
