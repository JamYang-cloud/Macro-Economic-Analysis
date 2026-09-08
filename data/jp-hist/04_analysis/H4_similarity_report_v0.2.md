# JP-HIST H4 Similarity Report v0.2 — JP 2001+ 拼接与假说验证（CN 2013-2025 ↔ JP 1986-1998）
日期：2026-09-06
上游：H4 v0.1（CN A 窗 2000-2012 × JP 1970-2000）+ H1-P1 CN 2013-2025 补采 + JP GDP 2001+ 拼接

## 1. 本版数据变化
1. **CN 2013-2025 补采**（H1-P1）：NBS 统计公报 13 份解析（GDP/CPI/M2/IIP/出口/出生率/社融）+ 腾讯上证 2008-2025 + 世行投资率 bridge + 2020 出生率普查修订 8.52‰
2. **JP GDP 2001+ 拼接**：JP1-lineage FRED 2008SNA（JPNNGDP/JPNRGDPEXP 1994-2026 季度）→ annual YoY 2001-2025；deflator 2001+ = implicit ratio YoY；junction 披露（1995-2000 两 SNA growth 差均值 1.03pp）
3. **方法论修正——JP robust z 全样本重标定（1970-2025）**：v0.1 用 1970-2000 标定使 JP 1990s 状态未显极端；相对 JP 全史（含 2000s 零利率/通缩/停滞）才反映"在 JP 历史中的真实位置"。JP 窗从 2000 扩至 2025 同时解除 CN 2024/2025 匹配的边界截断。

## 2. 结果（JP 1970-2025 全窗，null = 10k bootstrap 随机配对）

### 窗口 lag profile（稳定 L≈21-22）
| CN 窗 | best L | S | null pctile |
|---|---|---|---|
| A 2000-2012 | 19 | 0.375 | —（旧窗） |
| B 2005-2015 | 21 | 0.516 | 0.989 SIG |
| C 2010-2020 | 21 | 0.640 | 1.000 SIG |
| D 2015-2025 | 22 | 0.684 | 1.000 SIG |

### 假说对角线（CN 2013-2025 vs JP 1986-1998）
| lag | 对应 JP 段 | 均 S | null pctile |
|---|---|---|---|
| 22 | JP 1991-2003 | 0.692 | 1.000 SIG |
| 24 | JP 1989-2001 | 0.637 | 1.000 SIG |
| 27 | JP 1986-1998 | 0.541 | 0.998 SIG |

### CN 2013-2025 逐年 best-match JP 年份
{1991, 1992×3, 1993, 1994, 1995, 1998, 2003×2, 2006, 2011×2}
- **8/13 年 → JP 1991-1998**（2013-2016/2018-2020/2022）
- **5/13 年 → JP 2003-2011**（2017/2021/2023/2024/2025）
- best-match 均 S=0.805（null pctile 1.000）

## 3. 结论（修正 v0.1）
1. **假说获显著支持、时点修正**：CN 2013-2025 结构高度相似 JP 泡沫破灭后停滞段（1991-1998，8/13 年）+ 尾部推进至失去的二十年后期（2003-2011，5/13 年）。用户原始假说（1986-1998）方向成立但 CN 实际对应更聚焦 1991+，且 2017 后部分年份已越过 1998 进入 JP 2000s。
2. **稳定 lag 21-22 而非 27**：B/C/D 窗全样本一致。CN 2013-2025 相对 JP 滞后 ~21-22 年（CN 2013≈JP 1991、CN 2025≈JP 2003）。
3. **CN 轨迹推进**：A 窗（2000-2012）best L=19 ↔ JP 1981-1993 → 本版（2013-2025）L≈21-22 ↔ JP 1991-2011。CN 对应 JP 时段随时间后移，但**推进速度慢于 1:1**（CN 25 年 → JP 段约 20-30 年跨度）。
4. **v0.1 的 L≈14-19 平台结论被修正**：那是 JP 1970-2000 截断样本 + CN 2000-2012 标定的人为产物；JP 全史标定后真实平台 21-22。

## 4. 限定与披露（新增）
1. JP 全样本标定（1970-2025）使 JP 状态含 2000s 信息——RETROSPECTIVE 定位已声明，H4 不做 PIT
2. 5/13 年匹配 JP 2000s 的判定基于 JP 2001+ 变量子集（GDP/cpi/policy/m2-2017/利率/工资/失业等；investment 2001+ 无、m2 止 2017）——GROWTH 模块 JP 2001+ 少 investment
3. CN wage 2013-2022 GAP（2023-25 已采）→ DEMOGRAPHY 模块 B/C/D 窗 wage pair 缺失，实际贡献变量有限（birth ΔCBR + wage 2023-25）
4. CN investment 2013-2024（WB bridge，2012 junction ~2pp SNA 修订 break）
5. CN export 2013+ rmb / iip 2013+ 规上工业口径 breaks
6. 模块 coverage gate 从简（≥1 pair/模块，n_mod=4 常达）——严格 50% 门未跑，报告为 exploratory
7. 人口 anchor（working_age/dependency/youth）未入 S_total（C 级）——demography 结论仅基于 birth ΔCBR

## 5. 产物
04_analysis/jp_panel_1970_2025/（21 变量）+ jp_state_1970_2025/（6 module wide）+ cn_state_2000_2025/ + h4_hyp2_c0_jp2025.csv（816 pairings）+ 本报告
02_standardized/h1p1_extension/（CN 8 + JP 3 延伸文件 + GAPS 记录）
01_raw/nbs_gongbao/（13 html）+ cn_extracted/cn_gongbao_2013_2025.csv + tencent_equity/sh000001_daily_2008_2025.csv + cn_investment_share_gdp_wb_2013_2025.csv
