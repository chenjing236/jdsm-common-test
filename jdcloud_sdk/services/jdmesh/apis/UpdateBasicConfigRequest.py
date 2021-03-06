# coding=utf8

# Copyright 2018 JDCLOUD.COM
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# NOTE: This class is auto generated by the jdcloud code generator program.

from jdcloud_sdk.core.jdcloudrequest import JDCloudRequest


class UpdateBasicConfigRequest(JDCloudRequest):
    """
    修改应用基本配置，是否开启网格白名单和被动健康检查及其参数。

    """

    def __init__(self, parameters, header=None, version="v1"):
        super(UpdateBasicConfigRequest, self).__init__(
            '/envs/{env}/apps/{appId}/basicconfig', 'POST', header, version)
        self.parameters = parameters


class UpdateBasicConfigParameters(object):

    def __init__(self, env, appId, enableWhiteListCheck, enableNegativeHealthCheck, ):
        """
        :param env: 环境名，pre/product
        :param appId: 应用ID
        :param enableWhiteListCheck: 启用网格白名单检查
        :param enableNegativeHealthCheck: 启用被动健康检查
        """

        self.env = env
        self.appId = appId
        self.enableWhiteListCheck = enableWhiteListCheck
        self.enableNegativeHealthCheck = enableNegativeHealthCheck
        self.healthCheckParameters = None
        self.serviceEntries = None

    def setHealthCheckParameters(self, healthCheckParameters):
        """
        :param healthCheckParameters: (Optional) 被动健康检查参数
        """
        self.healthCheckParameters = healthCheckParameters

    def setServiceEntries(self, serviceEntries):
        """
        :param serviceEntries: (Optional) 网格外部服务依赖项
        """
        self.serviceEntries = serviceEntries

