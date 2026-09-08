# H6-B D 模块（独立通胀机制 Deflation Gate）— 结果报告 v1.1

日期：2026-09-08
版本：v1.0（REWORK）→ **v1.1（D0 spec 冻结 + 三态语义修正 + machine 扩展）**
上游：D0_spec_FROZEN_v0.1_20260908.md（spec sha 79845895…，冻结于任何 v1.1 output 之前）+ h6b_spec_FROZEN_v1.2.3 §9 + FREEZE_H6B_B3
引擎：engine/h6b_d_engine.py（sha b1fade2f…，H6B_BASE 参数化）+ d_run_record.json + d_cleanroom_runner.py

## v1.1 修订（响应外审 P0×2/P1×5/P2×2）
- **P0-1**：CN 状态三态语义修正——COLLECTION_INCOMPLETE（官方 core 2013+/services 2016+ 渠道已知未采）不再被改写为 INFEASIBLE；D-B verdict = COLLECTION_INCOMPLETE（直至补采完成方可判定）。
- **P0-2**：D-D 改为 **JOINT_STATUS 输出**（不合成否定）：main_chain=GEOMETRY_WITHOUT_MECHANISM + CN_DEFLATION_GATE=COLLECTION_INCOMPLETE → joint = MECHANISM_NOT_REPLICATED; CN_DEFLATION_STATE_NOT_YET_ADJUDICATED。**COLLECTION_INCOMPLETE/INFEASIBLE 不得充当 negative evidence。**
- **P1-1**：D0 spec FROZEN v0.1（含窗口/阈值/D1 布尔式/D2 schema/D-D 语义），spec SHA 冻结于 output 前（run record 记录时间戳）。
- **P1-2**：engine 归档 + d_run_record.json + clean-room runner（B3 同等级）。
- **P1-3**：D1 机器定义冻结（D0 spec §4：相对 1.0% 阈值的 low 状态同向性布尔式）。
- **P1-4**：D2 执行（输出 schema 齐全；JP=INFEASIBLE_NO_OLDBASE_ARCHIVE 如实——2020 基原始文件未归档；CN=NA_NO_REBASE_EVENT）。
- **P1-5**：quarter detail 扩展（n_negative/negative_share/cpi_sign/ppi_sign/deflator_sign/divergence_flag）；summary 由 detail 机器聚合。
- **P2-1**：JP 表述改"**四个可得价格类别**（CPI/Core/PPI/GDP deflator）"——禁"六类"。
- **P2-2**：CN D-C = NOT_EVALUATED_UPSTREAM_INCOMPLETE（继承上游不可判定，禁 NO_BROAD_QUARTER 误读）。

## 一、机器判定（D_gate_machine_v1.1.csv + D_gate_quarter_detail_v1.1.csv）

### JP（主窗 1985Q1-2005Q4；D-B 有效窗 1995Q1-2005Q4 = 4 类齐 44 季）
| Gate | 结果 |
|---|---|
| D-A | CPI<0 = 31/84 季；最长连续 20 季（1999Q4 起） |
| D-B | 40/44 季 ≥3/4 类 <1.0%（broad_share 0.9091）→ **BROAD** |
| D-C | 最长连续 31 季（1998Q2 起）→ **PERSISTENT** |
| D-D | **JP_BROAD_PERSISTENT_REGIME_ARCHIVED; MECHANISM_EVIDENCE_ABSENT**（B3 GEOMETRY） |
| D1 | headline∈[-0.5,+0.5] 时 22/22 季 core/PPI/deflator 与 headline 同为 low 状态（<1.0%）——band 期广泛低通胀自洽 |
| D2 | INFEASIBLE_NO_OLDBASE_ARCHIVE（2020 基未归档，如实） |
| D3 | 有效段 mean negative-share 0.761；negative_share≥0.75 的季数见 detail（广泛负增长扩散） |
| D4 | **PRICE_SYSTEM_DIVERGENCE**（三角符号不一致季数见 detail：CPI 微正/PPI 负/deflator 负结构期；非 manipulation，禁 manipulation_score） |

### CN（2010Q1-2026Q2）
| Gate | 结果 |
|---|---|
| D-A | CPI<0 = 6/66 季；最长连续 3 季（2025Q1 起）——描述性事实 |
| D-B | **COLLECTION_INCOMPLETE**（已采集 CPI/PPI 2 类 <4；core 2013+/services 2016+ 官方渠道已知未采）——补采完成前不判定 |
| D-C | NOT_EVALUATED_UPSTREAM_INCOMPLETE |
| D-D | **CN_DEFLATION_GATE_NOT_YET_ADJUDICATED (COLLECTION_INCOMPLETE); MECHANISM_NOT_REPLICATED (B3)** |
| D1/D2/D3/D4 | 无 4 类有效窗 → D1/D3/D4 出口；D2=NA_NO_REBASE_EVENT |

## 二、JP 通缩 regime 量化档案（可接受的实质结论）
JP 1995Q1-2005Q4（四个可得价格类别口径）：40/44 broad 季、1998Q2 起 31 季 persistent、CPI<0 自 1999Q4 连续 20 季、有效段 mean negative-share 0.761——**1990s 末-2000s 初日本 broad/persistent 低通胀-通缩 regime 的冻结级量化档案**（与 H6-A JP J90 结构状态衔接）。

## 三、合成解读（修正版）
- **主链**（B3 FROZEN）：GEOMETRY WITHOUT MECHANISM——完整日本式传导机制未获跨国复制支持。
- **CN deflation state**：**尚未判定**（COLLECTION_INCOMPLETE）——不得表述为"CN 无 broad/persistent deflation"。
- 正确联合表述：**MECHANISM_NOT_REPLICATED (B3); CN_DEFLATION_STATE_NOT_YET_ADJUDICATED (D 数据待补采)**。
- PPI 结构共性（JP 主窗 59/84 季 <0、CN 2010-2026 38/66 季 <0）为描述性事实，不断言传导。

## 四、待办（P0-1 补采，进行中）
CN Core CPI（2013+）+ Services CPI（2016+）官方月度历史采集 → 季度化 → lineage/QC → 若 2016+ 可成 4 类窗则执行 CN D-B/D-C。Services 月度连续官方序列可得性需核实（新闻稿仅偶发披露服务价格）。

## 五、产物
- D0_spec_FROZEN_v0.1_20260908.md / D_执行规约（并入 spec）
- D_gate_machine_v1.1.csv / D_gate_quarter_detail_v1.1.csv
- engine/h6b_d_engine.py + d_run_record.json + d_cleanroom_runner.py + cleanroom 证据
- 本报告 v1.1 + 审核包
