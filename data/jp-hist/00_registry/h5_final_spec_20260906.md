# JP-HIST H5-FINAL Independent Mechanism Validation — 规格（预注册）
日期：2026-09-06
状态：**FROZEN**（用户授权启动；执行后禁移动阈值/判据）
依据：外部审核 JP-HIST_H5_外部审核及下一步方向_20260906.md §12-14（Test 1/2/3）、§17（JGAP）、§22（event-time 辅助）、§23（Q Final gate）、§25（H5-FINAL 定义）；响应文档 JP-HIST_H5_审核响应与修订_20260906.md（R1-R7 已采纳）
上游：H5 spec FROZEN（00_registry/h5_mechanism_spec_20260906.md，含 §11 修订记录）；H5 = CONDITIONAL PASS
目的：打破 Q2 circular validation——**用于验证机制的变量不参与该年份的 regime 分类**；若 CPI/investment/REER 中 ≥2 核心通道 held-out 后方向仍复现 → MECHANISM CORRESPONDENCE = SUPPORTED，H5 可正式 Freeze；否则接受「稳定可解释 structural-state geometry（非已验证共同机制）」
不做：补数据 / 改 regime 区间 / 重找 lag / 调整 Q1-Q3 阈值 / 硬年份拼接（event-time 只比路径）

## 1. 冻结 search space / 参数（沿用 H5）
- CN years（held-out 检验组）: 2013-2025（与 Q2 画像同窗）；分类执行 2000-2025 全段（drift 报告 2013-2025）
- JP years 1970-2025；lag 10-45；regime J90=[1991,1998] / J00=[2003,2011] / OTHER=其余（JGAP 见 §5）
- module coverage CR-2026-09（valid/eligible≥50% 且 ≥1 valid）；总 gate ≥4 存活模块
- norm 主 = z1970-2025（JP）/ z2000-2025（CN）；**aux norm = percentile**（Q2-Final「≥1 辅助 normalization 不反转」）
- 变量集（9）：real_gdp_yoy / iip_yoy / investment_gdp / cpi_yoy / m2_yoy / export_yoy / reer / wage_yoy / birth_rate（birth_rate 一律 ΔCBR）

## 2. 通道级 held-out（Test 1，外审 §12；5 通道）
对每个通道定义 drop 集并**只用剩余变量重新分类**（regime-level argmax），再检验被分到 J90/J00 的 CN 年（2013-2025）在**未参与分类的通道变量**上是否呈现 JP J90/J00 方向差异：
| 通道 | drop 集 | held-out 检验变量 |
|---|---|---|
| CH-CPI | {cpi_yoy}（INFLATION 死） | cpi_yoy |
| CH-M2 | {m2_yoy}（MONEY_CREDIT 死） | m2_yoy |
| CH-INV | {investment_gdp} | investment_gdp |
| CH-REER | {reer} | reer |
| CH-DEMO | {wage_yoy, birth_rate}（DEMOGRAPHY 死） | wage_yoy、birth_rate 各一 |

## 3. 变量级 LOVO（Test 2，外审 §13；9 变量逐个 drop）
drop {v} 后重分类 + v 的 held-out 方向检验（同 §2 流程）。作用：排除模块内其他变量间接携带同一信息。

## 4. Mechanism Direction Score + 不确定性（Test 3，外审 §14）
对每个 held-out 检验（drop 集 d、变量 v）：
- D_v^JP = mean(z_v | JP J90 年) − mean(z_v | JP J00 年)（JP 侧参考方向，固定）
- D_v^{CN,−v} = mean(z_v | CN→J90 年, 分类不含 v) − mean(z_v | CN→J00 年, 分类不含 v)
- 判定方向一致 ⇔ sign(D_v^JP) == sign(D_v^{CN,−v}) 且 D_v^{CN,−v}≠0
- 报告：effect size（|D| 与 JP 侧 |D^JP| 之比）、**permutation p**（2000 reps，随机打乱 CN 年组标签，双侧 |D| 统计量）、**bootstrap 90% CI**（组内重抽 1000，percentile）
- 组约束：J90/J00 任一组 <3 年 → 检验不可行（infeasible，如实报；记录原因——若系该 drop 使 J00 组消失，即 held-out 变量是 J00 归属的铰链证据）
- 显著性口径（n 小，描述性声明）：p<0.10 记 *、p<0.05 记 **；p 不达标但同号记「同号未达显著」——Q2-Final 判据以**方向一致 + aux/permutation 不反转**为准，非单独 p 门槛

## 5. JGAP（1999-2002）四态 diagnostic sensitivity（外审 §17）
- 冻结 J90/J00 边界与 Q3 判定不变；另跑四态分类 J90/JGAP(1999-2002)/J00/OTHER（full 变量集）
- 用途：判断 2024（基线 rep=JP 2002）是「脱离 J00」还是「绕 J90→J00 过渡带摆动」；2015（rep=1999）同步检查
- 输出：四态序列 + 与三态分类差异表；解释口径变更登记，不改变 frozen Q3

## 6. Event-time 辅助（外审 §22；held-out 之后）
只比机制变量路径形状/持续时间/深度，禁硬年份拼接：
- Price：JP CPI yoy deflation-onset 路径（t0=1998 附近，视序列）vs CN disinflation 路径（t0≈2023 近零）；路径表 ±8y
- Investment：JP investment_gdp 泡沫后下行段 vs CN 投资率放缓段（斜率高估以同窗年数截断，注明 CN 未来截断）
- Asset：仅 JP 侧可完整（land/equity 泡沫破灭路径）；CN 房价段不完整（2013-25 GAP）→ 注明数据限制，不做硬比较
- 输出定位：辅助叙事支持（HYP-H5-M1 语境），不进主判定

## 7. Q Final gate（外审 §23，判据冻结）
- **Q1 Final**：是否存在 classification hinge？= YES（CPI/INFLATION，H5 v02 已定）→ 可冻结
- **Q2 Final**：核心通道 {CPI, INVESTMENT, REER} 中 **≥2 个** held-out 后仍方向一致（sign 匹配），且 ≥1 辅助（percentile norm 分类 / bootstrap / permutation）不反转 → **MECHANISM CORRESPONDENCE = SUPPORTED**；否则 **INTERPRETABLE FEATURE GEOMETRY ONLY**
  - held-out 不可行（无 J00 组）的通道计 not-supported；以可行且方向一致的通道数判定
  - 附加报告：非核心通道（M2/wage/birth/export/iip/real_gdp）held-out 结果作 evidence table，不进 gate
- **Q3 Final**：NO PERSISTENT J00 TRANSITION（H5 v02 已 PASS）→ 可冻结；JGAP 只改解释不改判定

## 8. 产物与纪律
- 04_analysis/h5_final/：h5final_classification_{drop}.csv / h5final_direction_scores.csv / h5final_jgap_sequence.csv / h5final_eventtime_paths.csv / H5_FINAL_validation_report.md（自动生成，数字从 CSV）+ engine 快照 h5_final_*.py
- 每 CSV 带 method_id（H5F-T1-CH-* / H5F-T2-LOVO-* / H5F-T3-DSC / H5F-JGAP / H5F-EVT）/ norm / metric / status
- 引擎复用 h4v03d_engine.py（state 缓存）；分类重算须与 H5 v02 baseline 对齐校验（drop=∅ 时 13/13）
- 三问 Final 判定表 + 表述边界（Q2-Final 结果只两档：SUPPORTED / GEOMETRY ONLY）
- 审核包 v03 送审（若 Q2-Final SUPPORTED → H5 Freeze 前置）
