# h6a_a4_method_spec_v1.1（预注册，SHA 冻结于结果产生前）
日期：2026-09-07
状态：FROZEN（结果产生前冻结；SHA256 见 00_registry/a4/h6a_a4_method_spec_v1.1.md.sha256）
背景：外审《JP-HIST_H6A4_BreakDiagnostics_外部审核报告》（REWORK）要求 A4.1 先冻结 exact criterion 再运行，双 penalty + m_max 扩搜 + boundary 标记 + N≥1000。

## 冻结方法（A4.1 primary）
- model：break-in-mean（intercept-only）全局最小二乘分割；动态规划精确求解（prefix-sum O(1) 段成本）。
- min segment length：5（年）。
- 标准化：国家域 robust-z（JP 1970-2025 / CN 2000-2025）；flavors = raw / ResidA（Model A: x ~ 1 + G + D_COVID，残差再 robust-z）。
- 变量：investment_gdp / cpi_yoy / m2_yoy。
- m_max（primary 搜索域）：JP = 6，CN = 4（由 minseg=5 可行上限内预注册放宽；不再 4/2）。
- 断点数选择：BIC2（主准则）——penalty (2m+1)·ln n，理由：unknown break locations 是模型复杂度一部分（segment means m+1 + break locations m）；BIC1（敏感度，penalty (m+1)·ln n）仅作 auxiliary 报告，不用于结论措辞。两条准则均输出、不事后选优。
- 断点日期定义：break_after_year = 前一 regime 的最后一个日历年；new_segment_start_year = break_after_year + 1。两列均输出。
- 不确定性：iid 残差 bootstrap，N = 1000，seed 20260907，m 固定于主准则选择，CI90 = 5/95 百分位；auxiliary：moving-block 残差 bootstrap（L=3，N=300，同 seed）作 serial-dependence 敏感度（P2-1/P2-2）。
- boundary 纪律：任何 m_selected == m_max 记 selected_at_boundary=True；m_max 扩搜敏感度单独输出（JP 2..6 / CN 2..4）。
- diagnostic-only：不进 Gate；不改 E01-E06；无 post-hoc rescue；断点 = 统计位置，非经济事件归因。

## narrative 纪律（沿用外审 §26）
- 禁「2007 断点消失」→ 仅「该 segmentation 下 ResidA point-estimate break set 不再单列 2007；CI 仍覆盖晚 2000s」。
- 禁「国内通缩起始 1993」→ 「point estimate 1993，位置不确定性覆盖 1989-2009，无法绑定单一历史事件」。
- 禁「2019-20 显现」→ 「后期 break component，CI 2003-2020，定位弱」。
- 禁把 CN/JP 断点年份重合写成共因/固定滞后证据。

## 产物（04_analysis/h6a/a4/）
a4_method_freeze_meta.csv / a4_criterion_sensitivity.csv / a4_mmax_sensitivity.csv /
a4_breaks_primary.csv / a4_breaks_aux.csv / a4_bootstrap_validation.csv / A4_QC_v1.1.txt / a4_report_v1.1.txt
