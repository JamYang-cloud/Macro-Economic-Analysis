# JP-HIST H4 Similarity / Event-Time 规格
日期：2026-09-06
状态：DRAFT（G-H4-1/2/3/4 设计；crosswalk 已建，方法待拍板）
上游：H3 FEATURE ENGINEERING FREEZE（FREEZE_H3_20260906.txt）+ 方法论稿 §31-47
研究问题：CN 2000-2012 与 JP 哪个 lag（20-45y）最相似？结构阶段/事件是否对齐？1970 假说（CN 滞后 JP 30-40 年）是否成立？

## 1. 定位
H4 是**分析层**（非数据层）：在 H3 冻结的六模块 robust z 状态上做跨期比较。
- 输入：03_features/module/*_robustz_wide.csv（JP 1970-1995 / CN 2000-2012，六模块）
- 分层（§42-43）：MacroSimilarity ≠ ReturnSimilarity ≠ RiskSimilarity，分开计算、绝不互推
- 输出：lag 结构、模块/变量相似度、事件对齐、null benchmark 显著性

## 2. 模块与变量（H3 实际覆盖）
| 模块 | JP | CN | 配对 |
|---|---|---|---|
| GROWTH | real_gdp/iip/investment | 同 | ✓ |
| INFLATION | cpi/deflator | cpi（deflator 无） | 部分 |
| MONEY_CREDIT | m2/policy/jgb10y | m2 | 部分 |
| EXTERNAL | export/trade_gdp/reer/fx | export/reer（trade deferred） | 部分 |
| PROPERTY_ASSET | land/nikkei | equity/property_price | ✓（名称异质，crosswalk 需对齐） |
| DEMOGRAPHY_LABOR | wage/unemp/workage/dependency/youth/tfr/birth | wage/workage/dependency/youth/birth | 部分（JP unemp/tfr 无 CN；CN 无 unemp/tfr） |

## 3. Similarity 公式（方法论 §31）
模块 m 的相似度：
D_m(t,τ) = Σ_k w_k|Z^CN_k,t − Z^JP_k,τ| / (2Σ_k w_k)
S_m = 1 − D_m
S_total = Σ_m W_m S_m（第一版 module equal weight、within-module equal weight——防变量多的模块自动权重大）

Coverage Gate（§32）：总 Coverage≥70% 才算 S_total；模块独立≥50%（不能 NA→0）

## 4. 三层分析顺序（§39 固定顺序，DTW 只作第三层）
- C0 Fixed-Lag Scan（§33）：L∈{20,25,30,35,40,45} → 扩展 15..45；Score(L)=Mean_t S(CN_t,JP_{t−L})；同时存 median/P25/P75/coverage/module scores
- C1 Rolling / nearest-state（§35）：对每个 CN 年 t 找 L*_t=argmax_L S(CN_t,JP_{t−L})；输出 year/best lag/best S/second lag/gap；lag 剧烈跳动=不稳定信号
- C2 Event-Time Analysis（§37-38）：固定 temporal lead 与 structural event alignment 分开。事件候选：growth slowdown/oil shock/currency regime shift/asset peak/credit peak/working-age peak/property peak/policy easing start。t=0 归一比较 t=−5..+10
- C3 Constrained DTW（§39，最后才用）：|L_t−L_{t−1}|≤2y 或 Sakoe-Chiba band——禁无限扭曲

## 5. 多窗口验证（§34，防单窗偶然）
至少四 CN 窗：A 2000-2010 / B 2005-2015 / C 2010-2020 / D 2015-2025
（注意：H2/H3 当前 CN 段 2000-2012 冻结；B/C/D 窗需要 CN 2013-2025 = H1-P1 未授权项 → 当前只能做 A 窗 + 以 JP 侧滑动窗口做 robust 检验；窗 B/C/D 依赖 H1-P1 采集，列为依赖项）

## 6. 不确定性报告（§36）
ΔS = S_best − S_second；若 ΔS≈0 → "lag interval unresolved"，输出 L*=35 + plausible interval=30-40 而非单一 L*（避免假精确）

## 7. Null Benchmark（§40，任何 similarity 都要比）
- 随机打乱 JP 年份 / block permutation / random contiguous windows → S^null 分布
- S^observed 不显著高于 S^null → 不能称结构相似
- 输出：S^obs 在 null 分布的 percentile / p-value（经验）

## 8. Similarity Metric 三套（§41，多 metric 一致才升级证据）
1. Rank-state distance（robust z 已 rank 化，对 regime 鲁棒）——S 公式即此
2. Standardized Euclidean/Manhattan（连续宏观状态）
3. Distribution/trajectory（Wasserstein；DTW 属 C3 层）
只当 multiple metrics broadly agree 才升级证据等级

## 9. 阶段/事件（descriptive context only，§44-45，不替代连续 similarity）
JP 阶段（人工冻结 descriptive）：HIGH_GROWTH_LATE(~1970)/OIL_SHOCK_TRANSITION(1973-78)/STABLE_GROWTH(1980-84)/PLAZA_REFLATION(1985-87)/BUBBLE(1988-90)/POST_BUBBLE(1991+)
事件表（初版）：1971 Nixon / 1973 Oil1 / 1979 Oil2 / 1985 Plaza / 1987 crash / 1989 Nikkei peak / 1990 land-credit tightening

## 10. 执行顺序（分步）
H4.1 crosswalk（已完成建档）
H4.2 方法冻结（决策点拍板：lag 集/Coverage 阈值/metric 三套/Null 排列数/CN 窗范围）
H4.3 C0 Fixed-Lag Scan 实现 + 结果
H4.4 C1 Rolling + 不确定性
H4.5 C2 Event-Time + 事件表核验
H4.6 C3 Constrained DTW（如 C0-C2 结论需验证）
H4.7 Null Benchmark 全量
H4.8 H4 报告 + 审核包

## 11. 依赖/缺口（如实声明）
- CN 窗 B/C/D（2013-2025）依赖 H1-P1 采集 → 当前 H4 主结果限 A 窗（2000-2010/2012）
- CN equity 止 2007、trade /GDP deferred → EXTERNAL/PROPERTY 模块 CN 侧变量少
- JP unemp/tfr vs CN 无对应 → DEMOGRAPHY_LABOR 部分配对需 crosswalk 声明 comparison_grade
- full-sample robust z 的 lookahead（RETROSPECTIVE 定位）→ Null 用 block permutation 缓解；H4 不做 PIT 声明

## 12. 决策冻结（2026-09-06 用户拍板）
- D-H4-5：A 窗先行（CN 2000-2012 现有数据跑 C0-C2）；B/C/D 窗（2013-2025）依赖 H1-P1，后续补
- D-H4-1：L∈{20,25,30,35,40,45} 初扫 → 峰邻域 ±5 年逐 1 加密
- D-H4-2：Coverage Gate 总≥70% / 模块≥50%（方法论推荐值）
- D-H4-3：metric 三套 = Rank-state（主）+ Standardized Euclidean + Wasserstein
- D-H4-4：Null = 随机打乱 + block permutation(block=3y) 各 1000 次

## 13. 执行状态（2026-09-06）
- H4.1 crosswalk ✅（00_registry/cn_jp_concept_crosswalk.csv，23 pairs）
- H4.2 方法冻结 ✅（本节 D-H4-1~5）
- H4.3 C0 Fixed-Lag Scan（进行中）
- H4.4 C1 Rolling / H4.5 C2 Event-Time / H4.6 C3 DTW / H4.7 Null / H4.8 报告（待 C0）
