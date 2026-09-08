# H6-B External Mechanism Validation — Spec Candidate v1.1（待复审）
版本：2026-09-07 v1.1 candidate（A0 v1.0 外审 REWORK 后修订）
状态：candidate——外审 PASS 后提升 FROZEN。
元数据：spec_version=v1.1-candidate；freeze_date=2026-09-07；parent=v1.0（REWORK）；sha256 见 audit_package_v1.1 manifest。

## 0. 决策记录
- 2026-09-07 v1.0 FROZEN（用户「按默认执行」）；同日外审 REWORK；v1.1 candidate 修订如下。v1.0 文件保持只读。
- v1.1 变更（P1-4/P1-5/P2 + CSV P0-1）：registry 13 列机器化；housing_starts=CONCEPT_PROXY；property_investment=PENDING_CROSSWALK；property_price 拆 land_price / residential_property_price；event-time 锚点=investment anchor；bootstrap 增 L=2/4 aux。

## 1. 核心问题与主机制链（同 v1.0）
主链 Property → Corporate Balance Sheet → Profitability → Credit → Investment；辅助链 Demography → Housing Demand → Property → Investment。
明确不做：新变量进旧 classifier；以"像日本"回选变量；causal 主张（Level 4 不做）。

## 2. 机制假说（同 v1.0，H6B-H1..H5；H2 含去杠杆方向陷阱）

## 3. MVMD 与变量清单
见 h6b_mechanism_registry_v1.1.csv（语义逐项冻结）。v1.1 语义修订（外审 P1-4）：
- housing_starts：CONCEPT_PROXY（JP 户数 vs CN 面积；统一单位或转 YoY 后再定级，不自动 EXACT）。
- property_investment：PENDING_CROSSWALK（source-definition audit 后再定 EXACT/PROXY）。
- property_price 拆分：land_price（JP MLIT，CN NA=无同概念官方长史）与 residential_property_price（BIS 主干 + NBS 70城辅助，两国不同资产概念 → PROXY，CN 70城起点 2011 覆盖缺口显式标注）。
- 其余：EXACT/PROXY/SECONDARY/FLOW_PROXY 按 v1.0；空源用空字段，不靠少列。

## 4. 采集阶段与 Gate（同 v1.0：B1a/B1b/B2/B3；Gate1 五问 ≤1 停/≥3 进 B2；Gate2 四环≥3 且跨源→Mechanism-Consistent，禁 causal）

## 5. 分析工具（v1.1 修订）
- **Event-time（外审 P1-5）**：confirmatory 锚点 = investment-peak anchor，τ^{INV}_{JP}=t−1990、τ^{INV}_{CN}=t−2011；所有机制变量围绕该 investment anchor 展开（回答"投资峰值前后 property/profit/credit 如何变化"）。variable-specific 自身峰值仅 exploratory，不进 Gate。
- directional replication（同 v1.0，用冻结逐年归属，天然 held-out）。
- 相关：Spearman 主 / Pearson 辅；cross-correlation |k|≤3 exploratory。
- **推断（外审 P1-5 §13）**：moving block bootstrap 主参数 L=3、n_boot=2000；aux sensitivity L=2 与 L=4（同为 2000 reps）；Gate 只认 L=3；不得事后按结果选 block length；L=2/4 用于判断推断是否极端依赖 block choice。
- 不采用：VAR/SVAR/Granger/local projections/自动因果发现。

## 6. 证据分级与 scorecard（同 v1.0：Level 0-3；Level 4 不做；scorecard 条件 frozen 不变）

## 7. 语义与拼接纪律（同 v1.0：EXACT↔PROXY 显式标注；bis_dsr 与 mof_interest_burden_proxy 分列禁拼；TSF flow≠stock；留缺口不补二手）

## 8. 交付物（同 v1.0 + h6b_mechanism_registry_v1.1.csv）

## 9. 与 H6-A 联动（同 v1.0：Mechanism^Raw 与 Mechanism^ShockAdjusted 双版必须；仅 Raw 成立→如实降级）

## 10. 修订记录
v1.0→v1.1：registry CSV 修复（P0-1）+ 语义重审（P1-4）+ event-time anchor 定义（P1-5）+ bootstrap aux block（P1-5 §13）+ freeze meta。
