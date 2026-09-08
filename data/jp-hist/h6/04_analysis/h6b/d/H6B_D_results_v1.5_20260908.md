# H6-B D 模块（独立通胀机制 Deflation Gate）— 结果报告 v1.5（外审 2019-2022 补采并入,availability 粒度修正）

日期：2026-09-08
版本：v1.0→v1.1→v1.2→v1.3→v1.4→ **v1.5（外审补采 2019-2022 并入,CN 4 类长窗 2019Q1-2026Q2 判定；P1 availability 粒度拆分）**
上游：D0_spec_FROZEN_v0.1（sha 79845895…,immutable 零修改）+ h6b_spec_FROZEN_v1.2.3 §9 + FREEZE_H6B_B3
引擎：engine/h6b_d_engine_v15.py（sha 66d530a8…）+ d_run_record_v1.5.json

## v1.5 变更（仅输入并入 + 状态输出修正;D0 spec/判据/JP 处理零变更）
1. **CN Services CPI 外审补采并入**（canonical monthly table v1.5,sha 00997a48…,100 行）:
   - S4 外审 supplement:2019 全 12 月 + 2020 全 12 月 + 2021-06 + 2022-01/02/05/11（29 月,grade A + URL）
   - 与 v1.4 已归档月度（S1 用户 28 月 + S2 主会话抓取 27 月 + S3 正文级 6 月）合并,**0 值冲突**;v1.4 奇偶校验 22/22 全 OK（仅 S1+S2+S3 即可逐季度复现 v1.4 值）
   - 结果:月度 100（窗口内 99）;services 完整季 30,**连续完整季 2019Q1-2026Q2(n=30)**
2. **2016-2018 官方可得性核验**（审计 P0 部分完成）:
   - 已定位并核验 9 月（2016-12=2.5、2017-12=3.0、2018-01/03/04/08/09/10/11=2.3/2.8/2.6/2.6/2.1/2.1/2.1）——**官方月度"服务"行在该段存在,页面级/官方 description 级双源核验**,入 canonical（S5）
   - 其余 27 月（2016-01..11、2017-01..11、2018-02/05/06/07/12）官方当年发布,但 NBS zxfb/202302 迁移区无对应号段/高速抓取触发反爬——**如实 COLLECTION_INCOMPLETE（PARTIAL）,禁插值**;探测日志与 URL/值存档见 07_外部采集 与 手动数据采集/
3. **availability 粒度拆分**（审计 P1-1）:
   - series_collection_status（层 1）:CN services = `PARTIAL_COLLECTION_complete_q=30`;core = COLLECTED_2013PLUS;deflator = INFEASIBLE_AFTER_PRESPECIFIED_MASK;wage = SOURCE_NOT_FOUND
   - quarter_availability（层 2）:detail 表逐季 services_q_status 字段;n_available 逐季
   - 移除 v1.4 中"静态注册被运行时静默覆盖为 COLLECTED"的混合逻辑

## 一、机器判定（D_gate_machine_v1.5.csv + D_gate_quarter_detail_v1.5.csv）

### JP（不变,v1.2-v1.5 逐字节一致）
| Gate | 结果 |
|---|---|
| D-A | CPI<0 = 31/84 季;最长连续 20 季(1999Q4 起) |
| D-B | 40/44 季 ≥3/4 类 <1.0% → **BROAD**(1995Q1-2005Q4,share 0.9091) |
| D-C | 最长 31 季(1998Q2 起)→ **PERSISTENT** |
| D1/D3/D4 | 22/22 LOW_STATE_CONCORDANCE;mean neg-share 0.761;**D4 PRICE_SYSTEM_DIVERGENCE 18/44** |

### CN（2010Q1-2026Q2;4 类主窗现为 2019Q1-2026Q2 n=30）
| Gate | 结果 |
|---|---|
| D-A | CPI<0 = 6/66 季(2025Q1 起最长 3 季)——CN 无 CPI 深度持续负段 |
| 4 类可得段 | 主窗 **2019Q1-2026Q2(n=30)**（唯一 ≥4 类连续段） |
| **D-B** | **17/30 季 ≥3/4 类 <1.0% → BROAD**(share 0.5667) |
| **D-C** | 最长连续 **14 季(2022Q4 起)→ PERSISTENT** |
| D-D | **CN_DEFLATION_GATE_BROAD_PERSISTENT_IN_2019Q1-2026Q2(n=30,17/30); EARLIER WINDOW NOT_ADJUDICATED (services 2016-2018 PARTIAL)** |
| D1 | 无 deflator → 出口;D3 mean actual-neg-share 0.225;D4 INFEASIBLE_NO_DEFLATOR |

### 与外审独立敏感性复跑互证
外部审核报告 §8 敏感性表（补采后）:
```text
main window 2019Q1-2026Q2 n=30 | BROAD 17/30 = 0.5667 | D-C longest 14 from 2022Q4
```
与 v1.5 机器输出**完全一致**（D-B_share 0.5667、D-C 14/2022Q4）。两路独立执行互证。

## 二、合成解读（维持三态纪律;采纳外审 P2-1/P2-2 措辞）
- 主链（B3 FROZEN）:GEOMETRY WITHOUT MECHANISM。
- **CN 结论表述（按外审 P2-1）**:2019Q1-2026Q2 四类价格体系内存在**若干持续 Broad low-inflation episode,其中 2022Q4 以后形成最长持续段（14 季）;2023-2026 为最密集阶段**。BROAD/PERSISTENT 分类在窗由 14 季扩至 30 季后保持稳定（17/30 而非 13/14 的局部强度数字）。
- **价格结构表述（按外审 P2-2）**:same gate classification ≢ same price-system structure。
  - JP 1995-2005 = economy-wide CPI/core/deflator 全面负增长（CPI<0 连续 20 季、deflator 44/44 季 <1%、mean neg-share 0.761）——全面通缩配置
  - CN 2019-2026 = **producer-deflation（PPI 深负）+ consumer/service low-inflation（core/services 0.3-1.5%、CPI 未深负,窗内 CPI<0 仅零星）configuration**——非日本式全面通缩
- 两国均过冻结 D-B/D-C 判据（状态相似）但价格系统结构不同 → 与 H6-A/B3"State similarity ≢ Transmission-mechanism similarity"一致;D 模块增量结论:同一 gate 分类下的结构性差异已由 B3 否定机制跨国产复制。

## 三、缺口与限制（如实）
1. **services 2016-2018 部分未采（27 月）**:官方月度"服务"行存在且已核验 9 月,但 NBS 官网迁移区号段缺失（2018-02/05/06/07/12）+ 反爬限流中断逐月定位（2016-01..11、2017-01..11）;已核验 9 月入册（S5）,未采部分**如实 PARTIAL,不插值** → CN 4 类主窗起点限 2019Q1;2016-2018 中任何补齐后主窗可再扩（engine 参数化自动重判）
2. JP 2020 基原始未归档 → D2 INFEASIBLE_NO_OLDBASE_ARCHIVE
3. CN 无 deflator → D1/D4 CN 出口（INFEASIBLE_NO_DEFLATOR）
4. P1-2 canonical lineage 已闭合 99/100 行（S1 用户 28 月 + S3 正文级 6 月无 URL,如实标注 NA——用户采集未记录 URL;其余 66 行含 source_url）

## 四、产物
- D0_spec_FROZEN_v0.1（immutable,零修改）/ D_gate_machine_v1.5.csv（e1f55b71…）/ D_gate_quarter_detail_v1.5.csv（a637dca6…）
- engine/h6b_d_engine_v15.py（66d530a8…）+ d_run_record_v1.5.json（bfca4b65…）
- 输入:8 个 D 文件(services 季度 37f2cce1…)+ canonical monthly v1.5（00997a48…）+ 外审 supplement/verified + 2016-2018 核验存档
- 本报告 v1.5 + 审核响应 + 审核包
