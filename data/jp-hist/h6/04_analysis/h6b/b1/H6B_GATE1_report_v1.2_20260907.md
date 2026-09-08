# H6-B B1 Data Collection & Lineage — GATE1 Report（v1.2，B1.2 metadata/unit closure 后）

日期：2026-09-07
冻结上游：h6b_spec_FROZEN_v1.2.3（f73994f2）+ FREEZE_H6B_B0_20260907.txt
版本沿革：v1.0（待外审）→ 外审 REWORK → v1.1（B1.1 data-correction，CONDITIONAL PASS）→ **v1.2（B1.2 metadata/unit closure，本版）**
B1.1 外审裁定：**CONDITIONAL PASS — CORE DATA ACCEPTED / P0=0 / P1=2 / P2=3；B2 APPROVED TO START；B3 HOLD pending B1.2**
本版修订（对应外审 §19 七项）：credit_flow source_note 删 SAAR、GDP 单位转换明确、coverage QC effective denominator、CN structural-pre-start 从 denominator 排除、FFA obs 机器计数、BOJ legacy sampling-density 标签、manifest/QC 重生成。

## 一、采集完成矩阵（B1.2 后；obs = primary window 内机器计数）

| 变量 | country | 文件 | 覆盖 | 主窗 obs(nominal) | effective | 锚点验证 |
|---|---|---|---|---|---|---|
| corporate_leverage | JP | h6b_q_corporate_leverage.csv | 1954Q2-2026Q1 | 84/84 | 84/84 | 1990Q4 0.803→2005Q4 0.678 去杠杆 ✓ |
| corporate_profitability | JP | h6b_q_corporate_profitability.csv | 1954Q2-2026Q1 | 84/84 | 84/84 | 1985Q4 0.0248/1990Q4 0.0289 ✓ |
| mof_interest_burden | JP | h6b_q_mof_interest_burden.csv | 1954Q2-2026Q1 | 84/84 | 84/84 | 1990Q4 0.957→2005Q4 0.131 零利率 ✓ |
| corporate_land_share | JP | h6b_q_corporate_land_share.csv | 1954Q2-2026Q1 | 84/84 | 84/84 | JP-only 辅助 ✓ |
| i_q_gfcf | JP | h6b_q_i_q_gfcf_jp.csv | 1955Q1-2026Q2 | 84/84 | 84/84 | 1990Q1 0.370 峰值/2026Q2 0.280 ✓（growth-link） |
| housing_starts | JP | h6b_q_housing_starts_jp.csv | 1965Q1-2026Q2 | 84/84 | 84/84 | 2026Q2 186,790 戸（MLIT 锚）✓ |
| boj_ffa_corp_liab | JP | h6b_q_boj_ffa_corp_liab.csv | 1964Q2-2026Q1 | 42/84 | 42/84 | 自然季;SEMIANNUAL_LEGACY(SECONDARY_AUX) |
| credit_flow_jp | JP | h6b_q_credit_flow_jp.csv | 1994Q1-2026Q1 | 48/84 | 48/48(GDP 1994+) | FFA flow/GDP ±6%;NOT SAAR |
| credit_impulse_jp | JP | h6b_q_credit_impulse_jp.csv | 1994Q2-2026Q1 | 47/84 | 47/47(GDP 1994+) | = ΔCF;真 impulse |
| corporate_leverage | CN | h6b_q_corporate_leverage_cn.csv | 2011Q1-2026Q2 | 62/66 | **62/62** | 2021Q4 56.08% ✓（2010=SPRE） |
| corporate_profitability | CN | h6b_q_corporate_profitability_cn.csv | 2011Q1-2026Q2 | 62/66 | **62/62** | 2021Q1 单季 6.64% ✓ |
| property_investment | CN | h6b_q_property_investment_cn.csv | 2000Q1-2026Q2 | 66/66 | 66/66 | 2021 峰值后下滑 ✓ |
| housing_starts | CN | h6b_q_housing_starts_cn.csv | 2000Q1+2001Q1-2026Q2 | 66/66 | 66/66 | 2019 峰值 22.7亿㎡ ✓ |
| property_sales_area | CN | h6b_q_property_sales_area_cn.csv | 2000Q1-2026Q2 | 66/66 | 66/66 | 2021 ~17.9 亿 m2 ✓ |
| property_sales_value | CN | h6b_q_property_sales_value_cn.csv | 2000Q1-2026Q2 | 66/66 | 66/66 | 2021 峰值 ✓ |
| developer_funding | CN | h6b_q_developer_funding_cn.csv | 2000Q1-2026Q2 | 66/66 | 66/66 | 2021 峰值 ✓ |
| cn_pboc_sector_credit | CN | h6b_q_cn_pboc_sector_credit.csv | 2010Q1-2026Q2 | 66/66 | 66/66 | 2010 21→2020 65→2024 109 万亿 ✓ |
| nfc_credit_gdp | JP+CN | h6b_q_nfc_credit_gdp.csv | JP 1964Q4+/CN 2006Q1+ | JP 84/84, CN 64/66 | 同 | JP 1990 139.3% ✓ |
| hh_credit_gdp | JP+CN | h6b_q_hh_credit_gdp.csv | 同上 | JP 84/84, CN 64/66 | 同 | JP 1990 68.4% ✓ |
| residential_property_price | JP+CN | h6b_q_residential_property_price.csv | JP 1955Q1+/CN 2005Q2+ | JP 84/84, CN 65/66 | 同 | JP 1990 180.6→2012 98.8 ✓ |

注：CN BIS credit 64/66、property 65/66 缺尾季为 BIS release 滞后（下一 release 2026-09-14 > cutoff），latest-available 如实记录。CN corporate 2010Q1-Q4 = STRUCTURAL_PRE_START（不计 missing）→ effective 62/62。

## 二、GATE1 五问（B1.2 后；外审 §17 重判一致）

**Q1 Property: YES**（PRICE+ACTIVITY 两国全备;CN SALES 增强;待售面积 aux 不阻断）
**Q2 Profitability: YES**（JP MOF 84/84 + CN 单季 margin 62/62 effective）
**Q3 Balance Sheet: YES**（JP leverage/interest burden + CN leverage 全可用）
**Q4 Credit: YES, WITH AUX METADATA PATCH**（BIS 主 Gate 充足;PBOC proxy 66/66;JP FFA flow/impulse 真公式;SAAR 已改 metadata）
**Q5 Investment: DATA READY**（JP GFCF growth-link + CN investment）

**GATE1 substantive data readiness = PASS**（外审 §17 裁定一致）。

## 三、B1.2 closure 明细（外审 §19）

1. credit_flow_jp source_note：删 "SAAR"，改为 "FRED JPNNGDP official metadata: Billions of Yen, Seasonally Adjusted, Quarterly; NOT SAAR"。
2. 单位转换明确：GDP_億円 = 10 × GDP_billion_yen（十亿→亿），note 已含。
3. coverage QC 增加 nominal_window_req / effective_window_start / effective_window_req / structural_pre_start_excluded / effective_obs / coverage_ratio_effective。
4. CN corporate（leverage/profitability）structural-pre-start 已从 denominator 排除：62/66 nominal → 62/62 effective = 1.0。
5. credit_flow/impulse 机器计数：48/48、47/47 effective（nominal 48/84、47/84 因 GDP 1994 起 availability）——GATE1 v1.2 与 coverage_qc 一致，均机器生成不手填。
6. BOJ legacy FFA：coverage 标 sampling_density=SEMIANNUAL_LEGACY + gate_role=SECONDARY_AUX。
7. manifest（81 raw/23 std/23 lineage）+ coverage_qc + anchor_qc + definition_break_registry 重生成；SHA 复核 0 mismatch。

## 四、B1.2 建议 QC 断言（全过）

credit_flow_gdp_saar_flag=FALSE / credit_flow_unit_conversion_valid=TRUE / structural_pre_start_in_denominator=0 / coverage_report_machine_count_mismatch=0（手动核:file rows=coverage counts）/ aux_sampling_density_declared=TRUE / manifest_sha_failed=0

## 五、缺口与限制（如实）
1. CN 待售面积（inventory_area）aux 未采——NBS esData 无此指标；外审 §16 建议补采但明确"不应因此阻断 B1 Freeze"；MVMD sales/inventory 二选一已满足。
2. JP FFA 系列 1994+（GDP availability）/旧序列 1985-95 半年密度（SEMIANNUAL_LEGACY）——SECONDARY_AUX，BIS credit 主窗已覆盖。
3. BIS CN credit 止 2025Q4 / property 止 2026Q1（release 滞后）。
4. CN 规上工业 2010 = STRUCTURAL_PRE_START。

## 六、产物清单
- b1_source_manifest_full.csv(81) / b1_standardized_manifest_full.csv(23) / b1_lineage_summary.csv(23)
- b1_coverage_qc.csv(effective denominator 版) / b1_anchor_qc.csv(11 锚点 PASS)
- definition_break_registry_B1.1_20260907.md / BIS_vintage_registry_20260907.md
- 20 季度序列 + 2 aux + MOF identity QC
- 审核响应与修订（B1.2）：01_数据采集/外部审核意见/JP-HIST_H6B_B1.1_审核响应与修订_B1.2_20260907.md
- 审核包（单 ZIP）随本报告交付
