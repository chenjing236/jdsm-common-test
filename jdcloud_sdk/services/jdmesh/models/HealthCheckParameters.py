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


class HealthCheckParameters(object):

    def __init__(self, interval, consecutiveErrors, maxEjectionPercent, baseEjectionTime, ):
        """
        :param interval:  检查间隔
        :param consecutiveErrors:  连续错误次数
        :param maxEjectionPercent:  最大剔除比例
        :param baseEjectionTime:  最小恢复时间
        """

        self.interval = interval
        self.consecutiveErrors = consecutiveErrors
        self.maxEjectionPercent = maxEjectionPercent
        self.baseEjectionTime = baseEjectionTime