import subprocess
import unittest
from unittest.mock import Mock, patch

from src.fail2ban_exporter.__main__ import clean_name, \
    get_jail_number, get_jail_state, get_jails


class TestFail2BanExporter(unittest.TestCase):

    def test_get_jail_number(self):
        input = """Status
                |- Number of jail:      7
                `- Jail list:   apache-log4j, nginx-badbots, \
                    nginx-http-auth, nginx-nohome, nginx-noproxy, \
                        nginx-noscript, sshd """

        self.assertEqual('7', get_jail_number(input))

    def test_get_jails(self):
        input = """Status
                |- Number of jail:      7
                `- Jail list:   apache-log4j, nginx-badbots, \
                    nginx-http-auth, nginx-nohome, nginx-noproxy, \
                        nginx-noscript, sshd """

        jail_list = get_jails(input)
        self.assertEqual(7, len(jail_list))

    def test_clean_name(self):
        self.assertEqual('nginx_http_auth', clean_name('nginx-http-auth'))

    @patch('subprocess.run')
    def test_get_jail_state(self, mock_run: Mock):
        value = """
        Status for the jail: sshd
            |- Filter
            |  |- Currently failed: 0
            |  |- Total failed:     55
            |  `- File list:        /var/log/nginx/access.log
            `- Actions
            |- Currently banned: 1
            |- Total banned:     1
            `- Banned IP list:   10.0.0.1
        """
        process = subprocess.CompletedProcess(
            '/usr/bin/fail2ban-client status sshd',
            0,
            stdout=value
        )
        mock_run.return_value = process
        result = get_jail_state('sshd')
        self.assertTrue(mock_run.called)
        mock_run.assert_called_once_with(
            ['/usr/bin/fail2ban-client', 'status', 'sshd'],
            text=True,
            capture_output=True,
            check=True,
            encoding='utf-8'
        )
        self.assertEqual('0', result['currently_failed'])
        self.assertEqual('55', result['total_failed'])
        self.assertEqual('1', result['currently_banned'])
        self.assertEqual('1', result['total_banned'])


if __name__ == '__main__':
    unittest.main()
