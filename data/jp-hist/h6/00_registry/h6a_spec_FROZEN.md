# H6-A External Shock Robustness — Frozen Spec（FROZEN）
版本：2026-09-07 v1.0 FROZEN
项目：JP-HIST（Japan Historical Macro Comparison）· 链 08_jp_hist/h6/
上游建议书：01_数据采集/外部审核意见/JP-HIST_H6A_H6B_下一步工作方向与数据采集建议书_20260907.md（本 spec 以其为蓝本并吸收其全部纪律）
状态：本文件签署后为只读；任何修订须走 errata + 版本化（v1.1…），不得静默改写。

## 0. 冻结记录
- 用户授权：2026-09-07「按默认执行」——结构=并入既有链 08_jp_hist/h6/；顺序=先冻结 A+B 双 spec → 立即执行 H6-A → 按 Gate 决定 B1；H6-A v1=按建议书全含（3 因子+OxCGRT 辅助+Bai-Perron 诊断层）。
- 每一步关键步骤完成后提供完整审核文档供外部审核（H4/H5 同款节奏）。
- 决策记录 §10（追加用）。

## 1. 研究问题与目标（可证伪表述）
在事先定义的外部冲击约束下，检验 H4/H5 冻结结论是否稳健：
- Q-A1：剔除/屏蔽任一 confirmatory 事件（E01/E02/E03/E05）后，2013-2025 结构态归属（J90/J00/JGAP/OTHER 份额、逐年代表年）是否根本翻转？
- Q-A2：COVID（E05，2020-2022，含 CN 特异性 E06）调整后，2013-2019 与 2023-2025 的状态结构是否仍存在？
- Q-A3：Investment held-out 方向复现在 baseline、-COVID、shock-residualized 三类口径中是否至少两类保持同方向？
- Q-A4（诊断，不改窗）：Bai-Perron 识别的断点是否集中在已知事件附近？
明确不做：不以"提高 lag/regime 一致性"为优化目标；不因结果修改事件窗口；不把 adjustment 后的稳定 22 年自动升级为 fixed lag（见 Gate A4）。

## 2. 事件注册表（FROZEN，见 h6a_external_event_registry.csv）
| ID | 事件 | 窗口 | Scope | 角色 |
|---|---|---|---|---|
| E01 | 亚洲金融危机+日本金融压力 | 1997-1998 | Asia/JP-heavy | confirmatory |
| E02 | Dot-com 破裂 | 2000-2002 | global/US-led | confirmatory |
| E03 | 全球金融危机 | 2008-2009 | global | confirmatory |
| E04 | 欧债/二次金融压力 | 2011-2012 | global/Europe-led | auxiliary（不参与 confirmatory 判定） |
| E05 | COVID-19 | 2020-2022 | global + country-specific | confirmatory |
| E06 | 中国 2022 防疫/活动冲击 | 2022 | CN-specific | diagnostic（与 E05 不等同） |

## 3. 掩码（h6a_event_mask.csv；只新增，不改原数据）
- LEO-1 window aggregation mask：事件年保留单年分类，但不参与 window best lag mode、median lag、cluster share、transition probability 的汇总。
- LEO-2 JP candidate mask：如 CN 年份寻找 JP 候选时禁止 JP 2000-2002（E02）成为候选 → 回答"CN 被分到 JGAP/J00 是否只因 JP 该段自身异常"。
- LEO-3 CN event-year mask：CN 2020-2022（E05）与 2022（E06）保留 diagnostic classification，但从"当前中国长期状态"整体总结剔除。
- 组合方式：每次只 leave-one-event-out（E01..E05 逐一），E04 仅作敏感性；E06 只与 E05 并列做 diagnostic 说明，不单独构 confirmatory。

## 4. 全球因子（v1 仅此清单，FROZEN；h6a_global_factor_registry.csv）
- g1 world_gdp_growth：World Bank NY.GDP.MKTP.KD.ZG，aggregate=World，年度，直接匹配年频；历史缺口不插值。主因子。
- g2 vix_mean：FRED VIXCLS 日度 → 年度算术均值（主）；vix_max 年度最大值仅 aux sensitivity。
- g3 covid_dummy：1(2020≤t≤2022)（主检验中最稳、零额外数据）。
- aux oxcgrt_stringency_{cn,jp}：OxCGRT（GitHub OxCGRT/covid-policy-dataset）CN/JP Stringency Index 年度均值 + 可选 days>threshold；仅 auxiliary（中国 2022 地方差异大，全国聚合低估局部封控，不作唯一 COVID adjustment）。
- 明确不采（v1）：oil、global trade、Fed funds、dollar、更多 crisis dummy（防 CN 短样本高维控制）。

## 5. 残差化模型（FROZEN；施加于 standardized 水平序列、robust-z 归一化之前）
主模型 A：z_{i,c,t} = α_{i,c} + δ_{i,c}·t + β_{i,c}·G_t^growth + γ_{i,c}·D_t^COVID + u_{i,c,t}
辅助模型 B：A + β2_{i,c}·G_t^financial(vix_mean)（VIX 仅覆盖 1990+，spec 注明其对 JP 早段无解释力，结果分层报告）
- 回归方法：主 OLS；辅助 Huber robust（statsmodels）。若 OLS 与 Huber 残差结果差别巨大 → 该 shock model 受极端值支配，residualized 结果证据等级下调（如实报告）。
- 残差 û 再按各窗口既有 robust-z 规则归一化后重跑 similarity engine。
- 拒绝规则：不得为让 lag 变稳定而逐步加控制。

## 6. 引擎复用与注入点（add-alongside，v1 本体零改动）
- 复用 04_analysis/h5/engine/：h4v03d_engine（曼哈顿/欧氏/秩态/形状相关 + robust-z 窗口）、分类 argmax、held-out 方向检验（h5_final_tests.py 模式）。
- 改动仅为薄包装：新增事件掩码参数（哪些年不进汇总/不进候选/从总结剔除），引擎文件不改。
- H4/H5 baseline 冻结文件只读；新产物一律进 h6/04_analysis/h6a/。

## 7. Reconciliation 输出规格（机器生成 CSV，数字不手写）
h6a_lag_reconciliation.csv：D 窗 4 metric（MANHATTAN/EUCLID/RANKSTATE/SHAPECORR）× {Baseline, -E01..-E05, -COVID(LEO-3), Residual-A, Residual-B}。
h6a_regime_reconciliation.csv：2013-25 J90/JGAP/J00/OTHER share × 同上；**每格同时给"全 13 年"与"mask 后剩余年"两版份额**（防选择性报告；13/13 一致性与 7/4/2 计数一并重算）。
h6a_mechanism_reconciliation.csv：CPI/INVESTMENT/M2 held-out D、CI、perm p × 同上。

## 8. Gates（FROZEN；达标/不达标都如实冻结）
- Gate A1 Event Robustness：去除任一单个 confirmatory 事件后核心结构态结论不发生根本翻转。"根本翻转"= J90/J00 整体主导状态互换，或 H4 retrospective similarity 全部消失。
- Gate A2 COVID Robustness：2020-2022 剔除/调整后 2013-2019 与 2023-2025 的状态结构仍存在；否则"向 J00 靠近"的观感可能受 COVID 污染（如实降级）。
- Gate A3 Investment Robustness：investment held-out 在 baseline、-COVID、shock-residualized 三类中至少两类同方向；全消失 → H6-B investment 通道降级。
- Gate A4 No Fixed-Lag Rescue：即使 adjustment 后出现 22 年稳定也不自动升级 fixed lag；需 ≥3/4 metrics ∧ ≥2 normalization families ∧ LOMO ∧ event robustness 同时支持才允许重开讨论。

## 9. 交付物与验收
h6a_spec_FROZEN.md / h6a_external_event_registry.csv / h6a_global_factor_registry.csv / h6a_event_mask.csv / h6a_global_factors.csv / h6a_leo_results.csv / h6a_residualized_features/ / h6a_lag_reconciliation.csv / h6a_regime_reconciliation.csv / h6a_mechanism_reconciliation.csv / h6a_break_diagnostics.csv / H6A_final_report.md / SHA256_manifest_h6a.txt（audit_package 收档）
步骤：A0 冻结本 spec（本文件）→ A1 因子采集（3+OxCGRT）→ A2 LEO → A3 残差化 → A4 Bai-Perron → A5 冻结 H6-A + 外审文档。每完成 A1/A2/A3/A4 形成审核材料；A5 出统一审核包。

## 10. 决策记录（追加制）
- 2026-09-07 用户「按默认执行」：结构 08_jp_hist/h6/；顺序 A→B；A v1 全含；每步关键完成后出审核文档。→ 本 spec FROZEN v1.0。
