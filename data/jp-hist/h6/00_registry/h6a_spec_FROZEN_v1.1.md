# H6-A External Shock Robustness — Spec FROZEN v1.1
版本：2026-09-07 v1.1 FROZEN（外审 PASS / APPROVE A0 v1.1 FREEZE）
项目：JP-HIST（Japan Historical Macro Comparison）· 链 08_jp_hist/h6/
上游建议书：01_数据采集/外部审核意见/JP-HIST_H6A_H6B_下一步工作方向与数据采集建议书_20260907.md
状态：FROZEN——签署后只读；修订走 errata + 版本化。v1.0（已被本版取代）文件保留只读备查。
元数据：spec_version=v1.1-FROZEN；freeze_date=2026-09-07；parent=A0 v1.0（REWORK）→ v1.1 candidate（外审 PASS）；sha256 见 h6_freeze_meta_v1.1.csv 与定档包 manifest。

## 0. 决策记录（追加制）
- 2026-09-07 v1.0 FROZEN（用户「按默认执行」）。
- 2026-09-07 外审 v1.0 = REWORK：P0×3/P1×5/P2×4（不冻结、不启动 A1）。
- 2026-09-07 v1.1 candidate 修订（见 v1.1 变更清单）。
- 2026-09-07 外审 v1.1 = PASS / APPROVE A0 v1.1 FREEZE（0 P0 / 0 阻断 P1 / 3 非阻断 P2：rows_expected 文书残留→18、property_investment semantic 统一 PENDING_CROSSWALK、residualization 输入命名 standardized_pre_normalization_value——三项均已修正）；本文件正式冻结。

## 1. 研究问题与目标（可证伪表述，同 v1.0）
- Q-A1：剔除/屏蔽任一 confirmatory 事件（E01/E02/E03/E05）后，2013-2025 结构态归属是否根本翻转？
- Q-A2：COVID 调整后，2013-2019 与 2023-2025 的状态结构是否仍存在？
- Q-A3：investment held-out 方向复现在 baseline、-COVID、shock-residualized 三类中是否≥两类满足冻结效应规则（见 Gate A3）？
- Q-A4（诊断，不改窗）：Bai-Perron 断点是否集中在已知事件附近？
明确不做：不以提高一致性为目标；不因结果改事件窗；adjustment 后稳定 22 年不自动升级 fixed lag（Gate A4）。

## 2. 事件注册表（v1.1 修订：expected_modules → affected_modules_expected=ALL_ALLOWED，见 h6a_external_event_registry_v1.1.csv）
E01 1997-98 JP-heavy confirmatory；E02 2000-02 global confirmatory；E03 2008-09 global confirmatory；E04 2011-12 aux（v1 不跑 -E04 LEO）；E05 2020-22 confirmatory；E06 CN 2022 diagnostic。
事件窗口的权威依据（非"事件是否发生"，而是"为何这些年份"）见 governance/h6_event_definition_memo_v1.0.md（A1 前完成项，现已提供）。

## 3. LEO 与事件操作矩阵（机器可执行，FROZEN 于 h6a_event_operation_matrix_v1.1.csv）
对每个 E×country×year：mask_single_year_classification / mask_window_aggregation / mask_jp_candidate / mask_cn_summary 四布尔位 + confirmatory_use。规则摘要：
- E01/E02/E03 仅作用 JP 候选位（LEO-2）；E03-CN 行显式 NA（CN 2008-09 不在主窗样本，记录而非遗漏）。
- E05-CN 2020-22：single=NO（保留分类）、window_aggregation=YES（LEO-1）、cn_summary=YES（LEO-3）；E05-JP：天然非候选（lag 3-5<10），JP 侧冲击由残差化 COVID dummy 覆盖。
- E06-CN 2022：全部 NO（diagnostic 注，不加掩码）。
- reconciliation 每个 -E k 列必须唯一追溯本矩阵；看到结果后不得在 candidate/summary/aggregation 位之间再选择。

## 4. 全球因子（v1.1；h6a_global_factor_registry_v1.1.csv）
g1 world_gdp_growth（WB NY.GDP.MKTP.KD.ZG, World；1961+；**可用性措辞改为 complete for H6-A confirmatory window**，不称覆盖全部 JP-HIST 历史）。
g2 vix_mean（FRED VIXCLS→年度均值，main）；g2aux vix_max（aux）。
g3 covid_dummy = 1(2020≤t≤2022)。
aux oxcgrt_stringency_{cn,jp}（仅 auxiliary）。
v1 不采：oil/trade/Fed/dollar/更多 dummy。

## 5. 残差化（v1.1 修订核心）
符号约定（消除记号歧义）：x_{i,c,t} = standardized_pre_normalization_value（标准化后、归一化前的年度序列；**代码/数据字典中必须命名为 standardized_pre_normalization_value，禁止命名为 raw_value**——它不是 H1 Raw Layer 的原始金额/单位，P2-3）；先对该值做 shock 回归，残差 û 经引擎既存 robust-z 层得 z^res = RZ(û)，再跑 similarity。顺序 = standardized_pre_normalization_value → shock regression → residual → robust-z → similarity（审核认可顺序）。
- 主模型 A（confirmatory）：x_{i,c,t} = α_{i,c} + β_{i,c}·G_t^growth + γ_{i,c}·D_t^COVID + u_{i,c,t}
- 辅助模型 B（confirmatory，aux 通道）：A + β2_{i,c}·VIX_t^mean
- **Model T（detrended diagnostic）**：A + δ_{i,c}·t —— 仅诊断，不参与 Gate A1-A4 判定，禁止与 A/B 并列后选优（外审 P0-2：趋势项会剥离本项目研究对象=长期结构趋势）。
- 回归方法：主 OLS；辅助 Huber；两法残差差异巨大 → shock model 受极端值支配，residualized 证据等级下调。
- VIX common-support（外审 P1-3，方案 1 冻结）：Residual-B 只与 Baseline-B^{1990+} 比较（JP 候选史截断至 VIX 覆盖起点，消除"adjustment+样本截断"混淆）；Residual-A 保持全史。禁止 Baseline^{full} ↔ ResidualB^{1990+} 跨样本比较。
- 拒绝规则：不得为让 lag 稳定而加控制。

## 6. 引擎复用（同 v1.0）：薄包装注入掩码；v1 引擎本体零改动；H4/H5 冻结文件只读。

## 7. Reconciliation（v1.1：双分母+样本掩码数+逐年一致率）
- h6a_lag_reconciliation.csv：D 窗 4 metric × {Baseline^{full}, Baseline^{avail}, -E01,-E02,-E03,-E05, -COVID(LEO3), ResidA, BaselineB^{1990+}, ResidB^{1990+}}。
- h6a_regime_reconciliation.csv：2013-25 {J90,JGAP,J00,OTHER} share × 同上；**每格三列**：Share^{13}=N_r/13（固定分母）、Share^{avail}=N_r/N_unmasked（可用年分母）、N_masked；并附 year-level agreement（adj vs Baseline^{avail}，见 Gate A1b）。
- h6a_mechanism_reconciliation.csv：CPI/INVESTMENT/M2 held-out D、CI、perm p、effect-rule 判定 × 同上。
- 样本不足预定出口（外审 §15 采纳）：若 mask 后有效样本不足执行原 held-out 推断检验 → 该检验标记 INFEASIBLE_AFTER_PRESPECIFIED_MASK，保留 descriptive effect；不改窗口、不改阈值、不扩样本。

## 8. Gates（v1.1 机器化；continuous diagnostics 与布尔 Gate 同时报告）
定义（FROZEN）：Baseline^{avail} = 用冻结的逐年分类，剔除被掩码年份后重算的份额/一致率基准（逐年分类本身不变）。
- **Gate A1（Event Robustness）** PASS ⇔ 对每个 confirmatory LEO（E01,E02,E03,E05）与 ResidA 同时满足：
  (a) 主导 regime 不变：argmax_r Share_r^{adj,avail}（r∈J90/J00/JGAP）== argmax_r Share_r^{base,avail}；
  (b) year-level Agreement = (1/N_unmasked)Σ_t 1[R_t^{adj}=R_t^{base}] ≥ 0.60；
  (c) D 窗 best-lag 不塌缩：4 metric 中 ≥3 个非 NA 且非 NA 者 |lag^{adj}−lag^{base^{full}}| ≤ 5 年。
- **Gate A2（COVID Robustness）** PASS ⇔ 2020-2022 剔除/调整后：2013-2019 与 2023-2025 两个子集各自 majority regime 与 Baseline^{avail} 同子集一致（2023-25 baseline=J00 主导 2/3），且各子集内 Agreement ≥ 0.5。
- **Gate A3（Investment Robustness）** PASS ⇔ 效应规则（sgn(D_CN)=sgn(D_JP) ∧ |D_CN| ≥ ε=0.25 ∧（moving-block 90% CI 下界>0 ∨ perm p<0.15））在 ResidA 成立，且 {Baseline, -COVID} 中至少一个也成立；三类全部不满足→H6-B investment 降级。报告沿用 H5-FINAL 四项纪律（方向/CI/perm/量级），Gate 只用上述预注册最小组合。
- **Gate A4（No Fixed-Lag Rescue）** 同 v1.0：≥3/4 metrics ∧ ≥2 normalization families ∧ LOMO ∧ event robustness 才允许重开 fixed-lag 讨论。

## 9. 交付物（v1.1 增加）
h6a_spec_candidate_v1.1.md / h6a_event_operation_matrix_v1.1.csv / h6a_external_event_registry_v1.1.csv / h6a_global_factor_registry_v1.1.csv /（其余产物同 v1.0 清单）/ H6A_final_report.md / SHA256_manifest_h6a.txt。
A1 启动条件：v1.1 外审 PASS → 提升 FROZEN → 方可下载/计算。

## 10. 修订记录
v1.0→v1.1 变更：删 confirmatory 趋势项（+Model T diagnostic）；新增事件操作矩阵；Gate 机器化（A1a/b/c、A2 子集规则、A3 ε=0.25 效应规则）；VIX common-support 方案 1；记号 x→û→z^res；双分母+N_masked+Agreement；INFEASIBLE 标记；P2-1 event memo、P2-2 可用性措辞、P2-3 affected_modules_expected、P2-4 freeze meta（h6_freeze_meta_v1.1.csv）。
