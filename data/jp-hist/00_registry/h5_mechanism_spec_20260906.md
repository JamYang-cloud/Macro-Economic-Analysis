# JP-HIST H5 Mechanism Decomposition / Regime Attribution — 规格（预注册 DRAFT）
日期：2026-09-06
状态：**FROZEN**（2026-09-06 用户 clarify 拍板 D-H5-1..4 全按推荐；批准后不得根据输出移动区间/阈值）
依据：外部审核 JP-HIST_H4v03e_外部审核及H5工作方向_20260906.md（§11 批准 / §12 H5-1..5 方向 / §13 三问 Q1-Q3 / §14 研究主问题升级）
上游：FREEZE_H4_20260906.txt（G-H5-1..3）；冻结资产 v03e 集只读
性质：**机制分解 / regime 归因**——不预设 lag=22、不做逐年"哪年像哪年"对齐、不用视觉事件拼接

## 0. 研究主问题（§14 升级版）
由"CN 是否滞后 JP 30-40 年"升级为：
> CN 与 JP 在长期宏观发展中是否出现**可重复识别的相似 structural regimes**？这些 regime 的**经济机制是否相同**？CN 是否正在发生**从一种日本式 regime 向另一种的状态迁移**？

H5 回答其三个子问题（§13）：
- **Q1**：中日 structural similarity 是否由少数模块主导？若是 → 结论降级为 module-specific analogy。
- **Q2**：J90（JP 1991-1998）与 J00（JP 2003-2011）两类 regime 是否具有**可解释且稳定不同**的经济机制？若否 → mixed cluster 只是 metric geometry，不赋予历史阶段含义。
- **Q3**：CN 2023-2025 对 J00 的匹配是否构成**持续 regime transition**？若只是短暂跳动 → 不得写"进入失去的二十年后期"。

## 1. 冻结 search space / 参数（沿用 H4 v03，禁移动）
- CN years: 2000-2025；JP years: 1970-2025（panel 均为 H4 FROZEN 输入，只读）
- lag search: 10-45；模块: GROWTH / INFLATION / MONEY_CREDIT / EXTERNAL / DEMOGRAPHY_LABOR（5；PROPERTY_ASSET 因 crosswalk 无 A/B 对仍不在主检验）
- coverage_rule_id: CR-2026-09（module ≥50% A/B 对有效；≥4 模块存活才给 S_total）
- normalization（主）: JP robust-z full-sample 1970-2025 / CN robust-z full-sample 2000-2025（CALIB 与 v03e 主档一致）；percentile 为辅助诊断
- metric（主）: MANHATTAN（S_total 引擎原生）；RANKSTATE 辅助
- module weight: 等权 w_m = 1/n_alive（引擎 total_score 现状，H5-1 分解不改变它）
- birth_rate 一律 ΔCBR 后进 state（H0 冻结变换）；matched pair 的 z 值直接从引擎 state() 缓存取——**H5 不重算任何 H3/H4 状态，只做分类与分解**

## 2. Regime 定义（外审 §12 定界，非数据驱动重切——重切即 post-hoc）
- **J90** = JP 年份 ∈ [1991, 1998]（泡沫破灭→停滞初期）
- **J00** = JP 年份 ∈ [2003, 2011]（2000s 通缩/低增长段，BIS 亦止 2011 前后）
- **OTHER** = 其余 JP 可达年份（1970-1990 / 1999-2002 / 2012-2025）
- 可达性约束（lag 10-45 下限决定）：J90 对 CN 年最早自 CN=2001 可达（lag≤45 上界不构成约束，因 jp≥1970）；**J00 对 CN 年最早自 CN=2013 可达**（CN 2012 - 2003 = lag 9 < 10）。→ CN ≤2012 的 J00 分类在几何上不可能，transition 主表须落在 2013-2025（见 D-H5-4）。

## 3. 数据基线（现状观察，供画像对照——非冻结结论）
CN 2013-2025 cluster-median jp_year（800/800 valid，module-subset bootstrap，v03e）：
| CN 年 | jp_median | regime | CN 年 | jp_median | regime |
|---|---|---|---|---|---|
| 2013 | 1991 | J90 | 2020 | 1993 | J90 |
| 2014 | 1992 | J90 | 2021 | 2005 | J00 |
| 2015 | 1999 | OTHER | 2022 | 1995 | J90 |
| 2016 | 1994 | J90 | 2023 | 2011 | J00 |
| 2017 | 2003 | J00 | 2024 | 2002 | OTHER |
| 2018 | 1993 | J90 | 2025 | 2003 | J00 |
| 2019 | 1993 | J90 | | | |

汇总 7 J90 + 4 J00 + 2 OTHER（cluster 口径）。注意 **2023/2024/2025 = J00/OTHER/J00**——Q3 "persistent J00" 现状并非常态化，须由 H5-4 transition 检验而非直接断言。

## 4. H5-1 Module Contribution Decomposition（第一执行任务）
对每个 CN 年 c × 其 JP matched state y，分解 5 模块对 S_total 的贡献。
- matched state 定义：由 D-H5-2 的分类口径给出（regime-level argmax 或 cluster median → 取该 regime 内最优 S 对应 jp_year 作代表对）
- 引擎原生分解：S_total(c,y) = (1/n_alive)·Σ_m S_m(c,y)（m 遍历存活模块）→ 每模块**水平贡献** = S_m/n_alive，天然精确加总（负值如实保留——MANHATTAN 下 S_m≤0，报告以"相似度增量/亏损"解读，不做 share-of-positive 归一化）
- 输出 `h5_module_contribution_{cn_year}.csv`：cn_year / jp_year(代表) / regime / module / S_m / valid_pairs / eligible_pairs / coverage_ratio / contribution(=S_m/n_alive) / S_total
- 聚合表 `h5_module_contribution_summary.csv`：按 regime（J90-matched / J00-matched / OTHER）分组的模块均分与判别差
- **判别力指标**（直接服务 Q1/Q2）：对每个 CN 年，Δ_m = |S_m^{best-in-J90} − S_m^{best-in-J00}|（模块 m 在两个 regime 组内最佳相似度之差）——衡量该模块对"CN 分到 J90 还是 J00"的区分贡献；跨年汇总后给出模块排序。
- Q1 判据（预注册）：若存在单一模块满足「其 removal 翻转 ≥3/13 个 CN 年的 regime 归属」或「Δ_m 占全模块 Δ 总和 >50%」→ 判定 module dominance → 结论降级 module-specific analogy；否则 aggregate structural-state analogy 成立前提。

## 5. H5-2 J90 vs J00 Regime 机制画像
- 构造两 regime 的机制变量画像（不找视觉相似、不比日历年份）：
  1. **JP 侧**：J90 年集与 J00 年集内各变量（含模块内每个 A/B pair 变量）robust-z 的均值/中位/四分位——"JP 处于该 regime 时，结构状态是什么样"
  2. **CN 侧**：被分到 J90 的 CN 年、被分到 J00 的 CN 年，各自模块/变量 z 画像
  3. **对照表**：JP-J90 画像 vs CN→J90 画像；JP-J00 画像 vs CN→J00 画像——逐变量同号/异号、|z| 差距
- 输出 `h5_regime_profiles_{jp|cn}.csv` + `h5_regime_profile_contrast.csv`
- Q2 判据（预注册）：J90/J00 机制差异"可解释且稳定"需同时满足 ① ≥2 个模块在 J90 与 J00 的 JP 侧画像呈同符号且差异 ≥0.5 z（如 J90 更多地产/投资下行 + J00 更多低利率/低名义增长）；② CN→J90 年画像与 JP-J90 画像在这些模块同号，CN→J00 亦然（CN 年携带了对应 regime 的机制指纹）；③ 该差异跨 norm（percentile 辅助）不反转。不满足 → Q2 回答"几何说"，mixed cluster 不赋予历史阶段含义。

## 6. H5-3 Counterfactual Module Removal（分类翻转检验）
问题（外审原文）：把某模块替换为长期均值后，CN 年份还会被分到同一 JP regime 吗？——识别 classification 的 causal-like driver（非因果识别，但强于简单 LOMO）。
口径候选（D-H5-3 待拍板，均在引擎 z-state 空间内实现，**不触碰 H3 FROZEN 变换**）：
- **CF-A（LOMO 基线）**：剔除模块 m、余模块权重再归一 → 重分类（外审明言"不仅做这个"）
- **CF-B（CN 侧长期均值中和；对应外审"替换为长期均值"直读）**：CN 模块 m 的 z 全部置 0（= CN 自身长期中位水平）→ 模块 m 距离项变为 |z_jp_m(y)| → 问"若 CN 在 m 上是平均的，还会落同一 regime 吗"
- **CF-C（双侧中和/惰性模块）**：模块 m 每对 dz 置 0（视 CN≡JP on m at all y）→ 模块 m 失去一切区分与吸引作用 → 问"m 作为相似度吸引子的角色"
- 输出 `h5_counterfactual_classification.csv`：cn_year / baseline_regime / per-CF 新 regime / flip(0/1) / per-module 汇总行；翻转年数汇总 `h5_cf_flip_summary.csv`
- 判别口径：翻转 = baseline regime ≠ CF 后 regime（或代表 jp_year 移出原 regime 域）。CF-B 与 CF-C 的差异拆开报（区分"平均化"vs"惰性"两种归因语义）。

## 7. H5-4 Transition Matrix
- 每 CN 年分类 s_t ∈ {J90, J00, OTHER}（分类口径 = D-H5-2 拍板结果）
- 主表 span 由 D-H5-4 拍板（推荐 2013-2025 为主；2000-2012 受可达性约束仅描述性附表）
- 输出：
  - `h5_state_sequence.csv`：cn_year / state / representative_jp_year / reachability_note（J00 不可达年份显式标注）
  - `h5_transition_matrix.csv`：3×3 计数与行条件概率 P(s_t | s_{t−1})（含 2023-25 尾窗路径）
  - `h5_transition_path.csv`：逐年状态序列 + 连续 run 长度（persistence 统计）
- Q3 判据（预注册，n=13 小样本 → 描述性判定不称检验）：**persistent J00** 成立需同时满足 ① 末 3 年（2023-2025）模态 state = J00（modal 口径；若 2024 落 OTHER 则视为中断，如实报）；② 末 5 年内无 ≥2 年连续 OTHER/J90 反向 run；③ J00→J00 行条件概率 ≥0.5。三条齐 → "进入 J00 段"；否则表述为 "短暂/不持续 J00 匹配"。当前观察（2023 J00 / 2024 OTHER / 2025 J00）预示 ① 大概率不满足——如实检验，不得为结论调整判据。

## 8. H5-5 Event-time（辅助，机制识别后才有资格）
- 前置条件：H5-1..4 完成且 Q2 给出机制解释后才启动
- 比较对象 = **机制变量的路径形状**（JP asset-bust 段的 land/equity 路径 vs CN property 下行路径；JP deflation-onset 段 CPI 路径 vs CN disinflation 等），非日历年份拼接
- 输出定位：辅助说明/报告叙事层，不进主判定

## 9. 执行与治理纪律（H4 v0.3e 铁律延续）
- H5 引擎 = 以 /tmp/h4v03d_engine.py 为模块 import 扩展（module_diffs/module_score/total_score/state 复用；WAGE_EXCLUDE 保持 v03e 默认空）；**H5 引擎快照先归档** 04_analysis/h5/engine/（防 /tmp 丢失）再跑
- 引擎任何修改 → 先跑与 v03e 对齐的 sanity（如 B 窗 CN2013 MANHATTAN best 应 ≈1991-92 邻域）→ 再全量
- 报告数字禁手写：全部表格由 generator 从 h5_*.csv 渲染（single source of truth）；每 CSV 头带 method_id/calibration_id/coverage_rule_id/metric_id/status
- 产物规约：04_analysis/h5/（本 spec 的 H5-1..4 csv + H5_mechanism_report.md + engine 快照 + 审核包 ZIP+manifest，送审形态按 H2/H3/H4 惯例）
- 三问（Q1-Q3）判据冻结后禁移动；数据缺口（JP 连续年度人口/cgb10y/corp CN 侧）不阻塞——coverage 如实计

## 10. 决策记录（D-H5-1..4，2026-09-06 clarify 全按推荐拍板）
- **D-H5-1** 模块贡献定义 = **三层全做**：水平分解表（S_m/n_alive，引擎原生精确加总）+ LOMO 边际 Δ（去模块前后 S_total 差）+ J90/J00 判别力 Δ_m（模块对"CN 分到 J90 还是 J00"的区分贡献，直接服务 Q1/Q2）
- **D-H5-2** Regime 边界 = **沿用外审定界** J90=[1991,1998] / J00=[2003,2011] / OTHER=其余（禁数据重切）；CN 年分类口径 = **regime-level argmax**（各 regime 可达 JP 年组内取最佳 S 的 max，argmax 定 regime）
- **D-H5-3** Counterfactual = **三轨全跑，CF-B 作主口径**（CF-B=CN 模块 z 置 0 = CN 自身长期均值，对应外审原文；CF-A=LOMO 剔除对照；CF-C=双侧中和惰性模块）
- **D-H5-4** Transition 窗口 = **2013-2025 主表 + 2000-2012 可达性约束下描述性附表**（J00 对 CN≤2012 不可达如实标注）

本 spec 自本条签署后为 FROZEN 文档；H5 产物与报告逐条引用 D-H5-x 编号。

## 11. 审核响应修订记录（外审 JP-HIST_H5_外部审核及下一步方向_20260906.md，2026-09-06 采纳；阈值/search space/regime 边界零改动，仅表述与口径修订登记）
- **R1（P1 采纳）** CF-B 语义修正：z 置 0 = CN 该变量 full-sample robust-z 中位数（robust center），非算术均值——§6 CF-B 与 §10 D-H5-3 中「长期均值」措辞统一改为「robust-center / 长期中心水平（full-sample median）」
- **R2（Q1 表述修订采纳）** 不再用「module dominance / module-specific analogy」作 Q1 结论措辞；冻结表述 = 「INFLATION/CPI 是最强分类铰链（classification hinge），但不是整体 regime 判别力的多数主导来源」——CF-A 翻转 5/13 达预注册阈值是执行事实（OR 规则合规触发），解释从 dominance 降为 hinge/sensitivity
- **R3（Q2 状态降级采纳）** circular validation 成立（分类与机制证明共用变量集）；Q2 状态 = INTERPRETABLE FEATURE GEOMETRY / MECHANISM HYPOTHESIS（CONDITIONAL），撤销「mixed cluster 非纯 metric geometry」表述；机制复现确认须 H5-FINAL held-out（Test 1 分类去通道 + 通道 held-out 方向检验 / Test 3 Mechanism Direction Score）
- **R4（Q2 判据实现修正采纳）** DEMOGRAPHY 的 mean_abs_JP_sep=0.502 系 |−0.667| 与 |+0.337| 均值（方向相反）——分离判定分列 magnitude vs directional coherence；方向一致的分离模块 = INFLATION + GROWTH（2），DEMOGRAPHY 不计入
- **R5（人口结论收紧采纳）** 「人口不是 CN 与 JP 相似的原因」→「已纳入的人口/工资变量（wage_yoy/birth ΔCBR）未构成 CN-JP regime similarity 的主要正向驱动」；不宣称人口机制完全不相似（人口连续年度覆盖弱，H1-P1 遗留）
- **R6（叙事降级采纳）** 「价格先行于实体日本化」→ HYP-H5-M1（Price-channel-leading hypothesis，candidate）——部分由分类算法定义（CPI 参与分类），待 held-out CPI validation 升格/降级
- **R7（Q3 维持 + JGAP 新项）** Q3 = PASS / NO PERSISTENT J00 TRANSITION 维持；新增 H5-FINAL 项 JGAP（1999-2002）四态 diagnostic sensitivity（J90/JGAP/J00/OTHER，不改冻结边界、不改变 Q3 判定）
- H5 状态：CONDITIONAL PASS（外审 §25）；下一阶段 = H5-FINAL Independent Mechanism Validation（held-out channel/variable + direction score + bootstrap/permutation + JGAP + event-time 辅助）
