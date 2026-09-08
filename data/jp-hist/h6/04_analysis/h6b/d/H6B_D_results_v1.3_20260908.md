# H6-B D 模块（独立通胀机制 Deflation Gate）— 结果报告 v1.3（CN 补采并入版）

日期：2026-09-08
版本：v1.0(REWORK)→ v1.1(REWORK)→ v1.2(REWORK)→ **v1.3（CN Core CPI COLLECTED 并入 + Services 部分并入）**
上游：D0_spec_FROZEN_v0.1（sha 79845895…，**immutable 零修改**）+ h6b_spec_FROZEN_v1.2.3 §9 + FREEZE_H6B_B3
引擎：engine/h6b_d_engine_v13.py（sha d5a8fc2e…）+ d_run_record_v1.3.json
新输入：CN Core CPI（用户外部采集，2013Q1-2026Q2，54 季，锚点 7/7）与 CN Services CPI（2023+ 部分，7 完整季）

## v1.3 变更（仅输入并入 + 可得性判定，D0 spec / 判据 / JP 处理零变更）
- **CN Core CPI COLLECTED**：官方 NBS 月度发布转录(Trendonify 交叉)，2013-01..2026-07 完整 163 月 → 季均 54 季(2013Q1-2026Q2)。锚点 7/7 与官方值一致(2026-07=0.9/2026-02=1.8/2021-01=-0.3/2020-01=1.5/2019-01=1.9/2016-03=1.5/2013-01=1.5)。sha 680fa0fc。
- **CN Services CPI 部分**：2023 全 12 月 + 2024/2026 部分 = 28 月 → 7 完整季(2023Q1-Q4、2024Q3-Q4、2026Q2)。2016-2022 未采 → 长窗 COLLECTION_INCOMPLETE。sha 1d37dbbd。
- engine 可得性逻辑：类只在有数据季计为可得(services 仅 COMPLETE 3/3 季)；D-B 有效窗 = ≥4 类可得的最长连续段。

## 一、机器判定（D_gate_machine_v1.3.csv + D_gate_quarter_detail_v1.3.csv）

### JP（不变，与 v1.2 完全一致）
| Gate | 结果 |
|---|---|
| D-A | CPI<0 = 31/84 季；最长连续 20 季（1999Q4 起） |
| D-B | 40/44 季 ≥3/4 类 <1.0%（0.9091）→ **BROAD**（窗 1995Q1-2005Q4） |
| D-C | 最长连续 31 季（1998Q2 起）→ **PERSISTENT** |
| D-D | JP_BROAD_PERSISTENT_REGIME_ARCHIVED; MECHANISM_EVIDENCE_ABSENT |
| D1 | LOW_STATE_CONCORDANCE 22/22；D3 mean negative-share 0.761；**D4 PRICE_SYSTEM_DIVERGENCE 18/44**（actual sign） |

### CN（2010Q1-2026Q2，core/services 并入后）
| Gate | 结果 |
|---|---|
| D-A | CPI<0 = 6/66 季；最长连续 3 季（2025Q1 起）——描述性 |
| 4 类可得段 | **2023Q1-Q4（主窗 n=4）+ 2024Q3-Q4（n=2）+ 2026Q2（n=1）** |
| **D-B（2023 窗）** | **4/4 季 ≥3/4 类 <1.0% → BROAD** |
| **D-C（2023 窗）** | 4 季连续 → **PERSISTENT（窗口边界值，样本=单年，禁过度解读）** |
| D-D | **CN_DEFLATION_GATE_BROAD_PERSISTENT_IN_2023_WINDOW(n=4); LONG-WINDOW NOT_ADJUDICATED (services 2016-2022 missing)** |
| 长窗状态 | 2016-2022 无 services → 4 类窗中断 → 长期 broad/persistent deflation regime **仍未判定**（COLLECTION_INCOMPLETE） |
| 2024/2026 短段 | 2024Q3-Q4、2026Q2 亦 4 类可得（aux 观察：见 detail 表） |

### CN 2023 窗解读（审慎，窗口边界）
2023Q1-Q4 BROAD 主要由 **PPI 深度负增长**（-4.6..-2.7%）驱动；同期 CPI/core/services 均为温和正值（约 0.5-1.5%）。与 JP 1990s 末模式（CPI/core/PPI/deflator **全面**负增长，CPI<0 连续 20 季）**结构不同**——CN 2023 是"PPI 工业通缩 + 消费价格温和"组合，非全面价格萎缩。2023 单年 n=4 恰为 D-C 边界，不构成 regime 证据。

## 二、合成解读（修正版，维持三态纪律）
- 主链（B3 FROZEN）：GEOMETRY WITHOUT MECHANISM。
- CN deflation state：**长期窗未判定**（services 2016-2022 缺 → COLLECTION_INCOMPLETE）；2023 短窗 BROAD/PERSISTENT 为可得段内观察（窗口边界、PPI 驱动），禁表述为"CN 处于 broad/persistent deflation regime"。
- 联合表述：**MECHANISM_NOT_REPLICATED (B3); CN_LONG-WINDOW_DEFLATION_STATE_NOT_YET_ADJUDICATED; CN_2023_WINDOW_BROAD_PERSISTENT (n=4 boundary, PPI-driven)**。
- JP 档案（四类口径）：1995Q1-2005Q4 40/44 broad、31 季 persistent、CPI<0 20 季连续、D4 18/44——与 CN 2023 短窗形成对比材料，非同类 regime。

## 三、待办（残余缺口，如实）
1. Services CPI 2016-2022（官方月度新闻稿"服务"行存在，可补）——补后 CN 可得 2016+ 4 类长期窗，D-B/D-C 正式长期判定。
2. Services 2024-2026 内 15 个月缺口（2024-01/04、2025 十一个月、2026-01/02）——补后 2024-2026 连续。

## 四、产物
- D0_spec_FROZEN_v0.1（immutable）/ D_gate_machine_v1.3.csv / D_gate_quarter_detail_v1.3.csv
- engine/h6b_d_engine_v13.py + d_run_record_v1.3.json + cleanroom 证据
- 输入:02_standardized/h6b/h6b_d_cpi_core_cn.csv（sha 680fa0fc）+ h6b_d_cpi_services_cn.csv（sha 1d37dbbd）
- 本报告 v1.3 + 审核响应 + 审核包
