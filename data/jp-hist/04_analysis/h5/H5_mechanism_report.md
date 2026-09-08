# JP-HIST H5 Mechanism Decomposition / Regime Attribution — 综合报告（v02，外审修订版）

> 生成：2026-09-06 v02（外审 JP-HIST_H5_外部审核及下一步方向_20260906.md 修订采纳后重渲染；本报告数值全部由 h5_report_gen_v02.py 从 h5_*.csv 渲染，无手写数字；v01 版存于 v01 审核包 zip）
> 规格：00_registry/h5_mechanism_spec_20260906.md（FROZEN + §11 审核响应修订记录）｜主 norm z1970-2025（aux percentile）/ metric MANHATTAN / CR-2026-09
> 上游：FREEZE_H4_20260906.txt（v03e SCOPED FREEZE）｜引擎：04_analysis/h5/engine/
> 性质声明：retrospective structural-state 比较（RETROSPECTIVE_HISTORICAL，非 PIT）；classification/贡献度为描述性机制归因，非因果识别

## 0. 外审修订摘要（v02 相对 v01 的表述变更；阈值/search space 零改动）

- **R2/Q1**：不再用「module dominance」——冻结表述改为「INFLATION/CPI 是最强分类铰链（classification hinge），但不是整体 regime 判别力的多数主导来源」（§5.2）
- **R3/Q2**：Q2 状态 = **INTERPRETABLE FEATURE GEOMETRY / MECHANISM HYPOTHESIS（CONDITIONAL）**——分类与机制证明共用同一变量集（circular validation 未解），待 H5-FINAL held-out 验证；「mixed cluster 非纯 geometry」为过强表述，已删
- **R4**：DEMOGRAPHY_LABOR 分离 = magnitude 达标（0.502）但 directional coherence 不成立（birth +0.34 vs wage −0.67 反向）——不计入机制方向一致的分离模块
- **R5**：人口结论收紧为「已纳入的人口/工资变量未构成 CN-JP regime similarity 的主要正向驱动」，不宣称「人口机制完全不相似」（人口连续覆盖弱）
- **R6**：「价格先行于实体日本化」→ **HYP-H5-M1 candidate mechanism hypothesis**，待 held-out CPI 验证后升格
- **R1**：CF-B 语义 = robust-center（CN full-sample 中位数，z=0 ⇔ 原值=中位数），非算术均值
- Q3 维持 PASS；JGAP（1999-2002）diagnostic sensitivity 列入 H5-FINAL（不改冻结边界）

## Part 1｜分类骨架（D-H5-2 regime-level argmax）

| CN 年 | regime | rep JP 年 | S_total | cluster(v03e) | CN 年 | regime | rep JP 年 | S_total | cluster(v03e) |
|---|---|---|---|---|---|---|---|---|---|
| 2013 | J90 | 1991 | -0.433 | J90✓ | 2020 | J90 | 1993 | -0.754 | J90✓ |
| 2014 | J90 | 1992 | -0.510 | J90✓ | 2021 | J00 | 2005 | -0.352 | J00✓ |
| 2015 | OTHER | 1999 | -0.274 | OTHER✓ | 2022 | J90 | 1995 | -0.591 | J90✓ |
| 2016 | J90 | 1994 | -0.482 | J90✓ | 2023 | J00 | 2011 | -0.447 | J00✓ |
| 2017 | J00 | 2003 | -0.352 | J00✓ | 2024 | OTHER | 2002 | -0.742 | OTHER✓ |
| 2018 | J90 | 1993 | -0.553 | J90✓ | 2025 | J00 | 2003 | -0.730 | J00✓ |
| 2019 | J90 | 1993 | -0.374 | J90✓ |  |  |  |  |  |

**与 v03e cluster 基线对照：13/13 一致**（代表 JP 年亦同）。边界：两种方法共用同一 feature/state space——13/13 证明**分类结构稳定**，不单独证明分类具有独立经济机制含义（机制含义须 held-out 验证，见 Q2/Part 7）。

## Part 2｜H5-1 Module Contribution Decomposition（三层，D-H5-1）

### 2.1 水平分解（assigned pair，S_total=(1/n_alive)·ΣS_m；S_m≤0，越近 0 越相似）

| regime 组 | GROWTH | INFLATION | MONEY_CREDIT | EXTERNAL | DEMOGRAPHY_LABOR | n 年 |
|---|---|---|---|---|---|---|
| J90 | -0.943 | -0.631 | -0.255 | -0.739 | -0.888 | 12 |
| J00 | -0.559 | -0.393 | -0.261 | -0.344 | -0.795 | 4 |
| OTHER | -0.923 | -1.044 | -0.683 | -0.642 | -1.472 | 10 |

**MONEY_CREDIT（=m2_yoy 单变量模块）是 J90/J00 两组共同最相似模块**（≈-0.26）——货币增速状态收敛是匹配相似度的稳定支撑（与 Q1 的 LOMO 正向主力一致）。**DEMOGRAPHY_LABOR 是最大负贡献**（J90 -0.888 / J00 -0.795 / OTHER -1.472）——已纳入的人口/工资变量在匹配对上持续不相似，regime 匹配在水平相似度上绕过该维度（表述边界见 R5：此观察限于已纳入变量，不扩展为人口机制完全不相似）。

### 2.2 LOMO 边际 Δ（2013-2025 assigned pair；Δ>0 = 该模块支撑相似度，去除则 S_total 降）

| 去除模块 | mean Δ | median Δ | Δ>0/13 | 角色 |
|---|---|---|---|---|
| DEMOGRAPHY_LABOR | -0.0739 | -0.0214 | 4 | 负向拖累（已纳入人口/工资变量不相似） |
| EXTERNAL | +0.0260 | +0.0337 | 9 | 正向（外需/汇率次要支撑） |
| GROWTH | -0.0414 | -0.0472 | 4 | 负向拖累（增长结构在匹配对上偏不相似） |
| INFLATION | +0.0335 | +0.0279 | 7 | 正向（通胀通道次要支撑） |
| MONEY_CREDIT | +0.0558 | +0.0854 | 11 | 正向主力（货币通道稳定支撑） |

### 2.3 J90/J00 判别力 Δ_m（2013-2025；|S_m^J90best − S_m^J00best|）

| 模块 | mean Δ_m | 占 Δ 总和 | | 模块 | mean Δ_m | 占 Δ 总和 |
|---|---|---|---|---|---|---|
| INFLATION | 0.442 | 24.0% | | GROWTH | 0.333 | 18.1% |
| MONEY_CREDIT | 0.373 | 20.3% | | EXTERNAL | 0.332 | 18.0% |
| DEMOGRAPHY_LABOR | 0.359 | 19.5% | | | | |

## Part 3｜H5-2 Regime 画像：J90 vs J00（Q2 证据 + circularity 边界）

### 3.1 JP 侧：regime 期间 JP 自己的状态（robust-z 均值；机制差异的 JP 侧事实）

| 模块 | 变量 | J90(1991-98) | J00(2003-11) | J90−J00 | 读数 |
|---|---|---|---|---|---|
| GROWTH | real_gdp_yoy | -0.16 | -0.51 | +0.36 | J90 略低于均位，J00 更低 |
| GROWTH | iip_yoy | -0.75 | -0.37 | -0.38 | J90 工业收缩深于 J00 |
| GROWTH | investment_gdp | +0.41 | -0.57 | +0.99 | 投资通道分离最强：J90 仍高于自身长史均位（高位回落期），J00 低于均位 |
| INFLATION | cpi_yoy | +0.11 | -0.59 | +0.70 | J90 温和正通胀，J00 通缩——通胀通道分离第二强 |
| MONEY_CREDIT | m2_yoy | -0.35 | -0.58 | +0.23 | 两态均低于均位，J00 更甚（分离弱 0.23） |
| EXTERNAL | export_yoy | -0.20 | -0.08 | -0.12 | 差异小 |
| EXTERNAL | reer | +0.95 | +0.09 | +0.86 | J90 日元实际汇率极端强势，J00 回落均位附近 |
| DEMOGRAPHY_LABOR | wage_yoy | -0.28 | +0.39 | -0.67 | J90 低于均位，J00 相对自身历史偏高（方向异号项） |
| DEMOGRAPHY_LABOR | birth_rate | +1.01 | +0.67 | +0.34 | ΔCBR J90 下探深、J00 缓和（分离弱 0.34） |

**JP 侧分离量级（magnitude）≥0.5z：INFLATION 0.70 / GROWTH 0.57 / DEMOGRAPHY_LABOR 0.50。** 但方向一致性（directional coherence）分列（R4）：DEMOGRAPHY 内部 birth(+0.34) 与 wage(−0.67) 反向——magnitude 达标 ≠ 机制方向一致，故**方向一致的分离模块 = INFLATION + GROWTH（2 个）**，DEMOGRAPHY 不计入。MONEY_CREDIT 0.23 / EXTERNAL 0.49 两态不分离。

### 3.2 CN 侧：CN 年被分到 J90/J00 时自己的状态（2013-2025 assigned sets）

| 变量 | CN→J90 年均值 | CN→J00 年均值 | 方向一致(JP) |
|---|---|---|---|
| birth_rate | -0.412 | -0.940 | 一致 |
| wage_yoy | -0.456 | -0.846 | 反向 |
| export_yoy | -0.289 | 0.041 | 一致 |
| reer | 0.668 | 0.502 | 一致 |
| iip_yoy | -0.658 | -0.544 | 一致 |
| investment_gdp | 0.502 | -0.251 | 一致 |
| real_gdp_yoy | -0.964 | -0.696 | 反向 |
| cpi_yoy | 0.270 | -0.826 | 一致 |
| m2_yoy | -0.516 | -0.906 | 一致 |

**方向一致 7/9 变量**（两国各自的 J90−J00 差同号）；反向仅 wage_yoy 与 real_gdp_yoy。水平同号（更严）：JP-J90 vs CN→J90 8/9、JP-J00 vs CN→J00 6/9（J00 侧较弱：export 边界、wage/birth 反向——CN 近年各维度普遍深负，水平同号受两国标定阶段位置影响）。

**水平同号**：JP-J90 vs CN→J90 8/9；JP-J00 vs CN→J00 6/9（数值如上表口径）

**跨 norm（Q2 判据③，percentile 辅助）**：主分离通道同号（cpi JP 0.55/CN 0.80；investment JP 0.79/CN 0.34；reer JP 0.60），方向一致 7/9，无反转——反向变量与主 norm 同集。

### 3.3 Q2 状态（外审 R3：circular validation 边界）

**关键方法边界（circular validation）**：本层用同一组变量先定义 CN 年属于 J90/J00（分类），再用同一组变量的画像差异证明 J90/J00 有机制意义——被分到 J00 的年份天然在某些变量上更靠近 J00，等价于 in-sample explanation of classifier features，不能独立区分「真实经济机制复现」与「分类器自身产生的组间差异」。

**Q2 状态：INTERPRETABLE FEATURE GEOMETRY / MECHANISM HYPOTHESIS（CONDITIONAL）**——当前可支持「分类具有可解释的 feature geometry，其中 cpi/investment/reer 是最清晰的分离通道」，**不**支持「这些差异已独立证明 CN 与 JP 相应历史阶段具有同构经济机制」（即不称 CONFIRMED MECHANISM REPLICATION）。JP 侧机制差异事实（3.1）与 CN 侧方向跟踪（3.2）作为 HYPOTHESIS 证据保留；「mixed cluster 非纯 metric geometry」为过强表述，撤销。正式确认须 H5-FINAL held-out validation（分类时不使用待验变量，再检查该变量在分类组间的方向差异）。

## Part 4｜H5-3 Counterfactual Module Removal（三轨；Q1 = classification hinge）

翻转 = 该 CF 下 CN 年 regime 归属 ≠ 基线。2013-2025 计数：

| 模块 | CF-A(剔除) | CF-B(robust-center) | CF-C(惰性) | CF-A 翻转年 |
|---|---|---|---|---|
| INFLATION | 5/13 | 4/13 | 5/13 | 2016,2018,2023,2024,2025 |
| MONEY_CREDIT | 2/13 | 3/13 | 2/13 | 2020,2021 |
| EXTERNAL | 2/13 | 1/13 | 2/13 | 2017,2025 |
| GROWTH | 1/13 | 1/13 | 1/13 | 2023 |
| DEMOGRAPHY_LABOR | 2/13 | 1/13 | 2/13 | 2015,2024 |

**CF 口径注（R1）**：CF-A=剔除模块重归一（LOMO 对照）；CF-B=CN 该模块 z 置 0——robust-z 中位数中心化使 z=0 ⇔ 原值=CN 自身 full-sample 中位数（robust-center / 长期中心水平），非算术均值；CF-C=双侧 dz 置 0（惰性）。

**INFLATION 是唯一触及预注册翻转阈值（≥3/13）的模块**：CF-A 5/13、CF-B 4/13、CF-C 5/13 跨口径一致。翻转方向含实质内容：2023/2025（基线 J00）去通胀后落 J90、2024（基线 OTHER）落 J90、2018（基线 J90）落 J00——**CN 2023-25 的 J00/近态归属对 CPI 通道高敏感**（cpi 近零 z≈-0.8 仿 JP 2000s），剥离后增长/货币状态回落到 JP 1990s 匹配。

### Q1 判定（外审 R2 表述修订）

| 预注册判据（执行） | 值 | 触发 |
|---|---|---|
| CF-A 单一模块 removal 翻转 ≥3/13 | INFLATION 5/13 | YES（冻结 OR 规则触发，执行合规） |
| Δ_m 占全模块 Δ 总和 >50% | 最高 INFLATION 24.0% | NO（<50%） |

**Q1 = INFLATION/CPI 是最强分类铰链（classification hinge），但不是整体 regime 判别力的多数主导来源。** 并观两指标：Δ_m 份额 24%<50% → 无模块在判别水平占多数；CF-A 翻转 5/13（8/13 不翻转）→ 边界年份的 regime assignment 对 CPI 单变量高敏感；MONEY_CREDIT 在水平相似度与 LOMO 中是更稳定的支撑项（Part 2）。「模块」措辞不放大证据规模：INFLATION=cpi_yoy 单变量，「通胀铰链」≡「CPI 对部分年份分类高敏感」。不再使用「module dominance / module-specific analogy」作结论措辞。

## Part 5｜H5-4 Transition Matrix（Q3 判定，PASS）

### 5.1 状态序列与转移（2013-2025 主表）

状态序列：2013:J90 → 2014:J90 → 2015:OTHER → 2016:J90 → 2017:J00 → 2018:J90 → 2019:J90 → 2020:J90 → 2021:J00 → 2022:J90 → 2023:J00 → 2024:OTHER → 2025:J00

| 转移 | J90 | J00 | OTHER | 行条件概率（→） |
|---|---|---|---|---|
| J90→（7） | 3 | 3 | 1 | J90 0.43 / J00 0.43 / OTHER 0.14 |
| J00→（3） | 2 | 0 | 1 | J90 0.67 / J00 0.00 / OTHER 0.33 |
| OTHER→（2） | 1 | 1 | 0 | J90 0.50 / J00 0.50 / OTHER 0.00 |

连续 run：J90×2(2013-2014)；OTHER×1(2015-2015)；J90×1(2016-2016)；J00×1(2017-2017)；J90×3(2018-2020)；J00×1(2021-2021)；J90×1(2022-2022)；J00×1(2023-2023)；OTHER×1(2024-2024)；J00×1(2025-2025)

| Q3 判据 | 值 | 通过 |
|---|---|---|
| ① 末 3 年（2023-25）模态 = J00 且 2024 不中断 | 2023:J00;2024:OTHER;2025:J00（2024=OTHER） | **FAIL** |
| ② 末 5 年无 ≥2 年连续 OTHER/J90 run | 2021:J00;2022:J90;2023:J00;2024:OTHER;2025:J00 | PASS |
| ③ P(J00→J00) ≥ 0.5 | 0.0（0/3：J00 年份全部次年跳出） | **FAIL** |

**Q3 = PASS / NO PERSISTENT J00 TRANSITION。** 2023-25 的 J00 匹配为间歇摆动而非 regime 进入——2024 回落 OTHER 中断；J00 从不持续（3/3 次年跳出：2 回 J90、1 OTHER）；J90→J00（0.43）= J90→J90（0.43）对称，无单调迁移；最长 run J90×3（2018-20）。表述禁令（FREEZE_H4 W05）下不得写「CN 进入失去的二十年后期」。

**gap 边界注（外审 §16-17，JGAP 留 H5-FINAL）**：2024 rep=JP 2002 属冻结 OTHER（1999-2002 gap 段）；「不持续」结论在预注册分类下成立。JGAP=1999-2002 四态 diagnostic（J90/JGAP/J00/OTHER）不改冻结边界、不改变 Q3 判定，仅判断 2024 是「脱离 J00」还是「绕 J00 过渡带摆动」——列入 H5-FINAL。

### 5.2 附表：CN 2000-2012（J00 不可达，lag≥10 下界）

CN 2000-2012：J90×5（rep 1991-1997）、OTHER×8（rep 1984-1987）、J00×0（几何不可达）——早期 rep 集中于 JP 1980s（Plaza 前/中段），描述性不入主表。

## Part 6｜三问状态与边界（v02 修订）

| 问题 | 状态（v02） | 内容 |
|---|---|---|
| Q1 少数模块主导？ | **分类铰链 YES（INFLATION/CPI），非多数主导** | CF 翻转 5/13 达预注册阈值；Δ_m 份额 24%<50%——边界年份分类对 CPI 高敏感（R2） |
| Q2 J90/J00 机制可解释不同？ | **CONDITIONAL：INTERPRETABLE FEATURE GEOMETRY / MECHANISM HYPOTHESIS** | cpi/investment/reer 通道 JP 侧分离清晰、CN 侧方向一致 7/9；circular validation 未解，机制复现待 held-out（R3/R4） |
| Q3 2023-25 → J00 持续 transition？ | **NO（PASS）** | 2024 中断 + P(J00→J00)=0 + J90↔J00 对称 → 摆动非迁移 |

**研究主问题（升级版）分答（exploratory）**：

1. **可重复识别的相似 structural regimes？——是（分类结构层面）。** J90/J00/OTHER 三分在 H4 bootstrap 与 H5 regime-argmax 两法下 13/13 一致；此稳定性的机制含义待 held-out 验证。
2. **机制相同？——候选通道证据（CONDITIONAL）。** CN 落 J00 态携带「近零通胀/通缩 + 投资放缓」指纹、落 J90 态携带「温和通胀 + 投资率仍偏高」指纹；cpi/investment/reer 是最清晰分离通道（方向一致 + 跨 norm 不反转）。工资与真实增速通道方向不同构。**已纳入人口/工资变量未构成相似性的主要正向驱动**（不宣称人口机制完全不相似——R5）。
3. **CN 正在 regime 间迁移？——无证据（摆动）。** J00 全部瞬时、转移对称；2023-25 J00 归属为 CPI 单通道摆动。

**HYP-H5-M1（Price-channel-leading hypothesis，candidate，R6）**：CN 结构状态 ≈ JP1990s 实体/信用主体 × JP2000s 价格维度——物价动态先于实体/工资/人口进入「类 JP 2000s」区间。当前此叙事部分由分类算法定义（CPI 参与分类），**待 held-out CPI validation（H5-FINAL Test 1）后升格或降级**；未验证前不写入最终研究结论。

**表述边界**：① retrospective 比较，非 PIT/非因果；② Q1 用「classification hinge」不用「module dominance」，INFLATION/MONEY_CREDIT 单变量模块（模块结论≡单变量结论）；③ Q2 限于 interpretable feature geometry + mechanism hypothesis，不称机制确认（circularity 未解）；④ n 小（分类 13 年、J00 组 4 年）——Q 判定为描述性标准；⑤ 人口结论限于已纳入变量（wage/birth ΔCBR），人口连续覆盖弱；⑥ 2024=OTHER(JP 2002) 的 gap 态解读留 JGAP diagnostic；⑦ H5-5 event-time 未执行——列 H5-FINAL 辅助项（机制路径比较，非硬年份拼接）。

## 审计指引（复现；同 v01）

```bash
# 04_analysis/h5/engine/: h4v03d_engine.py + h5_h51_decomposition.py + h5_h234_analysis.py + h5_q2_percentile_aux.py
# H5-1:  /usr/bin/python3 engine/h5_h51_decomposition.py
# H5-2/3/4: /usr/bin/python3 engine/h5_h234_analysis.py
# Q2 aux: /usr/bin/python3 engine/h5_q2_percentile_aux.py
# 报告:  /usr/bin/python3 engine/h5_report_gen_v02.py
```