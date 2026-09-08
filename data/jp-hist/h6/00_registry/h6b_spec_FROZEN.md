# H6-B External Mechanism Validation — Frozen Spec（FROZEN）
版本：2026-09-07 v1.0 FROZEN
项目：JP-HIST · 链 08_jp_hist/h6/
上游建议书：01_数据采集/外部审核意见/JP-HIST_H6A_H6B_下一步工作方向与数据采集建议书_20260907.md（蓝本）
状态：签署后只读；修订走 errata + 版本化。本 spec 冻结时点与 H6-A 相同（双 spec 同日冻结）；H6-B 的执行 Gate 1 之前的 B1 数据下载可在 H6-A 冻结后按 §11 顺序启动（下载与 A 分析无数据依赖；但 B 的结果解读必须等 A 完成）。

## 0. 冻结记录
- 用户授权 2026-09-07「按默认执行」；每步关键完成后外审。
- 与 H6-A 联动：H6-B 最终结论必须同时给 Mechanism^Raw 与 Mechanism^ShockAdjusted 两版（建议书 §36）；仅 Raw 成立而 adjustment 后消失 → investment 相似可能主要由共同冲击驱动，如实降级。

## 1. 核心问题与主机制链（FROZEN）
检验 investment 相似信号是否对应真实经济机制：
主链 Property → Corporate Balance Sheet → Profitability → Credit → Investment
辅助链 Demography → Housing Demand → Property → Investment
明确不做：把任何 H6-B 新变量加入旧 J90/J00 classifier（circular validation 禁令，同 FREEZE_H5 W 纪律）；不以"像日本"回选变量；不声称 causal（证据等级 Level 4 明示不做）。

## 2. 机制假说（FROZEN；每链做方向 + 时序检验）
- H6B-H1 Property：PropertyPrice↓ ⇒ PropertyActivity↓ ⇒ InvestmentGDP↓。
- H6B-H2 Balance Sheet：Leverage↑ 或 InterestBurden↑ ⇒ Investment↓。去杠杆阶段本身也会 Leverage↓ → 不得只按单方向机械判断，须结合时序与资产价格变化。
- H6B-H3 Profitability：Profitability↓ ⇒ Investment↓。
- H6B-H4 Credit：CreditImpulse↓ ⇒ Investment↓。
- H6B-H5 Composite：JP 与 CN 均呈 Property↓ ∧ Profitability↓ ∧ CreditImpulse↓ ∧ Investment↓ 且时序合理 → investment correspondence 获更强机制支持。

## 3. Minimum Viable Mechanism Dataset（MVMD；11 项）
Property：房地产/土地价格、housing starts、property investment、sales/inventory 至少一项。
Corporate：corporate debt/GDP、leverage、profitability。
Credit：NFC credit/GDP、household credit/GDP、debt service 或 interest burden 之一。
Outcome：investment/GDP（已有，P0）。
完整变量清单与语义分类见 h6b_mechanism_registry.csv（PRIMARY/SECONDARY/PROXY/DROP 逐项冻结）。

## 4. 采集阶段与 Gate（FROZEN）
- Phase B1a（下载友好，先做）：BIS NFC credit/GDP、BIS household credit/GDP、BIS property price（季度→年度）；JP MOF 法人企业统计（leverage/margin/interest burden，全行业除金融保险）；JP MLIT 公示地价（衔接已标准化 land_price_yoy）与 housing starts；CN 侧先准备 NBS 房地产与工业数据源清单。
- Phase B1b（历史口径最费，后做）：CN NBS 房地产四条（开发投资/新开工/销售/库存）、规模以上工业 leverage/profit（semantic=SECTOR_PROXY）、PBOC 社融（credit impulse；2002-2012 段复用 02_standardized/annual_CN_credit_flow_level，2013+ 补齐）。
- Phase B2（金融深化，Gate1 ≥3 项支持才进）：BOJ FFA、PBOC TSF 结构、credit impulse 双侧、BIS DSR。
- Phase B3（难数据，仅 B1/B2 已现一致机制后）：listed-firm micro、NPL、developer leverage、vacancy、corporate q、household savings。
- Gate 1（B1a+B1b 完成后 H6B_GATE1_report.md，5 问）：property 同向？profitability 同向？leverage/balance-sheet 可解释状态？BIS credit 同向？investment held-out 在 H6-A 后仍稳？≤1 支持 → 停止深挖；≥3 支持 → 进 B2。
- Gate 2（B2 后）：Property+Corporate+Credit+Investment 四环 ≥3 环同向且跨源复现 → 可称 Mechanism-Consistent Correspondence，仍禁 causal equivalence。

## 5. 分析工具（FROZEN；年度短样本纪律）
- event-time 归一：τ = t − t_peak（JP 1990 / CN 2011），比较 X_τ/X_0 或 robust-z 路径。
- directional replication：D_v^JP = mean_{J90} − mean_{J00}，CN 对应状态方向用 H4/H5 冻结的逐年归属（新变量从未参与分类 → 天然 held-out）。
- 主相关：Spearman；Pearson 仅辅助。
- cross-correlation：仅 exploratory，|k| ∈ {0,1,2,3}，禁止无限扫描 lag。
- 推断：moving block bootstrap（block length=3 年，n_boot=2000）为主；不做 IID bootstrap 唯一方法。
- 不采用（v1）：大规模 VAR/SVAR/Granger/local projections/自动因果发现。

## 6. 证据分级与 scorecard（FROZEN；Level 4 明示不做）
Level 0 No Evidence / Level 1 Descriptive Correspondence（单源同向）/ Level 2 Cross-source Replication（≥2 独立源同向）/ Level 3 Mechanism-Consistent（五环节 ≥3 成立且有合理时序）/ Level 4 Causal — 本阶段不主张。
Scorecard 条件（frozen）：JP 方向合理论 required；CN 方向合理论 required；两国 event-time 同向 required；baseline/shock-adjusted 均成立 required；≥2 独立数据族 required；bootstrap 不明显反转 preferred；temporal ordering 合理 preferred。

## 7. 语义与拼接纪律（FROZEN）
- 每概念事先定义 PRIMARY/SECONDARY/PROXY/DROP；EXACT↔PROXY 非对称比较必须显式标注。
- 禁拼接：BIS DSR 与 MOF interest-burden proxy 是不同概念（bis_dsr / mof_interest_burden_proxy 分列）；credit flow ≠ credit stock（TSF^flow 禁当存量）；两国口径不同不静默接。
- 无法确认 definition break 的历史片段留缺口，不补二手数字（宁可留缺口）。

## 8. 交付物
h6b_spec_FROZEN.md / h6b_mechanism_registry.csv / h6b_source_manifest.csv / h6b_crosswalk.csv / raw/ / standardized/ / h6b_property_paths.csv / h6b_corporate_paths.csv / h6b_credit_paths.csv / h6b_eventtime_results.csv / h6b_direction_results.csv / h6b_bootstrap_results.csv / h6b_evidence_scorecard.csv / H6B_GATE1_report.md / H6B_final_report.md / SHA256_manifest_h6b.txt

## 9. 决策记录
- 2026-09-07 用户「按默认执行」→ 本 spec FROZEN v1.0（与 H6-A 同日；B1 数据下载在 A 冻结后按 §4 启动）。
