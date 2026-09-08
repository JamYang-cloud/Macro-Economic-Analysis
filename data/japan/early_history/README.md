# 06_可视化/early_history — 早期段比对数据（COMPARISON-ONLY，2026-09-05 补采）

用途：支撑中日 30-40 年间隔的"同阶段形态对比"（如中国 2008-2026 vs 日本
1968-1986/1978-1996）。**仅供可视化国家间比对，不进入任何结构化分析/模型/回测**，
因此不套用 JP1.x 六层冻结+外部审核流程（用户确认）。

定位与隔离：
- 非 FROZEN 数据层（不属 JP1/1.5/1.6/1.7/1.8/1.9 任何冻结层）
- 与 data_snapshot/（FROZEN 副本）物理分离——可视化比对时本目录序列覆盖更早段，
  与主网格（1995+）重叠部分已做交叉核验（日经全史 vs 副本 10,261 日 mismatch=0）
- 准确性保障（轻治理）：官方源优先（内閣府/総務省/FRED 官方镜像）、provenance
  manifest（URL/retrieved_at/SHA256/覆盖）、数值锚点核验（各文件见 manifest
  anchor_checks 列，全部命中日本经济史已知值）

文件清单（6 序列，manifest 见 early_history_manifest.csv）：
  nikkei225_daily_full_1949.csv   日经 225 日次全史 1949-2026（FRED 官方镜像,扩全）
  discount_rate_boj_1953.csv      公定歩合贴现率 1953-2017（早期政策利率代理）
  retail_sales_mom_1955.csv       零售销售环比 1955-2026（OECD 镜像,环比%）
  ppi_manufacturing_1960.csv      制造 PPI 1960-2022（OECD 镜像,2015=100）
  gdp_real_yoy_fy_1955_cao.csv    実質GDP增速 FY1955-2022（内閣府白书附表,官方）
  aging_65plus_share_1950_soumu.csv  65岁+人口占比 1950-2025+推计（総務省官方）

已知边界（诚实标注，可视化时显示）：
- 镜像序列（retail/PPI/1955+ FRED 系）为 OECD 镜像：口径与官方可能存在差异，
  只做形态对比；PPI 2022 停更
- GDP 为跨基准拼接（68SNA/93SNA/08SNA，白书官方已注明连接处理），且为 FY 年度
  （4-3月）——与中国 CY 年度对齐时差半年，比对增速形态影响小但须标注
- 老龄 2021-2023 官方表未列（5 年间隔观察为主）；2030+ 为社人研将来推计
- 日经可覆盖 1949+，但 TOPIX TRI canonical Gate C 仍挂起——股票对比为
  PRICE 形态，不伪装 TRI
