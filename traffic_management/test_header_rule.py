import logging
import requests
import time
import unittest
import test_base
from jdcloud_client.route_rule import JdmeshTestObj


class HttpHeaderRuleTest(test_base.BaseTest):

    @classmethod
    def setUpClass(cls):
        logging.debug('suite begin')

    @classmethod
    def tearDownClass(cls):
        logging.debug('suite end')

    def setUp(self):
        test_base.BaseTest.setUp(self)
        self.get_product_ingress_domain()
        self.get_jdk_info()
        self.get_header_rule_info()

        self.obj = JdmeshTestObj(self.ak, self.sk, self.domain)

    def tearDown(self):
        pass

    def _get_review_rule(self, url, headers=None):
        review1, review2, review3 = 0, 0, 0

        for i in range(int(self.request_count)):
            r = requests.get(url, headers=headers, verify=True)
            response = r.json()
            try:
                if response[u'reviews'][0][u'rating'][u'color'] in 'red':
                    review3 += 1
                if response[u'reviews'][0][u'rating'][u'color'] in 'black':
                    review2 += 1
            except KeyError:
                review1 += 1
        print('review1=%s; review2=%s; review3=%s' % (review1, review2, review3))

        return review1, review2, review3

    def test_header_rule(self):
        # set up the rule based on http header
        # default: v2
        # header=x-b3-flags:jason
        # policy=v3
        self.obj.testUpdateRouteRuleRequest(self.env, self.app_name,
                                            self.header, self.user,
                                            self.user_rule, self.default_rule)

        time.sleep(20)
        # check review match the default "x-b3-flags" header
        url = 'http://' + self.productpage_ingress + '/api/v1/products/0/reviews'
        review1, review2, review3 = self._get_review_rule(url)
        self.assertTrue(review1 == 0 and review2 == int(self.request_count) and review3 == 0,
                        "The default header rule of review is v2")

        time.sleep(20)
        # check review match jason "x-b3-flags" header
        url = 'http://' + self.productpage_ingress + '/api/v1/products/0/reviews'
        headers = {self.header: self.user}
        review1, review2, review3 = self._get_review_rule(url, headers)
        self.assertTrue(review1 == 0 and review2 == 0 and review3 == int(self.request_count),
                        "Login on with jason, the expect review is v3.")

        # delete http header, load balance recovery
        self.obj.testDeleteRouteRuleRequest(self.env, self.app_name, self.default_rule)


if __name__ == "__main__":
    unittest.main()
