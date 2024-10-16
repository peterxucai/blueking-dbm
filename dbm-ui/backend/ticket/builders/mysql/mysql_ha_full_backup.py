# -*- coding: utf-8 -*-
"""
TencentBlueKing is pleased to support the open source community by making 蓝鲸智云-DB管理系统(BlueKing-BK-DBM) available.
Copyright (C) 2017-2023 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at https://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""

from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from backend.db_meta.enums import ClusterDBHAStatusFlags, InstanceInnerRole
from backend.db_meta.models import Cluster
from backend.flow.consts import MySQLBackupFileTagEnum, MySQLBackupTypeEnum
from backend.flow.engine.controller.mysql import MySQLController
from backend.ticket import builders
from backend.ticket.builders.common.base import fetch_cluster_ids
from backend.ticket.builders.mysql.base import BaseMySQLHATicketFlowBuilder, MySQLBaseOperateDetailSerializer
from backend.ticket.constants import FlowRetryType, TicketType


class MySQLHaFullBackupDetailSerializer(MySQLBaseOperateDetailSerializer):
    class FullBackupDataInfoSerializer(serializers.Serializer):
        class ClusterDetailSerializer(serializers.Serializer):
            cluster_id = serializers.IntegerField(help_text=_("集群ID"))
            backup_local = serializers.ChoiceField(
                help_text=_("备份位置"), choices=InstanceInnerRole.get_choices(), default=InstanceInnerRole.SLAVE.value
            )

        # 废弃online，暂时不需要传递
        # online = serializers.BooleanField(help_text=_("是否在线备份"), required=False)
        backup_type = serializers.ChoiceField(help_text=_("备份类型"), choices=MySQLBackupTypeEnum.get_choices())
        file_tag = serializers.ChoiceField(help_text=_("备份文件tag"), choices=MySQLBackupFileTagEnum.get_choices())
        clusters = serializers.ListSerializer(help_text=_("集群信息"), child=ClusterDetailSerializer())

    infos = FullBackupDataInfoSerializer()

    def validate(self, attrs):
        try:
            self.validate_cluster_can_access(attrs)
        except serializers.ValidationError as e:
            clusters = Cluster.objects.filter(id__in=fetch_cluster_ids(details=attrs))
            id__cluster = {cluster.id: cluster for cluster in clusters}
            # 如果备份位置选的是master，但是slave异常，则认为是可以的
            for info in attrs["infos"]["clusters"]:
                if info["backup_local"] != InstanceInnerRole.MASTER:
                    raise serializers.ValidationError(e)
                if id__cluster[info["cluster_id"]].status_flag & ClusterDBHAStatusFlags.BackendMasterUnavailable:
                    raise serializers.ValidationError(e)

        return attrs


class MySQLHaFullBackupFlowParamBuilder(builders.FlowParamBuilder):
    """MySQL HA 备份执行单据参数"""

    controller = MySQLController.mysql_full_backup_scene


@builders.BuilderFactory.register(TicketType.MYSQL_HA_FULL_BACKUP)
class MySQLHaFullBackupFlowBuilder(BaseMySQLHATicketFlowBuilder):
    serializer = MySQLHaFullBackupDetailSerializer
    inner_flow_builder = MySQLHaFullBackupFlowParamBuilder
    inner_flow_name = _("全库备份执行")
    retry_type = FlowRetryType.MANUAL_RETRY
