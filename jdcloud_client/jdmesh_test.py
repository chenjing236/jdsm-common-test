import unittest
import time
from jdcloud_sdk.core.credential import Credential
from jdcloud_sdk.core.config import Config
from jdcloud_sdk.core.const import SCHEME_HTTP
from jdcloud_sdk.services.jdmesh.client.JdmeshClient import JdmeshClient
from jdcloud_sdk.services.jdmesh.apis.DescribeDestinationRuleRequest import *
from jdcloud_sdk.services.jdmesh.apis.UpdateRouteRuleRequest import *

class JdmeshTest(unittest.TestCase):

    def setUp(self):
        access_key = '2FFA9E233949CAFA49B5CBAE9DB3A151'
        secret_key = '9D561D6F3430FA91A4899F8C546C27D0'
        self.credential = Credential(access_key, secret_key)
        config = Config('apigw-kong-internal.default.mesh.jdcloud.com:8000', scheme=SCHEME_HTTP)
        #self.client = VmClient(self.credential, config)
        self.client = JdmeshClient(self.credential, config)

    def tearDown(self):
        pass

    def testDescribeDestinationRule(self):
        parameters = DescribeDestinationRuleParameters('product', 'reviews')
        request = DescribeDestinationRuleRequest(parameters)

        resp = self.client.send(request)
        self.assertTrue(resp.error is None)

    def testUpdateRouteRuleRequest(self):
        header = {}
        header['end-user'] = 'jason'
        header_policy = {}
        header_policy['header'] = header
        header_policy['subsetId'] = 'v2'
        header_policy_list = []
        header_policy_list.append(header_policy)
        routeRuleSpec = {}
        routeRuleSpec['appId'] = 'reviews'
        routeRuleSpec['defaultRoute'] = 'v3'
        routeRuleSpec['headerPolicy'] = header_policy_list
        routeRuleSpec['hostPolicy'] = None
        routeRuleSpec['weightPolicy'] = None

        parameters = UpdateRouteRuleParameters('pre', 'reviews', routeRuleSpec)
        request = UpdateRouteRuleRequest(parameters)

        resp = self.client.send(request)
        self.assertTrue(resp.error is None)

    def testDeleteRouteRuleRequest(self):
        routeRuleSpec = {}
        routeRuleSpec['appId'] = 'reviews'
        routeRuleSpec['defaultRoute'] = 'v3'
        routeRuleSpec['headerPolicy'] = None
        routeRuleSpec['hostPolicy'] = None
        routeRuleSpec['weightPolicy'] = None

        parameters = UpdateRouteRuleParameters('pre', 'reviews', routeRuleSpec)
        request = UpdateRouteRuleRequest(parameters)

        resp = self.client.send(request)
        self.assertTrue(resp.error is None)


if __name__ == "__main__":
    unittest.main()
