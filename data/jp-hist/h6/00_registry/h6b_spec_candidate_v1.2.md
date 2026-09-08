# H6-B External Mechanism Validation — Spec Candidate v1.2（完整重设计，待外审）

版本：2026-09-07 v1.2 candidate（外部建议书 v1.2 采纳 + 执行评审 8 项修订吸收）
状态：candidate——外审 PASS 后提升 FROZEN v1.2。
上游：①《JP-HIST_H6B_外部机制验证研究建议书_v1.2_20260907.md》（蓝图，1427 行）②《JP-HIST_H6B_v1.2_执行评审与修订建议_20260907.md》（本 spec 的 8 项修订来源）③ h6b_spec_FROZEN_v1.1.md（A0 定档，被本版取代执行地位，只读存档）
元数据：spec_version=v1.2-candidate；candidate_date=2026-09-07；parent=v1.1-FROZEN → v1.2 重设计；sha256 见 B0 审核包 manifest。

## 0. 决策记录
- 2026-09-07 用户拍板：采纳 v1.2 为执行基线，走 B0 冻结流程（v1.1 只读存档）；本次推进=评审书落盘 + candidate 成稿，送审动作待用户确认。
- v1.1→v1.2 变更性质：**重设计**（非增量）——频率 annual→quarterly 主频；阶段 B1a/B1b/B2/B3→B0-B6 七阶段；Gate1/2→Gate B1-B4 分层 + Verdict 四档；新增 H6-B-D Deflation 模块；时间结构 event-time τ 锚点→窗内 lead/lag（τ 降辅助）。
- 评审修订项 8 条全部吸收（见 §10 修订记录逐条索引）。

## 1. 核心研究问题（FROZEN）
H6-A 已确认：broad structural-state geometry 存在、exact lag 不稳健、investment 是候选机制但未过 shock-robust Gate、CPI=hinge not mechanism。因此 H6-B 不再问"像不像"，而问：
> 如果中日部分宏观状态相似，这种相似是否来自可独立验证、具有时间顺序与经济逻辑的共同机制链？

主机制链（候选固定）：
Property / Asset-price Adjustment → Corporate Balance-sheet Deterioration → Profitability / Return Decline → Credit Demand / Allocation Change → Investment Decline

明确不做（禁改清单，同 FREEZE_H5/H6A W 纪律）：
- 任何 H6-B 新变量加入旧 H4/H5 J90/J00 classifier（circular validation 禁令）
- argmax_L similarity(L) 型 fixed-lag 搜索
- 以"像日本"回选变量
- causal 主张（Level 4 / causal proof 不做；本 spec 证据上限 = Level 3 Mechanism-Supported Chain，且措辞为 correspondence 非 equivalence）

## 2. 五 Channel + Deflation 模块（FROZEN 骨架）
| Channel | 概念 | 核心变量（两国至少各 1） | 辅助变量 |
|---|---|---|---|
| P | Property / Asset-price Adjustment | JP: land price(MLIT 年度) + housing starts(MLIT) / CN: NBS 70城新房价格 + 房地产开发投资 | JP: 住宅着工、property-related lending(如可得)；CN: 二手房价、销售额、新开工、待售 |
| B | Corporate Balance Sheet | JP: MOF 法人統計 liabilities/assets / CN: NBS 规上工业资产负债率 | 双方: debt/asset、liquid/liab、receivables/revenue、inventory/revenue、interest burden |
| R | Profitability / Return | JP: MOF ordinary profit/sales / CN: 规上工业营业收入利润率 | ROA、operating margin、每百元资产收入、应收回收期、库存周转天数 |
| C | Credit Demand / Allocation | JP: BIS NFC credit/GDP + HH credit/GDP / CN: PBOC 部门信贷（住户+企业） | BIS DSR、BOJ FFA、TSF 结构（人民币贷款/企业债/政府债）、credit impulse |
| I | Investment | JP: GFCF/GDP（年度 I_ratio 连续性锚）+ 季度 GFCF / CN: 固定资产投资/地产投资（季度代理） | MOF capex、制造业投资、private investment |
| D | Deflation Regime（独立模块，不进主 Gate） | JP/CN: CPI headline + core + services + PPI + GDP deflator + wage/income 六类 | item-level indices（diffusion） |

D 模块为独立研究问题（v1.2 §十九）：通缩结论不并入 Mechanism Verdict。

## 3. 机制假说（FROZEN；每链做方向 + 时序检验）
- H6B-H1 Property：Property↓ ⇒ Balance-sheet deterioration（杠杆↑/流动↓）
- H6B-H2 Balance Sheet：Leverage↑ 或 InterestBurden↑ 或 Liquidity↓ ⇒ Investment↓（去杠杆阶段本身 Leverage↓——不得只按单方向机械判断，须结合时序与资产价格；v1.1 H2 方向陷阱保留）
- H6B-H3 Profitability：Profitability↓ ⇒ Investment↓
- H6B-H4 Credit：CreditImpulse↓ / CreditDemand↓ ⇒ Investment↓（须区分 supply vs demand，见 §8 Gate B3）
- H6B-H5 Composite：JP 与 CN 均呈 Property↓ ∧ Profitability↓ ∧ CreditDemand↓ ∧ Investment↓ 且时序合理 → investment correspondence 获更强机制支持
- 符号统一：所有变量先定义"恶化方向"再检验（B0 预注册符号表，禁事后翻转）

## 4. 数据频率与窗口（FROZEN）
主频率：**Quarterly**。Monthly 仅作中间采集（CN 房地产/信贷/CPI/PPI 原生月度）；Annual 保留（长期工资、MLIT 地价、I_ratio、人口辅助）。
月度→季度预注册规则（v1.2 §十一）：
- stock：quarter-end；
- flow：quarter sum（CN 房地产 **YTD 累计必须先还原单季流量** Flow_m = YTD_m − YTD_{m−1}，禁直接平均累计值）；
- price/growth index：quarter average。

窗口（v1.2 §二十 + 评审修订项五）：
- JP primary：1985Q1–2005Q4（泡沫形成-破裂-资产负债表调整）；Long-window sensitivity：1970Q1+（若变量可得；68SNA/93SNA 季度衔接成本高，JP 侧按实际变量可用性标 common-support）
- CN primary：2010Q1–latest（地产主机制窗）；Extended：2005Q1–latest（信贷/价格可得的更长对照）
- COVID sensitivity：2019Q4 节点前后分段，不删除、不挑窗

## 5. 时间结构（FROZEN；评审修订项二）
双层：
(a) 主检验（进 Gate）：各 chain 相邻环节的窗内 lead/lag 传导——X_t → Y_{t+k}，k ∈ {0,1,2,3,4} 季度（预注册；用于检验传导速度，禁重新解释为"中国滞后日本 N 年"）。Spearman 主 / Pearson 辅；不以 max-correlation lag 为结论，只问"预注册窗口内是否存在方向一致关系"。
(b) 辅助视角（descriptive，不进 Gate）：τ^INV 锚点（JP1990 / CN2011 投资峰值 ±20 季），比较两国峰值前后变量路径是否同型——v1.1 event-time 设计降级为 descriptive auxiliary，修订记录明示。

## 6. 变换与 Channel Index 合成（FROZEN；评审修订项七）
- 逐变量标准化：robust-z（within-country full-sample 标定，沿用 H3 定义：z=(X−Median)/(1.4826×MAD)）；人口 rate 类（CBR/TFR）沿用 Δ 变换再 robust-z（H0 冻结）。
- Channel index：channel 内变量逐期 robust-z 后**等权平均**；权重冻结禁事后调权；输出单变量级 + channel 级双轨结果。
- Level / First-difference 双轨（v1.2 §十五 Test 3）：primary=standardized level/state；robustness=first-difference/YoY；detrended 仅辅助。**禁把长期结构趋势从主分析直接剥离**（H6-A A0 P0-2 教训）。
- 禁 level concat（跨 definition regime 各 regime 内 growth 再拼）；禁 NA→0；留缺口不补二手。

## 7. 三轨报告（FROZEN；评审修订项八）
每 chain 结论同时报告：
(a) Mechanism^Raw：原值/level 关系；
(b) Mechanism^ShockAdjusted：对 H6-A 冻结全球因子（World GDP growth + COVID dummy 2020-22；Model-B 增 VIX，JP 1990+ common-support）残差化后重估（H6-A A3 冻结 Model-A/B 语义沿用，输入=标准化前值，RobustZ(û)）；
(c) Mechanism^FirstDiff：first-difference/YoY 版。
Gate B1-B4 判定以 raw 为主、shock-adjusted 必须报告；仅 raw 成立而 adjustment 后消失 → 链降级 descriptive（v1.1 §9 同款，H6-A investment 教训承接）。

## 8. Gate B1-B4 + Mechanism Verdict（FROZEN；机器判据，engine 输出）
对每条相邻链 X→Y（P→B、B→R、R→C、C→I）：
- 方向复制：sgn(θ^JP_XY) = sgn(θ^CN_XY)；不要求系数绝对值相同。
- bootstrap：moving block bootstrap L=3、n_boot=2000 主（H6-A 全链四坑纪律：non-circular 块抽样 s∈[0,n−L]、refit 消费重抽样数据、obs stat 用真实分组）；aux L=2/4（各 2000 reps）判断 block 依赖；Gate 只认 L=3。JP/CN 各得 θ 的 bootstrap 90% CI。
- Gate B1（Property→BS）：≥2 独立 Property 指标 + ≥1 BS 指标在两国方向一致。
- Gate B2（BS→Profitability）：两国方向一致；且至少一国 bootstrap 90% CI 不跨 0；另一国不得显著反向。
- Gate B3（Profitability→Credit）：区分 supply/demand——credit quantity（stock/GDP）与 credit demand proxy（impulse、利率 vs 量的配合、企业主动融资）分列；仅"贷款增长下降"不足（须展示宽松环境下需求侧仍弱，M2↑/Supply↑ 而 CorporateDemand↓ 才接近 balance-sheet 机制）。
- Gate B4（Credit→Investment）：Investment 不进入 classifier 前提下独立成立（天然 held-out）。
- Mechanism Verdict（四档互斥）：
  STRONG MECHANISM CORRESPONDENCE = ≥3/4 链通过且不缺失 P→B 与 C→I 两端；
  PARTIAL MECHANISM CORRESPONDENCE = ≥2 链通过但完整链不闭合；
  GEOMETRY WITHOUT MECHANISM = 0-1 链通过或关键链方向相反；
  INFEASIBLE = 有效数据不足（预定出口，禁扩窗/降阈/合并）。
- Gate 判定由归档 engine 产出机器文件承载（Gate_machine_B*.txt/csv），narrative 不得先于 machine（H6-A P1 高发项）。

## 9. Deflation Gate（FROZEN；独立模块，不进主总 Gate；评审修订项五）
- D-A Headline Deflation：CPI<0，仅描述。
- D-B Broad Deflation：六类（CPI / Core / Services / PPI / GDP deflator / Wage-income）中 ≥3 进入预注册低位或负区间（低位阈值 B0 冻结：如 <1% 或 <0.5% 逐年定，禁看数据后调）。
- D-C Persistent Deflation：D-B 状态连续 ≥4 季度。
- D-D Japan-like Deflation Mechanism：须同时满足 (1) broad/persistent price weakness + (2) 主机制链（§8）有机制证据。CPI<0 永不单独触发 Japanization。
- 口径稳健性四检验（v1.2 §十）：D1 Sign robustness（headline 在 ±0.5% 附近时 core/services/PPI/deflator 是否同向）；D2 Rebase/weight robustness（重叠期差异记录，正常 rebase 不得自动解释为 manipulation）；D3 Price diffusion（分类指数负增长占比，如可得）；D4 Cross-system confirmation（CPI↔PPI↔GDP deflator 三角验证；若 CPI 持续略正而 PPI/deflator/wage 长期负 → 标 PRICE_SYSTEM_DIVERGENCE，禁标 STATISTICAL_MANIPULATION）。
- price_measurement_risk_registry.csv（country/variable/provider/weight_publication_level/microdata_public/methodology_public/rebase_frequency/historical_revision/known_definition_break/replication_level/risk_flag/notes）——只评估 measurement uncertainty，禁生成 manipulation_score。
- CN 指标起点（B0 冻结）：CPI 全史 / core 2013+ / services 2016+ / PPI 1996+ / GDP deflator 官方或明确构造（禁名义/实际 level 直接相除以构造连续 deflator，除非确认 chained volume 可重建）/ wage=城镇单位名义工资 YoY 年度。不足 3 类 → INFEASIBLE_AFTER_PRESPECIFIED_MASK 预定出口。

## 10. 数据源优先级与批次（FROZEN）
Tier A primary：JP=BOJ/MOF/MLIT/ESRI/Statistics Bureau(e-Stat)；CN=NBS/PBOC；Cross=BIS。
Tier B bridge/validation：OECD/World Bank/IMF；FRED 仅作官方序列的 distributor/bridge（已实测 BIS 镜像逐点零差异时可作缓存，官方 zip 留档）。
Tier C auxiliary：Wind/CEIC/Bloomberg/private——核心机制变量必须回溯官方 provider。

批次（v1.2 §二十四；每批完成为独立审核点）：
- Batch 1 可行性核心：JP MOF（季度 leverage/margin/interest burden——xls 已探明，assets22==liq23+fix29+net35 恒等式通过）+ BOJ FFA 企业信用 + MLIT land/housing + ESRI investment（季度 GFCF）；CN NBS 房地产（月度六线 YTD→单季还原）+ NBS 规上工业（月度高频→季度）+ PBOC 部门信贷 + NBS 投资。**若此批无法形成共同季度支持 → 调整设计，不扩张数据集。**
- Batch 2 credit refinement：BIS total credit（已下载 WS_TC bulk 1964Q4+/2006Q1+）+ BIS DSR（起点 1999——JP 1985-1998 段用 MOF interest burden 分列覆盖，评审修订项四）+ PBOC TSF 结构 + BOJ FFA 明细。
- Batch 3 deflation：CPI/core/services + PPI + GDP deflator + wage/income + category indices。

## 11. 数据质量 Gate（FROZEN；每核心变量进模型前十条全过）
source grade A/B；definition documented；frequency documented；unit documented；transform documented；missing share ≤ 预注册阈值（B0 冻结）；no silent interpolation；revisions/breaks explicit；source SHA frozen；reproducible parser（clean-rebuild 测试，H6-A A1.1 P1 教训）。Raw 不修改；source manifest / variable registry / definition-break registry / parent lineage 四件随 B1 建。

## 12. 交付物与产物结构（B0-B6 目录映射到 h6/ 既有树）
B0_SPEC/：h6b_spec_FROZEN_v1.2（本文件 PASS 后更名）+ h6b_variable_registry_v1.2.csv + h6b_gate_registry_v1.2.csv + h6b_source_priority_registry_v1.2.csv + 本评审书 + 修订响应 + SHA256 manifest
B1_RAW/：08_jp_hist/h6/01_raw/{jp,cn,bis}/（BIS bulk 已落位 bis_credit|bis_property_price——pre-B0 probe 定位，B1 正式 manifest 重建）
B2_STANDARDIZED/：08_jp_hist/h6/02_standardized/h6b/（quarterly 文件 + channel index 层）
B3_WITHIN_COUNTRY/、B4_CROSS_COUNTRY/：08_jp_hist/h6/04_analysis/h6b/
B5_DEFLATION/：deflation_registry.csv + price_measurement_risk_registry.csv + price_diffusion.csv + deflation_gate_results.csv
B6_SYNTHESIS/：H6B_FINAL_REPORT.md + ALLOWED_CLAIMS.md + PROHIBITED_CLAIMS.md + FREEZE_H6B.txt
governance/：lineage.csv + definition_break_registry.csv + manifest.sha256
每关键步完成 → 统一审核文档 + 单 ZIP（audit_package_h6b/）交付外审（项目单 ZIP 惯例）。

## 13. 证据分级与 scorecard（FROZEN）
Level 0 No Evidence / Level 1 Association（corr≠0，单源）/ Level 2 Replicated Directional Channel（两国预注册方向一致 + 主要稳健性检验不反向）/ Level 3 Mechanism-Supported Chain（多相邻环节同向 + 合理时序 + shock-adjusted 不反转）。
Scorecard 条件（frozen）：JP 方向合理论 required；CN 方向合理论 required；lead/lag 窗口合理 required；raw/shock-adjusted 双版均成立 required（同 §7）；≥2 独立数据族 required（跨国跨源复现）；bootstrap 不明显反转 preferred；temporal ordering 合理 preferred。

## 14. 修订记录（v1.1 → v1.2）
R1（评审修订项一）：v1.1 只读存档 + supersede 标注；registry 18 行映射至五 channel 双层新表（lineage 列保留 variable_id）。
R2（修订项二）：event-time τ^INV 降级 descriptive auxiliary；主检验=窗内 lead/lag k=0-4。
R3（修订项三）：Investment channel 双变量 I_ratio（年度，H6-A 同口径连续性锚）+ I_q（季度，主链检验）。
R4（修订项四）：BIS DSR 起点 1999 缺口 → JP 1985-1998 用 MOF interest burden 分列覆盖，禁拼。
R5（修订项五）：Deflation CN 指标起点逐项冻结 + INFEASIBLE 预定出口；阈值 B0 冻结。
R6（修订项六）：人口辅助链（Demography→Housing Demand→Property）保留为 AUXILIARY_EXPLORATORY，不进 Gate，annual 即可，不新增季度采集。
R7（修订项七）：channel index = within-country robust-z 等权平均，权重冻结，单变量+channel 双轨输出。
R8（修订项八）：三轨报告（Raw / ShockAdjusted / FirstDiff）每链必须，仅 raw 成立→降级。

## 15. 待外审确认点（candidate 送审问询）
1. 双层时间结构（lead/lag 主 + τ 辅助）是否接受——尤其 τ 从 v1.1 confirmatory 降 descriptive 的正当性。
2. Deflation 模块独立于主 Gate 的定位（不并入 Verdict）。
3. 三轨报告中 shock-adjusted 轨的 Model-A/B 语义沿用 H6-A A3 冻结定义是否足够。
4. CN 窗口 2010Q1 primary / 2005Q1 extended 的划分。
5. Gate B3（supply/demand 区分）的可操作判据——BIS/PBOC 数据能否支撑该区分，若无数据支持标 INFEASIBLE 是否接受。
