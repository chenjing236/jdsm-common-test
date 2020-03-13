import logging
import requests
import time

from remote import RemoteRunner
import test_base


class VirtualServiceTest(test_base.BaseTest):

    @classmethod
    def setUpClass(cls):
        logging.debug('suite begin')

    @classmethod
    def tearDownClass(cls):
        logging.debug('suite end')

    def setUp(self):
        test_base.BaseTest.setUp(self)
        self.get_product_ingress_domain()
        self.get_host_routing_info()

    def tearDown(self):
        pass

    def _get_special_label_in_log(self, cmd):
        results = []
        for host in self.productpage_hosts:
            session = RemoteRunner(client='ssh', host=host, username=self.productpage_user,
                                   port="22", password=self.productpage_password)
            result = session.run(cmd)
            results.append(result.stdout)
        return results

    def test_host_routing(self):
        befores = []
        afters = []
        cmd = "cat /export/Logs/mesh.log | grep health | wc -l"

        befores = self._get_special_label_in_log(cmd)

        url = 'http://' + self.productpage_ingress + '/health'
        for i in range(int(21)):
            r = requests.get(url, verify=True)
            print("The health response code is %s" % r.status_code)

            self.assertEqual(r.status_code, 200, "Invoke API health via ingress domain fail, "
                                             "response code is %s" % r.status_code)
        time.sleep(10)
        afters = self._get_special_label_in_log(cmd)

        for i in range(len(afters)):
            print("before is %s; after is %s" % (befores[i], afters[i]))
            self.assertTrue((int)(afters[i]) >= (int)(befores[i]))

