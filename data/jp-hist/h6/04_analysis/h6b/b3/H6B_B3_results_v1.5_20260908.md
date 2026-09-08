# H6-B B3 Formal Mechanism Validation — 结果报告 v1.5（freeze-closure 版本闭合版）

日期：2026-09-07（内容实质）/ 2026-09-08（版本闭合）
版本链：v1.0(REWORK)→ v1.1(B3.1)→ v1.2(B3.2, 内容实质冻结)→ **v1.5(B3.5 freeze-closure carrier)**
**results_content_version = v1.2**：B3.2 起的实质性结果（θ/Gate/verdict/annual I_ratio）在 B3.3-B3.5 零变更；v1.5 仅统一 freeze 版本身份（run record = B3.5、package = B3.5、results carrier = v1.5），并对 B3.3-B3.5 的 closure 修订做版本注记。本文件正文 = v1.2 内容 + closure 注记。

## 一、Frozen Verdict（b3_verdict_summary_v4.csv，B3.2 起逐字节不变）

| Track | B1(P→B) | B2(B→R) | B3(R→C) | B4(C→I) | clean_pass | key_reverse | **Verdict** |
|---|---|---|---|---|---|---|---|
| Raw | FAIL(rev) | PASS | COND_MIXED | FAIL(rev) | 1 | True | **GEOMETRY** |
| FirstDiff | FAIL(rev) | FAIL | COND_MIXED | FAIL_CI | 0 | True | **GEOMETRY** |
| ShockAdj-A | FAIL(rev) | PASS | COND_MIXED | FAIL(rev) | 1 | True | **GEOMETRY** |
| ShockAdj-B | FAIL(rev) | PASS | COND_MIXED | FAIL(rev) | 1 | True | **GEOMETRY** |

**冻结机制层结论 = GEOMETRY WITHOUT MECHANISM**（B1/B4 关键链跨国反向；B3=CONDITIONAL_MIXED 不计 clean pass；B3b_JP=MIXED_OR_THIN / B3b_CN=SUPPORT，由 b3b_stance_demand_machine.csv 机器派生）。

## 二、链级实质发现（frozen：average-rank Spearman, robust-z = median/1.4826·MAD, MBB L=3 main + L2/L4 aux）

1. **B1（Property→BS）**：JP 负（PRICE -0.37/ACTIVITY -0.57 显著）vs CN 正（ACTIVITY +0.41/INV_SALES +0.62）——跨国方向相反。
2. **B2（BS→Profitability）**：唯一稳定跨国同向链（Raw JP+0.18/CN+0.38；ShockAdj-B JP+0.43/CN+0.27）。
3. **B3a（R→C[nfc]）**：两国同向负（JP -0.50/CN -0.27）——observed equilibrium quantity，禁 identified demand。
4. **B3b**：CN 两口径 SUPPORT；JP MIXED_OR_THIN（level NOT_SUPPORT 平台期 + change SUPPORT_THIN n=7）。结论名 CREDIT_DEMAND_PROXY_EVIDENCE。
5. **B4（C→I）**：JP +0.69 显著 vs CN -0.42（Raw CI 跨 0）/ShockAdj -0.57/-0.48 显著负——跨国方向相反。**Annual I_ratio 口径独立复现**：JP +0.77 / CN -0.62（b4_iratio_annual_test.csv）。

## 三、与上游结论一致性
H5-FINAL（INTERPRETABLE FEATURE GEOMETRY ONLY）/ H6-A（Regime Geometry Robust / Exact Lag Not Event-Robust / Investment shock-robustness FAIL）→ B3 GEOMETRY WITHOUT MECHANISM 方向一致。

## 四、closure 修订版本注记（B3.3-B3.5，全部零 substantive 变更）
- **B3.3**：I_ratio JP 2001+ 单位 erratum ÷1e9 + annual C→I_ratio test；engine 归档/参数化初版；shock parent lineage；B3b 机器派生初版。
- **B3.4**：engine 6 模块 H6B_BASE 必填（禁绝对路径）；robust-z IQR→frozen MAD（max_abs_theta_diff_vs_B3.3 = **0.0072**，family-composite CN B1 行，sign/gate/verdict flip = 0）；B1 parent SHA 64-hex。
- **B3.5**：b3_input_lineage.csv（37 行 exact input lineage）+ b3_inputs/ 自足快照 + clean-room 审计证据（script/log/output-SHA）+ 版本身份闭合（run record=B3.5 / package=B3.5 / results=v1.5）。

## 五、产物索引
- b3_verdict_summary_v4.csv / 三轨 track 表（avg-rank, MAD, L2/L3/L4）/ b3_machine_gates_alltracks.csv
- b3b_stance_demand_machine.csv / B4_I_ratio_auxiliary.csv（unit-fixed）/ b4_iratio_annual_test.csv
- b3_shock_parent_lineage.csv / b3_input_lineage.csv / b3_inputs/ / engine/（run record B3.5）
- cleanroom 证据（script/log/output-SHA）/ 本报告 / 审核响应链
