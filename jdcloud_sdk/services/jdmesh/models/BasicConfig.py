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


class BasicConfig(object):

    def __init__(self, enableWhiteListCheck, enableNegativeHealthCheck, healthCheckParameters=None, serviceEntries=None):
        """
        :param enableWhiteListCheck:  启用网格白名单检查
        :param enableNegativeHealthCheck:  启用被动健康检查
        :param healthCheckParameters: (Optional) 被动健康检查参数
        :param serviceEntries: (Optional) 网格外部服务依赖项
        """

        self.enableWhiteListCheck = enableWhiteListCheck
        self.enableNegativeHealthCheck = enableNegativeHealthCheck
        self.healthCheckParameters = healthCheckParameters
        self.serviceEntries = serviceEntries
