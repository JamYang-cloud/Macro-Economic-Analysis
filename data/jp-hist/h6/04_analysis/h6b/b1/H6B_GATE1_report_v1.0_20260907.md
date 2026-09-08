# H6-B B1 Data Collection & Lineage — GATE1 Report（v1.0，待外审）

日期：2026-09-07
冻结上游：h6b_spec_FROZEN_v1.2.3（f73994f2）+ FREEZE_H6B_B0_20260907.txt
任务：B1 Batch 1 可行性核心采集（spec §10）+ source manifest + lineage + definition-break registry
状态：**Batch 1 完成 — GATE1 五问报告**（B2 是否启动由外审裁定）

## 一、采集完成矩阵（20 季度序列 + QC）

| 变量 | country | 文件 | 覆盖 | 主窗 obs | 锚点验证 |
|---|---|---|---|---|---|
| corporate_leverage | JP | h6b_q_corporate_leverage.csv | 1954Q2-2026Q2 | 84/84 | 1990Q4 0.803→2005Q4 0.678 去杠杆 ✓ |
| corporate_profitability | JP | h6b_q_corporate_profitability.csv | 1954Q2-2026Q2 | 84/84 | 1985Q4 0.0248/1990Q4 0.0289 ✓ |
| mof_interest_burden | JP | h6b_q_mof_interest_burden.csv | 1954Q2-2026Q2 | 84/84 | 1990Q4 0.957→2005Q4 0.131 零利率 ✓ |
| corporate_land_share | JP | h6b_q_corporate_land_share.csv | 1954Q2-2026Q2 | 84/84 | JP-only 辅助 ✓ |
| i_q_gfcf | JP | h6b_q_i_q_gfcf_jp.csv | 1955Q1-2024Q1 | 84/84 | 1985 27.5%/1990 31.7% 峰值/2000s 25.9%(与冻结基线一致)✓ |
| housing_starts | JP | h6b_q_housing_starts_jp.csv | 1965Q1-2024Q4 | 84/84 | 1987-90 年 ~167 万戸 峰值 ✓ |
| boj_ffa_corp_liab | JP | h6b_q_boj_ffa_corp_liab.csv | 1965Q1-2026Q2 | 62/84 | stock 拼接 ratio 0.9963 ✓ (旧序列半年点 PARTIAL) |
| credit_impulse | JP | h6b_q_credit_impulse_jp.csv | 1994Q2-2026Q2 | 41/84 | Δstock/GDP ✓ (GDP 1994 起 PARTIAL) |
| corporate_leverage | CN | h6b_q_corporate_leverage_cn.csv | 2011Q1-2026Q2 | 62/66 | 2021Q4 56.08% ✓ (2010 GAP) |
| corporate_profitability | CN | h6b_q_corporate_profitability_cn.csv | 2011Q1-2026Q2 | 62/66 | 2021Q4 6.81% ✓ (2010 GAP) |
| property_investment | CN | h6b_q_property_investment_cn.csv | 2000Q1-2026Q2 | 66/66 | 2021 峰值后下滑 ✓ |
| housing_starts | CN | h6b_q_housing_starts_cn.csv | 2000Q1-2026Q2 | 66/66 | 2021 峰值后下滑 ✓ |
| property_sales_area | CN | h6b_q_property_sales_area_cn.csv | 2000Q1-2026Q2 | 66/66 | 2021 全年 ~17.9 亿 m2 峰值 ✓ |
| property_sales_value | CN | h6b_q_property_sales_value_cn.csv | 2000Q1-2026Q2 | 66/66 | 同上 ✓ |
| developer_funding | CN | h6b_q_developer_funding_cn.csv | 2000Q1-2026Q2 | 66/66 | 同上 ✓ |
| cn_pboc_sector_credit | CN | h6b_q_cn_pboc_sector_credit.csv | 2010Q1-2026Q2 | 66/66 | 2010 21→2020 65→2024 109 万亿 ✓ |
| nfc_credit_gdp | JP+CN | h6b_q_nfc_credit_gdp.csv | JP 1964Q4+/CN 2006Q1+ | JP 84/84, CN 64 | JP 1990 139.3% / CN 2011 110.2% ✓ |
| hh_credit_gdp | JP+CN | h6b_q_hh_credit_gdp.csv | 同上 | JP 84/84, CN 64 | JP 1990 68.4% ✓ |
| residential_property_price | JP+CN | h6b_q_residential_property_price.csv | JP 1955Q1+/CN 2005Q2+ | JP 84/84, CN 65 | JP 1990 峰值 180.6→2012 98.8 ✓ |

## 二、raw lineage 汇总
- 67 raw 文件(b1_source_manifest_full.csv,逐 SHA)
- 复用 H1 FREEZE 层(JP MOF xls×3 + MLIT 地价×2 + ESRI 68SNA×5,SHA 与 H1 manifest 一致,不重复下载)
- 新下载:BIS bulk×2 / BOJ FFA json×14 / e-Stat housing starts json+csv / FRED GFCF+GDP / CN nbs_property json×7 / nbs_corporate json×6 / pboc htm×17+manifest
- lineage 19 行(b1_lineage_summary.csv,std←raw 映射)

## 三、definition breaks 登记(全部如实,无拼接掩盖)
1. JP MOF 1974-84 早期 coverage 过渡段:恒等式 gap 至 1.45%(1985+ 严格 0.0004)——primary 窗不受影响
2. JP GFCF 2000Q4→2001Q1:68SNA(1990基準 NSA)→FRED 93/2008SNA SAAR,断点 0.86pp
3. JP FFA 旧序列(法人企業,更新停止 2017,半年点)拼接新序列(非金融法人企業):stock ratio 0.9963 校准
4. CN 规上工业 2011 口径调整(500万→2000万):2010 GAP;2019 主营业务收入→营业收入更名
5. CN PBOC 栏目名沿革 3 次(2015/2020 重命名):观测值连续无跳变
6. CN NBS 房地产 YTD 累计→单季流量还原(全 5 线)
7. BIS/BOJ 数据发布 vintage 截止 2026-08-31 cutoff 前

## 四、GATE1 五问(冻结 spec 定义:property/profitability/leverage/credit/investment 五通道是否可支撑机制验证)

**Q1 Property 通道同向数据可得?** YES——JP(land_price 年度已有 + housing_starts 季度 + property price 季度)+ CN(开发投资/新开工/销售面积/销售额/到位资金 季度,2010 起全覆)。Property 三 family(PRICE/ACTIVITY/INVENTORY-SALES)中 PRICE+ACTIVITY 两国全备,INVENTORY-SALES 由 sales 满足(MVMD 二选一)。辅助缺口:CN 待售面积(aux,新闻稿 HTML 通道,不进主窗)。
**Q2 Profitability 通道同向数据可得?** YES——JP MOF margin 84/84 + CN 规上工业利润率 62/66(2011+,2010 GAP 如实)。
**Q3 Leverage/Balance-sheet 通道可解释状态?** YES——JP MOF liab/assets 84/84 + interest burden 84/84;CN 规上工业资产负债率 62/66(2011+);BOJ FFA stock 交叉核验(aux,62/84)。
**Q4 BIS Credit 同向数据可得?** YES——BIS nfc/hh credit %GDP JP 84/84 + CN 64;PBOC 企业中长期贷款 66/66 作 demand proxy(2020 疫情后激增可见)。
**Q5 Investment held-out 在 H6-A 后仍稳?** DATA READY——JP i_q_gfcf 84/84(1985 27.5%/1990 31.7% 峰值,与 H6-A investment_gdp 冻结基线年度一致);CN 地产投资+固定投资 66/66(2021 峰值后下滑,方向与 H6-A CN investment 匹配)。held-out 检验属 B3/B4 阶段,本报告只确认数据可支撑。

**GATE1 判定建议:五问全 YES → 建议进 B2(credit refinement)+ B3 机制验证**。外审裁定为准。

## 五、缺口与限制(如实)
1. CN 规上工业 2010Q1-Q4 GAP(库内稀疏,2011 口径调整)——CN primary 窗起点 2010 受影响 1 年,B2/B3 用 2011+ 连续段,2010 段标 GAP 不插值
2. JP FFA 旧序列半年点:credit_impulse 主窗 41/84(GDP 1994 起限制)——B2 phase aux,不进主 Gate;BIS credit 已覆盖
3. CN 待售面积未采(esData 无此指标)——aux,MVMD 二选一已满足
4. JP housing starts 止 2024Q4(2025+ 未入 e-Stat 时系列表)——主窗不受影响
5. JP GFCF 止 2024Q1(FRED 停更)——主窗不受影响

## 六、产物清单
- B1_采集规约_20260907.md / b1_source_manifest_full.csv(67)/ b1_standardized_manifest_full.csv(22)/ b1_lineage_summary.csv(19)
- 20 季度序列 + 2 aux(h6/02_standardized/h6b/)+ MOF identity QC
- 审核包(单 ZIP)随本报告交付
