# JP-HIST H2 Standardization 质量门报告 v0.1（2026-09-06）

规格：h2_standardization_spec_20260906.md | 决策：h2_decision_freeze_20260906.md
范围：H2-P0 年度 panel（六模块 core variables），02_standardized/

## 1. 总览
- 标准化文件：38（JP 21 / CN 17）
- manifest：h2_standardized_manifest_v0.1.csv（SHA256/bytes/start-end/source_note 全列）
- 统一格式：year, value, variable, country, unit, source_note（UTF-8-sig）

## 2. JP 侧目标窗覆盖（JP-HIST 核心 = JP 1970-1995）
**19/20 变量完整覆盖 1970-1995**：
GROWTH: real_gdp_yoy(1956-2001)/nominal_gdp_yoy/iip_yoy(1955-2026)/investment_gdp
INFLATION: cpi_yoy(1970-2026)/gdp_deflator_level
MONEY_CREDIT: m2_yoy(1955-2017)/policy_rate(1955-2026)/credit_stock_level(1964-2025)/credit_flow_level(1965-2025)
EXTERNAL: fx_usdjpy_level(1957-2026)/reer_level(1994-2026 宽口径)
PROPERTY: equity_return(日经1949-2026)
DEMOGRAPHY: unemployment(1955-2026)/wage_yoy/tfr(1947-2024)/birth_rate(1899-2024)/youth_dependency/dependency_ratio/working_age_anchor
例外：jgb10y 1986+（10Y 市场成熟晚，registry 预期内）
**JP GDP 2002+ 缺口**：ESRI 68SNA 止 2001Q1；2002+ 需 93SNA/2008SNA 官方连接序列（e-Stat 长期连接表）——不影响核心窗 1970-1995，列入 H2 后期/JP 侧扩展

## 3. CN 侧覆盖（2000-2012 主缺口窗）
覆盖 17 变量：real/nominal_gdp_yoy(2000-2012)/investment_gdp(1978-2012)/cpi_yoy/m2_yoy(1991-2012)/export_yoy/trade_balance(1978-2012)/wage_yoy(2000-2012)/property_price_level(1998-2012)/birth_rate/dependency/youth/working_age(1982-2012)/iip_yoy(OECD 1999-2023)/reer_level(1994-2026)/equity_return(2000-2007)/credit_flow(2002-2012)
**CN 缺口（如实标注）**：policy_rate/cgb10y/corp_leverage/corp_profit(GAP 2000s 未采)；unemployment(结构性 2018+)；tfr(ANCHOR_ONLY)；corp_land_share(STRUCTURAL_NA)
**CN 2013-2025 段**：本批仅 2000-2012（H1-P0 raw 范围）；2013+ 需 JP1 CN lineage/公报拼接——列入 H1-P1/H2 后期

## 4. 质量锚点验证汇总（全部通过）
| 变量 | 锚点 | 结果 |
|---|---|---|
| JP CPI | 1974=+23.1% (石油危机) | ✓ |
| JP TFR | 1970=2.13 / 1989=1.57 (1.57 shock) / 2005=1.26 | ✓ |
| JP policy_rate | 1990-08=6.0% 顶点 / 1995-09=0.5% | ✓ |
| JP real GDP | 1960=+13.1% 高速增长 / 1973=+8.0% | ✓ |
| JP investment | 1970=35.5% 投资高峰 | ✓ |
| JP 老年抚养比 | 1970=10.2% → 2020=48.5% | ✓ |
| JP 日经 return | 1990=-38.7% / 2008=-42.1% | ✓ |
| JP JGB 10Y | 1990=6.62% / 2000=1.65% | ✓ |
| JP 失业率 | 2003=5.24% | ✓ |
| CN M2 | 2009=+27.68% (四万亿) | ✓ |
| CN 社融 flow | 2009=139,104亿 | ✓ |
| CN 出生率 | 2000=14.03‰ | ✓ |
| CN 年龄结构 | 2010 15-64=74.5% | ✓ |

## 5. 已知披露项（进 Gate H2）
1. JP BIS credit_flow 2000 年负值（-32,925）——Q4 存量点差，疑 BIS 口径修正非真实信贷收缩，H3 前核查
2. JP GDP 系列止 2001（68SNA 边界）；investment/deflator 同
3. CN export_yoy 起点 1980（1979 前 shift 无值）
4. CN working_age_growth 起点 1987（1982-86 inter-anchor）
5. equity_return CN 仅 2000-2007（腾讯采集范围）；2013+ 待补
6. policy_rate 用 year-end（规格冻结），其余 rate 用 annual avg
7. 所有 series 为 RETROSPECTIVE_HISTORICAL（非 PIT），direct_model_use=false

## 6. 下一步（H2 后期/Gate H2）
- 比较层变换（robust z/percentile/ΔCBR）→ H3 structural state 层应用
- JP GDP 2002+ 拼接（93SNA/2008SNA 连接序列）
- CN 2013+ 段拼接（JP1 CN lineage retrospective 值）
- corp 系列（JP 解析 + CN 补采后）
- standardized manifest 纳入 08_jp_hist manifest 体系 → Gate H2 审核包（如需）
