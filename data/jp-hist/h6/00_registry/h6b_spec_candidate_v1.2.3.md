# H6-B External Mechanism Validation — Spec Candidate v1.2.3（METADATA CONSISTENCY CLOSURE，待外审）

版本：2026-09-07 v1.2.3 candidate（B0 v1.2.2 外审 CONDITIONAL PASS 响应：metadata-only patch，P1×1/P2×1 全闭）
状态：candidate——外审 PASS 后提升 FROZEN v1.2.3。
上游：①v1.2.2 candidate（本版基于其 metadata consistency 修订；v1.2.2 文件只读保留）②《JP-HIST_H6B_B0_v1.2.2_外部审核报告_20260907.md》（CONDITIONAL PASS：D-B notes 残留旧阈值 P1 + latest 简写 P2 + gate registry B1-B4 列错位【自查新增，超出外审范围】）③执行评审书（R1-R8 仍有效）
元数据：spec_version=v1.2.3-candidate；candidate_date=2026-09-07；sha256 见 B0 v1.2.3 审核包 manifest。

## 0. 决策记录
- 2026-09-07 B0 v1.2 外审 REWORK（架构保留，preregistration closure 不足）→ 本版 v1.2.1 最小 PATCH：只做 specification-closure，不重写研究设计。
- 外审 P0×3（D-B 阈值未冻结 / missingness 阈值未冻结 / lead-lag θ 隐含多重搜索）、P1×5（θ 机器定义 / sign registry / Gate B1 独立性 / Gate B3 机器化 / shock-application registry）、P2×3（source-priority registry / latest→cutoff / MBB resampling 规则）——逐条核实属实，本版全部关闭。
- 外审 §十八 十项闭包动作 + machine QC 11 项作为本版验收标准，全部落实（见 §16 QC）。
- v1.2.2（前版）：v1.2.1 外审 REWORK 响应——sign registry 方向修复 + B3 语义冻结 + stance 分列 + annual-step 标注（SIGN/SEMANTIC CLOSURE）。
- v1.2.3（本版，metadata-only）：v1.2.2 外审 CONDITIONAL PASS——P1（Gate registry D-B notes 残留 "如 <1% 或 <0.5%" 旧候选阈值，与冻结 1.0% 主判据冲突）+ P2（registry `latest` 简写，建议统一 latest_by_cutoff_2026-08-31）。另自查发现并修复 v1.2.1/v1.2.2 gate registry **Gate B1-B4 列错位**（生成脚本拆包 bug：criteria 文本落入 ci_rule 列、gate_criteria 列变 TRUE、machine_executable 变 "-"；Verdict/D 行因 fallback 未现形）——本版 16 行全量重建为正确列序。零实质方法变更。

## 1. 核心研究问题（FROZEN，同 v1.2）
主机制链 Property→BS→Profitability→Credit→Investment；禁新变量回 H4/H5 classifier；禁 argmax_L fixed-lag 搜索；禁 causal（上限 Level 3）。

## 2. 五 Channel + Deflation 模块（FROZEN，同 v1.2 §2）
骨架不变。变量全集见 h6b_variable_registry_v1.2.3.csv（37 行，19 列）。

## 3. 机制假说（FROZEN，同 v1.2 §3）+ 符号系统（v1.2.1 闭包 P1-2）
- H6B-H1..H5 不变。
- **符号系统机器化（v1.2.2 修复版 h6b_sign_registry_v1.2.3.csv）**：每个变量定义 (a) raw_series_definition、(b) deterioration_direction（恶化方向：↑ 或 ↓）、(c) sign_multiplier、(d) expected_chain_sign。
  - **sign_multiplier 机器推导规则（唯一真源 = deterioration_direction）**：若 raw↓ 表示恶化（deterioration_direction=↓）则 X^d=−X、sign_multiplier=−1；若 raw↑ 表示恶化（direction=↑）则 X^d=+X、sign_multiplier=+1。**禁止手工赋值方向与乘子不一致**（v1.2.1 曾 10-17 行违反，涉 investment/credit 端点，被外审判 P0）。
  - expected_chain_sign：主链（I/C/P/B/R）相邻链预期符号 = +1（恶化同向传导）；D 模块变量 = NA（独立模块不进 Gate 链，其符号方向由 D-A~D-D 判据承载）。
  - 所有检验在 deterioration 变换后序列上进行——变量先乘 sign_multiplier 再进 robust-z/channel index，Gate 判据统一为"θ 与预期同号且显著"。
  - 机器 QC（必过）：sign_direction_multiplier_mismatch=0（37 行 direction↔multiplier 一致）、sign_variable_registry_cross_mismatch=0（sign registry 与 variable registry 乘子列一致）、sign_expected_chain_invalid=0（主链 +1 / D 模块 NA）。

## 4. 数据频率与窗口（FROZEN；v1.2.1 闭包 P2-2 source cutoff）
主频率 quarterly；月度→季度规则不变（stock=quarter-end / flow=quarter sum / index=quarter average；CN YTD 累计先还原单季流量）。
窗口：
- JP primary 1985Q1–2005Q4；Long-window sensitivity 1970Q1+（按变量可用性标 common-support）。
- CN primary 2010Q1–latest；Extended 2005Q1–latest。
- **Source cutoff（P2-2 闭包）**：`analysis_cutoff_date = 2026-08-31`（冻结）。每变量取该日之前官方发布的 latest observation；该日之后发布的 revision/data 不纳入（防 release data snooping）。跨变量分析取 common support = 各变量有效期的交集（机器计算并报告 min/max 期）。B1 抓取批次日期须 ≤ cutoff+合理下载窗口（retrieved_at 记录，晚于 cutoff 的抓取仍只保留 cutoff 前 release 数据，manifest 明示）。
- COVID sensitivity：2019Q4 节点前后分段。

## 5. 时间结构与主统计量 θ（FROZEN；v1.2.1 闭包 P0-3 + P1-1）
- (a) 主检验（进 Gate）：相邻链 X→Y 的窗内 lead/lag。**θ 定义冻结（采纳外审推荐 window-average）**：
  θ_XY = (1/5) Σ_{k=0}^{4} ρ_S(X_t^d, Y_{t+k}^d)
  其中 X^d、Y^d 为 deterioration 变换后的序列，ρ_S = Spearman。**JP 与 CN 使用同一 k∈{0..4} 集、同一公式**（不逐国选 lag）。
- 同时完整报告 lag profile：ρ_S(X_t, Y_{t+k}) 每个 k 单独输出（k=0..4 五行）——lag profile 是透明度报告项，**不是** Gate 判据（禁"任一 lag 同号即 PASS"）。
- bootstrap 90% CI 的对象 = θ_XY（window-average），不是单个 lag。
- **多重比较处理**：主判据是单一预设统计量 θ_XY（5-lag 平均），非 max-over-lag，故无 lag 维多重搜索；5 个 lag 只作 profile 描述，不进入 PASS/FAIL。
- (b) 辅助视角（descriptive，不进 Gate）：τ^INV 锚点 ±20 季路径同型比较（同 v1.2 §5b）。

## 6. 变换与 Channel Index 合成（FROZEN，同 v1.2 §6；符号乘子前置）
逐变量：sign_multiplier × raw → deterioration 序列 → robust-z（within-country full-sample）→ channel/family index（等权平均，权重冻结）。Level/First-diff 双轨；禁 level concat；禁 NA→0。

## 7. 三轨报告（FROZEN，同 v1.2 §7；应用细节见 h6b_shock_adjustment_registry_v1.2.1.csv = P1-5 闭包）
- Mechanism^Raw / Mechanism^ShockAdjusted / Mechanism^FirstDiff 每链必须。
- Shock-adjusted 轨应用规则冻结（新 registry）：
  - 季度 World GDP growth 构造：WB annual growth（1961-2025，h6a 已有）年内平铺为季度 step 值（4 季同值），禁插值平滑；
  - VIX：CBOE 日度 → 季度 mean（与年度 mean 规则同构）；
  - COVID dummy 季度定义：2020Q1–2022Q4 = 1（对应 H6-A annual 2020-22），其余 0；
  - JP fit domain：1985Q1–2005Q4 primary 窗内回归（Model A=[1, WorldGDP, COVID]）；Model B 增 VIX——VIX 1990 起 → JP Model-B 只在 1990Q1+ common-support 段估计，**不缩 robust-z 标定窗**（H6-A A3.2 教训：候选年下限与标准化观察集是两个正交轴）；
  - CN fit domain：2005Q1（或 2010Q1 primary）—latest；
  - 残差化输入 = 标准化前值（raw annual/quarterly value），输出 RobustZ(û)（H6-A 教训 6）；
  - minimum N：回归段 n≥20 季，否则 INFEASIBLE_AFTER_PRESPECIFIED_MASK；
  - **annual slow variables（land price、wage、I_ratio）不参与季度 shock 回归**——它们保留 raw 版 + annual 单独 robustness，不进季度残差化（外审 P1-5 问询项）；
  - **reporting limitation（外审 v1.2.1 P2）**：WB annual growth 年内平铺不产生真正季度全球冲击信息，Model A quarterly track 实为 annual-step control——最终报告必须标注 `GLOBAL_GROWTH_CONTROL_ANNUAL_STEP_QUARTERLY`（见 shock_adjustment_registry_v1.2.3.csv reporting_limitation 行）；
  - infeasibility：数据不足 → INFEASIBLE_AFTER_PRESPECIFIED_MASK（禁扩窗/降阈）。

## 8. Gate B1-B4 + Mechanism Verdict（FROZEN；v1.2.1 闭包 P1-1/P1-3/P1-4 + P0-3）
机器判据（engine 输出 Gate_machine_B*.txt/csv）。所有 θ 为 §5 冻结定义，所有序列先乘 sign_multiplier。

- **Gate B1（Property→BS）**（P1-3 闭包：independence 按 family）：
  - Property family 冻结为三族：PRICE（land price、residential property price）/ ACTIVITY（housing starts、property investment、construction）/ INVENTORY-SALES（sales area/value、inventory area）。
  - 每 family 内变量 robust-z 等权平均 → family index（若该 family 只有 1 个可得变量则直接用该变量）。
  - PASS 判据：**≥2 个不同 family** 的 family index 与 BS（leverage 或 liquid/asset）在两国方向一致（sgn(θ^JP_f)=sgn(θ^CN_f)=expected +1），且每个方向一致的 family θ 的 bootstrap 90% CI 不含 0 至少在一国成立、另一国不显著反向。
  - 同 family 内多条高度相关 series 不算独立（新房/二手同属 PRICE）。
  - 可得 family <2 → INFEASIBLE。
- **Gate B2（BS→Profitability）**：θ_B→R 两国方向一致；至少一国 bootstrap 90% CI 不跨 0；另一国不得显著反向。（同 v1.2）
- **Gate B3（Profitability→Credit）**（P1-4 闭包：supply/demand 机器化）：
  - 两腿并列，均需数据：
    - B3a quantity 腿：θ_R→Cq（Cq = credit quantity：credit/GDP growth 或 flow）方向一致；
    - B3b demand 腿（区分供给/需求）：冻结 stance proxy 与 demand proxy 集合——stance：JP=政策利率（贴现率/无担保隔夜，季度 avg）、CN=1Y LPR/贷款基准利率（历史衔接，季度 avg）；demand proxy：CN=PBOC 企业中长期贷款余额 YoY（信贷收支表）、JP=BOJ FFA NFC 借贷流量（credit impulse）。
    - B3b 判据：在 stance 宽松子窗（政策利率 ≤ 全窗中位数 或 环比下行）内，demand proxy 的中位变化 ≤ 全窗中位变化（宽松未刺激企业主动加杠杆）；若 stance 与 demand proxy 任一不可得 → B3b INFEASIBLE，**Gate B3 整体 INFEASIBLE_AFTER_PRESPECIFIED_MASK**（禁止用"贷款增长下降"单独替代信用需求判据）。
  - PASS = B3a 方向一致（两国同号 = expected）且 B3b 支持（或 B3b 单独 INFEASIBLE 时 B3 仍记 INFEASIBLE 而非 PASS）。
  - **B3 语义冻结（外审 v1.2.1 P1）**：B3 结论名称固定 = `CREDIT_DEMAND_PROXY_EVIDENCE`（demand-consistent credit behavior / credit-demand proxy evidence），**禁止** `IDENTIFIED_CREDIT_DEMAND`——CN 企业中长期贷款 YoY 与 JP NFC credit impulse 均为 observed equilibrium credit quantity（受供给/政策/置换/利率多因素影响），最多是 credit-demand proxy 而非 identified demand。B1 若寻得更直接的企业贷款需求调查，按预注册 source-priority/substitution rule 使用；否则 proxy 可执行但结论降级。
  - **stance 拆分报告（外审 v1.2.1 P2）**：B3b 宽松子窗按 `stance_by_level`（政策利率≤全窗中位数）与 `stance_by_change`（QoQ 下行）**分列输出**，禁 OR 合并后无法归因驱动来源。
- **Gate B4（Credit→Investment）**：θ_C→I 两国方向一致 + CI 规则同 B2；I_q 与 I_ratio 双口径分别报告（I 不进入 classifier，天然 held-out）。
- **Mechanism Verdict（含 INFEASIBLE precedence，P2 外审 §十五 闭包）**：
  - evaluable links = 四链中去掉 INFEASIBLE 后剩余；**minimum evaluable links = 3**：evaluable <3 → 直接 INFEASIBLE（不得因 0-1 通过误判 GEOMETRY）。
  - STRONG：evaluable≥3 且 ≥3 链 PASS 且不缺 P→B 与 C→I；
  - PARTIAL：evaluable≥3 且 ≥2 链 PASS 但非 STRONG；
  - GEOMETRY：evaluable≥3 且 ≤1 链 PASS 或关键链方向相反；
  - INFEASIBLE：evaluable<3。
  - Gate 判定由归档 engine 机器输出（narrative 不得先于 machine）。

## 9. Deflation Gate（FROZEN；v1.2.1 闭包 P0-1 阈值落定）
- **阈值冻结（P0-1 闭包，不再"如 <1% 或 <0.5%"）**：
  - 统一绝对阈值：**LOW_OR_NEGATIVE = YoY < 1.0%**；NEGATIVE = YoY < 0%（报告子计数，D-B 主判据用 <1.0%）。
  - 六类指标：CPI / Core CPI / Services CPI / PPI / GDP deflator / Wage-income（全部转 YoY；annual 工资序列按年标注，不与季度指标机械拼接——六类各自在可得频率判定，D-B/D-C 用"可得类别"计）。
- D-A：CPI YoY < 0，仅描述。
- D-B Broad：六类中 **≥3 类（分母=可得类别，至少需 4 类可得，否则 INFEASIBLE）YoY < 1.0%**。
- D-C Persistent：D-B 状态连续 **≥4 季度**。
- D-D：broad/persistent + 主机制链（§8）机制证据，两者同时才可作 Japan-like 解释；CPI<0 永不单独触发。
- **阈值属性注记（外审 v1.2.1 补充）**：1.0% 是研究分类阈值，不应在最终报告描述为经济学上唯一"通缩边界"——D-A 保留 CPI<0 描述、D-B/D-C 作为 broad/persistent regime 判据。
  - **冻结文本一致性（v1.2.3）**：任何冻结文件（spec/gate registry/QC）不得残留 "<0.5%" 等候选阈值措辞——D-B notes 已统一为 "阈值 B0 冻结：YoY<1.0%；1.0% 为研究分类阈值"；QC `unresolved_deflation_candidate_threshold=0` 机器断言。
- D1-D4 口径稳健性 + price_measurement_risk_registry 禁 manipulation_score（同 v1.2 §9）。
- CN 起点：CPI 全史 / core 2013+ / services 2016+ / PPI 1996+ / GDP deflator（官方或明确构造，禁名义/实际 level 相除）/ wage 城镇单位名义 YoY annual。

## 10. Missingness Gate（FROZEN；v1.2.1 闭包 P0-2 数值落定）
每核心变量进模型前（§11 十条之外）另过 missingness Gate：
- **core 变量**：analysis-window observed share ≥ **0.85**；最大连续缺失 ≤ **2 季度**。
- **aux 变量**：observed share ≥ **0.70**；最大连续缺失 ≤ **4 季度**。
- **structural pre-start 不计 missing**：变量官方起点晚于窗首（如 CN core CPI 2013+ vs 2010 窗首）——不计入 missing，但须显式报告 `n_available / n_window / structural_gap_years`；若 structural 缺口使窗内有效观测 <50% 窗长 → 该变量标 PARTIAL_WINDOW，不参与该窗主检验（可参与 extended 窗）。
- **任何插值不得用于过 Gate**：missingness 基于原始 NA 计数；插值后的序列不得声称 0 missing（no silent interpolation 纪律）。
- 输出 per-variable：n_expected / n_observed / n_structural_gap / max_consecutive_missing / observed_share / gate_status（PASS/PARTIAL_WINDOW/FAIL）。

## 11. 数据质量 Gate（FROZEN，同 v1.2 §11；missingness 数值见 §10）

## 12. Bootstrap resampling 规则（FROZEN；P2-3 闭包）
- moving block bootstrap L=3、n_boot=2000 主；aux L=2/4（各 2000 reps）；Gate 只认 L=3。
- **resampling unit（P2-3 闭包）**：时间索引对 (t, t+k)——对时间索引做 non-circular block 抽样（块起点 s∈[0, n−L]，线性切片禁取模，H6-A 四坑纪律），抽中的 t 同时取 X_t 与 Y_{t+k}（**不分别抽 X 与 Y 的块**，否则破坏 X-Y 联合相关结构）；joint-pair 逐 rep 重算 θ_XY（window-average），得到 θ 的 bootstrap 分布。
- valid-share：n_boot_valid ≥ 0.9 × 2000 要求；0.5-0.9 → conditional 标注（CI conditional-on-feasible-resamples，H6-A A3.2 P2 教训）；<0.5 → INFEASIBLE。
- refit 必须消费重抽样数据（data= 参数化，禁闭包捕获原序列——CI 点退化即 plumbing bug 信号）。
- 输出：requested/valid/failed/valid_share/block_lengths/wrap_blocks=0。

## 13. 数据源优先级（FROZEN；P2-1 闭包 → h6b_source_priority_registry_v1.2.3.csv）
逐变量 Tier A/B/C + primary/secondary source + source cutoff 记录列。Tier 定义同 v1.2 §10。

## 14. 交付物与产物结构（FROZEN，同 v1.2 §12；audit_package_h6b/ 目录）
B0 v1.2.1 包：本 spec + variable/sign/gate/shock_adjustment/source_priority 五 registry + 响应文档 + 审核说明 + SHA256 manifest（单 ZIP）。

## 15. 证据分级与 scorecard（FROZEN，同 v1.2 §13；θ/sign/missingness 引用本版 §5/§3/§10）

## 16. Machine QC（v1.2.3 验收；metadata consistency）
```
n_variables=37
n_gates=16
sign_direction_multiplier_mismatch=0
gate_criteria_placeholder_left=0
gate_machine_executable_all_true=TRUE
unresolved_deflation_candidate_threshold=0
unresolved_latest_without_cutoff_reference=0
deflation_threshold_missing=0
missingness_threshold_missing=0
theta_definition_missing=0
sign_orientation_missing=0
gate_b1_machine_executable=TRUE
gate_b3_machine_executable=TRUE
b3_demand_interpretation=PROXY
shock_application_missing=0
source_priority_missing=0
analysis_cutoff_frozen=TRUE
manifest_sha_failed=0
```
以上 18 项机器断言由 engine/QC 脚本输出（h6b_b0_v123_qc.txt），全 PASS 方可送审。

## 17. 待外审确认点（v1.2.1 送审问询）
1. θ = 5-lag window-average Spearman（JP/CN 同公式）作为主判据、lag profile 仅作透明度报告——是否接受此多重比较处理？
2. Deflation 阈值统一 LOW_OR_NEGATIVE = YoY <1.0%（D-B ≥3/≥4 可得类）——数值是否接受？
3. Missingness 数值（core obs≥0.85 & 连续缺失≤2 季；aux ≥0.70 & ≤4 季；structural pre-start 不计 missing）——是否接受？
4. Gate B3 两腿（B3a quantity + B3b stance/demand）——CN demand proxy=PBOC 企业中长期贷款 YoY、JP=BOJ FFA NFC credit impulse 的 proxy 选择是否可辩护？B3b 不可得时 B3 整体 INFEASIBLE 的处理是否接受？
5. Verdict INFEASIBLE precedence（minimum evaluable links=3）——是否接受？
6. Source cutoff 2026-08-31 冻结——是否接受？
7. （v1.2.2 新增）sign_multiplier 机器推导（direction 唯一真源：↓→−1、↑→+1）+ 新 QC 五项——是否接受？
8. （v1.2.2 新增）B3 语义冻结为 CREDIT_DEMAND_PROXY_EVIDENCE（禁 IDENTIFIED_CREDIT_DEMAND）+ stance_by_level/stance_by_change 分列——是否接受？
9. （v1.2.3 新增）D-B notes 清理 + latest→latest_by_cutoff_2026-08-31 + gate registry B1-B4 列错位修复（自查发现）——metadata-only，是否接受？

## 18. 修订记录（v1.2 → v1.2.1）
- P0-1 → §9 阈值落定（统一 <1.0%）；P0-2 → §10 missingness 数值；P0-3 + P1-1 → §5 θ 定义（window-average + profile 双输出）。
- P1-2 → §3 sign registry；P1-3 → §8 Gate B1 family 判据；P1-4 → §8 Gate B3 两腿；P1-5 → §7 shock registry。
- P2-1 → §13 source_priority registry；P2-2 → §4 source cutoff；P2-3 → §12 MBB resampling unit。
- 外审 §十五 Verdict precedence → §8（minimum evaluable=3）。
- 研究设计零改动（五 channel / quarterly / D 模块独立 / 三轨 / 禁 classifier / 禁 fixed-lag 全保留）。
v1.2.2 → v1.2.3（metadata-only）：Gate registry D-B notes 清除 0.5% 候选措辞（冻结 YoY<1.0%）；registry `latest` 统一改 latest_by_cutoff_2026-08-31；**自查修复 Gate B1-B4 列错位**（v1.2.1/v1.2.2 生成脚本拆包 bug：criteria 文本误入 ci_rule、gate_criteria=TRUE、machine_executable=-；Verdict/D 行因 fallback 未受影响）——16 行全量重建正确列序；新 QC（gate_criteria_placeholder_left=0 / gate_machine_executable_all_true=TRUE / unresolved_deflation_candidate_threshold=0 / unresolved_latest_without_cutoff_reference=0）；closed set 重签 SHA。
v1.2.1 → v1.2.2：sign registry/variable registry 方向-乘子一致性修复（direction 唯一真源，37 行机器推导；涉 investment/credit/profitability/liquidity/diffusion 端点 17-20 行）；新 QC 五项（sign_direction_multiplier_mismatch / cross_mismatch / expected_chain_invalid / gate_variable_unregistered / duplicate_id）+ b3_demand_interpretation=PROXY + manifest_sha_failed=0；B3 语义冻结 CREDIT_DEMAND_PROXY_EVIDENCE；stance 分列报告；annual-step 低频限制标注；closed set 同步重签 SHA。
