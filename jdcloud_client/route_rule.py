from jdcloud_sdk.core.credential import Credential
from jdcloud_sdk.core.config import Config
from jdcloud_sdk.core.const import SCHEME_HTTP
from jdcloud_sdk.services.jdmesh.client.JdmeshClient import JdmeshClient
from jdcloud_sdk.services.jdmesh.apis.DescribeDestinationRuleRequest import *
from jdcloud_sdk.services.jdmesh.apis.UpdateRouteRuleRequest import *


class JdmeshTestObj(object):

    def __init__(self, ak, sk, domain):
        if ak is None:
            raise ValueError("Ak should NOT be None.")
        if sk is None:
            raise ValueError("Ak should NOT be None.")
        if domain is None:
            raise ValueError("Domain should NOT be None.")
        self.create_client(ak, sk, domain)

    def create_client(self, ak, sk, domain):
        access_key = ak
        secret_key = sk
        self.credential = Credential(access_key, secret_key)
        config = Config(domain, scheme=SCHEME_HTTP)
        self.client = JdmeshClient(self.credential, config)

    def testDescribeDestinationRule(self, env, app_name):
        parameters = DescribeDestinationRuleParameters(env, app_name)
        request = DescribeDestinationRuleRequest(parameters)

        resp = self.client.send(request)
        print("result is %s" % resp.error)

    def testUpdateRouteRuleRequest(self, env, app_name, rule_header,
                                   user, user_rule, default_rule):
        print("user_rule is %s" % user_rule)
        header = {}
        header[rule_header] = user
        header_policy = {}
        header_policy['header'] = header
        header_policy['subsetId'] = user_rule
        header_policy_list = []
        header_policy_list.append(header_policy)
        routeRuleSpec = {}
        routeRuleSpec['appId'] = app_name
        routeRuleSpec['defaultRoute'] = default_rule
        routeRuleSpec['headerPolicy'] = header_policy_list
        routeRuleSpec['hostPolicy'] = None
        routeRuleSpec['weightPolicy'] = None

        parameters = UpdateRouteRuleParameters(env, app_name, routeRuleSpec)
        request = UpdateRouteRuleRequest(parameters)

        resp = self.client.send(request)
        print(resp.error)

    def testDeleteRouteRuleRequest(self, env, app_name, default_rule):
        routeRuleSpec = {}
        routeRuleSpec['appId'] = app_name
        routeRuleSpec['defaultRoute'] = default_rule
        routeRuleSpec['headerPolicy'] = None
        routeRuleSpec['hostPolicy'] = None
        routeRuleSpec['weightPolicy'] = None

        parameters = UpdateRouteRuleParameters(env, app_name, routeRuleSpec)
        request = UpdateRouteRuleRequest(parameters)

        resp = self.client.send(request)
        print(resp.error)


if __name__ == "__main__":
    obj = JdmeshTestObj('2FFA9E233949CAFA49B5CBAE9DB3A151',
                        '9D561D6F3430FA91A4899F8C546C27D0',
                        'apigw-kong-internal.default.mesh.jdcloud.com:8000')
    obj.testDescribeDestinationRule()
    obj.testDeleteRouteRuleRequest()

