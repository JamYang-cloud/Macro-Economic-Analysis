# JP-HIST H2 Standardization 质量门报告 v0.2（2026-09-06）

修订：v0.1 → v0.2（外部审核 REWORK：coverage gate NA-validity 修复 + semantic_status 落地 + 计数程序化）
覆盖统计由 h2_coverage_map_v0.2.csv 程序生成（本文件摘要；明细以 CSV 为准，防 Markdown 分叉）

## 1. Standardized 资产
- 41 文件（JP 24 / CN 17），统一 schema：year,value,variable,country,unit,source_note
- manifest：h2_standardized_manifest_v0.1.csv（41/41 SHA+bytes+n_rows+start/end 对齐，year 升序唯一）
- anchor tests：h2_anchor_tests_v0.1.csv 20/20 PASS（actual 为 3 位小数展示值，判定以 tolerance 计）

## 2. Coverage 统计（coverage_map v0.2，value-validity gate）
- JP 核心窗 1970-1995：FULL_WINDOW 16 / PARTIAL_WINDOW 4 / ANCHOR_COVERAGE 3 / NOT_MAPPED 3
- CN 主窗 2000-2012：FULL_WINDOW 13 / PARTIAL_WINDOW 4 / NOT_MAPPED 9
- 判定规则：valid = year row 存在 AND value 非 NA；ratio = n_valid_in_window / n_expected
- ANCHOR_COVERAGE（普查锚点，非年度连续）：JP working_age_growth / dependency_ratio / youth_dependency（各 6/26 窗内观测）

## 3. 已知 PARTIAL 原因（非缺陷，数据可得性）
- JP cpi_yoy：1970 NA（shift 首年，1971+ valid）→ 25/26
- JP jgb10y：1986+（10Y 市场成熟晚）
- JP reer：1994+（RBJPBIS 起点）
- JP land_price：1975+（MLIT 公示地価起点；1970-74 用 JREI cross-check 备选）
- CN nominal/real GDP、wage：2000 NA（shift 首年）→ 12/13
- CN equity_return：2000-2007（腾讯采集窗）→ 7/13
- CN iip：OECD 1999-2023 bridge（2023-11 停更）

## 4. Semantic 标注（coverage_map v0.2 semantic_status）
- EXACT 31：registry 概念与 std artifact 同语义同形态
- PRE_TRANSFORM 4：gdp_deflator_yoy→level / trade_balance_gdp→level ×2 / property_price_yoy→level（H3 需 transform）
- PROXY_FLOW 1：cn credit_gdp→credit_flow_level（D01 scheme B，flow 概念）
- PROXY_STOCK 1：jp credit_gdp→credit_stock_level（D01 note）
- ANCHOR 3：JP 人口稀疏系列（普查锚点，H3 不得当年度连续用）
- NOT_MAPPED 行语义留空（无 std artifact）：corp×3 JP、policy_rate/cgb10y/corp×2/unemployment/deflator/tfr/fx CN

## 5. 披露项（承 v0.1 + 新增）
1. JP ESRI 68SNA 段止 2000；2001+ GDP 需 93SNA/2008SNA 连接（H2 后期）
2. JP BIS credit_flow 2000 负值（Q4 存量点差疑口径修正）— H3 前核查
3. RETROSPECTIVE_HISTORICAL 非 PIT；direct_model_use=false
4. 禁 level concat（68SNA 独立 regime；各 regime 内 growth）
5. 比较层变换（robust z/percentile/ΔCBR）属 H3，本层不含
6. policy_rate=year-end（无事件年沿用前值=利率制度事实）；其余 rate=annual avg
7. anchor_tests actual 为 3 位小数展示（display_precision=3），非原始全精度
8. CN 2013+ 段（公报/JP1 CN lineage）与 JP 2001+ 段拼接列 H1-P1/H2 后期

## 6. Gate 状态
H2 Standardization v0.2 修复完成 → 建议 H2 = STANDARDIZATION FREEZE（待 targeted re-audit）
下一阶段：H3 Feature Engineering（structural state 变换：robust z/percentile/ΔCBR + module state 构造）
