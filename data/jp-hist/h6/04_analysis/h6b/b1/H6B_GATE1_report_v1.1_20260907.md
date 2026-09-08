# H6-B B1 Data Collection & Lineage — GATE1 Report（v1.1，B1.1 patch 后重判）

日期：2026-09-07
冻结上游：h6b_spec_FROZEN_v1.2.3（f73994f2）+ FREEZE_H6B_B0_20260907.txt
版本：v1.0（2026-09-07，待外审）→ 外审 REWORK → **v1.1（B1.1 data-correction & coverage patch 后重判）**
本版修订：MOF/FFA 季度映射修复、cutoff 2026Q2 剔除、credit impulse 真公式、GFCF growth-link、housing starts 补至 2026Q2、CN 单季利润率、2010 structural pre-start、BIS vintage registry、property price schema、housing starts 2000 覆盖与 2019 峰值锚点修正。

## 一、采集完成矩阵（B1.1 patch 后）

| 变量 | country | 文件 | 覆盖 | 主窗 obs | 锚点验证 |
|---|---|---|---|---|---|
| corporate_leverage | JP | h6b_q_corporate_leverage.csv | 1954Q2-2026Q1 | 84/84 | 1990Q4 0.803→2005Q4 0.678 去杠杆 ✓ |
| corporate_profitability | JP | h6b_q_corporate_profitability.csv | 1954Q2-2026Q1 | 84/84 | 1985Q4 0.0248/1990Q4 0.0289 ✓ |
| mof_interest_burden | JP | h6b_q_mof_interest_burden.csv | 1954Q2-2026Q1 | 84/84 | 1990Q4 0.957→2005Q4 0.131 零利率 ✓ |
| corporate_land_share | JP | h6b_q_corporate_land_share.csv | 1954Q2-2026Q1 | 84/84 | JP-only 辅助 ✓ |
| i_q_gfcf | JP | h6b_q_i_q_gfcf_jp.csv | 1955Q1-2026Q2 | 84/84 | 1985 0.325/1990 0.370 峰值/2026Q2 0.280 ✓（growth-link splice） |
| housing_starts | JP | h6b_q_housing_starts_jp.csv | 1965Q1-2026Q2 | 84/84 | 1987-90 年 ~167 万戸 峰值; 2026Q2 186,790 戸(月报锚点)✓ |
| boj_ffa_corp_liab | JP | h6b_q_boj_ffa_corp_liab.csv | 1964Q2-2026Q1 | 42/84* | 自然季度;旧序列 1985-95 半年密度 PARTIAL *（B2 SECONDARY aux） |
| credit_flow_jp | JP | h6b_q_credit_flow_jp.csv | 1994Q1-2026Q1 | 33/84* | FFA flow/GDP,±6% 量级正常 *（GDP 1994 起,aux） |
| credit_impulse_jp | JP | h6b_q_credit_impulse_jp.csv | 1994Q2-2026Q1 | 32/84* | = ΔCF（真 impulse）*（aux） |
| corporate_leverage | CN | h6b_q_corporate_leverage_cn.csv | 2011Q1-2026Q2 | 62/66 | 2021Q4 56.08% ✓（2010=STRUCTURAL_PRE_START） |
| corporate_profitability | CN | h6b_q_corporate_profitability_cn.csv | 2011Q1-2026Q2 | 62/66 | 2021Q1 单季 6.64% ✓（单季流量,非 YTD） |
| property_investment | CN | h6b_q_property_investment_cn.csv | 2000Q1-2026Q2 | 66/66 | 2021 峰值后下滑 ✓ |
| housing_starts | CN | h6b_q_housing_starts_cn.csv | 2000Q1+2001Q1-2026Q2 | 66/66 | **2019 峰值 ~22.7 亿㎡**（2021=19.9 亿㎡ 已回落）✓ 修正 |
| property_sales_area | CN | h6b_q_property_sales_area_cn.csv | 2000Q1-2026Q2 | 66/66 | 2021 全年 ~17.9 亿 m2 峰值 ✓ |
| property_sales_value | CN | h6b_q_property_sales_value_cn.csv | 2000Q1-2026Q2 | 66/66 | 2021 峰值 ✓ |
| developer_funding | CN | h6b_q_developer_funding_cn.csv | 2000Q1-2026Q2 | 66/66 | 2021 峰值 ✓ |
| cn_pboc_sector_credit | CN | h6b_q_cn_pboc_sector_credit.csv | 2010Q1-2026Q2 | 66/66 | 2010 21→2020 65→2024 109 万亿 ✓ |
| nfc_credit_gdp | JP+CN | h6b_q_nfc_credit_gdp.csv | JP 1964Q4+/CN 2006Q1+ | JP 84/84, CN 64 | JP 1990 139.3% / CN 2011 110.2% ✓ |
| hh_credit_gdp | JP+CN | h6b_q_hh_credit_gdp.csv | 同上 | JP 84/84, CN 64 | JP 1990 68.4% ✓ |
| residential_property_price | JP+CN | h6b_q_residential_property_price.csv | JP 1955Q1+/CN 2005Q2+ | JP 84/84, CN 65 | JP 1990 峰值 180.6→2012 98.8 ✓ |

注：*JP FFA 相关（boj_ffa/credit_flow/credit_impulse）为 B2 SECONDARY aux，BIS credit 主窗 84/84 已覆盖主 Gate 需求。主窗 obs 显示为 aux 在该窗可得点数（半年密度/GDP 起点限制），如实标注。

## 二、raw lineage 汇总
- 67 raw 文件（b1_source_manifest_full.csv，逐 SHA）
- 复用 H1 FREEZE 层（JP MOF xls×3 + MLIT 地价×2 + ESRI 68SNA×5，SHA 与 H1 manifest 一致）
- B1.1 新增：ESRI QE 2026Q2 CSV（gaku-mk2621.csv）+ MLIT 月报 publication7{01-06}/8{01-06}.xls ×12
- 新下载：BIS bulk×2 / BOJ FFA json×14 / e-Stat housing starts / FRED GDP / CN nbs_property json×7 / nbs_corporate json×6 / pboc htm×17
- lineage 19 行（b1_lineage_summary.csv）

## 三、definition breaks 登记（definition_break_registry_B1.1_20260907.md，D1-D11）
1. CN 规上工业 2011Q1 STRUCTURAL_PRE_START（门槛 500万→2000万；2010 不计 missing）
2. CN 规上工业 2019 主营业务收入→营业收入更名（月度累计口径不变）
3. CN 规上工业 2011Q1 前稀疏前导点（2001-2006）独立 aux
4. CN housing starts 2000Q2-Q4 缺失登记（2000Q1 + 2001Q1+）
5. JP FFA 1998Q1 旧(法人企業)→新(非金融法人企業)序列 splice
6. JP FFA/GDP 1994Q1 DATA_AVAILABILITY（FRED 名义 GDP 起点）
7. JP GFCF 68SNA→QE growth-link splice（重叠 1994-2000,28 季,factor 0.2027；2000Q4→2001Q1 跳变 0.00026）
8. JP housing starts 2025Q1 源通道切换（e-Stat DB→MLIT 月报）
9. MOF/FFA 2026Q2 CUTOFF_EXCLUSION（2026-09-01/未发布）
10. BIS vintage（见 BIS_vintage_registry_20260907.md）

## 四、GATE1 五问（B1.1 patch 后重判）

**Q1 Property 通道同向数据可得? YES**——JP（housing_starts 季度 84/84 + property price 84/84 + 年度 land_price）+ CN（开发投资/新开工/销售面积/销售额/到位资金 66/66）。PRICE+ACTIVITY 两国全备；INVENTORY-SALES 由 sales 满足（MVMD 二选一）。辅助缺口：CN 待售面积（aux，不进主窗）。
**Q2 Profitability 通道同向数据可得? YES**——JP MOF margin 84/84（自然季度修复后）；CN 规上工业单季利润率 62/66（2011+，单季流量构造）。
**Q3 Leverage/Balance-sheet 通道可解释状态? YES**——JP MOF liab/assets 84/84 + interest burden 84/84；CN 规上工业资产负债率 62/66（2011+，月末存量正确）；BOJ FFA stock 交叉核验 aux。
**Q4 Credit 通道同向数据可得? YES**——BIS nfc/hh credit %GDP JP 84/84 + CN 64；PBOC 企业中长期贷款 66/66 作 demand proxy（2020 疫情后激增可见）；JP credit_impulse 真公式重建（FFA flow/GDP 的差分，1994+ aux）。
**Q5 Investment held-out 在 H6-A 后仍稳? DATA READY**——JP i_q_gfcf 84/84（growth-link splice 消除断点；1985 0.325/1990 0.370 峰值，与 H6-A investment_gdp 冻结基线年度一致）；CN 地产投资 66/66（2021 峰值后下滑）。held-out 检验属 B3/B4。

**GATE1 判定建议（v1.1）：五问全 YES → 建议进 B2（credit refinement）+ B3 机制验证**。外审裁定为准。

## 五、缺口与限制（如实，B1.1 patch 后）
1. CN 规上工业 2010Q1-Q4 = STRUCTURAL_PRE_START（2011 门槛变更，非 GAP；不计 missing）
2. JP FFA 旧序列（1985-95）半年密度；credit flow/impulse 1994+（GDP 起点）——B2 aux，BIS credit 覆盖主 Gate
3. CN 待售面积未采（NBS esData 无此指标；外审建议新闻稿通道）——aux，MVMD sales/inventory 二选一已满足
4. JP housing starts CN 对照窗尾部已补至 2026Q2（MLIT 月报 12 份）
5. BIS CN credit 止 2025Q4 / property 止 2026Q1（BIS release 滞后，下一 release 2026-09-14 > cutoff）

## 六、机器断言（外审 §17 要求，全部通过）
quarter_monotonic_all=TRUE / quarter_parser_shift_detected=0 / observation_after_cutoff_release=0 / future_quarter=0 / credit_impulse_formula_valid=TRUE / level_concat_across_definition_regime=0 / ytd_ratio_used_as_single_quarter=0 / variable_id_missing=0 / coverage_claim_mismatch=0

## 七、产物清单
- B1_采集规约_20260907.md / b1_source_manifest_full.csv(67) / b1_standardized_manifest_full.csv(22) / b1_lineage_summary.csv(19)
- definition_break_registry_B1.1_20260907.md / BIS_vintage_registry_20260907.md
- 20 季度序列 + 2 aux + MOF identity QC（h6/02_standardized/h6b/）
- 审核响应与修订（01_数据采集/外部审核意见/JP-HIST_H6B_B1_GATE1_审核响应与修订_B1.1_20260907.md）
- 审核包（单 ZIP）随本报告交付
