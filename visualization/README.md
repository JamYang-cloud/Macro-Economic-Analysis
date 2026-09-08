# 宏观股市罗盘 · 可视化程序（整合版）

中日整合可视化（Streamlit + Plotly）。数据自包含：CN 面板在 `data_snapshot_v2/`，
JP-HIST 展示层在 `data_snapshot_annual|h6|h6raw|jphist/`，日本官方冻结副本与早期段读取
本仓库 `../data/japan/`（country.py 已本地化，跨机可跑，不依赖任何本机绝对路径）。

## 运行

```bash
pip install -r requirements.txt
streamlit run app/app.py
```

依赖：streamlit ≥ 1.62、pandas、plotly ≥ 5.15。PNG 导出需 playwright + chromium（可选）。

## 四个视图

| 视图 | 内容 |
|---|---|
| 🇨🇳 中国数据 | 月度状态面板 + 特征 + 补充数据（年度/机制季度/通缩季度/原始月度）；叠加/分面/双轴/分布/箱线；缺失色带与口径断点；原始值下钻 |
| 🇯🇵 日本数据 | 统一变量池（state 10 + PIT 33 + 早期 5 + 日经全史 + 补充数据年度 8 + 季度 11）；政策 regime 底色；PIT 下钻；12-target；当前读数 |
| ⚖️ 中日对比 | 三数据层：**月频概念族**（crosswalk 13 族，锚点对齐）/ **年度重点族**（6 族）/ **季度机制族**（H6-B 5 族：核心 CPI/企业杠杆/PPI/地产活动·新开工/住宅价格）；对齐轴或日历轴；直出/重基/双 Y；强制可比性与口径图注 |
| 🧭 JP-HIST 结构发现 | H0–H5 冻结结论可视化（regime 全景/状态迁移/判别/证据矩阵等 11 图 + 纪律图注） |

## 目录

```
app/                  # app.py（入口）+ core/（loader/country/charts/annotate/export/theme/presentation）+ render_*
catalog/              # catalog_v2.csv（变量目录/分组）等
data_snapshot_v2/     # CN 月频快照（面板+特征+缺失+目标+raw 下钻，SHA manifest）
data_snapshot_annual|h6|h6raw|jphist/   # JP-HIST 展示投影（SHA manifest）
scripts/              # 离线导出（export_chart.py + 本地 plotly.js）
```

## 展示纪律（内置）

- 观察尺度 月/季/年；低频列 held-last 显示（切尺度取真实周期末值）；缺失色带/断点虚线来自注册口径。
- 中日对比仅形态/相对幅度：可比性 A=同口径 / B=近似 / C=形态；SECTOR_PROXY、CONCEPT_PROXY、停更注强制图下。
- JP-HIST 视图与移轴比较均声明：非投资信号、不做因果断言。

## 数据来源声明

CN：NBS/PBOC/中登等（Phase2 v2 冻结）；JP：BOJ/e-Stat/MLIT/内閣府 + FRED/BIS 镜像（官方口径优先）；
JP-HIST：上述 + H6 补采（冻结 2026-09-08）。完整性详见仓库 `docs/` 数据说明三篇。
