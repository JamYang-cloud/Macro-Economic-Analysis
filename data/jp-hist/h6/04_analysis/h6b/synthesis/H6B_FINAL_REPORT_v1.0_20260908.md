# H6-B Joint Synthesis — 最终联合综合报告 v1.0

日期：2026-09-08
定位：**H6-B B6 Joint Synthesis / Freeze（非新增实证）**——将"状态几何""机制证据""通缩证据"三个冻结层汇总为分层结论，明确 Allowed / Prohibited Claims，并签署 H6-B 整体冻结。
依据：《JP-HIST_H6B_外部机制验证研究建议书_v1.2》B6 定义 + 各模块外审 PASS / FREEZE 报告。
纪律：**零新统计**——本报告全部数字来自冻结产物（single source of truth），不做任何新计算、不改任何冻结表述；凡超出 Allowed Claims 的新表述须先预注册。

---

## 1. 冻结资产清单（引用单源）

| 模块 | 冻结文件 | 审计包 SHA（zip） | 核心冻结 |
|---|---|---|---|
| H6-A（状态几何上游） | FREEZE_H6A_20260907.txt（+A2/A3/A4 逐级） | A5 全链汇总包（27 artifacts） | J90 dominant state geometry；exact lag NOT ROBUST；Investment NOT SHOCK-ROBUST；CPI=hinge |
| H6-B B0（spec） | FREEZE_H6B_B0_20260907.txt；h6b_spec_FROZEN_v1.2.3（sha f73994f2） | 329e6a8f | 五 channel 主链 + D 模块；θ 冻结；sign 机器化；missingness；cutoff 2026-08-31 |
| H6-B B1（data） | FREEZE_H6B_B1_20260907.txt | 921e17e8 | 23 standardized artifacts（20 分析季度序列 + 2 aux + 1 identity QC）；lineage 23/23；anchor QC 11/11 |
| H6-B B3（机制） | FREEZE_H6B_B3_20260908.txt | 4d702036 | **GEOMETRY WITHOUT MECHANISM（FINAL）**；B1/B4 跨国反向；B2 唯一稳定共同链 |
| H6-B D（通缩） | FREEZE_H6B_D_20260908.txt | 7523abeb | CN 2016Q1-2026Q2 n=42 窗 D-B 17/42 BROAD、D-C 14 季（2022Q4 起）；JP 40/44、31 季；结构不同 |

---

## 2. 层 1 — 状态几何（H6-A / H5 冻结层,上游引用）

摘自 FREEZE_H6A / H6A3 / A5 统一审核文档（逐字引用冻结断言,不扩展）：

1. **中日部分宏观结构状态存在可重复识别的相似性**（broad structural-state geometry）；J90 dominant state geometry 在预注册事件删除（Agreement≥0.923）与 Model-A residualization（ResidA 7/13）下保持；对 Model-B/common-support specification 敏感（不得称"全面 robust"）。
2. **精确滞后不支持**：A2 Gate A1 4/4 LEO FAIL；无 fixed-lag rescue；无唯一稳健固定滞后——该相似性**不能被稳定压缩为固定时间滞后**。
3. **Investment 是 H5 中最有希望的 held-out channel,但未通过 H6-A A3 shock-robustness gate**（Baseline perm 0.1584 FAIL / ResidA 不可估 / CS raw <0.25）——不升级为 broad common mechanism。
4. CPI = classification hinge（非独立机制）；M2 = secondary only。
5. Structural break timing/count 常 specification-sensitive；CN Investment 2007/2014 为相对稳定 recurring statistical locations（非机制证据）。

证据稳健性层级（A5 冻结）：**broad structural-state geometry > exact lag / exact breakpoint timing-count / broad common mechanism**。

---

## 3. 层 2 — 机制证据（H6-B B3 FROZEN, GEOMETRY WITHOUT MECHANISM）

摘自 FREEZE_H6B_B3（四轨全 GEOMETRY,冻结 B0 hierarchy key_chain_reverse 规则驱动）：

| 链 | 方向 | Gate |
|---|---|---|
| B1 Property→BS | **跨国方向差异**：JP 负 / CN 正 | FAIL（key reverse） |
| B2 BS→Profitability | 跨国同向（JP +0.18 / CN +0.38） | **PASS（唯一稳定共同链）** |
| B3a Profitability→Credit(q) | 两国同向负（-0.50 / -0.27） | SAME；B3 = CONDITIONAL_MIXED（不计 clean pass） |
| B3b stance/demand | JP = MIXED_OR_THIN / CN = SUPPORT（CREDIT_DEMAND_PROXY_EVIDENCE 语义,非 identified demand） | — |
| B4 Credit→Investment | **跨国方向差异**（JP +0.69 / CN -0.42；annual I/GDP aux 复现 JP +0.77 / CN -0.62） | FAIL_DIR（key reverse） |

**冻结机制层结论（逐字）**：中国与日本存在部分宏观结构状态与中间通道（B2/B3a）的相似性，但 **Property→BS 与 Credit→Investment 两关键链不能跨国复制**（后者季度+年度双口径方向差异），**State similarity ≢ Transmission-mechanism similarity**——不能将中国当前状态解释为日本资产负债表衰退机制的整体重演。Verdict = **GEOMETRY WITHOUT MECHANISM（FINAL）**，与 H5-FINAL（INTERPRETABLE FEATURE GEOMETRY ONLY）/ H6-A（Regime Geometry Robust / Exact Lag Not Event-Robust）证据层级一致。

---

## 4. 层 3 — 通缩证据（H6-B D FROZEN, D v1.6）

摘自 FREEZE_H6B_D（冻结核心事实逐项签署）：

### Japan（主窗 1995Q1-2005Q4,四类 CPI/Core/PPI/GDP deflator）
```text
D-A: CPI<0 31/84 季,最长连续 20 季（1999Q4 起）
D-B: 40/44 = 0.9091 → BROAD
D-C: 连续 31 季（1998Q2 起）→ PERSISTENT
D1: 22/22 LOW_STATE_CONCORDANCE
D3: mean actual-negative share 0.761
D4: 18/44 PRICE_SYSTEM_DIVERGENCE（actual_sign x<0；非 <1% low-state；非统计操纵）
```

### China（主窗 2016Q1-2026Q2,四类 Headline CPI/Core CPI/Services CPI/PPI）
```text
D-A: CPI<0 6/66 季,最长 3 季（2025Q1 起,描述性）——无 CPI 深度持续负段
D-B: 17/42 = 0.4048 → BROAD
D-C: 连续 14 季（2022Q4 起）→ PERSISTENT
D1/D4: INFEASIBLE_NO_DEFLATOR（D0 预注册出口）
services 2010-2015: structural pre-start（NBS"服务"行 2016 起）
```

### 结构区分（same gate classification ≢ same price-system structure）
- **JP = economy-wide deflation configuration**：CPI/Core/Deflator 广泛实际负增长 + PPI weakness。
- **CN = producer-deflation + consumer/service low-inflation configuration**：PPI 深度偏弱/负增长 + Core/Services 低通胀 + Headline CPI 多数接近零但非长期深度负增长。
- CN 表述约束（冻结）：broad share 0.4048 反映 2016-2018 高服务通胀年份稀释——**Broad 状态非贯穿 2016-2026**；稳定核心 = **2022Q4 起连续 14 季 Broad low-inflation episode**（三次扩窗 14→30→42 季 verdict 零 flip：0.9286 → 0.5667 → 0.4048）。

---

## 5. 联合结论（三层合流,最强可声明表述）

> 日本与中国均可进入 Broad/Persistent low-inflation 状态（各自通过冻结 D-B + D-C 判据），但**进入该分类的价格体系结构不同**：日本历史阶段（1995-2005）更接近 economy-wide CPI/core/deflator 全面通缩；中国当前（2016-2026 四类窗,2022Q4 起连续 episode）更接近 producer deflation + consumer/service low inflation,Headline CPI 未深负。结合 H6-B B3 对房地产—资产负债表—信贷—投资传导链的检验（关键链 B1/B4 跨国方向相反、Verdict GEOMETRY WITHOUT MECHANISM）与 H6-A 状态几何层（broad geometry 相似、exact lag 不支持）：
>
> **现有证据支持"中日宏观状态几何相似",不支持"中国正在复制日本式经济机制";支持"两国各自进入可比较的 Broad/Persistent 低通胀状态分类",不支持"同一价格体系结构"或"全面通缩等同"。**

证据层级（贯穿 H5→H6-A→H6-B）：broad structural-state geometry（稳健）> 状态分类可比性（D-B/D-C 判据,窗扩稳定）> exact lag / breakpoint timing（不支持）> broad common mechanism（B3 否定跨国复制）。

---

## 6. 局限（如实,不消解结论）

1. 机制层：因果上限 Level 3（关联+时序+方向预设,非因果识别）；B3b = credit-demand proxy evidence 而非 identified demand。
2. 冲击控制：Model A quarterly track 实为 annual-step control（WB 年度增长率年内平铺,标注 GLOBAL_GROWTH_CONTROL_ANNUAL_STEP_QUARTERLY）。
3. 状态几何层：Model-B/common-support 规格敏感；无唯一稳健固定滞后；Investment 未过 shock-robustness gate。
4. 通缩层：CN 无 GDP deflator（D1/D4 CN 出口 INFEASIBLE_NO_DEFLATOR）；services 2016 前 structural pre-start；JP D2 rebase overlap 因旧基未归档不可得。
5. 本报告为汇总,不新增任何统计结果；一切数字须回溯至第 1 节冻结资产。

---

## 7. 下游交付
- `H6B_ALLOWED_CLAIMS_v1.0_20260908.md`（逐字可声明清单,含 H6-A 继承 + H6-B 新增）
- `H6B_PROHIBITED_CLAIMS_v1.0_20260908.md`（逐字禁声明清单）
- `FREEZE_H6B_20260908.txt`（H6-B 整体冻结签署,含 B0/B1/B3/D 引用与联合结论）
