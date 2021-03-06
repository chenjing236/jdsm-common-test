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


class DescribeDependServicesRequest(JDCloudRequest):
    """
    查询某应用对外依赖服务的信息

    """

    def __init__(self, parameters, header=None, version="v1"):
        super(DescribeDependServicesRequest, self).__init__(
            '/envs/{env}/apps/{appId}/dependservices', 'GET', header, version)
        self.parameters = parameters


class DescribeDependServicesParameters(object):

    def __init__(self, env, appId, ):
        """
        :param env: 环境名，pre/product
        :param appId: 应用ID
        """

        self.env = env
        self.appId = appId

