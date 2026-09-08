# JP-HIST Final Evidence Synthesis（H0-H5 全链证据综合）
日期：2026-09-06
定位：外部审核 JP-HIST_H5FINAL_外部审核及下一步方向_20260906.md §17-18 指定的最终主目标——把所有核心假设按证据等级整理，作为 JP-HIST 最终论文/报告主干。
依据：FREEZE_H0/H1/H2/H3/H4/H5 + JP2 FREEZE + 外审报告链（H0.8/H1/H2/H3/H4/H4v02/v03d/v03e/H5/H5-FINAL）+ 各阶段响应文档。本文件**不引入任何新分析**——全部数字可追溯至 08_jp_hist/ 冻结文档与 04_analysis 产物 CSV。
研究定位声明：retrospective structural-state comparison（RETROSPECTIVE_HISTORICAL），非 PIT、非因果识别；「CN 是否滞后 JP N 年」已按外审 §14 升级为「相似 structural regimes 是否可重复识别、机制是否相同、CN 是否在 regime 间迁移」。

================================================================
1. 证据分层口径
================================================================
- REJECTED：作为一般命题被本项目自身的稳健性检验否定（不因个别窗口/method 复活）。
- NOT SUPPORTED：经检验无支持证据（含 held-out 负结果、效应坍缩、方向反转）。
- SUPPORTED：跨方法/跨 robustness 一致（在 retrospective 边界内；非 PIT 因果）。
- SUPPORTED DESCRIPTIVELY：方向性/描述性成立，n 小或口径特异——不称统计确认、不称因果。
- SECONDARY SUPPORT：非主 gate 的附加佐证（不参与主判据）。
- CANDIDATE：待外部变量验证的机制假说（H6 候选对象）。

================================================================
2. Evidence Matrix（核心成果）
================================================================
| # | Claim | Status | 关键证据（可追溯） |
|---|---|---|---|
| E01 | CN 固定滞后 JP 30-40 年 | **REJECTED** | 方法论预设区间未获支持；H4 normalization/metric 不稳、跨 norm 漂移（H4 v0.1-v0.3e 报告；FREEZE_H4） |
| E02 | CN 固定滞后 JP 22 年（一般命题） | **REJECTED AS GENERAL CLAIM** | 仅部分窗口/method：B 窗 cross-metric L22（4/4）、D 窗 MANHATTAN L22（10k null p=0.0009）method-specific；无跨 metric/norm 稳健单一 fixed lag（FREEZE_H4 F04） |
| E03 | CN-JP 存在 retrospective structural-state similarity | **SUPPORTED** | H4 v03e FINAL：B 窗 L22 cross-metric；D 窗 method-specific SIG；LOMO/覆盖/锚点全过（FREEZE_H4 F01-F03） |
| E04 | J90/J00 structural regimes 可重复识别 | **SUPPORTED** | 两独立方法 13/13（H4 module-subset bootstrap vs H5 regime-level argmax，代表 JP 年亦同）（FREEZE_H5 F01） |
| E05 | CN 2013-25 呈 single-cluster 对应 JP 1991-98 | **REJECTED** | 单簇表述经 H4 v0.3d 数据修正后不成立（v03d 修正 6×P0 后 mixed-state 回潮）（FREEZE_H4 F05） |
| E06 | CN 2013-25 = mixed-state（7/13 J90 + 4/13 J00 + 2/13） | **SUPPORTED DESCRIPTIVELY** | cluster 800/800 valid；非单调时间推进（FREEZE_H4 F06；h5_state_sequence.csv） |
| E07 | CN→J00 persistent transition（2023-25） | **REJECTED** | 2024 落 OTHER/JGAP 中断；P(J00→J00)=0（0/3）；J90→J00=J90→J90=0.43 对称（FREEZE_H5 F05；h5_transition_matrix_*.csv） |
| E08 | 近年 CN 绕 J90/JGAP/J00 摆动（非进入 J00） | **SUPPORTED DESCRIPTIVELY** | JGAP(1999-2002) 四态：2015、2024 ∈ JGAP；2023:J00→2024:JGAP→2025:J00（h5final_jgap_sequence.csv） |
| E09 | CPI/INFLATION 是 classification hinge | **SUPPORTED** | CF 三轨翻转唯一达阈值（CF-A 5/13、CF-B 4/13、CF-C 5/13）；held-out 坍缩证实 hinge 性质（FREEZE_H5 F02） |
| E10 | CPI 是跨期共同机制 | **REJECTED** | held-out D_CN,−CPI=+0.011≈0 vs D_JP=+0.704（1.6%）；boot CI 跨 0；p=1.0；percentile aux 反转（FREEZE_H5 F02） |
| E11 | Investment 通道 held-out 同向复现 | **SUPPORTED DESCRIPTIVELY** | D_CN,−INV=+0.753 vs D_JP=+0.989（standardized magnitude ≈3/4）；boot90 CI [0.151,1.433] 不含 0；perm p≈0.16（n 小，非统计显著）（FREEZE_H5 F03） |
| E12 | M2 通道同向复现 | **SECONDARY SUPPORT（non-gate）** | D_CN,−M2=+0.369 vs D_JP=+0.234；boot90 CI [0.096,0.636] 不含 0；perm p≈0.20（FREEZE_H5 F03） |
| E13 | 广泛共同机制 correspondence（across CN-JP regimes） | **NOT SUPPORTED** | Q2-Final：核心三通道（CPI/INV/REER）仅 1 个 held-out 复现 <2 阈值；REER/wage/real_gdp 反向；birth/iip 无独立证据（FREEZE_H5 F04） |
| E14 | 低通胀/近零 CPI 本身意味着日本化 | **NOT SUPPORTED** | CN 2023-25 CPI 0.2/0.2/0.0 未转负（JP 1999 转负、2002 最深 −0.91）；CPI held-out 坍缩（FREEZE_H5 F06） |
| E15 | CN=滞后 N 年的日本（整体机制复制） | **REJECTED** | H4 norm 漂移 + H5 Q2-Final 全链否定（FREEZE_H5 总体结论；audit H5-FINAL §21） |
| E16 | 已纳入人口/工资变量构成相似性的主要正向驱动 | **NOT SUPPORTED** | DEMOGRAPHY 是最大负贡献（S_m J90 −0.89/J00 −0.80/OTHER −1.47）；LOMO 负 Δ；held-out wage 反向/birth 弱化（H5 v02/FINAL；不宣称人口机制完全不相似——人口连续年度覆盖弱，H1-P1 遗留） |
| E17 | 价格先行于实体日本化（HYP-H5-M1） | **CANDIDATE（偏弱）** | CPI held-out 无独立证据 + CN 未转负 + 2023/25 的 J00 归属系 CPI 自指（H5-FINAL §6.1） |
| E18 | macro-state 相似 ≠ return 相似（层分离） | **SUPPORTED（JP2 层）** | JP2 三层分离结论：macro/return/risk 分列报告（FREEZE_JP2；勿混 JP2 return-layer 30-40y 方向模式与 H4 macro-layer 结论） |
| E19 | CN 2000-2012（A 窗）rep 集中于 JP 1980s | **DESCRIPTIVE（附录口径）** | H5 分类 2000-2012：OTHER×8（rep 1984-87）+ J90×5（rep 1991-97）；J00 几何不可达（lag≥10）——不入主结论（h5_state_sequence.csv） |

================================================================
3. 结论分层叙事（按研究问题组织）
================================================================
## 3.1 时间滞后类：被否定的一般命题
项目最初的「CN 滞后 JP 30-40 年」在 H4 多轮证伪后不成立为一般命题；「滞后 22 年」仅存活于部分窗口与特定方法（B 窗 cross-metric、D 窗 MANHATTAN），且随 normalization 漂移——**不存在一个稳健的固定时间滞后**（E01/E02）。JP2 return 层曾见 30-40 年方向模式（跨窗一致 6/6）属回报层描述，与 H4 macro 层窗口结果分层处理（E18）——两结论不冲突、不可混用。

## 3.2 结构相似类：稳健且可重复
在 structural-state 空间（六模块×九变量的 robust-z 标定）里，CN 2013-2025 与 JP 1990s/2000s 态的相似是**可重复识别的几何事实**（E03/E04）：13 年分类在两套独立方法下 13/13 一致。但该相似呈 mixed-state（7/13 落 J90 + 4/13 落 J00 + 2/13 过渡带），非沿 JP 轨迹单调推进（E05/E06）。

## 3.3 机制类：分通道、多否定、少复现
- CPI：最强分类铰链（E09）却非机制（E10）——近零 CPI 年份（2023/25）被分到 J00 只因为 CPI 在分类器里；把它从分类中拿走，这些年份立刻回到 J90。held-out 后 CPI 效应坍缩至 JP 差的 1.6%。
- Investment：唯一在核心 gate 中 held-out 复现的通道（E11）——分类不含 investment_gdp 时，被其他维度分到 J90/J00 的 CN 年仍在该变量上沿 JP 方向显著分离（标准化幅度 ≈ JP 的四分之三）。JP 侧机制内容：泡沫后投资率从高位长下行（31.7%→25.6%，−19%）；CN 侧同形态（48.3%→40.5%，−16% 未止跌）——仅路径形态比较，SNA 不可横比。
- M2：次级复现（E12）——货币增速在两 regime 组间亦沿 JP 方向分离（非 gate 证据）。investment+M2 是目前仅有的两个「分类器之外仍独立同向」的通道，列为 H6 候选动机。
- 否定项：REER（held-out 反向）、wage（反向）、real_gdp（反向）、birth/iip（无独立证据）→ **广泛共同机制对应不成立**（E13）。
- 人口：已纳入变量（wage_yoy/birth ΔCBR）是相似度的**负向拖累**而非驱动（E16）——「人口不是 CN 与 JP 相似的原因」在已纳入变量范围内成立；不扩展到「人口机制完全不相似」（人口连续年度覆盖弱）。

## 3.4 迁移类：摆动而非进入
2023-2025 无 persistent J00（E07）；2024 的 rep 落在 JP 1999-2002 过渡带（JGAP），四态视角下 CN 近年围绕 J90→J00 transition band 摆动（E08）——「进入失去的二十年后期」式表述被冻结禁令排除。

## 3.5 现实命题：低通胀≠日本化
近零 CPI 本身不足以证明日本化（E14）：(i) CN 尚未出现 JP 式持续负 CPI；(ii) CPI 一旦移出分类器即不再区分 J90/J00（self-referential hinge）；(iii) 因此「单凭低通胀就把 CN 判为进入 JP 式 J00 regime」是被本项目数据直接否定的强命题。「价格先行于实体日本化」作为候选假说保留（E17，偏弱）。

================================================================
4. 研究框架转型
================================================================
经 H4/H5/H5-FINAL 证伪链，JP-HIST 已从「寻找日本化/固定滞后证据」转为：
> 一个能够区分**结构相似、时间滞后、机制复现与表面宏观类比**的可证伪历史比较框架（audit H5-FINAL §22）。
最可靠的总体结论（audit §21）：
> CN 与 JP 在部分宏观状态上存在可重复识别的历史结构相似性，但不是稳定固定时间滞后，也没有证据表明 CN 正在整体复制 JP 经济机制；投资率长期下行与货币增速状态存在一定跨国同向复现（描述性）；近零 CPI 更多是分类铰链而非独立机制证据；「低通胀=日本化」与「CN=滞后 N 年的日本」均被本项目自身稳健性检验否定。

================================================================
5. 表述纪律（研究与写作强制）
================================================================
- 凡称「复现」限定 descriptively / under held-out classification；「分类空间分离轴 ≠ held-out mechanism」。
- 「共同经济机制未验证（NOT SUPPORTED）」是主结论，不是 limitation。
- 标准化幅度比值（如 76%）不作经济强度/因果效应解读。
- 禁写：「复制 2000s 机制」「已进入通缩型日本化」「投资路径相似→资产负债表衰退」「M2+investment 证明共同机制」（FREEZE_H5 W01）。
- INFLATION/MONEY_CREDIT 是单变量模块——「模块」结论与单变量结论等价，写作勿放大证据规模。
- macro（结构状态）/ return（回报）/ risk（风险）三层永远分列报告。

================================================================
6. 关键 artifact 索引（复核路径）
================================================================
- 冻结链：08_jp_hist/FREEZE_H0..H5_20260906.txt（H5 = GEOMETRY-LEVEL）
- H4 最终证据：08_jp_hist/04_analysis/v03e/H4_v03e_final_report.md（自动生成）
- H5 机制证据：08_jp_hist/04_analysis/h5/H5_mechanism_report.md（v02）+ 产物 CSV（h5_state_sequence / h5_h51_* / h5_regime_* / h5_cf_* / h5_transition_*）
- H5-FINAL：08_jp_hist/04_analysis/h5_final/H5_FINAL_validation_report.md（v03.1）+ h5final_direction_scores / h5final_jgap_sequence / h5final_eventtime_paths
- 审核包：source_snapshot/h5_audit_package/（v01）、h5_audit_package_v02/、h5_audit_package_v03/（manifest 各自闭合）
- 外审报告与响应：01_数据采集/外部审核意见/JP-HIST_H4v03e_*、JP-HIST_H5_*、JP-HIST_H5FINAL_*
- 方法论规格：00_registry/h4_*/h5_*/h5_final_spec_20260906.md
- 数据 bug 现行处置：00_registry/H2_ERRATA_20260906.csv（下游一律用 FIX 文件/panels）

================================================================
7. 局限性与未决项
================================================================
- retrospective 定位：1970s 发布时点信息不存在是结构性事实，相似性比较用 ex-post 结构态，不做 PIT 宣称。
- 样本极小（J00 组 3-4 年）：held-out/permutation 为描述性检验，**负结果强于正结果**；investment/M2 的正结果停留在 bootstrap-supported 层级。
- 数据缺口：JP 连续年度人口、cgb10y 2002-2007、corp 系列 CN 侧、CN 房价 2013-25、CN wage 2014/2020 为增速反推——均如实计入 coverage，不阻塞已冻结结论。
- 分类器变量仅九项且两个单变量模块；机制候选（investment/M2）为何复现、是否在更广变量集成立——留 H6 External Mechanism Validation（须分类器外新变量 + 授权）。
- JGAP 四态只做了诊断 relabel，未独立估计 gap 态机制；transition 解释随未来数据可更新（Q3 表述「至 2025 无持续 J00」时间戳化）。

================================================================
8. 下一阶段选项
================================================================
1. **研究写作**：本 Synthesis + Evidence Matrix 作为 JP-HIST 最终报告/论文主干（E01-E19 + §3 叙事 + §5 纪律可直接成稿）。
2. **H6 External Mechanism Validation（条件性）**：若判定 investment/M2 值得深挖——新变量（企业杠杆/利润率/非金融债务/地产库存·新开工·房价/银行不良率/信贷投向/saving 两侧/fiscal impulse/real rate/debt-service）+ 预注册 + 只验证不重分类。需用户另行授权。
3. 项目收束：JP-HIST 分析链（H0-H5）正式闭合于本文件与 FREEZE_H5。
