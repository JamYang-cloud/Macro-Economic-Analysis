# H6-B B1.1 — Definition Break Registry

日期：2026-09-07（B1.1 data-correction patch 后重建）
依据：JP-HIST_H6B_B1_GATE1 审核报告 §17 要求（definition_break_registry 重生成）

规则：定义断点入册不插值；structural pre-start 不计 missing；CONCEPT_PROXY 沿用冻结口径。

| # | variable | country | break_quarter | type | 说明 | 处理 |
|---|---|---|---|---|---|---|
| D1 | corporate_leverage / corporate_profitability | CN | 2011Q1 | STRUCTURAL_PRE_START | 规上工业门槛 主营业务收入 500万→2000万 (2011),2010 与 2011+ 非同一总体; 2010Q1-Q4 无法同口径季度化 | 连续段 2011Q1+ 为主文件; 2010 标 PRE_2011_INCOMPATIBLE_UNIVERSE,不计 missing; 前导稀疏点(2001-2006)独立 aux 文件 |
| D2 | corporate_leverage / corporate_profitability | CN | 2019 起(月度) | DEFINITION_RENAME | 2018 前"主营业务收入"→2019 起"营业收入"(指标更名,月度累计口径不变) | 单季还原时双源拼接:2011-2018 主营业务收入累计、2019+ 营业收入累计;source_note 注明 |
| D3 | corporate_leverage / corporate_profitability | CN | 2011Q1 前 | PRE_START_SPARSE | 2001-2006 稀疏前导点(esData 月度库限 2011 后连续),2007-2010 全缺 | 前导点独立 aux 文件(_leading_sparse),不并入主序列 |
| D4 | housing_starts | CN | 2000Q2-Q4 | MISSING_GAP(登记) | NBS 新开工面积 2000Q1 孤立点,2000Q2-Q4 缺(esData 库限),2001Q1+ 连续 | source_note 精确化"2000Q1 + 2001Q1-2026Q2";2000 三季登记 missing(主窗 2010+ 不受影响) |
| D5 | corporate_leverage / corporate_profitability / mof_interest_burden / land_share | JP | 无 | (无) | MOF 法人企業統計 1954Q2-2026Q1 全自然季度,显式 Jan-Mar→Q1 映射,无断点 | parser 修复后 monotonic;1985+ 恒等式 max rel 0.0004 |
| D6 | boj_ffa_corp_liab / credit_flow_jp / credit_impulse_jp | JP | 1998Q1 | SPLICE(旧→新序列) | 旧 fffa260(法人企業,更新停止 1964-1999) → 新 ffaf410(非金融法人企業,1998Q1+); 1998-1999 重叠 | 旧序列覆盖 1964Q4-1997Q4,新序列 1998Q1+; 语义差异(法人企業 vs 非金融法人企業)已记录,观测连续无跳变检查 |
| D7 | boj_ffa / credit_* | JP | 1994Q1 | DATA_AVAILABILITY | FRED JPNNGDP 名义 GDP 自 1994Q1 起(FRED 起点),故 credit_flow/impulse 覆盖 1994+; 1985-1993 无 GDP 分母 | 如实记录:FFA 为 B2 SECONDARY aux,BIS credit 主窗 84/84 已覆盖 |
| D8 | i_q_gfcf | JP | 2001Q1 附近 | REGIME_SPLICE(growth-link) | 68SNA(1990基準 NSA,1955-1993Q4×factor) + ESRI QE 2008SNA(1994Q1+,SA); 重叠 1994-2000 28 季 splice factor=0.2027 | growth-link splice 非裸 level concat; 2000Q4→2001Q1 跳变 0.00026(消除原 0.86pp);2026Q2 补至(2026-08-17 发布) |
| D9 | residential_property_price | JP/CN | 无 | (无) | BIS WS_SPP 单序列全历史(JP 1955Q1+、CN 2005Q2+),无拼接 | 无断点;vintage 见 BIS_vintage_registry |
| D10 | housing_starts | JP | 2025Q1 | SOURCE_CHANNEL | e-Stat DB 时系列止 2024M12; 2025+ 转 MLIT 月报 publication7/8xx.xls 月度原值 | 月报逐月提取→季度求和(非 SAAR);2026-06=66,344 户锚点与 MLIT 一致 |
| D11 | 所有 JP 季度序列 | JP | 2026Q2 | CUTOFF_EXCLUSION | MOF 2026Q2 官方发布 2026-09-01(>cutoff 2026-08-31);BOJ FFA 2026Q2 未发布 | MOF/FFA 序列止 2026Q1;ESRI/MLIT/NBS 2026Q2 在 cutoff 内保留 |

## Structural pre-start 汇总（不计 missing）

| variable | country | structural_start | 类型 |
|---|---|---|---|
| corporate_leverage | CN | 2011Q1 | STRUCTURAL_PRE_START(门槛变更) |
| corporate_profitability | CN | 2011Q1 | STRUCTURAL_PRE_START(门槛变更) |
| credit_flow_jp / credit_impulse_jp | JP | 1994Q1 | DATA_AVAILABILITY(GDP 分母起点) |

## B1.2 补充登记（2026-09-07，B1.1 CONDITIONAL PASS 后）

| # | 事项 | 说明 |
|---|---|---|
| B1.2-1 | CN inventory_area(商品房待售面积) = **AUX_PARTIAL** | NBS esData 库确认无此指标(probe 500/不在库);官方通道=NBS 月度新闻稿 HTML(已实证 2026 各月末值:4月末 77,801/5月末 77,182/6月末 76,315/7月末 75,911 万㎡,来源 stats.gov.cn zxfb);历史逐月拼接需 ~200 篇(2010-2026)成本高;外审 §16 允许 AUX_PARTIAL,不阻断 B1 Freeze;MVMD sales/inventory 二选一已满足 |
| B1.2-2 | FRED JPNNGDP 元数据 | Billions of Yen, Seasonally Adjusted, Quarterly;**NOT SAAR**(外审 §12 纠正);credit_flow source_note 已删 SAAR;单位换算 GDP_億円=10×GDP_billion |
| B1.2-3 | coverage effective denominator | coverage_qc 增加 nominal_window_req/effective_window_start/effective_window_req/structural_pre_start_excluded/effective_obs/coverage_ratio_effective;Gate 只读 effective;CN corp 62/62=1.0;FFA aux 用 availability 分母 |
| B1.2-4 | BOJ legacy FFA density | boj_ffa_corp_liab coverage 标 sampling_density=SEMIANNUAL_LEGACY + gate_role=SECONDARY_AUX |
