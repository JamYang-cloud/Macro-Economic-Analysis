# JP-HIST H5-FINAL Independent Mechanism Validation — 验证报告

> 生成：2026-09-06（数值全部由 h5_final_report_gen.py 从 h5_final/*.csv 与 annual panels 渲染，无手写数字）
> 规格：00_registry/h5_final_spec_20260906.md（FROZEN）｜上游：H5 CONDITIONAL PASS（外审 + 响应 R1-R7 采纳）
> 方法：held-out validation——用于验证机制的变量不参与该年份 regime 分类；permutation 2000 reps / bootstrap 90% CI 1000 reps（n 小，描述性声明）

## 1. 分类骨架基线校验

drop=∅ 重分类 vs h5_state_sequence（2000-2025）：**0/26 漂移**——held-out 引擎与 H5 v02 基线完全一致，无实现漂移。

## 2. 通道级 held-out（Test 1）与变量级 LOVO（Test 2）——主 norm z1970-2025

符号约定：sign_match = sign(D_v^CN,−v)==sign(D_v^JP)；D_v^CN,−v = 分类不含 v 时 CN→J90 组与 CN→J00 组的 z_v 均差。feasible 要求 J90/J00 组各 ≥3 年且双侧值齐。

| drop | held-out v | n_J90/n_J00 | D_v^JP | D_v^CN(−v) | sign | boot90 CI | perm p | 判定 |
|---|---|---|---|---|---|---|---|---|
| CH-CPI_YOY | cpi_yoy | 8/3 | 0.704 | 0.011 | Y | [-0.540,0.590] | 1.0 | **FAIL（效应坍缩≈0）** |
| CH-INVESTMENT_GDP | investment_gdp | 7/4 | 0.989 | 0.753 | Y | [0.151,1.433] | 0.1589 | HELD-OUT SUPPORTED（bootstrap-supported separation；perm p<0.10 未达·n 小） |
| CH-REER | reer | 8/3 | 0.860 | -0.071 | N | [-0.349,0.183] | 0.7281 | **FAIL（方向不一致/无效应）** |
| CH-M2_YOY | m2_yoy | 7/3 | 0.234 | 0.368 | Y | [0.096,0.636] | 0.1984 | HELD-OUT SUPPORTED（bootstrap-supported separation；perm p<0.10 未达·n 小） |
| CH-WAGE_BIRTH | birth_rate | 8/5 | 0.337 | 0.114 | Y | [-1.156,1.371] | 0.91 | 方向一致（弱：CI 含 0） |
| CH-WAGE_BIRTH | wage_yoy | 8/5 | -0.667 | 0.642 | N | [0.147,1.210] | 0.064 | **FAIL（方向不一致/无效应）** |
| LOVO-birth_rate | birth_rate | 9/4 | 0.337 | -0.347 | N | [-1.626,0.861] | 0.7286 | **FAIL（方向不一致/无效应）** |
| LOVO-cpi_yoy | cpi_yoy | 8/3 | 0.704 | 0.011 | Y | [-0.548,0.568] | 1.0 | **FAIL（效应坍缩≈0）** |
| LOVO-export_yoy | export_yoy | 9/2 | -0.119 | 0.419 | — | — | — | 不可行 |
| LOVO-iip_yoy | iip_yoy | 7/4 | -0.377 | -0.114 | Y | [-0.501,0.260] | 0.6632 | 方向一致（弱：CI 含 0） |
| LOVO-investment_gdp | investment_gdp | 7/4 | 0.989 | 0.753 | Y | [0.153,1.425] | 0.1629 | HELD-OUT SUPPORTED（bootstrap-supported separation；perm p<0.10 未达·n 小） |
| LOVO-m2_yoy | m2_yoy | 7/3 | 0.234 | 0.368 | Y | [0.096,0.619] | 0.1974 | HELD-OUT SUPPORTED（bootstrap-supported separation；perm p<0.10 未达·n 小） |
| LOVO-real_gdp_yoy | real_gdp_yoy | 7/5 | 0.356 | -0.154 | N | [-0.869,0.516] | 0.7406 | **FAIL（方向不一致/无效应）** |
| LOVO-reer | reer | 8/3 | 0.860 | -0.071 | N | [-0.329,0.195] | 0.7211 | **FAIL（方向不一致/无效应）** |
| LOVO-wage_yoy | wage_yoy | 6/4 | -0.667 | 0.449 | N | [-0.087,0.981] | 0.2259 | **FAIL（方向不一致/无效应）** |

**通道级核心结果**：
- **CH-INVESTMENT（held-out 方向性复现，descriptively）**：分类不含 investment_gdp 时 J90/J00 组仍沿 JP 方向分离——D_CN=+0.753（与 JP D=+0.989 同号，标准化分离幅度约为日本的四分之三；此比值是 standardized separation magnitude ratio，非经济强度复制比例），bootstrap 90% CI [0.151,1.433] 不含 0；permutation p≈0.16 未达常规 10% 阈值（n 小）——称「bootstrap-supported held-out directional replication」，不称统计显著机制。
- **CH-CPI（FAIL，效应坍缩）**：分类不含 CPI 后，J00(−CPI) 组={2017,2018,2021}（2023/2025 被其他维度拉回 J90）——组间 CPI 差 D_CN=+0.011≈0（JP 差 +0.704 的 1.6%），boot CI 跨 0，perm p=1.0。**CPI 相似度不独立复现：近零 CPI 的 2023/2025 之所以落 J00 只因为 CPI 在分类器里（self-referential）**——直接支持 Q1 的 hinge 判定并否定 CPI 通道的独立机制地位。
- **CH-REER（FAIL）**：D_CN=−0.071（JP +0.860），方向相反且≈0。人民币强势在 CN 2013-25 各组间无 JP 式分化。
- **CH-M2（held-out 方向性复现，secondary non-gate evidence）**：D_CN=+0.369（JP +0.234 同向），boot CI [0.096,0.636] 不含 0（perm p≈0.20 未达 10% 阈值）——货币增速通道为附加复现证据，按冻结 gate 不计入 Q2-Final 主判据。
- **CH-WAGE_BIRTH**：wage D_CN=+0.642 反向于 JP(−0.667)（FAIL）；birth D_CN=+0.114 仅为 JP 差 34%、CI 跨 0、p=0.91——held-out 无独立证据（此前循环口径下 birth 的「方向一致」在 held-out 下弱化消失，循环伪影实证）。

## 3. Q2-Final gate（外审 §23，冻结判据）

| 核心通道 | held-out 方向一致 | ≥1 辅助不反转 | gate 计入 |
|---|---|---|---|
| CPI | FAIL（D≈0.011，p=1.0） | percentile aux 亦反转 | ✗ |
| INVESTMENT | **Y**（D=+0.753，CI 不含 0） | bootstrap 不反转 | ✓ |
| REER | FAIL（反向 ≈0） | — | ✗ |

**Q2-Final = INTERPRETABLE FEATURE GEOMETRY ONLY**（3 核心通道中仅 INVESTMENT 1 个 held-out 复现，<2 阈值）。按冻结 gate（外审 §23），机制对应关系**不**获 SUPPORTED 状态。补充说明（不改判据）：非 gate 的 M2 通道 held-out 亦复现（CI 不含 0）——gate 通道清单敏感性留给复审决定；本报告按预注册判据如实判定。

## 4. Q1-Final 与 Q3-Final

- **Q1-Final = YES（classification hinge：INFLATION/CPI）——可冻结**。H5-FINAL 进一步强化：held-out 显示 CPI 是纯分类铰链（剥离后效应坍缩至 0），不是独立机制——hinge 判定与机制否定互洽。
- **Q3-Final = NO PERSISTENT J00 TRANSITION（PASS）——可冻结**。2023:J00/2024:OTHER/2025:J00；P(J00→J00)=0。

## 5. JGAP（1999-2002）四态 diagnostic（不改冻结边界，不改变 Q3 判定）

四态序列（2013-2025）：2013:J90 → 2014:J90 → 2015:JGAP → 2016:J90 → 2017:J00 → 2018:J90 → 2019:J90 → 2020:J90 → 2021:J00 → 2022:J90 → 2023:J00 → 2024:JGAP → 2025:J00

三态 OTHER 中的 2015(rep JP 1999) 与 2024(rep JP 2002) 在四态下均落入 **JGAP（1999-2002）**——2023:J00 → 2024:JGAP → 2025:J00 的解读从「突然回到 OTHER」修正为**「绕 J90→J00 过渡带摆动」**（2024 处于 JP 两 regime 之间的 gap 段，非 1970-90/2012+ 的远 OTHER）。Q3 判定（非持续 J00）不变；2022:J90 与 2024:JGAP 的存在提示 CN 在 1990s 态与过渡带之间往返，而非沿 JP 轨迹单调推进。

## 6. Event-time 辅助（机制变量路径；HYP-H5-M1 语境，非主判定）

### 6.1 Price 路径（JP deflation onset vs CN 近零通胀）

JP CPI yoy（t0=1999 首次持续负值前段 1993-2006）：1991:3.28，1992:1.74，1993:1.26，1994:0.69，1995:-0.11，1996:0.14，1997:1.70，1998:0.68，1999:-0.34，2000:-0.68，2001:-0.72，2002:-0.91，2003:-0.26，2004:-0.02，2005:-0.24，2006:0.22（%）

CN CPI yoy（t0=2023 首次 ≤0.5，2017-2025）：2017:1.60，2018:2.10，2019:2.90，2020:2.50，2021:0.90，2022:2.00，2023:0.20，2024:0.20，2025:0.00（%）

路径对照：JP 从 1991 年 +3.3% 滑入 1999-2005 持续负区间（−0.3~−0.9，其中 1999 进入持续负值、2002 最深 −0.91，3 年触底）；CN 从 2019 年 +2.9% 滑至 2023-2025 的 0.2/0.2/0.0——**截至 2025 CN 尚未进入负区间**（0.0 为边界），且近零路径仅 3 年。JP 自 1999 年进入负区间后持续 7 年（1999-2005 仅 2004 ≈0）；CN 是否进入负区间不可知（未来截断）。「CN 价格进入 JP 2000s 通缩带」作为**事实**暂不成立（CN 未转负）；作为**预测方向**（价格先行）在 held-out 下无独立证据（§2 CH-CPI）。HYP-H5-M1 维持 candidate 且偏弱。

### 6.2 Investment 路径（JP 泡沫后 vs CN 高位回落）

JP investment_gdp（% of GDP，1988-2003）：1988:29.64，1989:30.57，1990:31.73，1991:31.42，1992:30.47，1993:29.54，1994:28.65，1995:28.48，1996:29.47，1997:28.57，1998:26.80，1999:26.07，2000:25.61，2001:26.57，2002:25.63，2003:25.59

CN investment_gdp（2005-2024）：2005:41.54，2006:41.74，2007:41.61，2008:43.78，2009:47.16，2010:48.06，2011:48.31，2012:47.76，2013:45.92，2014:45.31，2015:42.73，2016:42.14，2017:42.55，2018:43.31，2019:42.67，2020:42.57，2021:42.68，2022:42.36，2023:41.13，2024:40.48

路径对照：JP 峰值 1990 年 31.7% → 10 年后 25.6%（−6.1pp / -19.3% 相对）；CN 峰值 2011 年 48.3% → 2024 40.5%（−7.8pp / -16.2% 相对，13 年）——两段均为「高平台后长下行」，JP 10 年 −19% vs CN 13 年 −16.2%（尚未止跌）；CN 斜率更缓、仍在途中。跨 SNA 基准的绝对水平不可比，只比相对下行。

## 7. H5-FINAL 综合结论（exploratory 表述）

| 问题 | Final 状态 |
|---|---|
| Q1 分类铰链 | **YES（CPI/INFLATION）——冻结**：hinge 而非机制（held-out 证实） |
| Q2 机制复现 | **INTERPRETABLE FEATURE GEOMETRY ONLY**（核心三通道仅 INVESTMENT held-out 方向性复现；M2 = secondary non-gate evidence——外审裁定不扩 gate） |
| Q3 持续 transition | **NO（PASS）——冻结**；JGAP 修正解释为绕过渡带摆动 |

**最终表述（替代 v02 的 CONDITIONAL；外审 §13 措辞调整采纳）**：CN-JP regime 分类是**稳定、可解释的 structural-state geometry**（13/13 跨方法复现）——注意**分类空间分离轴 ≠ held-out mechanism**（CPI/REER 恰为此区别的实证）；**broad common mechanism correspondence 未获支持（NOT SUPPORTED）是本研究主结论而非局限**。held-out 后仅 investment 在核心 gate 中呈方向性复现（M2 为 secondary non-gate 复现证据）；CPI 是纯分类铰链（近零通胀年份的 J00 归属自指）；reer/wage/birth/real_gdp 通道不独立复现。现实结论：**低通胀/近零 CPI 本身不足以证明日本化**——本研究否定的是「单凭近零 CPI 判 CN 进入 JP 式 J00 regime」这一强命题（CN 价格 0.0-0.2% 未转负，未达 JP 通缩带；其 J00 归属又系 CPI 自指）。

**表述边界**：① n 极小（组 3-8 年），held-out/permutation 为描述性检验，负结果强于正结果；② gate 通道清单（CPI/INV/REER）按外审冻结，M2 复现不计入主判据（外审 §7 明确支持不扩 gate）；③ JGAP 只改解释不改 Q3；④ event-time 因 CN 未来截断仅部分可比。

## 8. 外审裁定（JP-HIST_H5FINAL_外部审核及下一步方向_20260906.md）

> **H5-FINAL = PASS / GEOMETRY-LEVEL FREEZE**（Q1 hinge SUPPORTED；Q2 broad mechanism correspondence NOT SUPPORTED；Q3 persistent J00 transition NOT SUPPORTED）。冻结项 H5-F1..F6 与不冻结清单签署于 FREEZE_H5_20260906.txt（08_jp_hist/ 根）；表述调整（§13 四项 + 76% 口径 + 显著性克制）已并入本报告 v03.1。下一步主目标 = Final Evidence Synthesis（09_中日比较/JP-HIST_Final_Evidence_Synthesis_20260906.md）；H6 External Mechanism Validation 仅在 Synthesis 后启动且须用分类器外新变量。

## 审计指引

```bash
# /usr/bin/python3 04_analysis/h5/engine/h5_final_tests.py      -> h5_final/h5final_direction_scores.csv + h5final_jgap_sequence.csv
# /usr/bin/python3 04_analysis/h5/engine/h5_final_report_gen.py -> h5_final/h5final_eventtime_paths.csv + H5_FINAL_validation_report.md
```