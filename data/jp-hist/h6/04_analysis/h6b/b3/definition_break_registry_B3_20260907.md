# H6-B B3 Definition Break Registry（B3.1 版）

日期:2026-09-07
上游:B1.3 FROZEN registry(definition_break_registry_B1.3)+ B3.1 patch


## B3.1 补充登记（2026-09-07，B3 v1.0 REWORK 响应）

| # | 事项 | 类型 |
|---|---|---|
| B3-1 | CN policy stance 制度断点 **POLICY_REGIME_BREAK_2019Q3** | benchmark 1Y 贷款基准利率(至 2019Q2, 4.35%)→ 1Y LPR(2019Q3 起, 首报 4.25%)。两制度变量作 stance proxy 拼接,level/change 双口径敏感度已报(b3b machine)。 |
| B3-2 | CN FAI 季度化口径修正 | 累计同比为 YTD 累计状态指标 → **季度末月值**(3/6/9/12 月),禁季内月均(v1.0 误用季均致 B4 CN 污染,P0-1)。 |
| B3-3 | JP policy rate provider lineage | 标准化文件源=FRED INTDSRJPM193N(贴现率,月度),provider-native raw 已归档 INTDSRJPM193N_provider_raw.csv;标准化=月度→季均(rate 类 index=季均)。 |
| B3-4 | CN B4 I proxy 口径 | FAI 累计 YoY(PROXY_NFC_INVESTMENT,registry i_q_gfcf CN 语义),与 JP GFCF/GDP 口径异——各自 internal robust-z 后方向可比,量级不可比(冻结时已注)。 |
