# H6-B B3 Formal Mechanism Validation — 结果报告（v1.1，B3.1 patch 后）

日期：2026-09-07
版本：v1.0（REWORK）→ **v1.1（B3.1 data-correction & gate-completion）**
B3.1 修订：①CN FAI 季度化改季末月值(P0-1)；②完整 B3 Gate 机器化(B3a+B3b,P0-2)；③track lineage 闭合(P1-1)；④engine/seed/run-record 归档(P1-2)；⑤shock lineage+residual QC(P1-3)；⑥CN D 模块源尝试 registry(P1-4)；⑦JP policy provider raw(P2-1)；⑧CN 制度断点(P2-2)。

## 一、Verdict（完整机器 Gate；b3_verdict_summary_v2.csv）

| 轨 | B1(P→B) | B2(B→R) | B3(R→C) | B4(C→I) | pass | Verdict |
|---|---|---|---|---|---|---|
| Raw | FAIL | PASS | **PASS**(B3a+B3b) | FAIL | 2 | **PARTIAL** |
| FirstDiff | FAIL | FAIL | PASS | FAIL_CI | 1 | GEOMETRY |
| ShockAdj-A | FAIL | PASS | PASS | FAIL | 2 | **PARTIAL** |
| ShockAdj-B | FAIL | PASS | PASS | FAIL | 2 | **PARTIAL** |

主轨 Raw/ShockAdj-A/B = **PARTIAL**（B2 与 B3 完整通过；B1、B4 方向性 FAIL）。

## 二、逐 Gate 机器明细（修正后）

**B1（Property→BS）FAIL**：JP 两 family 显著负（PRICE -0.37 CI(-0.73,+0.02) 边缘 / ACTIVITY -0.57 CI(-0.76,-0.38)）、CN 三 family 显著正（+0.49/+0.41/+0.62）→ 两国方向相反。JP 泡沫-破灭期价格与杠杆同降（去杠杆），P 恶化未传导为 B 恶化。

**B2（BS→Profitability）PASS**：JP +0.18(CI 跨 0) + CN +0.38(CI +0.26,+0.49) → 方向一致 + CN CI 排除 0 + JP 未显著反向。ShockAdj-B 两国均显著正（+0.43/+0.27）。B2 是**最稳健正向链**。

**B3（Profitability→Credit）PASS**：
- B3a：R→C[nfc] 两国同向负（JP -0.49 CI 显著 / CN -0.27 CI(-0.42,-0.05) 显著）——盈利恶化伴随信贷/GDP 恶化序列反向（即盈利降期信贷/GDP 升）。
- B3b（machine）：CN 两口径 SUPPORT（宽松期 PBOC 企业中长期 YoY 中位变化 -0.42 < 全窗 -0.21）；JP stance_by_change SUPPORT_THIN(7 季)、level NOT_SUPPORT（1994-2005 利率平台期区分度弱，41/47 季宽松）。
- 结论名称=CREDIT_DEMAND_PROXY_EVIDENCE（禁 IDENTIFIED_CREDIT_DEMAND）。

**B4（Credit→Investment）FAIL**：JP +0.69 CI(+0.49,+0.81) 显著（信贷恶化→投资恶化同向）；CN Raw θ=-0.42 CI(-0.68,+0.01) 跨 0、ShockAdj-A/B 显著负（-0.57/-0.48）→ 两国方向不一致（CN 信贷收缩伴随投资 YoY 回升，政策逆周期）。CN I 用 FAI 累计 YoY 代理（季末月值修正后），与 JP GFCF/GDP 口径异（如实）。

## 三、核心发现（machine 支撑，narrative 从属）

1. **P→B 与 C→I 两链在 JP 与 CN 方向系统性相反**（JP 负/正 与 CN 正/负）；B2、B3 方向一致。
2. JP 侧 P 恶化→去杠杆（非加杠杆）、信贷恶化→投资升的组合，与"资产负债表衰退+僵尸借贷"叙事相容；CN 侧政策逆周期信贷与投资特征明显。
3. Verdict PARTIAL = 存在跨国同向链（B2/B3）但无统一机制链（B1/B4 反向）。

## 四、D 模块（独立）

- JP：4 类可判（CPI/Core/Deflator/PPI）；D-A CPI<0 31 季；D-B 40/44 季（deflator 1995Q1+ 可得段）；D-C 最长 31 季。
- CN：仅 CPI/PPI 2 类 → INFEASIBLE（源尝试 registry 已证：core/services/deflator/wage 官方季度不可得）。

## 五、缺口与限制（如实）

1. JP credit_impulse 1994+（GDP availability）→ B3b JP 窗 47 季；stance_by_level 平台期区分度弱。
2. JP deflator 季度 1995+；D 模块 JP 1985-94 类别缺口。
3. CN B4 用 FAI YoY 代理（水平值不可得），口径异于 JP GFCF/GDP。
4. CN D 模块 INFEASIBLE。
5. B3b combine 规则（≥1 国 SUPPORT 且无 NOT_SUPPORT）为 B3.1 明示假设，待外审确认。

## 六、产物（b3/ 目录 + 包）

- b3_verdict_summary_v2.csv（完整 B3 版）
- b3_{raw,firstdiff,shockadj}_track_theta_mbb.csv（FAI 修正、lineage 闭合）
- b3_machine_gates_alltracks.csv（=track concat）
- b3b_stance_demand_machine.csv + b3_gate_combine_machine.csv（B3b/B3 机器）
- engine/（8 脚本 + b3_run_record.json）
- shock_lineage_residual_qc_B3.1_20260907.md / deflation_source_attempt_registry_CN.csv / definition_break_registry_B3_20260907.md
- 标准化：h6b_q_cn_fai_yoy_q.csv（修正）等

## 七、待外审确认

1. Verdict PARTIAL（主轨）接受为冻结结论？
2. B3 combine 规则与 JP B3b SUPPORT_THIN 处理？
3. B4 CN FAI YoY 代理口径（方向检验）可辩护性？
