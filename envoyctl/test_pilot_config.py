import unittest
import logging
from remote import RemoteRunner
import test_base


class PilotConfigTest(test_base.BaseTest):

    @classmethod
    def setUpClass(cls):
        logging.debug('suite begin')

    @classmethod
    def tearDownClass(cls):
        logging.debug('suite end')

    def setUp(self):
        test_base.BaseTest.setUp(self)
        self.get_envoy_info()
        self.session = RemoteRunner(client='ssh', host=self.envoyctl_host,
                                    username=self.envoyctl_host_user, port="22", password=self.envoyctl_host_password)
        self.proxy_server_list = self.proxy_server_list
        self.port = self.proxy_server_port

    def tearDown(self):
        pass

    def test_create_pilot_config(self):
        proxy_list = ''
        for ip in self.proxy_server_list:
            proxy_list += ' ' + ip + (":%s" % self.port)

        cmd = "envoyctl pilot-config " + proxy_list
        print(cmd)

        result = self.session.run(cmd)

        print(result)
        self.assertTrue(result.exit_status == 0, "Execute envoyctl pilot-config fail.")


if __name__ == "__main__":
    unittest.main()






