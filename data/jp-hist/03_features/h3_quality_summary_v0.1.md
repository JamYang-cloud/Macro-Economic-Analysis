# JP-HIST H3 Feature Engineering — Semantic-Aware Transformation Layer v0.1 质量摘要

日期：2026-09-06
上游：H2 STANDARDIZATION FREEZE（FREEZE_H2_20260906.txt）+ H3 spec（00_registry/h3_semantic_transform_spec_20260906.md）+ 决策 D-H3-1/2/3/4（用户拍板：full-sample robust z 主 + full-sample percentile 辅 / 六模块组织 / ANCHOR 点文件 / raw z 利率 regime 留 H4）

## 1. Semantic 消费（硬断言）
- coverage_map 40 个 mapped 行 → 39 processed + 1 DEFERRED（CN trade_balance_gdp：美元差额/亿元 GDP 币种不匹配，需 USDCNY 年均汇率——H1-P1 采集项；非静默绕过，h3_deferred.csv 记录）
- 无 HARD-FAIL（每 mapped 行有分支）；NOT_MAPPED 12 行跳过留 GAP

## 2. 处理分布
- EXACT 31 → robustz + pctrank（62 state files）
- PRE_TRANSFORM 3 → deflator_yoy(JP, level→YoY) / trade_balance_gdp(JP, /GDE) / property_price_yoy(CN, level→YoY) 先行变换再 state
- PROXY 2（JP credit_stock / CN credit_flow）→ state_proxy/ 独立 track（不混 comparison）
- ANCHOR 3（JP working_age/dependency/youth）→ state_anchor/ 锚点 only（不插值）
- 产物：03_features/state 68 + state_proxy 2 + state_anchor 3 + module 12 wide + manifest + deferred

## 3. 六模块 wide 表（12 = 6 模块 × JP/CN，robustz）
GROWTH / INFLATION / MONEY_CREDIT / EXTERNAL / PROPERTY_ASSET / DEMOGRAPHY_LABOR 全产出；
CN 侧 PROPERTY_ASSET 含 equity_return（2000-07）与 property_price_yoy，缺失年如实 NaN。

## 4. 状态锚点抽查（全符合经济史）
- JP real GDP z：1974=-1.37（石油危机）、1992-93=-0.86/-1.02（泡沫破灭）、1970=+1.23（高增长尾）
- CN real GDP z：2007=+3.88（过热极值）、2012=-1.60（放缓）
- JP trade_balance/GDP z：1985-87=+1.17/+1.49/+1.14（广场协议后顺差高峰→日元升值→泡沫链条）、1990=+0.44（回落）
- CN property_price YoY z：2009=+3.18（四万亿刺激房价）；CN equity 2007=+5.76（牛市）
- JP nominal GDE level 因子（CY 十亿日元）：1990=430,040 十亿（史实 ~430 兆日元 ✓）

## 5. 披露
1. full-sample robust z（含未来段）——RETROSPECTIVE_HISTORICAL 定位声明，lookahead 敏感性留 H4 rolling 检验
2. percentile 同 full-sample（辅助诊断，非主）
3. JP 利率 robust z 未做 regime 切分（D-H3-4：raw z 如实产出，零利率 regime dummy 留 H4）
4. CN trade_balance_gdp DEFERRED（FX 因子缺）
5. PRE_TRANSFORM 后文件只存 robustz/pctrank（transformed level 中间值未单存——manifest 记录 transform_id 可重建）

## 6. 产物清单
03_features/
  inputs/jp_nominal_gde_level_cy.csv      （47 行 1955-2000，/GDP 归一因子）
  state/*.csv       68（robustz + pctrank）
  state_proxy/*.csv 2
  state_anchor/*.csv 3
  module/*_robustz_wide.csv 12
  h3_transform_manifest.csv  （40 行：action/transform 全记录）
  h3_deferred.csv    （CN trade FX defer 原因）
