/*
 * TencentBlueKing is pleased to support the open source community by making 蓝鲸智云-DB管理系统(BlueKing-BK-DBM) available.
 *
 * Copyright (C) 2017-2023 THL A29 Limited, a Tencent company. All rights reserved.
 *
 * Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at https://opensource.org/licenses/MIT
 *
 * Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
 * on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for
 * the specific language governing permissions and limitations under the License.
 */

import http, { type IRequestPayload } from '../http';

const path = '/apis/event/dbha';

/**
 * DBHA切换事件列表
 */
export function getEventSwitchList(params: Record<string, any>, payload = {} as IRequestPayload) {
  return http.get<
    {
      app: string;
      bk_biz_id: number;
      bk_biz_name: string;
      cloud: string;
      cluster: string;
      cluster_info: {
        cluster_type: string;
        id: number;
        immute_domain: string;
      };
      confirm_check_time: string;
      confirm_result: string;
      db_role: string;
      db_type: string;
      idc: string;
      ip: string;
      port: number;
      remark: string;
      slave_ip: string;
      slave_port: number;
      status: string;
      switch_finished_time: string;
      switch_result: string;
      switch_start_time: string;
      uid: number;
    }[]
  >(`${path}/ls/`, params, payload);
}

/**
 * DBHA切换事件详情（日志）
 */
export function getEventSwitchLog(params: Record<string, any> & { sw_id: number }) {
  return http.get<
    {
      levelname: string;
      message: string;
      timestamp: number;
    }[]
  >(`${path}/cat/`, params);
}
