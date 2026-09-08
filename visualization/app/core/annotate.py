#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core/annotate.py — 图标注层（宏观股市罗盘 · 可视化系统）

职责：把 Phase 2 沉淀的元数据叠加到 Plotly 图上：
  1) 缺失区间色带：从 missing_matrix 的逐月 NA reason 合并为连续区间，
     按 reason 大类着色（NOT_APPLICABLE=变量成立前，属正常，不标）
  2) 口径断点竖线：显式 BREAKPOINTS 表（来源见注释），在切换月画虚线
  3) 纯函数，输入 figure 返回 figure（可链式调用）；零 Streamlit 依赖
"""

import pandas as pd
import plotly.graph_objects as go

# ----------------------------------------------------------------------
# 口径/制度断点表（显式、可审计；来源 = RECORD Step 2.2d / 2.4b / 2.6b）
# 格式：variable_id -> [(切换月 YYYY-MM, 说明)]
# 注意：这是"已知口径切换"的白名单，后续发现新断点在此追加；
#       数据缺口（SOURCE_GAP 等）由缺失色带覆盖，不在此表。
# ----------------------------------------------------------------------
BREAKPOINTS = {
    "liq.m1_yoy": [("2025-01", "M1新口径(纳入个人活期存款)")],      # Step 2.2d P0-3
    "rate.lpr1y": [("2019-08", "LPR改革(8/20起)")],                 # Step 2.2d P0-1
    "rate.lpr5y": [("2019-08", "LPR改革(8/20起)")],
    "cre.tsf_stock": [("2020-02", "可比口径追溯公开")],              # Step 2.6b ③
    "cre.tsf_flow": [("2020-02", "可比口径追溯公开")],
    "afre_yoy": [("2020-02", "可比口径追溯公开")],
    "hh.income_annual": [("2021-10", "转季度口径(HANDOFF)")],        # Step 2.4b-II
    "rate.fdr007_mean": [("2017-05", "FDR007上市")],                # Step 2.6b ①
}

# NA reason -> 色带颜色（异常性缺失才着色；NOT_APPLICABLE 正常不画）
REASON_COLORS = {
    "SOURCE_GAP": "rgba(255,165,0,0.22)",            # 橙：中间缺月
    "STALE_SOURCE": "rgba(255,69,0,0.28)",           # 深橙红：数据陈旧
    "COVERAGE_LOW": "rgba(255,99,71,0.25)",          # 珊瑚：覆盖率低
    "NOT_RELEASED": "rgba(169,169,169,0.20)",        # 灰：首月发布滞后
    "LEGACY_REGIME": "rgba(128,0,128,0.20)",         # 紫：旧口径段
    "RETROSPECTIVE_NOT_AVAILABLE": "rgba(75,0,130,0.25)",  # 深紫：追溯不可得
    "INSUFFICIENT_HISTORY": "rgba(70,130,180,0.20)", # 蓝：窗口 warm-up
    "HANDOFF_TO_QUARTERLY": "rgba(0,139,139,0.25)",  # 青：换季度口径
    "HISTORY_SNAPSHOT_ONLY": "rgba(105,105,105,0.18)",  # 灰：仅历史快照
}

# 需要画色带的 reason（其余如 NOT_APPLICABLE 属正常状态）
BANDED_REASONS = set(REASON_COLORS.keys())


def missing_spans(missing_df, col, start=None, end=None):
    """把逐月 NA reason 合并为连续区间，返回 [(start_ts, end_ts, reason)]。

    规则：reason 相同且连续的月份合并为一段；reason 变化即切段；
    NOT_APPLICABLE（变量成立前）与空（有值）跳过不视为异常。
    输入 missing_df：index=Timestamp、每格 reason 或空串（loader.load_missing）。
    """
    if col not in missing_df.columns:
        return []
    ser = missing_df[col]
    if start is not None:
        ser = ser.loc[start:]
    if end is not None:
        ser = ser.loc[:end]
    spans = []
    cur_reason = None
    cur_start = None
    prev = None
    for ts, reason in ser.items():
        if reason in ("", "NOT_APPLICABLE"):
            if cur_reason is not None:
                spans.append((cur_start, prev, cur_reason))
                cur_reason = None
        else:
            if cur_reason is None:
                cur_reason, cur_start = reason, ts
            elif reason != cur_reason:
                spans.append((cur_start, prev, cur_reason))
                cur_reason, cur_start = reason, ts
        prev = ts
    if cur_reason is not None:
        spans.append((cur_start, prev, cur_reason))
    return spans


def add_missing_bands(fig, missing_df, col, start=None, end=None, xref="x"):
    """在图上叠加缺失区间色带（vrect），只画异常性缺失。
    xref：默认 "x"（整图布局）；分面子图传 "x2"/"x3"… 定位到对应子图。"""
    for s, e, reason in missing_spans(missing_df, col, start, end):
        if reason not in BANDED_REASONS:
            continue
        color = REASON_COLORS.get(reason, "rgba(128,128,128,0.15)")
        # 色带覆盖整月：[s, e+1月)（月度索引均为每月 1 日）
        x1 = e + pd.DateOffset(months=1)
        fig.add_vrect(
            x0=s, x1=x1, fillcolor=color, line_width=0, xref=xref,
            layer="below", opacity=1.0,
            annotation_text=reason, annotation_position="top left",
            annotation_font_size=9, annotation_font_color="#888888",
        )
    return fig


def add_break_lines(fig, col, start=None, end=None, xref="x"):
    """在口径切换月画虚线竖线 + 文字标注（BREAKPOINTS 白名单）。

    实现注意：plotly 5.15 的 add_vline(x=Timestamp, annotation_position=...)
    在 pandas 2.1.4 下会触发内部 Timestamp 加法 bug（实测 cre.tsf_flow
    2020-02 断点崩），改用 add_shape + 手动 add_annotation 绕开。
    """
    for month_str, label in BREAKPOINTS.get(col, []):
        ts = pd.to_datetime(month_str)
        if start is not None and ts < start:
            continue
        if end is not None and ts > end:
            continue
        fig.add_shape(
            type="line", x0=ts, x1=ts, y0=0, y1=1, yref="paper",
            xref=xref, line=dict(dash="dash", color="#7f7f7f", width=1),
        )
        fig.add_annotation(
            x=ts, y=1.02, yref="paper", xref=xref, text=label,
            showarrow=False, yanchor="bottom",
            font=dict(size=10, color="#666666"),
        )
    return fig


def annotate(fig, missing_df, col, start=None, end=None, with_breaks=True,
             xref="x"):
    """便捷入口：一次叠加缺失色带 + 口径断点。"""
    add_missing_bands(fig, missing_df, col, start, end, xref=xref)
    if with_breaks:
        add_break_lines(fig, col, start, end, xref=xref)
    return fig
