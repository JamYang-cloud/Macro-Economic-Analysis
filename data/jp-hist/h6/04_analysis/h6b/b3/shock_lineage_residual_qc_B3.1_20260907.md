# H6-B B3.1 — Shock-Adjusted Track Lineage & Residual QC

日期：2026-09-07（B3.1 patch）
对应外审：P1-3（shock-adjusted track 缺输入/残差 lineage）

## Global shock 输入（引用 H6-A FROZEN 资产，不复制）

| factor | 文件 | SHA-256 | H6-A 定位 |
|---|---|---|---|
| World GDP growth (annual, WB) | `h6/01_raw/global_shocks/wb_ny_gdp_mktp_kd_zg_world_api.json` | 67a8e393… | H6-A a1 global factor registry 同源 |
| VIX daily → quarterly mean | `h6/01_raw/global_shocks/cboe_vix_history_daily.csv` | 9258a258… | 同 |
| COVID dummy（冻结定义 2020Q1-2022Q4=1，非 oxcgrt 派生） | spec §7 冻结 | — | 构造规则冻结，不依赖 oxcgrt 文件 |

## 季度化规则（spec §7 冻结，逐条执行）

- WB annual growth → quarterly STEP（4 季同值，禁插值平滑）——reporting limitation `GLOBAL_GROWTH_CONTROL_ANNUAL_STEP_QUARTERLY` 已标注
- VIX：日度 close → 季度 mean（1990Q1 起）
- COVID：2020Q1-2022Q4=1
- JP Model A fit domain 1985Q1-2005Q4；Model B 增 VIX，fit 1990Q1+（不缩 robust-z 标定窗）
- CN fit domain 2010Q1-2026Q2
- 残差化输入 = 标准化前值（signed raw），输出 RobustZ(û)；minimum N=20 季否则 INFEASIBLE
- annual slow variables（land/wage/I_ratio）不参与季度 shock 回归

## Residual QC

- 每变量每 model 记录 fit n（residual sample window）——见 track 表 n_grid 列
- OLS 解算：normal equations + Gaussian elimination（engine/h6b_b3_shockadj.py ols_resid）
- 无 look-ahead：fit 域内窗口 = WIN 窗（JP 1985-2005 / CN 2010-2026），COVID dummy 已知区间
- 无 silent fill：残差化仅对 fit 域内有值观测；缺失不填充

## 主链消费说明

三轨一致性已核（Raw/ShockAdj 同向结论不变）：B1 JP 负 CN 正、B2 两国正、B3a 两国负、B4 JP 正 CN 负（FAI 修正后 Raw CI 跨 0 但 ShockAdj 显著负）。

## Engine 引用

- shock 因子构造：`engine/h6b_b3_shockadj.py`
- 全配对残差化+θ：`engine/h6b_b31_shock.py`
