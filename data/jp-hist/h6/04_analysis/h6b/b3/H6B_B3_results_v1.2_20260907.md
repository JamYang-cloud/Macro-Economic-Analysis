# H6-B B3 Formal Mechanism Validation — 结果报告（v1.2，B3.2 verdict-governance closure 后）

日期：2026-09-07
版本：v1.0(REWORK)→ v1.1(B3.1,REWORK)→ **v1.2(B3.2,冻结方向 GEOMETRY)**
B3.2 修订（零 substantive data 变更）：①verdict engine 执行 frozen key-chain-reverse→GEOMETRY(P0-1)；②B3 不聚合为确定 PASS,记 CONDITIONAL/MIXED(P0-2)；③Spearman average-rank(P1-1)；④MBB L2/L4 输出(P1-2)；⑤B4 I_ratio annual aux(P1-3)；⑥CN D 模块 COLLECTION_INCOMPLETE(P1-4)；⑦shock parent full SHA(P1-5)；⑧JP policy standardized 移出 raw(P2)。

## 一、Frozen Verdict（b3_verdict_summary_v3.csv）

| Track | B1(P→B) | B2(B→R) | B3(R→C) | B4(C→I) | clean_pass | key_reverse | **Verdict** |
|---|---|---|---|---|---|---|---|
| Raw | FAIL(rev) | PASS | COND_MIXED | FAIL(rev) | 1 | True | **GEOMETRY** |
| FirstDiff | FAIL(rev) | FAIL | COND_MIXED | FAIL_CI | 0 | True | **GEOMETRY** |
| ShockAdj-A | FAIL(rev) | PASS | COND_MIXED | FAIL(rev) | 1 | True | **GEOMETRY** |
| ShockAdj-B | FAIL(rev) | PASS | COND_MIXED | FAIL(rev) | 1 | True | **GEOMETRY** |

**冻结机制层结论 = GEOMETRY WITHOUT MECHANISM**（B1/B4 关键链跨国反向;B3=CONDITIONAL_MIXED 不计 clean pass;B3b_JP=MIXED_OR_THIN / B3b_CN=SUPPORT）。

## 二、链级实质发现（average-rank Spearman, L=3 MBB）

1. **B1（Property→BS）**:JP 负（PRICE -0.37/ACTIVITY -0.57,CI 显著）vs CN 正（+0.49/+0.41/+0.62）——跨国方向相反。JP 泡沫-破灭期价格与杠杆同降。
2. **B2（BS→Profitability）**:唯一稳定跨国同向链。Raw JP+0.18/CN+0.38(CN CI 显著);ShockAdj-B JP+0.43/CN+0.27 均正。**JP 主窗 B2 不显著(Raw CI 跨 0)但方向与 CN 一致。**
3. **B3a（R→C[nfc]）**:两国同向负（JP -0.50/CN -0.27,CI 均显著）——盈利恶化期信贷/GDP 上升。observed equilibrium quantity,禁 identified demand。
4. **B3b**:CN 两口径 SUPPORT（宽松期 PBOC 企业中长期 YoY 中位变化降更多）;JP MIXED（level NOT_SUPPORT 平台期区分度弱 + change SUPPORT_THIN n=7）。结论名 CREDIT_DEMAND_PROXY_EVIDENCE。
5. **B4（C→I）**:JP +0.69 显著正 vs CN -0.42(Raw CI 跨 0)/ShockAdj -0.57/-0.48 显著负——跨国方向相反。CN I 用 FAI 累计 YoY 代理（季末月值）。

## 三、与上游结论一致性
H5-FINAL/H6-A:结构状态几何相似存在、广义共同机制证据不足、投资/信用环节不支持"中国整体复制日本"——**B3 GEOMETRY 与此方向一致**。

## 四、D 模块（独立）
JP:4 类可判 D-B 40/44、D-C 31 季(1995+ deflator 段);CN:COLLECTION_INCOMPLETE(core/services 官方渠道已知未采,源尝试 registry 有据)。

## 五、缺口与限制（如实）
1. JP credit_impulse 1994+;B3b JP stance_by_level 平台期区分度弱。
2. JP deflator 1995+ 季度;CN D 模块类别不足。
3. CN B4 用 FAI YoY 代理(水平值不可得),与 JP GFCF/GDP 口径异;Raw CI 跨 0 而 ShockAdj 显著负——block-length 敏感(L2 显著/L3-L4 跨 0)。
4. B3=CONDITIONAL/MIXED 因 B3b 聚合规则未预注册(冻结为不聚合,分列报告)。

## 六、产物
- b3_verdict_summary_v3.csv + 三轨 track 表(avg-rank, L2/L3/L4)+ machine_gates_alltracks + b3b_stance_demand_machine + b3_gate_combine_machine
- B4_I_ratio_auxiliary.csv / b3_shock_parent_lineage.csv / deflation registry / engine/(run record 更新)
- 本报告 + 审核响应(B3.2)
