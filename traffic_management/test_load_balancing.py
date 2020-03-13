import logging
import requests
import test_base


class LoadBalancingTest(test_base.BaseTest):

    @classmethod
    def setUpClass(cls):
        logging.debug('suite begin')

    @classmethod
    def tearDownClass(cls):
        logging.debug('suite end')

    def setUp(self):
        test_base.BaseTest.setUp(self)
        self.get_product_ingress_domain()
        self.re_count, self.sla = self.get_load_balancing_info()

    def tearDown(self):
        pass

    def test_load_balancing(self):
        url = 'http://' + self.productpage_ingress + '/api/v1/products/0/reviews'
        review1, review2, review3 = 0, 0, 0

        for i in range(int(self.re_count)):
            r = requests.get(url, verify=True)
            response = r.json()
            try:
                if response[u'reviews'][0][u'rating'][u'color'] in 'red':
                    review3 += 1
                if response[u'reviews'][0][u'rating'][u'color'] in 'black':
                    review2 += 1
            except KeyError:
                review1 += 1
        print('review1=%s; review2=%s; review3=%s' % (review1, review2, review3))

        self.assertTrue(abs(review1 - review2) / review1 < float(self.sla),
                        "The requests to review1 and the requests to review2 is greater then 10%.")
        self.assertTrue(abs(review1 - review3) / review1 < float(self.sla),
                        "The requests to review1 and the requests to review3 is greater then 10%.")




