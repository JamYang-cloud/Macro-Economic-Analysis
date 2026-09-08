# H6-B B3 Formal Mechanism Validation — 结果报告（v1.0 机器版）

日期：2026-09-07
上游：FREEZE_H6B_B1_20260907.txt + h6b_spec_FROZEN_v1.2.3.md（§5/§7/§8/§12）+ B1 数据 FREEZE
状态：**B3 机器判定完成（Raw/FirstDiff/ShockAdj-A/B 四轨）——待外审**

## 一、方法与冻结基线

- θ_XY = (1/5)Σ_{k=0..4}ρ_S(X_t^d, Y_{t+k}^d)，Spearman window-average（§5）
- 变换：sign_multiplier × raw → robust-z（within-country full-sample）（§6）
- MBB：L=3 n=2000 non-circular time-index joint-pair，90%CI；L=2/4 aux（§12）
- 窗口：JP 1985Q1-2005Q4 / CN 2010Q1-2026Q2（B1 数据覆盖 84/84、62-66 季）
- 三轨：Raw / FirstDiff / ShockAdjusted（Model A=[1,WB growth,COVID]；B 增 VIX 1990Q1+）（§7）
- 主窗 obs 缺口：JP credit_impulse 1994+（GDP availability，B3b 47/84）；CN corporate 2011+（structural pre-start 62/62 eff）

## 二、主链 Gate 判定（四轨汇总，b3_verdict_summary.csv）

| Gate | 链 | Raw | FirstDiff | ShockAdj-A | ShockAdj-B | 一致性 |
|---|---|---|---|---|---|---|
| B1 | P→B | FAIL | FAIL | FAIL | FAIL | 一致 FAIL |
| B2 | B→R | PASS | FAIL | PASS | PASS | 3/4 PASS |
| B3a | R→C | SAME(负) | SAME(负) | SAME(负) | SAME(负) | 一致 SAME |
| B4 | C→I | FAIL | FAIL_CI | FAIL | FAIL | 一致 FAIL |
| **Verdict** | | **PARTIAL** | **GEOMETRY** | **PARTIAL** | **PARTIAL** | 主轨 PARTIAL |

**B3b demand 腿（R→C 区分供需）**：
- JP：stance_by_change 支持；stance_by_level 不支持（1994-2005 利率 0.5% 平台期，41/47 季宽松，区分度限制）
- CN：两口径均支持（宽松期 PBOC 企业中长期贷款 YoY 中位变化 -0.42 < 全窗 -0.21）
- 结论名称冻结 = CREDIT_DEMAND_PROXY_EVIDENCE（demand-consistent credit behavior；禁 IDENTIFIED_CREDIT_DEMAND）

## 三、核心发现（机器表读数，narrative 附于 machine 后）

1. **B1（Property→BS）两国系统性反向**：JP 主窗 P 恶化与 B 恶化负相关（PRICE -0.37/ACTIVITY -0.57，CI 显著负），CN 正相关（+0.49/+0.41/+0.62）。JP 泡沫-破灭期：价格/活动上升期企业加杠杆、破灭后价格与杠杆同降——与"P 恶化⇒B 恶化"传导假设**反向**。
2. **B2（BS→Profitability）方向一致且 CN 显著**：JP +0.18（CI 跨 0 不显著）、CN +0.38（CI +0.26,+0.49 显著）。ShockAdj 后 JP 增强（Model B +0.43 显著）。
3. **B3a（Profitability→Credit）两国同向显著为负**：JP -0.49、CN -0.27（nfc）；盈利恶化伴随信贷/GDP 恶化序列同向下降→即盈利恶化期信贷/GDP 上升（deterioration 后负相关 = 原始序列盈利↓信贷/GDP↑）。JP 1990s 僵尸借贷/信贷惯性、CN 政策逆周期信贷——interpretation 须谨慎（observed equilibrium quantity）。
4. **B4（Credit→Investment）两国反向**：JP +0.69 显著（信贷恶化→投资恶化同向）、CN -0.42/-0.56 显著负（信贷收缩伴随投资 YoY 回升——CN 政策驱动信贷周期与投资周期错位）。ShockAdj 后 CN 负相关增强。
5. **Verdict：PARTIAL MECHANISM CORRESPONDENCE（主轨 Raw/ShockAdj）**——B2 与 B3a 方向一致且部分显著，但 B1（P→B）与 B4（C→I）两国方向相反，不支持统一机制链。FirstDiff 轨弱化至 GEOMETRY（差分消除持续性后仅 B3a 同向）。

## 四、D 模块（Deflation Gate，独立不进主 Verdict）

- JP（4 类可得 CPI/Core/Deflator/PPI）：D-A CPI<0 31 季；D-B（≥3 类 <1.0%）40/44 季（1995Q1-2005Q4 deflator 可得段）；D-C 最长连续 31 季。1985-1994 deflator 类别缺口（无季度 deflator），如实记录。
- CN（2 类 CPI/PPI）：D-B INFEASIBLE（可用类别 <4，冻结出口）。

## 五、缺口与限制（如实）

1. JP credit_impulse/GDP 1994+（FRED GDP 起点）→ B3b JP 窗 47 季（1994-2005），stance_by_level 区分度弱。
2. JP GDP deflator 季度 1995+（1985-1994 无季度 deflator）；D 模块 JP 早期段类别不足。
3. CN D 模块 INFEASIBLE（仅 CPI/PPI 2 类）。
4. CN B4 用 FAI 累计 YoY 代理（水平值不可得），与 JP GFCF/GDP 口径不同——两国各自内部 robust-z 后方向可比，但量级不可比。
5. B3a 负相关的 supply/demand 解读边界：observed equilibrium quantity，禁 identified demand（冻结）。

## 六、产物清单（b3/ 目录）

- b3_verdict_summary.csv（四轨 Verdict 机器表）
- b3_raw_track_theta_mbb.csv / b3_firstdiff_track_theta_mbb.csv / b3_shockadj_track_theta_mbb.csv / b3_machine_gates_alltracks.csv（三轨 θ+MBB 全表）
- B3_执行规约_v0.1 / B3_补采规约（文档）
- D 模块：h6b_d_cpi_headline_{jp,cn} / cpi_core_jp / ppi_{jp,cn} / gdp_deflator_jp
- 补采：h6b_q_jp_policy_rate_stance / h6b_q_cn_policy_rate_stance / h6b_q_cn_fai_yoy_q / h6b_q_cn_pboc_sector_credit_yoy
- 审核包（单 ZIP）待构建

## 七、待外审确认点

1. PARTIAL verdict（主轨）是否接受？B1/B4 两国反向是真实发现 vs 数据/口径 artifact？
2. B3b JP stance_by_level 平台期限制的处理是否可辩护？
3. CN B4 用 FAI YoY 代理（口径异于 JP GFCF/GDP）是否可接受作方向检验？
4. D 模块 CN INFEASIBLE（2 类）+ JP 早期段类别缺口是否接受？
