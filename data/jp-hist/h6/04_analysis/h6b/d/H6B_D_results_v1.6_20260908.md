# H6-B D 模块（独立通胀机制 Deflation Gate）— 结果报告 v1.6（2016-2018 services 完整并入,CN 4 类主窗 42 季终判）

日期：2026-09-08
版本：v1.0→…→v1.5→ **v1.6（外审 2016-2018 完整补采并入,CN 主窗扩至 2016Q1-2026Q2 n=42；D-D 文本动态化）**
上游：D0_spec_FROZEN_v0.1（sha 79845895…,immutable 零修改）+ h6b_spec_FROZEN_v1.2.3 §9 + FREEZE_H6B_B3
引擎：engine/h6b_d_engine_v16.py（sha 1c3242de…）+ d_run_record_v1.6.json

## v1.6 变更（仅输入并入 + 状态输出动态化;D0 spec/判据/阈值/窗口规则零变更）
1. **CN Services CPI 2016-2018 完整并入**（外审补采 36/36 月,canonical v1.6,sha f5c9eabd…,127 行）:
   - S6 逐月 URL + grade(A 官方直链 / A-mirror 国家级转载)入册;与主会话已核验 9 月重叠 **9/9 值 MATCH**;月度→季度独立复算 **12/12 与外部季度文件一致**;NBS 直链抽查(2016-05/2017-09/2018-12,主会话先前扫漏月份)**3/3 页面级验证存在+值匹配**
   - canonical 全窗 **2016-01..2026-06 126/126 月覆盖,0 缺失,0 冲突**;季度文件(sha f7d2cf01…)42 完整季,连续 2016Q1-2026Q2
2. **availability 语义精确化**:services series_collection_status 机械化 = `COLLECTED_2016Q1+ (structural pre-start before 2016-Q1)`——2016 起 NBS 月度稿"服务"行稳定可得且已全采;2016 前为结构性起点(非采集缺口)
3. **D-D 文本动态化(响应外审 P2)**:joint_conclusion 机械读取主窗 + 主窗前 ≥4 类段,不再硬编码年份文本

## 一、机器判定（D_gate_machine_v1.6.csv + D_gate_quarter_detail_v1.6.csv）

### JP（不变,v1.2-v1.6 逐字节一致）
| Gate | 结果 |
|---|---|
| D-A | CPI<0 = 31/84 季;最长连续 20 季(1999Q4 起) |
| D-B | 40/44 季 ≥3/4 类 <1.0% → **BROAD**(1995Q1-2005Q4,share 0.9091) |
| D-C | 最长 31 季(1998Q2 起)→ **PERSISTENT** |
| D1/D3/D4 | 22/22 LOW_STATE_CONCORDANCE;mean neg-share 0.761;**D4 PRICE_SYSTEM_DIVERGENCE 18/44** |

### CN（2010Q1-2026Q2;4 类主窗现为 2016Q1-2026Q2 n=42）
| Gate | 结果 |
|---|---|
| D-A | CPI<0 = 6/66 季(2025Q1 起最长 3 季)——CN 无 CPI 深度持续负段 |
| 4 类可得段 | 主窗 **2016Q1-2026Q2(n=42)**(唯一 ≥4 类连续段;PRE_MAIN_4CLASS_RUNS=NONE) |
| **D-B** | **17/42 季 ≥3/4 类 <1.0% → BROAD**(share 0.4048) |
| **D-C** | 最长连续 **14 季(2022Q4 起)→ PERSISTENT** |
| D-D | **CN_DEFLATION_GATE_BROAD_PERSISTENT_IN_2016Q1-2026Q2_WINDOW(n=42,17/42broad); PRE_MAIN_4CLASS_RUNS=NONE**(机械文本) |
| D1 | 无 deflator → 出口;D3 mean actual-neg-share 0.179;D4 INFEASIBLE_NO_DEFLATOR |

### 与外审独立复跑互证（第三次扩窗）
外审 §5（+2016-2018 complete）= 主窗 2016Q1-2026Q2 n=42 / BROAD 17/42 = 0.4048 / D-C 14 from 2022Q4。
engine v1.6 独立机器输出:**完全相同**。三次扩窗 verdict 稳定性:
```text
0.9286 (2023Q1-2026Q2 n=14) → 0.5667 (2019Q1-2026Q2 n=30) → 0.4048 (2016Q1-2026Q2 n=42)
BROAD → BROAD;PERSISTENT → PERSISTENT(最长段始终 2022Q4 起)
```

## 二、合成解读（维持三态纪律;外审 §8 措辞采纳）
- **CN 结论**:broad share 0.4048(17/42)说明 Broad 状态并非贯穿 2016-2026,而主要集中于后期;**真正稳定的事实 = 2022Q4 起持续 14 季的 Broad low-inflation episode**;加入 2016-2018 高服务通胀年份会显著降低全窗 share,但不改变 episode 存在。
- **结构区分(不变)**:CN = producer-deflation(PPI 深负)+ consumer/service low-inflation(core/services 低位、CPI 未深负)≢ JP economy-wide CPI/core/deflator 全面通缩——same gate classification ≢ same price-system structure。
- 与 B3 主链 GEOMETRY WITHOUT MECHANISM 完全兼容(状态几何相似不复制机制)。

## 三、缺口与限制（如实）
1. services 2016 前 = structural pre-start(NBS 月度稿"服务"行 2016 起稳定;外审确认无追采价值);2016-2026 可得窗已全采
2. canonical 33 行(2023+ 用户转录 28 + 正文级 5)无网页 URL,标 **A-unresolved-lineage**(parent_identifier=源文件 SHA 引用,可重定位但不指向网页)——外审 §6 建议的折中
3. JP 2020 基未归档 → D2 INFEASIBLE_NO_OLDBASE_ARCHIVE;CN 无 deflator → D1/D4 CN 出口(不变)

## 四、产物
- D0_spec_FROZEN_v0.1(immutable)/ D_gate_machine_v1.6.csv(6d4b3e11…)/ D_gate_quarter_detail_v1.6.csv(befb1d69…)
- engine/h6b_d_engine_v16.py(1c3242de…)+ d_run_record_v1.6.json(741ffe00…)
- 输入:8 个 D 文件(services 季度 f7d2cf01…)+ canonical monthly v1.6(f5c9eabd…)+ 外审 2016-2018 complete/quarterly + 外审 2019-2022 supplement + 2016-2018 verified 9m(S5)
- 本报告 v1.6 + 审核响应 + 审核包
