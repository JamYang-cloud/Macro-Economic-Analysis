# 06_可视化/data_snapshot — 日本数据副本（可视化专用，只读）

用途：供可视化程序调用的日本数据副本。**所有程序数据调用均使用本目录副本**，
不直接读 01_数据采集/02_清洗标准化/03_state/04_targets 下的 FROZEN 原件——
防止编程误操作破坏已冻结数据（与宏观股市罗盘/08_可视化/data_snapshot_v2 同模式）。

冻结来源：JP1.x 数据治理全链 FROZEN（2026-09-05 最终审核收官）：
  JP1 Raw → JP1.5 Standardized → JP1.6 PIT → JP1.7 Monthly State →
  JP1.8 Proxy Targets → JP1.9 Revision Audit
副本清单（55 文件，其中 53 个源文件副本 SHA256 与 FROZEN 原件一致，见
data_snapshot_manifest.csv；2 个为本层生成：jp_viz_feature_names.csv 中文可读名、
policy_regime_11段.csv 政策 regime 段表）：

状态层（月度决策状态，1995-01~2026-07，379 月）：
  state_monthly_primary.csv        PRIMARY 分支（市场级：拆借利率 1998+、USDJPY 1971+）
  state_monthly_sensitivity.csv    SENSITIVITY 分支（10 列：+M2 canonical/基础货币/
                                   BOJ 资产/短观×2；M2 三 audit 列）
  state_descriptive_current.csv    当前读数快照（2026-09-05；含 freshness）
  state_equity_primary/sensitivity.csv  Layer B（每月最后 TSE 交易日 re-asof）
特征注册与命名：
  jp17_feature_registry_v1.csv     特征注册（v1，FROZEN）
  jp_viz_feature_names.csv         中文可读名/单位/分组（可视化层，用户可见用）
  jp_registry_v1.1.csv             概念注册（21 列，FROZEN）
  policy_regime_11段.csv           货币政策 regime 段表（RATE_BASED_PRE_ZIRP…）

目标层（12-target，NIKKEI225 PRICE PROXY；canonical TOPIX_TRI Gate C 挂起）：
  target_monthly_v2.csv            379 月 × 14 列（state/exec/loss/MDD × 36/60/120m）
  jp18_target_registry_v3.csv      target 注册（role=PROXY, frozen=false）

价格/日历层（Layer B 决策基础设施）：
  nikkei225_daily_fred.csv         日经 225 日次收盘 1985-2026（10,261 obs）
  price_manifest.csv / price_completeness_qc.csv  价源元数据/完整性
  tse_sessions.csv (7,846) / tse_monthly_last_day.csv (379)  TSE 交易日历
  pit/（39 文件）                   PIT 层原始 18 列文件（下钻审计用）

禁则：
  1. 本目录为只读快照——程序不得回写/修改任何文件；需要修正一律回 FROZEN 层走流程
  2. 中文名以 jp_viz_feature_names.csv 为准（用户可见界面禁直接显示 feature_id）
  3. PROXY 标注：股票 target 一律显示"日经225 价格指数(代理)"并注明 TOPIX TRI 未解
  4. 更新流程：仅当上游 FROZEN 层经外部审核变更后，由复制脚本重新生成副本+manifest
