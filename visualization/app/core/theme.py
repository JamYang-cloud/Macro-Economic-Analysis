#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core/theme.py — 公众号视觉常量（宏观股市罗盘 · 可视化系统，M4）

与 chart-pipeline 技能同源（红涨绿跌/暖白底/主题红/标题色），集中定义
保证全应用一致。引用方：charts.py（布局/色板）、annotate.py（如需）。

常量来源（chart-pipeline SKILL.md，2026-08 定稿）：
  - 红涨 #e74c3c / 绿跌 #27ae60（条件色 colorRule）
  - 主题红 #c0392b
  - 页面暖白 #faf7f2
  - title 色 #7a5c3e
"""

# ---- 基础色 ----
BG = "#faf7f2"            # 页面暖白底（paper + plot 背景）
THEME_RED = "#c0392b"     # 主题红（主强调）
UP_RED = "#e74c3c"        # 红涨（盈利/上涨）
DOWN_GREEN = "#27ae60"    # 绿跌（亏损/下跌）
TITLE_BROWN = "#7a5c3e"   # 标题/主色（暖棕）
INK = "#3d3d3d"           # 正文深灰
GRID = "#ece5da"          # 暖灰网格线
AXIS = "#8a8178"          # 轴刻度/标签灰
ZERO_LINE = "#b0a89c"     # 0 轴参考线（比 GRID 深一点，弱于数据线）
FIT_LINE = TITLE_BROWN    # 拟合线（与标题同色系，暖棕虚线）

# ---- 多序列折线色板（公众号风格：低饱和暖调，10 色可区分）----
# 首色=主题红（单序列默认红）；后续按色相环排布，饱和度收敛
PALETTE = [
    THEME_RED,            # 0 主题红
    "#2c5f8a",            # 1 深蓝
    "#d97b29",            # 2 暖橙
    DOWN_GREEN,           # 3 绿
    "#7a5c8a",            # 4 紫
    "#3d9a9a",            # 5 青
    "#8e3b46",            # 6 酒红
    "#5b7a9d",            # 7 蓝灰
    "#b07a2e",            # 8 棕金
    "#6b7f4f",            # 9 橄榄
]

# ---- 导出 ----
FONT_FAMILY = '"Microsoft YaHei", "PingFang SC", "Noto Sans CJK SC", sans-serif'

# 图例/标注底色（半透明白，暖白底上不遮挡）
NOTE_BG = "rgba(255,255,255,0.88)"
NOTE_BORDER = "#d8d0c4"
