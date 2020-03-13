import logging
import requests
import test_base


class FailureRecoveryTest(test_base.BaseTest):

    @classmethod
    def setUpClass(cls):
        logging.debug('suite begin')

    @classmethod
    def tearDownClass(cls):
        logging.debug('suite end')

    def setUp(self):
        test_base.BaseTest.setUp(self)
        self.get_product_ingress_domain()
        self.get_skywing_info()
        self.data_center, self.failure_count = self.get_failure_recovery_info()
        print(self.data_center, self.failure_count)

    def tearDown(self):
        pass

    def test_failures_recovery(self):
        live_instance = 0
        dead_instance = 0
        failure_count = 0

        # Verify instance status
        instance_url = 'http://ark.jd.com/deploy/api/v1/instance?page_size=10&page=1&app_id=1657&group_id=&state=&' \
                       'sort=desc&order_by=group_id&ip:like='
        headers = {"Content-Type": "application/json", "token": self.token}
        r = requests.get(instance_url, headers=headers, verify=True)
        response = r.json()

        for instance in response[u'data'][u'item']:
            # print(len(response[u'data'][u'item']))
            if self.data_center in instance[u'AppInstance'][u'pod_name']:
                print(instance[u'AppInstance'][u'pause'])
                if instance[u'AppInstance'][u'pause'] == 0:
                    live_instance += 1
                else:
                    dead_instance += 1

        if dead_instance == 0:
            print("No instance is down.")
            return

        if dead_instance / (live_instance + dead_instance) > 0.5:
            self.fail("More than 50% instances down, failure recovery cannot work in this case.")

        # Send request in loop until get response code 503 5 times
        url = 'http://' + self.productpage_ingress + '/health'
        for i in range(int(90)):
            if failure_count >= self.failure_count:
                break

            r = requests.get(url, verify=True)
            if r.status_code != 200:
                failure_count += 1
        print("Failed Request count is %s" % failure_count)

        for i in range(int(20)):
            r = requests.get(url, verify=True)
            print("The response code is %s" % r.status_code)
            self.assertEqual(r.status_code, 200, "Invoke API health via ingress domain fail, "
                                                 "response code is %s" % r.status_code)



