# 数据说明 · JP-HIST（中日结构对比研究链）

JP-HIST 是「日本长历史 → 中国当前结构」对照研究的数据链：把日本 1954–2026 的法人资产负债表周期、
通缩、地产、人口等冻结成链，与中国 2000s+ 的同概念序列并排，检验结构相似性问题。
**本目录只发布冻结/经核验产物**（冻结标记 FREEZE_*.txt 随附）；中间件、采集 raw 与审核材料不发布。

## 链结构与目录

| 目录 | 内容 |
|---|---|
| 00_registry/ | 各阶段注册表（变量/规则/来源） |
| 02_standardized/ | 标准化冻结序列（annual_* 命名：CN/JP 双国面板，1978+/1955+ 长史；含 H1/H2 清洗产物） |
| 03_features/ | 结构特征（regime 分类、迁移矩阵等输入） |
| 04_analysis/ | 分析结论：cn_panel/jp_panel（面板）、cn_state/jp_state（状态）、h5（regime 画像/迁移/判别/证据矩阵）、report md |
| h6/ | **H6-A/H6-B 补采链（2026-09-08 冻结）**：00_registry / 02_standardized（h6b：机制与通缩季度标准化，35 文件）/ 04_analysis（b1–b3、d 子链 + synthesis 综合） |
| FREEZE_H0..H5.txt / H6-B | 各阶段冻结标记（含 SHA 说明） |

## 双侧覆盖与频率

- **日本长史**：法人企业统计（1954Q2+，MOF）、GDP 68SNA 段（1955+）、住宅着工（1965+）、CPI 2025 基准核心（1971+）、
  政策利率贴现率（1984Q1–2017Q2 停更）、BIS 住宅价格（1955+）、GFCF/投资率等。
- **中国段**：规上工业杠杆/利润率（2011Q1+）、PBOC 部门信贷（2010Q1+）、政策利率 LPR 链（2010Q1+）、
  房地产（新开工/销售/开发投资，2000Q1+）、核心/服务 CPI（2013Q1+/2016Q1+）、PPI（2006Q1+）、BIS 房价（2005Q2+）。
- 频次：以季度（季首单点）与年度为主；与月频数据并列时强制频次标签。

## H6-B 综合结论（冻结，2026-09-08）

- 结论文件：`h6/04_analysis/h6b/synthesis/`（3 件综合 + FREEZE 标记；B0–B3、D 子链各自冻结）。
- 核心判断：**中日均可通过 Broad / Persistent 通缩判据，但结构不同**（日本的通缩与资产负债表/信贷周期纠缠更深；
  中国的价格弱势更多来自供给与地产信用收缩）——详见报告 `reports/jp-hist/`，勿超范围解读。

## 展示投影（可视化侧）

`visualization/data_snapshot_{annual,h6,h6raw,jphist}/` 是本链冻结产物的**只读展示投影**（附 SHA256 manifest）：
- data_snapshot_annual：CN 6 + JP 8 年度长史（出生率/CPI/投资率/M2/GDP/工资/地价/TFR…）
- data_snapshot_h6：H6-B 季度机制/通缩 24 序列（供 M2 日本与 M3 季度机制族）
- data_snapshot_h6raw：原始层精选 2（CNY/USD、BIS REER）
- data_snapshot_jphist：结构发现视图（M4）的结论 CSV 快照

## 报告

- 中日宏观结构相似性深度研究报告（md/docx）
- 项目执行方法与可靠性论证报告（md/docx）
- JP-HIST 最终证据综合（Final Evidence Synthesis）
- JP-HIST 大众深度报告（docx）

**纪律**：时间移轴对比 = 形态/相对幅度比较，两窗共长；禁"日本化/固定滞后 N 年"断言；可视化非研究级严谨、非投资建议。
