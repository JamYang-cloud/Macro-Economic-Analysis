# H6-B D 模块（独立通胀机制 Deflation Gate）— 结果报告 v1.4（Services 补采并入终版）

日期：2026-09-08
版本：v1.0→v1.1→v1.2→v1.3→ **v1.4（Services 2016-2026 补采主体完成,CN 4 类长窗判定）**
上游：D0_spec_FROZEN_v0.1（sha 79845895…,immutable 零修改）+ h6b_spec_FROZEN_v1.2.3 §9 + FREEZE_H6B_B3
引擎：engine/h6b_d_engine_v14.py（sha 见 run record）+ d_run_record_v1.4.json

## v1.4 变更（仅输入并入;D0 spec/判据/JP 处理零变更）
- **CN Services CPI 补采并入**(2026-09-08 主会话 + 用户外部工具合并):
  - 用户外部:NBS 月度新闻稿"服务"行 2023 全 12 月 + 2024-2026 部分
  - 主会话:NBS 官方新闻稿表格/正文补 2021-2022 部分(2021-01/02/03/04/05/07/09/10/11/12、2022-03/04/06/07/08/09/10/12 等,含 description 级官方原文核对)+ 2024-2026 缺口 15 月
  - 合并后月度 62 个;**services 2022-12..2026-06 连续 43 个月**;完整季 18 个,**最长连续完整季 2023Q1-2026Q2(n=14)**
  - 落盘 h6b_d_cpi_services_cn.csv(sha 9f018b6f…;2016-2022 部分月份未采,如实)
- CN Core CPI:2023 v1.3 已入(h6b_d_cpi_core_cn.csv,sha 680fa0fc…)

## 一、机器判定（D_gate_machine_v1.4.csv + D_gate_quarter_detail_v1.4.csv）

### JP（不变,v1.2-v1.4 逐字节一致）
| Gate | 结果 |
|---|---|
| D-A | CPI<0 = 31/84 季;最长连续 20 季(1999Q4 起) |
| D-B | 40/44 季 ≥3/4 类 <1.0% → **BROAD**(1995Q1-2005Q4) |
| D-C | 最长 31 季(1998Q2 起)→ **PERSISTENT** |
| D1/D3/D4 | 22/22 LOW_STATE_CONCORDANCE;mean neg-share 0.761;**D4 PRICE_SYSTEM_DIVERGENCE 18/44** |

### CN（2010Q1-2026Q2;4 类窗现为 2023Q1-2026Q2 n=14）
| Gate | 结果 |
|---|---|
| D-A | CPI<0 = 6/66 季(2025Q1 起最长 3 季)——CN 无 CPI 深度持续负段 |
| 4 类可得段 | 主窗 **2023Q1-2026Q2(n=14)**;其余 2021Q1/Q3-Q4、2022Q3 孤立完整季(aux) |
| **D-B** | **13/14 季 ≥3/4 类 <1.0% → BROAD**(2023Q1-2026Q2) |
| **D-C** | 最长连续 **13 季(2023Q1 起)→ PERSISTENT** |
| D-D | **CN_DEFLATION_GATE_BROAD_PERSISTENT_IN_2023Q1-2026Q2(n=14,13/14); EARLIER WINDOW NOT_ADJUDICATED(services pre-2023 部分缺)** |
| D1 | 无 deflator → 出口;D3 mean actual-neg-share 0.321;D4 INFEASIBLE_NO_DEFLATOR |

### CN 窗内结构解读(与 JP 对比,如实)
- CN 2023Q1-2026Q2 的 BROAD 由 **PPI 深度负(2023-2024 大部分 -2..-5%)+ core/services 低位(0.5-1.5%)+ CPI 温和(多数 <1.5%)** 驱动;窗内 CPI<0 仅零星(2025Q1 段 3 季)。
- JP 1995-2005 BROAD 段含 **CPI/core/deflator 全面负增长**(CPI<0 连续 20 季、deflator 44/44 季 <1%、negative-share 0.761)。
- 两国均达"≥3/4 类 <1.0% 持续 ≥4 季"的冻结判据(BROAD/PERSISTENT),但**价格系统内部结构不同**:JP = 全面通缩(含 CPI 核心负);CN = 工业品深通缩 + 消费服务低位,CPI 未深负。D4(JP 18/44 divergence)显示 JP 价格系统内部分化亦存在。

## 二、合成解读(维持三态纪律)
- 主链(B3 FROZEN):GEOMETRY WITHOUT MECHANISM。
- **CN deflation state(4 类可得窗 2023-2026):BROAD/PERSISTENT 低通胀 regime 成立**——但表述限定:①窗=2023Q1-2026Q2(n=14),2021 前未 adjudicate(services 缺口);②模式=PPI 驱动型 broad low-inflation,非 JP 式全面 CPI 通缩;③Japan-like 机制解释仍被 B3 主链否定(GEOMETRY)。
- JP 档案(四类口径)与 CN 2023-2026 窗构成**可比 broad/persistent 状态对**,但内部结构差异显著——与 H6-A"State similarity ≢ Transmission-mechanism similarity"一致:状态几何可相似(都过 D-B/D-C),机制链未复制(B3)。

## 三、缺口与限制(如实)
1. services 2016-2022 部分月份未采(官方月度"服务"行存在,采集成本;2021-2022 已补 12/24 月、2016-2020 未采)→ CN 4 类窗起点限 2023Q1(此前 3 类段 headline/core/PPI 有,但 D-B 需 4 类)
2. JP 2020 基原始未归档 → D2 INFEASIBLE_NO_OLDBASE_ARCHIVE
3. CN 无 deflator → D1/D4 CN 出口

## 四、产物
- D0_spec_FROZEN_v0.1(immutable)/ D_gate_machine_v1.4.csv / D_gate_quarter_detail_v1.4.csv
- engine/h6b_d_engine_v14.py + d_run_record_v1.4.json + cleanroom 证据
- 输入:h6b_d_cpi_core_cn.csv(680fa0fc)+ h6b_d_cpi_services_cn.csv(9f018b6f)+ 补采 raw(/tmp 与手动数据菜价/)
- 本报告 v1.4 + 审核响应 + 审核包
