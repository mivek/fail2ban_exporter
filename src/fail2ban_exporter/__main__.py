import sys
import os

from fail2ban_exporter.model.fail2ban_collector import Fail2BanCollector
from prometheus_client import start_http_server
from prometheus_client.core import REGISTRY
from time import sleep

PORT = int(os.getenv('FAIL2BAN_EXPORTER_PORT', 9921))

if __name__ == '__main__':
    args = sys.argv[1:]
    socket_path = "/var/run/fail2ban/fail2ban.sock"
    if args and args[0] == '--socket-dir' and args[1]:
        socket_path = os.path.join(args[1], 'fail2ban.sock')
    start_http_server(PORT)
    print('The exporter is now running on port ', PORT)
    REGISTRY.register(Fail2BanCollector(socket_path))
    while True:
        sleep(10)
