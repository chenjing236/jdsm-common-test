import unittest
import logging
from remote import RemoteRunner
import test_base


class ProxyConfigTest(test_base.BaseTest):

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
        self.proxy_address = self.proxy_address

    def tearDown(self):
        pass

    def test_get_proxy_config(self):
        cmd = "envoyctl proxy-config serverinfo %s" % self.proxy_address
        result = self.session.run(cmd)

        print(result)
        self.assertTrue(result.exit_status == 0, "Execute envoyctl proxy-config fail.")


if __name__ == "__main__":
    unittest.main()
