import unittest
import logging
from remote import RemoteRunner
import test_base


class ProxyListTest(test_base.BaseTest):

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

    def tearDown(self):
        pass

    def test_list_proxy_servers(self):
        cmd = "envoyctl proxy-list"
        result = self.session.run(cmd)

        print(result)
        self.assertTrue(result.exit_status == 0, "Execute envoyctl proxy-list fail.")

    def test_list_proxy_servers_details(self):
        cmd = "envoyctl proxy-list -d"
        result = self.session.run(cmd)

        print(result)
        self.assertTrue(result.exit_status == 0, "Execute envoyctl proxy-list details fail.")


if __name__ == "__main__":
    unittest.main()

