# JP-HIST H4 Similarity Analysis v0.1 — 结果报告
日期：2026-09-06
方法冻结：h4_similarity_spec（D-H4-1~5 用户拍板）
数据：H3 冻结六模块 robust z（JP 1970-1995 / CN 2000-2012，full-sample within-country）
配对：cn_jp_concept_crosswalk（A/B 级入 S_total，C 级 descriptive，NA 单边缺口由 coverage gate 处理）

## 1. 核心发现：结构相似 lag 平台 ≈ 14-20 年（峰值 L=19），显著非随机

C0 Fixed-Lag（S_total = module-equal-weight mean of S_m，coverage 总≥70%/模块≥50%）：
- 最佳区间 **L=13-19，S=0.53-0.57**，峰值 L=19（S=0.570）
- L=28-32 深谷（S=0.11-0.18）；L=39-40 次级峰（S≈0.32）
- **方法论预设 30-40 年滞后未获支持**——CN 2000-2012 相似的是 JP 1981-1993，不是 1970s

Null Benchmark（bootstrap 10k + block-perm 1k）：
- null mean S=0.346，p95=0.475；L=19 observed=0.570 → **null percentile 1.000**
- **L=13-23 全部显著**（pctile 0.95-1.00）；**L=28-37 显著低于 null**（suppressed，pctile 0.01-0.08）
- 深谷存在 = 排除"时间序列平滑所以处处相似"的假象——短 lag 对齐是真实结构信号

## 2. 模块级（差异巨大，各有 lag 偏好）
| 模块 | best L | S | 解读 |
|---|---|---|---|
| MONEY_CREDIT | 20 | 0.714 | 信贷/M2 结构高度相似且 lag 清晰 |
| INFLATION | 14 | 0.666 | CPI 轨迹对齐（70s 石油危机 vs CN 2010s 通胀错位） |
| DEMOGRAPHY_LABOR | 10 | 0.769 | 人口结构（JP 更早老龄化 vs CN 尚年轻——C 级 anchor 不参与） |
| EXTERNAL | 23 | 0.664 | 出口/REER |
| GROWTH | 38 | 0.511 | 增长模块弱、lag 长——**增长结构是异类** |
| PROPERTY_ASSET | NA | — | crosswalk 无 A/B 对（nikkei↔上证不同股指、land↔住宅价不同概念） |

## 3. Rolling（C1）：2000-2008 稳定 resolve L=14-20；2009 偏离；2010-12 回 19-21
- 2003/2004/2007 UNRESOLVED（双峰，dS<0.02 → lag 不确定区间）
- **2009 深谷**（S=0.418 全场最低）：四万亿刺激使 CN 结构暂时偏离 JP 轨迹
- 2010-12 回到 L≈19-21 → 结构相似在刺激退坡后恢复

## 4. Event-Time（C2）：CN 事件最像 JP 泡沫段事件，不像石油危机
事件同步邻域（t=-3..+4，mean|dz|，越低越像）：
- CN 2007 股市顶 → **JP 1985 Plaza**（0.893，null SIG p=0.035）
- CN 2008 危机/四万亿 → **JP 1990 CreditTight**（0.872，null SIG p<0.001）
- CN 2009 刺激次波 → **JP 1991 BubbleBurst**（0.897，null SIG p<0.001）
- JP 1973 OilShock1 全事件最差（1.9-2.1，INFLATION |dz| 4.6-4.8）→ **排除石油危机类比**（CN 高增长期非通胀冲击型结构）
- 事件链 lag：2007→1985 / 2008→1990 / 2009→1991 均 L=22，与 C0 平台相邻

## 5. 综合解读（初步，待 H1-P1 扩展窗验证）
CN 2000-2012 与 JP 1981-1993（L≈19）结构最相似——即 CN 处于 JP"广场协议后 reflation → 泡沫生成"的前期/中期：
- 信贷扩张 + 通胀温和 + 人口红利仍存 + 出口顺差 + 资产价格上行
- 若轨迹延续，CN 2013-2025 或对应 JP 1986-1998（泡沫加速→破灭）——**此为可检验假说，需 B/C/D 窗（H1-P1 CN 2013-2025）验证**，当前不得外推为结论

## 6. 限定与披露
1. CN 仅 A 窗（2000-2012，13 年）——rolling/event 窗窄，B/C/D 窗需 H1-P1
2. CN equity 止 2007（PROPERTY 模块 CN 侧仅 property_price 2000-2012，JP 侧 land 1975+/nikkei——模块配对后整体 NA）
3. CN trade/GDP deferred（FX）→ EXTERNAL 缺 trade 变量
4. full-sample robust z 含未来段（RETROSPECTIVE 定位）；null 用 block-perm 缓解，未做 PIT 声明
5. GROWTH 模块 L=38 弱峰与主平台冲突——增长结构异质性需分解（投资率 1970s JP vs 2000s CN 制度差异）
6. 六模块 equal weight 是第一版；模块级差异提示后续可做敏感性子样本（去 GROWTH/仅 MONEY_CREDIT+INFLATION）

## 7. 产物（04_analysis/）
h4_c0_fixed_lag_results.csv（465 pairings 原始 S）/ h4_c0_lag_scores.csv / h4_c0b_rolling_preview.csv / h4_null_lag_significance.csv / h4_c1_rolling_lag.csv / h4_c2_event_time.csv / h4_c2_event_null.csv
