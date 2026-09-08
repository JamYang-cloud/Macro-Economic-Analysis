# H6-B D 模块（独立通胀机制 Deflation Gate）— 结果报告 v1.0

日期：2026-09-08
上游：h6b_spec_FROZEN_v1.2.3.md §9（Deflation Gate FROZEN）+ §10 Missingness + FREEZE_H6B_B3（主链 GEOMETRY）
数据：B1/B3 FROZEN 资产（h6b_d_*.csv，全部已入 b3_input_lineage 37 行）
判定：机器输出 D_gate_machine.csv + D_gate_quarter_detail.csv（无叙事先于 machine）

## 一、可得性（冻结资产逐季计）

| 类别 | JP（主窗 1985Q1-2005Q4, 84 季） | CN（2010Q1-2026Q2, 66 季） |
|---|---|---|
| CPI headline | 84/84（e-Stat 2025 基） | 66/66（NBS） |
| Core CPI | 84/84 | 官方 2013+（未采 COLLECTION_INCOMPLETE） |
| Services CPI | 未采 | 官方 2016+（未采） |
| PPI | 84/84（FRED） | 66/66（NBS） |
| GDP deflator | 44/84（1995Q1+ 结构性起点，n_structural_gap_years=10） | 官方季度不可得（INFEASIBLE 源记录） |
| Wage-income | annual 未采季度 | annual 未采季度 |
| **4 类可得段** | **1995Q1-2005Q4（44 季）** | 无（仅 2 类） |

## 二、机器判定（D_gate_machine.csv）

### JP（有效窗 1995Q1-2005Q4, 44 季）
- **D-A**：CPI<0 = 31/84 季，最长连续 20 季（1999Q4 起）——1990s 末-2000s 初名义通缩期如实呈现。
- **D-B Broad**：44 季中 **40 季** ≥3/4 类 YoY<1.0%（broad_share=0.9091）→ **BROAD**。
- **D-C Persistent**：broad 最长连续 **31 季（1998Q2 起）** ≥4 季 → **PERSISTENT**。
- **D-D**：**BROAD_PERSISTENT_WITHOUT_MECHANISM**——JP broad/persistent 是事实（1998-2005 六类广泛低通胀/负通胀），但 Japan-like 机制解释需要主链机制证据，B3 = GEOMETRY WITHOUT MECHANISM → 机制证据缺失，**不构成 Japan-like 机制确认**。
- **D1**（headline∈[-0.5,+0.5]% 时 core/PPI/deflator 同向）：22 季检查，12 季同向（~55%）——band 期类别方向非完全一致，如实报告（1990s 中期 CPI 粘性 vs PPI 工业通缩的结构差异）。
- **D3 diffusion**（负增长类别占比）：1995Q2 起多季 0.75-1.0——通缩广泛（≤4 类，coarse 如实标注）。
- **D4**（CPI↔PPI↔deflator 三角）：**PRICE_SYSTEM_DIVERGENCE**（18/44 季发散，典型 = CPI 微正 + PPI 负 + deflator 负，1995-96 结构期）——发散 = 真实价格结构现象（非 manipulation，price_measurement_risk_registry 禁 manipulation_score 纪律遵守）。

### CN（2010Q1-2026Q2, 66 季）
- **D-A**：CPI<0 = 6/66 季，最长连续 3 季（2025Q1 起）——2025 初短暂 CPI 负值段，仅描述。
- **D-B**：可得类仅 2（CPI/PPI）< 4 → **INFEASIBLE_AFTER_PRESPECIFIED_MASK**（冻结出口，禁缩分母）。
- **D-C**：NO_BROAD_QUARTER（上游出口）。
- **D-D**：INFEASIBLE_CN_NO_4CLASS——CN Japan-like 解释不获 D 侧数据支持。
- D1/D3/D4：无有效 4 类窗 → 出口。

## 三、合成解读（与主链衔接）
- **CN Japan-like 通缩-衰退机制解释 = 双否定**：①D 侧：CN 可得类别不足 4 类（2 类），D-B 判据 INFEASIBLE（补采 core 2013+/services 2016+ 可达 4 类但窗长受限，COLLECTION_INCOMPLETE 留档）；②主链侧：B3 = GEOMETRY WITHOUT MECHANISM（B1/B4 关键链跨国反向）。两门均未过 → 数据不支持"中国当前处于日本式资产负债表衰退-通缩机制重演"。
- **JP 侧事实**：broad/persistent deflation（1998Q2-2005 段）在 D 模块独立确认——这是日本 1990s 后通缩 regime 的量化档案，与 H6-A"JP J90 结构状态"衔接。
- **PPI 是共同信号**：JP 主窗 PPI<0 59/84 季、CN 2010-2026 PPI<0 38/66 季——两国工业品价格长期承压是**结构共性**，但 CPI/deflator 传导与信贷-投资机制方向不同（B3 已证），价格系统发散模式亦不同。

## 四、缺口与限制（如实）
1. CN D-B INFEASIBLE（2 类可得）——核心缺口，补采渠道已记录（core/services 官方月度新闻稿），历史拼接成本高未采。
2. JP Wage/Services 季度未采（Wage annual 不与季度机械拼接——spec 明示）。
3. D1 同向率仅 ~55%（band 期类别分歧如实报）；D3 仅 4 类 coarse。
4. D4 PRICE_SYSTEM_DIVERGENCE 18/44 季——发散非 manipulation 的界定按 spec 记录，未升级为数据质量问题。

## 五、产物
- D_执行规约_v0.1_20260908.md（预注册）
- D_gate_machine.csv（2 行摘要）+ D_gate_quarter_detail.csv（44 行逐季）
- 本报告 v1.0
- 审核包（单 ZIP + SHA manifest）
