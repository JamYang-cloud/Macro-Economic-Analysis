# H6-B D0 Spec — Deflation Gate 执行冻结 v0.1（FROZEN BEFORE EXECUTION）

冻结时间：2026-09-08（D v1.1 执行前）
上游：h6b_spec_FROZEN_v1.2.3.md §9（D-A..D-D + D1-D4 FROZEN）+ §10 Missingness + FREEZE_H6B_B3（主链 GEOMETRY WITHOUT MECHANISM）
状态：**FROZEN**（本文件 SHA 冻结于任何 v1.1 machine output 之前）
规格 SHA：见本文件目录 manifest（engine 运行前计算并存档）

## 1. 判定窗口（继承 B0 主窗）
- JP 1985Q1–2005Q4（84 季）；CN 2010Q1–2026Q2（66 季）
- D-B/D-C 有效窗 = 该窗内 **≥4 类可得**的最长连续段；<4 类的季不判（INFEASIBLE_AFTER_PRESPECIFIED_MASK per-quarter，禁缩分母）

## 2. 类别与状态语义（FROZEN — 三态严格区分）
- **FAIL**：有足够数据且判据不满足（empirical negative）
- **INFEASIBLE_AFTER_PRESPECIFIED_MASK**：预注册 mask 后数据客观不可得/不可构造（源不存在、频率不可构造）
- **COLLECTION_INCOMPLETE**：官方渠道已知且存在，但尚未完成采集标准化（治理状态）
- 规则：COLLECTION_INCOMPLETE 的类别**不计入**可得类分母；COLLECTION_INCOMPLETE ≠ FAIL ≠ INFEASIBLE；任何 COLLECTION_INCOMPLETE/INFEASIBLE 不得在合成结论中充当 negative evidence。

## 3. D-A..D-D 判定（FROZEN §9 全文继承）
- D-A：CPI YoY<0 仅描述（季数/最长连续段/起点）
- D-B Broad：逐季：可得类（≥4）中 YoY<1.0% 类数 ≥3 → BROAD；输出 broad_q / effective_n / share + verdict
- D-C Persistent：D-B BROAD 连续 ≥4 季；无 BROAD 判定前置时 = NOT_EVALUATED_UPSTREAM_（继承上游状态）
- D-D：**JOINT_STATUS 输出（不合成否定）**：
  ```
  main_chain_status = GEOMETRY_WITHOUT_MECHANISM（B3 FROZEN）
  JP_deflation_gate = <D-B/D-C verdict>（BROAD/PERSISTENT 或出口）
  CN_deflation_gate = COLLECTION_INCOMPLETE（直至补采）
  joint_conclusion = MECHANISM_NOT_REPLICATED; <CN>_DEFLATION_STATE_NOT_YET_ADJUDICATED
  japan_like_mechanism_replication = NOT_SUPPORTED_BY_MAIN_CHAIN（B3）
  ```
  禁止：INFEASIBLE/COLLECTION_INCOMPLETE 充当"deflation state 不存在"证据。

## 4. D1 机器定义（FROZEN — 单一布尔式）
D1：对每季 headline ∈ [-0.5,+0.5]%：
`same_direction = [sign(core-1.0) == sign(headline-1.0)] AND [sign(ppi-1.0) == sign(headline-1.0)] AND [sign(deflator-1.0) == sign(headline-1.0)]`
其中 sign(x) = NEG if x<0 else NONNEG（相对于 1.0% 阈值的 low 状态同向性，非零对称）
输出：checked_quarters / same_dir_quarters / diff_dir_quarters + 每季明细。

## 5. D2 机器定义（FROZEN）
JP CPI rebase 记录：e-Stat 2025 基回溯序列（用户 2026-09-05 手动下载，raw 在 01_raw/stat/cpi_2025base/）——旧基 2020 基原始文件未归档 → 重叠期差异表客观不可得。
输出 schema：series_old_base=2020base(not archived) / series_new_base=2025base / overlap_period=NA / mean_abs_diff=NA / max_abs_diff=NA / sign_flip_count=NA / threshold_crossing_flip_count=NA / D2_verdict=INFEASIBLE_NO_OLDBASE_ARCHIVE（如实；rebase 处理已在 source_note 声明，不自动 = manipulation）
CN：月度 CPI 无 rebase 记录 → D2_CN=NA_NO_REBASE_EVENT

## 6. D3/D4 quarter-detail 字段（FROZEN）
quarter detail 每行扩展：n_available / n_low_lt1 / n_negative / negative_share / cpi_sign / ppi_sign / deflator_sign / divergence_flag（D4: CPI↔PPI↔deflator 三角任一符号不一致 → flag）
summary 必须由 detail 机器聚合（禁 narrative 先于 machine）。

## 7. 报告表述约束（FROZEN）
- JP 措辞：**"四个可得价格类别（CPI/Core/PPI/GDP deflator）中的广泛低通胀/负通胀"**——禁"六类"
- CN 措辞：D-A/PPI 描述性事实可报；D-B/D-C/joint D-D 在补采前一律 COLLECTION_INCOMPLETE / NOT_YET_ADJUDICATED

## 8. 可复现性要求（B3 同等级）
engine 归档 + run record（seed 无/确定性判定）+ clean-room（输入 = b3_inputs 内 D 文件 6 个）+ output SHA 比对。全链路 H6B_BASE 参数化，禁开发机绝对路径。

## 9. 冻结纪律
禁改：窗口/阈值 1.0%/三态语义/D1 布尔式/D2 schema/D-D JOINT_STATUS/四类表述。CN core/services 补采完成前 D-B/D-C 判定不执行（输出 COLLECTION_INCOMPLETE 状态，不填 verdict）。
