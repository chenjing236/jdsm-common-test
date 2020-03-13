import unittest
from ConfigParser import SafeConfigParser
import time
import os


class BaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        print("get update_env time is %s" % time.time())
        self.get_env()
        self.parser = SafeConfigParser()
        if self.env in 'pro':
            self.parser.read("etc/config.ini")
        if self.env in 'stag':
            self.parser.read("etc/config_stag.ini")

    def tearDown(self):
        os.remove(r'update_env.txt')

    def get_env(self):
        with open('update_env.txt', "r") as f:
            line = f.readlines()
        _, self.env = line[0].strip().split(':')

    def get_product_ingress_domain(self):
        self.productpage_ingress = self.parser.get('discovery', 'productpage_ingress')
        print(self.productpage_ingress)

    def get_product_lb_domain(self):
        self.productpage_lb = self.parser.get('discovery', 'productpage_lb')
        print(self.productpage_lb)

    def get_envoy_info(self):
        self.envoyctl_host = self.parser.get('envoyctl', 'envoyctl_host')
        self.envoyctl_host_user = self.parser.get('envoyctl', 'envoyctl_host_user')
        self.envoyctl_host_password = self.parser.get('envoyctl', 'envoyctl_host_password')
        self.proxy_server_list = self.parser.get('envoyctl', 'proxy_server_list').split(',')
        self.proxy_server_port = self.parser.get('envoyctl', 'proxy_server_port')
        self.proxy_address = self.parser.get('envoyctl', 'proxy_address')

        print(self.envoyctl_host)
        print(self.envoyctl_host_user)
        #print(self.envoyctl_host_password)
        print(self.proxy_server_list)
        print(self.proxy_server_port)
        print(self.proxy_address)

    def get_load_balancing_info(self):
        re_count = self.parser.get('load_balancing', 'request_count')
        sla = self.parser.get('load_balancing', 'lb_sla')

        return re_count, sla

    def get_host_routing_info(self):
        self.productpage_hosts = self.parser.get('host_routing', 'productpage_host').split(',')
        self.productpage_user = self.parser.get('host_routing', 'host_user')
        self.productpage_password = self.parser.get('host_routing', 'host_password')

        print(self.productpage_hosts)
        print(self.productpage_user)
        #print(self.productpage_password)

    def get_failure_recovery_info(self):
        data_center = self.parser.get('failure_recovery', 'data_center')
        failure_count = self.parser.get('failure_recovery', 'failure_count')

        return data_center, failure_count

    def get_skywing_info(self):
        self.token = self.parser.get('skywing', 'token')

    def get_jdk_info(self):
        self.ak = self.parser.get('jdk', 'ak')
        self.sk = self.parser.get('jdk', 'sk')
        self.domain = self.parser.get('jdk', 'jdk_domain')

    def get_header_rule_info(self):
        self.request_count = self.parser.get('header_rule', 'request_count')
        self.header = self.parser.get('header_rule', 'header')
        self.user = self.parser.get('header_rule', 'user')
        self.user_rule = self.parser.get('header_rule', 'user_rule')
        self.default_rule = self.parser.get('header_rule', 'default_rule')
        self.env = self.parser.get('header_rule', 'jdk_env')
        self.app_name = self.parser.get('header_rule', 'jdk_app_name')

        print("self.request_count=%s, self.header=%s, self.user=%s, "
              "self.user_rule=%s, self.default_rule=%s" % (self.request_count,
                                                           self.header,
                                                           self.user,
                                                           self.user_rule,
                                                           self.default_rule))


if __name__ == "__main__":
    unittest.main()







