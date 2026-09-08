# JP-HIST H3 Feature Engineering — Semantic-Aware Transformation Layer 规格
日期：2026-09-06
状态：DRAFT（待用户授权 + 决策点拍板后冻结）
上游：H2 STANDARDIZATION FREEZE（FREEZE_H2_20260906.txt）；审核指引（H2 v0.3 PASS 报告 §11 P1-1 + §13）
方法论源：数据采集与分析方法论稿 §28-31（robust z / percentile / 六大模块）

## 1. 定位与边界
H3 将 standardized 数值序列转为"结构状态"，供 H4+ 做 JP(1970-1995) ↔ CN(2000-2012) 滞后结构比较。
第一 gate（审核要求）不是 similarity 计算，而是 **semantic-aware transformation layer**：
- 读取 H2 coverage_map 的 semantic_status + required_h3_transform，强制消费，不绕过
- 未处理/未知 semantic 状态 → 代码硬 fail（G-H3-2）
- 输出可审计的 feature files（每 feature 带 transform_id + 输入 lineage）

H3 不做：lag scan / similarity / DTW / rolling（方法论 §33-41 属 H4+）；不做新数据采集。

## 2. 输入
- 41 个 standardized CSV（02_standardized/annual_*.csv，H2 FREEZE 冻结）
- h2_coverage_map_v0.2.csv（semantic_status / required_h3_transform / status / coverage_ratio）
- 方法论稿 §30 模块归属

## 3. Semantic 处理规则（硬约束，来自 FREEZE_H2 W03-W06）
| semantic_status | H3 处理 | 约束 |
|---|---|---|
| EXACT | 直接进 state 变换 | 无前置 |
| PRE_TRANSFORM | 先执行 required_h3_transform（level→YoY、level→/GDP） | 变换后与 registry 概念同形态才可比较 |
| PROXY_FLOW / PROXY_STOCK | 独立 track，可各自做 state 变换 | 禁与 EXACT 同入一 comparison feature |
| ANCHOR | 保留锚点观测做状态点 | 禁插值成年度连续后入主模型 |
| NOT_MAPPED | 保持 NA/GAP | 禁自动填充 |

## 4. State 变换（方法论 §28）
两种状态量，均为 within-country 变换（本国历史制度中的位置）：
1. **Robust z-score**（优先，方法论 §28 建议）：Z = (X - Median) / (1.4826 × MAD)
2. **Historical percentile**：P = PercentileRank(X)（本国 expanding/full-sample——见决策点 D-H3-1）

产出形态：g_t（growth/rate 直接保留，已是状态）或 Z_{k,t} / P_{k,t}。

## 5. 六大模块（方法论 §30，映射到 H2 实际覆盖）
| 模块 | 变量（H2 有覆盖者） | 备注 |
|---|---|---|
| GROWTH | real_gdp_yoy, iip_yoy, investment_gdp | corp_profit_growth 无覆盖（JP corp NOT_MAPPED） |
| INFLATION | cpi_yoy, gdp_deflator(yoy，PRE_TRANSFORM 后) | |
| MONEY_CREDIT | m2_yoy, policy_rate, jgb10y | credit 仅 PROXY track（D01）；corp_leverage 无 |
| EXTERNAL | export_yoy, trade_balance(/GDP，PRE_TRANSFORM 后), reer, fx_usdjpy | |
| PROPERTY_ASSET | land_price_yoy, nikkei_return(equity_return) | |
| DEMOGRAPHY_LABOR | wage_yoy, unemployment, working_age_growth, dependency_ratio, youth_dependency, tfr, birth_rate | JP 人口 3 系列=ANCHOR；CN=annual |

## 6. 输出与审计
- 目录：03_features/（H3 产物独立于 02_standardized，不污染 H2 冻结层）
- 每 feature 文件：year, value(state), variable, country, unit, source_std_file, transform_id, semantic_status
- h3_transform_manifest.csv：feature × (std 输入文件, semantic, transform_id, 状态公式, 窗口定义, sha256)
- 硬断言：scan coverage_map 全部 mapped 行 → 每行必须有对应 H3 处理分支（EXACT→state；PRE_TRANSFORM→先 transform；PROXY→track 标注；ANCHOR→锚点处理；NOT_MAPPED→跳过留 NA）；无分支 → fail

## 7. 决策点（开工前拍板）
- **D-H3-1**：robust z / percentile 的参考窗口——full-sample（各国全史）vs expanding（至 t 为止）。方法论 P1-4 提示：日本利率长期近零，简单 expanding rank 信息量低——倾向 full-sample 或 regime-aware；但 full-sample 有 lookahead 风险（vintage 角度）。推荐：**主用 robust z（full-sample 但以 H1 冻结的 RETROSPECTIVE_HISTORICAL 定位声明）；percentile 作辅助诊断，窗口同 full-sample**。H4 lag scan 对状态序列敏感度做 robustness（rolling window 敏感性）再定。
- **D-H3-2**：六大模块是否为 H3 产物的组织单位（模块 state 向量文件）？推荐：是——03_features/ 下按 module 子目录组织 + module_state_{name}.csv 宽表（变量为列），供 H4 模块相似度直接读。
- **D-H3-3**：ANCHOR 系列（JP 人口 3 项）H3 处理——推荐：产出 anchor_state 点文件（仅普查年），标注不得插值；H4 模块相似度中 DEMOGRAPHY_LABOR 对 JP 侧 anchor 采用"最近锚点年匹配"或排除该变量（待 H4 定）。
- **D-H3-4**：policy_rate/jgb10y 是否做 regime-aware 变换——日本利率长期零下界，robust z 会把 1995+ 全部压成极端负值。推荐：H3 先产出 raw robust z（如实），regime 切分（零利率 regime dummy）作为 H4 模块输入，不在 H3 预判剔除。

## 8. 验收（Gate H3 审核包）
- transform 层代码可复现（每 feature 从 std CSV + 公式重建）
- semantic 消费断言全过（无未处理 mapped 行）
- 抽查锚点：GDP robust z 应把 1974 石油危机(-1.2%)/2009(-5.7%) 标为显著负态、1990s 泡沫顶 1989-90 高位态；CN 2007/2010 高位、2008/2009 低位态
