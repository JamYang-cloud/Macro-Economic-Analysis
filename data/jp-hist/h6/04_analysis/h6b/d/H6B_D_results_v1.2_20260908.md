# H6-B D 模块（独立通胀机制 Deflation Gate）— 结果报告 v1.2

日期：2026-09-08
版本：v1.0(REWORK)→ v1.1(REWORK)→ **v1.2（D4 actual-sign 修复 + availability 拆分 + immutable parent）**
上游：D0_spec_FROZEN_v0.1（sha 79845895…，**immutable，本版零修改**）+ h6b_spec_FROZEN_v1.2.3 §9 + FREEZE_H6B_B3
引擎：engine/h6b_d_engine_v12.py（sha 2837b3bf…）+ d_run_record_v1.2.json + d_cleanroom_runner.py

## v1.2 修订
- **D4 actual-sign 修复**（P0-2）：D1 low_state(<1.0%) 与 D4 actual_sign(<0%) 分离；字段 cpi_low/ppi_low/deflator_low + cpi_actual_sign/ppi_actual_sign/deflator_actual_sign。**JP D4 divergence 6/44 → 18/44**（machine 重生成，与外审独立重算一致）。
- **availability 拆分**（P1-1）：CN Core=COLLECTION_INCOMPLETE / Services=UNDER_SOURCE_VERIFICATION / GDP deflator=INFEASIBLE_AFTER_PRESPECIFIED_MASK / Wage=SOURCE_NOT_FOUND。
- **D1 命名**（P2-1）：D1_LOW_STATE_CONCORDANCE。
- **D2 措辞**（P2-2）：infeasibility correctly adjudicated; rebase overlap robustness NOT empirically completed。

## 一、机器判定（D_gate_machine_v1.2.csv + D_gate_quarter_detail_v1.2.csv）

### JP（主窗 1985Q1-2005Q4；D-B 有效窗 1995Q1-2005Q4 = 4 类齐 44 季）
| Gate | 结果 |
|---|---|
| D-A | CPI<0 = 31/84 季；最长连续 20 季（1999Q4 起） |
| D-B | 40/44 季 ≥3/4 类 <1.0%（0.9091）→ **BROAD** |
| D-C | 最长连续 31 季（1998Q2 起）→ **PERSISTENT** |
| D-D | **JP_BROAD_PERSISTENT_REGIME_ARCHIVED; MECHANISM_EVIDENCE_ABSENT**（B3 GEOMETRY） |
| D1 | LOW_STATE_CONCORDANCE：headline∈[-0.5,+0.5] 时 22/22 季 core/PPI/deflator 与 headline 同 low 状态（<1.0%） |
| D2 | INFEASIBLE_NO_OLDBASE_ARCHIVE（infeasibility correctly adjudicated; robustness 未实证执行） |
| D3 | 有效段 mean actual-negative share = 0.761（负增长扩散广泛） |
| D4 | **PRICE_SYSTEM_DIVERGENCE：18/44 季**（actual sign 口径：CPI 微正/PPI 负/deflator 负结构期；1995-96 典型 CPI +0.2/PPI -0.5/deflator -0.4；非 manipulation，禁 manipulation_score） |

### CN（2010Q1-2026Q2）
| Gate | 结果 |
|---|---|
| D-A | CPI<0 = 6/66 季；最长连续 3 季（2025Q1 起）——描述性 |
| D-B | **COLLECTION_INCOMPLETE**（collected 2 类 <4；core CPI 补采子任务 deleg_8cddc529 进行中） |
| D-C | NOT_EVALUATED_UPSTREAM_INCOMPLETE |
| D-D | **CN_DEFLATION_GATE_NOT_YET_ADJUDICATED (COLLECTION_INCOMPLETE); MECHANISM_NOT_REPLICATED (B3)** |
| D1/D3/D4 | 无 4 类有效窗 → 出口；D2=NA_NO_REBASE_EVENT |
| availability | Core=COLLECTION_INCOMPLETE / Services=UNDER_SOURCE_VERIFICATION / Deflator=INFEASIBLE_AFTER_PRESPECIFIED_MASK（registry NOT_CONSTRUCTIBLE）/ Wage=SOURCE_NOT_FOUND |

## 二、JP 通缩 regime 量化档案（实质结果，不受 D4 修复影响）
JP 1995Q1-2005Q4（四个可得价格类别）：40/44 broad 季、1998Q2 起 31 季 persistent、CPI<0 自 1999Q4 连续 20 季、D3 mean negative-share 0.761、D4 18/44 价格系统发散（CPI 微正 vs PPI/deflator 负）——**1990s 末-2000s 初日本 broad/persistent 低通胀-通缩 regime 冻结级量化档案**。

## 三、合成解读
- 主链（B3 FROZEN）：GEOMETRY WITHOUT MECHANISM——完整日本式传导机制未获跨国复制支持。
- CN deflation state：**尚未判定**（core/services 补采/adjudication 中）——禁表述为"CN 无 broad/persistent deflation"。
- 联合表述：**MECHANISM_NOT_REPLICATED (B3); CN_DEFLATION_STATE_NOT_YET_ADJUDICATED**。

## 四、产物
- D0_spec_FROZEN_v0.1（immutable，sha 79845895…）/ D_gate_machine_v1.2.csv / D_gate_quarter_detail_v1.2.csv
- engine/h6b_d_engine_v12.py + d_run_record_v1.2.json + d_cleanroom_runner.py + cleanroom 证据
- 本报告 v1.2 + 审核响应 + 审核包
