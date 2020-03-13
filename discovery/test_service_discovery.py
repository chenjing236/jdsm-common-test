import logging
import requests
import test_base


class DiscoveryTest(test_base.BaseTest):

    @classmethod
    def setUpClass(cls):
        logging.debug('suite begin')

    @classmethod
    def tearDownClass(cls):
        logging.debug('suite end')

    def setUp(self):
        test_base.BaseTest.setUp(self)
        self.get_product_ingress_domain()
        self.get_product_lb_domain()

    def tearDown(self):
        pass

    def test_ingress_domain_connection(self):
        url = 'http://' + self.productpage_ingress + '/productpage'
        r = requests.get(url, verify=True)
        print(r.status_code)

        self.assertEqual(r.status_code, 200, "Request ingress domain fail, "
                                           "response code is %s" % r.status_code)

    def test_lb_domain_connection(self):
        url = 'http://' + self.productpage_lb
        r = requests.get(url, verify=True)

        print(r.status_code)

        self.assertEqual(r.status_code, 200, "Request lb domain fail, "
                                             "response code is %s" % r.status_code)




