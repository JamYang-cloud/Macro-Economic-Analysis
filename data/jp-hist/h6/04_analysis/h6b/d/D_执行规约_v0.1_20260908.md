# H6-B D 模块（独立通胀机制 Deflation Gate）— 执行规约 v0.1（草案，执行前预注册）

日期：2026-09-08
上游：FREEZE_H6B_B1_20260907.txt + h6b_spec_FROZEN_v1.2.3.md（§9 Deflation Gate FROZEN + §10 Missingness + §13 源优先级）+ FREEZE_H6B_B3_20260908.txt（主链 GEOMETRY WITHOUT MECHANISM，D-D 合成输入）
状态：D 模块启动（B3 FREEZE 后按 B3.6 外审 §15 指引进入独立通胀机制模块）
范围：独立模块，不进主 Verdict；D-A..D-D 主判据 + D1-D4 口径稳健性

## 一、判定窗口（B0 冻结主窗继承）
- JP：1985Q1–2005Q4（84 季）
- CN：2010Q1–2026Q2（66 季）
- 每季分母 = 该季可得类别数；类别来自 D 六类（CPI / Core CPI / Services CPI / PPI / GDP deflator / Wage-income）

## 二、数据可得性（B1/B3 FROZEN 资产，逐季计）
| 类别 | JP | CN |
|---|---|---|
| CPI headline | e-Stat 2025 基 1971Q1+（84/84 主窗） | NBS akshare 2008Q1+（66/66） |
| Core CPI | e-Stat 2025 基 1971Q1+（84/84） | 官方 2013+（未采，COLLECTION_INCOMPLETE） |
| Services CPI | 未采（季度不可得性记录） | 官方 2016+（未采，COLLECTION_INCOMPLETE） |
| PPI | FRED 1984Q1+（84/84） | NBS akshare 2006Q1+（66/66） |
| GDP deflator | FRED 1995Q1+（44/84 主窗内） | 官方季度不可得（INFEASIBLE 有源记录） |
| Wage-income | annual（未采季度） | annual 城镇单位（未采季度） |

**JP 4 类可得**（CPI/Core/PPI/deflator）：满足 D-B "≥4 类可得"门槛的段 = 四类齐段 **1995Q1–2005Q4（44 季）**；此前 1985–1994（40 季）仅 3 类 → 该段逐季 D-B 判据 INFEASIBLE_AFTER_PRESPECIFIED_MASK（不缩分母，如实记录）。Wage/Services 缺类不影响 D-B（4 类门槛已过），如实报告 n_class_available。
**CN 2 类可得**（CPI/PPI）：< 4 → **D-B 全段 INFEASIBLE_AFTER_PRESPECIFIED_MASK**（冻结出口）；补采状态 COLLECTION_INCOMPLETE（core 2013+/services 2016+ 官方渠道已知，deflation_source_attempt_registry_CN.csv 记录）。CN D-A/D-C/D-D 依冻结层级不可升格。

## 三、判定序列（FROZEN §9）
- **D-A（CPI YoY<0，仅描述）**：主窗内 CPI<0 季数 + 最长连续段，JP/CN 分别报告。
- **D-B Broad**：有效段内**逐季**判定：该季可得类中 YoY<1.0% 的类数 ≥3（分母=可得类 ≥4）→ BROAD 季；D-B 结果 = broad_quarter_count / effective_window_length（JP 44 季窗）。
- **D-C Persistent**：D-B broad 状态**连续 ≥4 季** → persistent 段；报告最长连续段长度与起始季。
- **D-D（broad/persistent + 主机制链机制证据）**：D-D = D-B/D-C 状态 ∧ 主链机制证据。B3 FROZEN = GEOMETRY WITHOUT MECHANISM（无统一跨国机制证据）→ 合成：
  - JP：broad/persistent 判定（若成立）为 **JP 自 1990s 的通缩 regime 事实**，但研究问题（CN 是否重演 JP 机制）的 Japan-like 解释需要 CN 侧 D 状态 + 主链证据两者——CN D-B INFEASIBLE → **CN Japan-like 通缩-衰退机制解释不获数据支持（D 侧出口 INFEASIBLE + 主链 GEOMETRY 双否定）**。
- **D1-D4 口径稳健性**（按可得性执行，缺类如实）：
  - D1：headline ∈ [-0.5,+0.5]% 时 core/PPI/deflator 同向（JP 有效段；CN 2 类照做）
  - D2：rebase/weight 重叠期差异记录（e-Stat 2025 基 vs 2020 基；source_note 已注）——正常 rebase 不自动 = manipulation（price_measurement_risk_registry 禁 manipulation_score）
  - D3：负增长类别占比 diffusion——JP 4 类负增长占比（≤4 类，如实标注 coarse）
  - D4：CPI↔PPI↔GDP deflator 三角发散检测（JP；CN 无 deflator → INFEASIBLE）——发散 → PRICE_SYSTEM_DIVERGENCE 记录

## 四、缺口与出口（禁伪造）
- JP：Services/Wage 未采（Wage annual 单独报告不可拼接）；deflator 1995+ 结构性起点入册（n_structural_gap_years=10）
- CN：D-B 全段 INFEASIBLE（可得类 <4）；COLLECTION_INCOMPLETE 留档（core/services 官方渠道已知未采）
- 任何插值不得用于过 Gate

## 五、产物
- d/D_module_执行规约（本文件）
- d/D_gate_machine.csv（逐季/逐判机器表）+ d/H6B_D_results_v1.0_20260908.md（结果报告）
- 审核包（单 ZIP + manifest，参照 B3 惯例）
