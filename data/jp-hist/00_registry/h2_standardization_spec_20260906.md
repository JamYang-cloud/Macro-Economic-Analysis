# JP-HIST H2 Standardization 规格冻结（2026-09-06）

依据：方法论稿 v1.0 §25-30 + v1.1 定稿 + FREEZE_H1 + h2_decision_freeze_20260906.md
状态：H2 已获用户授权推进（"请按照你的建议推进"→ A: H2 Standardization）；本文件冻结标准化规格，为 H2 主体执行的开工基线

## 1. 产出目标
02_standardized/ 双 panel：
- annual_1960_2025（JP 起点 1960 warm-up / 1970 正式；CN 起点按 actual_start）
- quarterly_1970Q1_2025Q4（月度/季度变量聚合）
每 panel：country × variable × date × value(standardized) × 源序列标注

## 2. 变量→输入资产清单（H2.1 盘点结果）
### JP 侧输入（11 lineage FRED + CPI + H1 采集）
| variable | 输入文件 | 频率 | 状态 |
|---|---|---|---|
| real_gdp_yoy | esri_gdp_68sna/gaku_jg01168.csv（68SNA 实质量，1955Q1-2001Q1）| Q | RAW需解析(多级表头) |
| nominal_gdp_yoy | esri_gdp_68sna/gaku_mg01168_1.csv（名目量）| Q | RAW需解析 |
| gdp_deflator | esri_gdp_68sna/def_fy01168.csv（年度デフレーター）| FY | RAW需解析 |
| investment_gdp | ESRI（資本形成率构造，从 gaku_* 相关列）| Q/Y | RAW需解析 |
| iip_yoy | fred/JPNPRINTO01GPSAM.csv（1955-2026 月度）| M | TIDY ready |
| corp_profit_yoy | mof_corp_stat/income.xls（ordinary profit）| Q | xls 需解析 |
| cpi_yoy | stat/cpi_2025base/cpi_2025base_core_extracted.csv（1970+ 月度）| M | TIDY ready |
| m2_yoy | fred/MYAGM2JPM189S.csv（1955-2017）| M | TIDY ready |
| policy_rate | boj_discount/cdab0040/50/100/101.csv（事件日）| Event | 需事件→月末聚合 |
| jgb10y | mof_jgb/jgbcm_all.csv（1974+ 日度）| D | 需日→月末聚合 |
| corp_leverage | mof_corp_stat/assets+liabilities.xls | Q | xls 需解析 |
| credit_flow_gdp | fred/CRDQJPAPUBIS.csv（存量差分）| Q | TIDY→差分 |
| export_yoy | customs_trade/trade_annual_1950_2024（年度）| Y | TIDY ready |
| trade_balance_gdp | customs_trade（+GDP）| Y | TIDY ready |
| fx_usdjpy | fred/DEXJPUS.csv(日)/CCUSMA02JPM618N.csv(月均) | M/D | TIDY ready |
| reer | fred/RBJPBIS.csv（宽，1994+）| M | TIDY ready |
| land_price_yoy | mlit_land/land_price_annual_national_residential_mlit_1975_2026.csv | Y | TIDY ready |
| nikkei_return | fred/NIKKEI225.csv（1949+ 日）| D | TIDY→月收益 |
| working_age_growth | ipss_population/*.csv（27 obs 锚点）| Y anchor | TIDY ready |
| unemployment | fred/LRUNTTTTJPM156S.csv | M | TIDY ready |
| wage_yoy | fred/LCEAMN01JPM661N.csv | M | TIDY ready |
| dependency_ratio | ipss（派生）| Y anchor | derived |
| youth_dependency | ipss（派生）| Y anchor | derived |
| tfr | mhlw_vital（1947+ 年度）| Y | TIDY ready |
| birth_rate | mhlw_vital（1899+ 年度）| Y | TIDY ready |
| corp_land_share | mof_corp_stat/assets.xls sheet13/sheet22 | Q | JP_EXPLANATORY |

### CN 侧输入（13 extracted tidy + lineage + gongbao）
| variable | 输入文件 | 频率 | 状态 |
|---|---|---|---|
| real_gdp_yoy | cn_extracted/cn_gdp_real_yoy_2000_2012 | Y | TIDY（2013-2025 待 H1-P1）|
| nominal_gdp_yoy | cn_extracted/cn_gdp_nominal_2000_2012 | Y | TIDY |
| investment_gdp | cn_extracted/cn_expenditure_gdp（资本形成率 1978-2012）| Y | TIDY |
| iip_yoy | fred_bis_reer/CHNPRINTO01IXPYM | M | TIDY（OECD bridge）|
| cpi_yoy | cn_extracted/cn_price_indices（1978-2012）| Y | TIDY |
| gdp_deflator | cn_gdp_nominal/real 派生 | Y | derived |
| m2_yoy | cn_extracted/cn_m2_m1_growth（1991-2012）| Y | TIDY |
| policy_rate | CN_GAP（2000s 需 H1-P1）| - | GAP |
| cgb10y | GAP（中债受限）| - | GAP |
| corp_leverage | GAP（COMPARABILITY 2000s 待采）| - | GAP |
| credit_flow_gdp | cn_extracted/cn_social_financing（2002-2012 flow）| Y | TIDY（D01 B）|
| export_yoy | cn_extracted/cn_trade（1978-2012）| Y | TIDY |
| trade_balance_gdp | cn_extracted/cn_trade | Y | TIDY |
| fx_usdcny | CN 项目 lineage | - | LINEAGE |
| reer | fred_bis_reer/RBCNBIS（1994+）| M | TIDY |
| property_price_yoy | cn_extracted/cn_house_price（1998-2012）| Y | TIDY |
| equity_return | tencent_equity/sse_composite（2000-2007 日）| D | TIDY→月收益 |
| working_age_growth | cn_extracted/cn_age_structure（1982-2012）| Y | TIDY（15-64）|
| unemployment | GAP_STRUCTURAL（2018+）| - | GAP |
| wage_yoy | cn_extracted/cn_urban_wage（2000-2012）| Y | TIDY |
| dependency_ratio | cn_age_structure | Y | TIDY |
| corp_land_share | STRUCTURAL_NA | - | N/A |
| tfr | ANCHOR_ONLY（普查锚点）| - | ANCHOR |
| birth_rate | cn_extracted/cn_birth_death（1978-2012）| Y | TIDY |
| youth_dependency | cn_age_structure | Y | TIDY |

## 3. 标准化规格（冻结）
1. **频率**：年度 panel 为主（H4 fixed-lag 用）；季度 panel 仅 JP 侧支持变量（68SNA GDP/MOF 企业 1954+）
2. **rate 聚合**（月度/日度→年度）：level-type（利率/汇率/失业）用 year-end 或 annual avg——冻结为 **annual average**（除 policy_rate 用 year-end 反映年末状态）；asset price 用 **calendar year return**
3. **growth 口径**：冻结 **annual average YoY**（月度序列先算 YoY 再年均）；跨 definition regime 各 regime 内算 growth 后 concat（禁 level concat）
4. **CN 断点**：2000-2012（2013 版年鉴）与 2013+（JP1 lineage/公报）拼接——不同源但同口径变量（GDP/CPI/M2）用 growth concat；2013+ 缺失的变量如实标 GAP 至 H1-P1
5. **标准化数值变换**（比较层）：within-country robust z（Median+1.4826×MAD）或 percentile——H3 structural state 层应用，H2 只产出 clean series + growth
6. **15-64 canonical**（人口）：JP/CN working_age/youth_dependency/dependency_ratio 统一 15-64
7. **CBR 变换**：ΔCBR_t（per-mille points）——FERTILITY 通道
8. **质量门**：每个 standardized 变量与 raw 交叉验证（抽查 3-5 年数值）+ 断点标注 + coverage 报告

## 4. 执行顺序（H2 主体，预计新会话分步执行）
H2.3 JP tidy 提取（ESRI/BOJ/MOF 解析器 → tidy CSV）→ H2.4 JP standardized 年度 panel → H2.5 CN standardized（含拼接）→ H2.6 credit_flow_gdp → H2.7 manifest+质量门

## 5. 冻结补充（2026-09-06，H2 FREEZE 时追加）
coverage_ratio 舍入规则（P1-3）：`coverage_ratio = round(n_valid_in_window / n_expected, 3)`——三位小数展示；精确分数 n_valid/n_expected 与展示值的差异仅为舍入，非计算偏差。

semantic_status 语义约束（H3 强制消费，见 FREEZE_H2_20260906.txt W03-W06）：
- EXACT：与 registry 概念同语义同形态，可入 exact-comparison
- PRE_TRANSFORM：形态差一级变换（level→YoY、level→/GDP），H3 须先执行 required_h3_transform
- PROXY_FLOW / PROXY_STOCK：D01 scheme B 双轨（CN flow / JP stock），不得同入一 feature
- ANCHOR：普查锚点稀疏，禁插值后静默入主模型
- NOT_MAPPED：保持 NA/GAP，禁自动填充
