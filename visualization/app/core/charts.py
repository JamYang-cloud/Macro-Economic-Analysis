#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core/charts.py — 图表工厂 v1.1（宏观股市罗盘 · 可视化系统）

职责：把面板数据渲染为 Plotly Figure（纯函数，零 Streamlit 依赖）。
  - line_chart / area_chart / step_chart  多序列趋势（观察尺度 月/季/年）
  - histogram（分布视图）  单变量分布（固定月度，横轴=数值，非时间）
  - box_chart  单变量箱线图（离群点可视化）
  - dual_axis  双轴叠加（两个不同量纲变量）
  - facet_figures  分面：每变量独立子图、独立呈现方式（默认=推荐）
铁律：
  - connectgaps=False：缺月绝不连线
  - 横轴默认 = 时间（分布视图/箱线图除外：横轴=数值，由 UI 标注语义）
  - 重采样用周期末值（状态语义，低频变量阶梯消除）；
    缺失色带/口径断点基于原始月度元数据叠加（时间轴一致）
  - 差值/利差类自动加 0 轴参考线（zero_cols 由调用方传入）
"""

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

from . import theme

# 统一视觉（M4：公众号视觉常量，与 chart-pipeline 同源）：
# 暖白底 #faf7f2、主题红 #c0392b、标题暖棕 #7a5c3e、红涨绿跌
BASE_LAYOUT = dict(
    template="plotly_white",
    paper_bgcolor=theme.BG,
    plot_bgcolor=theme.BG,
    font=dict(family=theme.FONT_FAMILY, color=theme.INK, size=13),
    title=dict(font=dict(color=theme.TITLE_BROWN, size=17)),
    xaxis=dict(gridcolor=theme.GRID, zerolinecolor=theme.GRID,
               linecolor=theme.AXIS, tickcolor=theme.AXIS),
    yaxis=dict(gridcolor=theme.GRID, zerolinecolor=theme.GRID,
               linecolor=theme.AXIS, tickcolor=theme.AXIS),
    hovermode="x unified",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0,
                font=dict(size=12)),
    margin=dict(l=60, r=60, t=60, b=40),
)

PALETTE = theme.PALETTE


def style_title(fig):
    """统一标题样式（M4）：标题暖棕 + 字号。

    为什么需要：BASE_LAYOUT 里的 title.font 会被各图函数的
    `update_layout(title="字符串")` 覆盖（plotly 把字符串规范化成
    dict 时丢失 font）——实测 title.font.color=None。在输出边界
    （export.fig_to_html / app 渲染前）统一应用。
    """
    t = fig.layout.title
    if t is not None and getattr(t, "text", None):
        fig.update_layout(title=dict(
            text=t.text,
            font=dict(color=theme.TITLE_BROWN, size=17),
        ))
    return fig

# 观察尺度 -> pandas resample 规则（周期末值）
# 注意：pandas 2.1.4 不支持 "QE"/"YE"（2.2+ 别名），用 "Q"/"A" 兼容
SCALE_RULES = {"月": None, "季": "Q", "年": "A"}
CHART_TYPES = ["折线", "分布视图", "箱线图", "面积"]

# PIT hover 模板：值 + 发布日/源文件/vintage/陈旧月数/参考期/缺失原因
PIT_HOVER = ("<b>%{fullData.name}</b><br>时间 %{x|%Y-%m}<br>值 %{y:.3f}"
             "<br>发布日 %{customdata[0]}<br>源文件 %{customdata[1]}"
             "<br>vintage %{customdata[2]}<br>陈旧月数 %{customdata[3]}"
             "<br>参考期 %{customdata[4]}<br>缺失原因 %{customdata[5]}"
             "<extra></extra>")


def _pit_customdata(data, col, pit_meta):
    """按 (variable_id, 月) 查 PIT 溯源，构造每点 customdata（6 字段）。
    pit_meta 来自 loader.load_pit_meta()；无溯源时返回 None（默认 hover）。"""
    if not pit_meta:
        return None
    rows = []
    for ts in data.index:
        m = ts.strftime("%Y-%m")
        meta = pit_meta.get((col, m), {})
        na = meta.get("na_reason", "")
        rows.append([meta.get("avail", ""), meta.get("source", ""),
                     meta.get("vintage", ""), meta.get("stale", ""),
                     meta.get("ref", ""), na if na else "有值"])
    return rows


def _resample(df, scale):
    """按观察尺度重采样：季/年取周期末值（状态语义，保持低频变量真实观测）。"""
    rule = SCALE_RULES.get(scale)
    if rule is None:
        return df
    return df.resample(rule).last()


def _slice(df, start, end):
    if start is not None:
        df = df.loc[start:]
    if end is not None:
        df = df.loc[:end]
    return df


def _line_trace(data, col, name, color, shape="linear", fill=None,
                customdata=None, hovertemplate=None):
    return go.Scatter(
        x=data.index, y=data[col], name=name, mode="lines",
        line=dict(color=color, width=2, shape=shape),
        connectgaps=False, fill=fill,
        customdata=customdata, hovertemplate=hovertemplate,
    )


def _with_pit(trace_kw, data, col, pit_meta):
    """为 trace 附加 PIT hover（customdata + hovertemplate）。"""
    cd = _pit_customdata(data, col, pit_meta)
    if cd is not None:
        trace_kw["customdata"] = cd
        trace_kw["hovertemplate"] = PIT_HOVER
    return trace_kw


def _apply_annotations(fig, missing_df, cols, start, end, zero_cols=(),
                       xref="x"):
    """叠加缺失色带 + 口径断点 + 0 轴参考线（差值/利差类）。"""
    if missing_df is not None:
        from .annotate import annotate
        for col in cols:
            annotate(fig, missing_df, col, start, end, xref=xref)
    for col in cols:
        if col in zero_cols:
            # add_hline 默认 xref=paper domain（整图宽），只需指定 yref
            yref = "y" if xref == "x" else xref.replace("x", "y")
            fig.add_hline(y=0, line_dash="dot", line_color=theme.ZERO_LINE,
                          line_width=1, yref=yref)
    return fig


def line_chart(df, cols, names, start=None, end=None, missing_df=None,
               scale="月", log_y=False, zero_cols=(), pit_meta=None):
    """多序列折线（时间轴，支持观察尺度/对数轴/PIT hover）。"""
    data = _resample(_slice(df, start, end), scale)
    fig = go.Figure(layout=BASE_LAYOUT)
    for i, (col, name) in enumerate(zip(cols, names)):
        kw = _with_pit({}, data, col, pit_meta)
        fig.add_trace(_line_trace(data, col, name,
                                  PALETTE[i % len(PALETTE)], **kw))
    fig.update_layout(title=f"{' / '.join(names)}", yaxis_title="")
    if log_y:
        fig.update_yaxes(type="log")
    _apply_annotations(fig, missing_df, cols, start, end, zero_cols)
    return fig


def area_chart(df, cols, names, start=None, end=None, missing_df=None,
               scale="月", log_y=False, zero_cols=(), pit_meta=None):
    """面积图：折线 + 填充，看量感。"""
    data = _resample(_slice(df, start, end), scale)
    fig = go.Figure(layout=BASE_LAYOUT)
    for i, (col, name) in enumerate(zip(cols, names)):
        kw = _with_pit({}, data, col, pit_meta)
        fig.add_trace(_line_trace(data, col, name,
                                  PALETTE[i % len(PALETTE)], fill="tozeroy",
                                  **kw))
    fig.update_layout(title=f"{' / '.join(names)}（面积）")
    if log_y:
        fig.update_yaxes(type="log")
    _apply_annotations(fig, missing_df, cols, start, end, zero_cols)
    return fig


def step_chart(df, cols, names, start=None, end=None, missing_df=None,
               scale="月", log_y=False, zero_cols=(), pit_meta=None):
    """阶梯图：台阶式折线，低频 forward-hold 数据的诚实呈现。"""
    data = _resample(_slice(df, start, end), scale)
    fig = go.Figure(layout=BASE_LAYOUT)
    for i, (col, name) in enumerate(zip(cols, names)):
        kw = _with_pit({}, data, col, pit_meta)
        fig.add_trace(_line_trace(data, col, name,
                                  PALETTE[i % len(PALETTE)], shape="hv",
                                  **kw))
    fig.update_layout(title=f"{' / '.join(names)}（阶梯）")
    if log_y:
        fig.update_yaxes(type="log")
    _apply_annotations(fig, missing_df, cols, start, end, zero_cols)
    return fig


def histogram(df, col, name, start=None, end=None, missing_df=None):
    """分布视图：单变量直方图。横轴=数值（非时间），固定月度样本。
    用于核查分布形态与离群点。"""
    data = _slice(df, start, end)
    values = data[col].dropna()
    fig = go.Figure(layout=BASE_LAYOUT)
    fig.add_trace(go.Histogram(
        x=values, name=name, nbinsx=30,
        marker=dict(color="rgba(192,57,43,0.7)",
                    line=dict(color="white", width=1)),
    ))
    if len(values):
        mean = float(values.mean())
        fig.add_vline(x=mean, line_dash="dash", line_color=theme.FIT_LINE,
                      annotation_text=f"均值 {mean:.3f}",
                      annotation_position="top right")
    fig.update_layout(
        title=f"{name} · 分布视图（{len(values)} 个月有效值）",
        xaxis_title=f"{name} 数值（非时间）", yaxis_title="月数",
        bargap=0.05,
    )
    if missing_df is not None:
        from .annotate import annotate
        annotate(fig, missing_df, col, start, end)
    return fig


def box_chart(df, col, name, start=None, end=None):
    """箱线图：分布 + 离群点（hover 标注月份）。横轴=变量（非时间）。"""
    data = _slice(df, start, end)
    s = data[col].dropna()
    months = [ts.strftime("%Y-%m") for ts in s.index]
    fig = go.Figure(layout=BASE_LAYOUT)
    fig.add_trace(go.Box(
        y=s.values, name=name, boxpoints="outliers",
        marker=dict(color=PALETTE[0], size=5),
        line=dict(color=PALETTE[0], width=2),
        customdata=months,
        hovertemplate=("<b>%{fullData.name}</b><br>值 %{y:.3f}"
                       "<br>月份 %{customdata}<extra></extra>"),
    ))
    fig.update_layout(
        title=f"{name} · 箱线图（{len(s)} 个月有效值）",
        yaxis_title=f"{name} 数值（非时间）",
    )
    return fig


def dual_axis(df, col_l, name_l, col_r, name_r, start=None, end=None,
              missing_df=None, scale="月", log_y=False, zero_cols=(),
              pit_meta=None):
    """双轴折线：左轴=col_l，右轴=col_r（两个不同量纲对比趋势）。"""
    data = _resample(_slice(df, start, end), scale)
    kw_l = _with_pit({}, data, col_l, pit_meta)
    kw_r = _with_pit({}, data, col_r, pit_meta)
    fig = go.Figure(layout=BASE_LAYOUT)
    fig.add_trace(go.Scatter(
        x=data.index, y=data[col_l], name=name_l, mode="lines",
        line=dict(color=PALETTE[0], width=2), connectgaps=False, **kw_l,
    ))
    fig.add_trace(go.Scatter(
        x=data.index, y=data[col_r], name=name_r, mode="lines",
        line=dict(color=PALETTE[1], width=2), connectgaps=False,
        yaxis="y2", **kw_r,
    ))
    fig.update_layout(
        title=f"{name_l}（左轴） vs {name_r}（右轴）",
        yaxis=dict(title=name_l, side="left"),
        yaxis2=dict(title=name_r, side="right", overlaying="y", showgrid=False),
    )
    if log_y:
        fig.update_yaxes(type="log")
    _apply_annotations(fig, missing_df, [col_l, col_r], start, end, zero_cols)
    return fig


def facet_figures(df, specs, start=None, end=None, missing_df=None,
                  scale="月", log_y=False, zero_cols=(), pit_meta=None):
    """分面图：每个选中变量一个子图，独立呈现方式（折线/分布/箱线/面积）。
    specs = [(col, name, chart_type)]，chart_type ∈ CHART_TYPES。
    折线/面积子图横轴=时间（含缺失色带/断点/0轴/PIT hover）；
    分布/箱线横轴=数值。
    """
    data = _resample(_slice(df, start, end), scale)
    n = len(specs)
    titles = [f"{name}（{ctype}）" for _, name, ctype in specs]
    fig = make_subplots(rows=n, cols=1, shared_xaxes=False,
                        vertical_spacing=0.15, subplot_titles=titles)
    for i, (col, name, ctype) in enumerate(specs, start=1):
        color = PALETTE[i % len(PALETTE)]
        if ctype == "分布视图":
            vals = df[col].dropna()
            fig.add_trace(go.Histogram(
                x=vals, name=name, nbinsx=30,
                marker=dict(color="rgba(192,57,43,0.7)",
                            line=dict(color="white", width=1)),
            ), row=i, col=1)
        elif ctype == "箱线图":
            s = df[col].dropna()
            months = [ts.strftime("%Y-%m") for ts in s.index]
            fig.add_trace(go.Box(
                y=s.values, name=name, boxpoints="outliers",
                marker=dict(color=color, size=5), line=dict(color=color, width=2),
                customdata=months,
                hovertemplate=("<b>%{fullData.name}</b><br>值 %{y:.3f}"
                               "<br>月份 %{customdata}<extra></extra>"),
            ), row=i, col=1)
        elif ctype == "面积":
            kw = _with_pit({}, data, col, pit_meta)
            fig.add_trace(_line_trace(data, col, name, color, fill="tozeroy",
                                      **kw), row=i, col=1)
        else:  # 折线
            kw = _with_pit({}, data, col, pit_meta)
            fig.add_trace(_line_trace(data, col, name, color, **kw),
                          row=i, col=1)

        if ctype in ("折线", "面积"):
            # 时间轴子图：缺失色带/断点/0轴/对数轴
            if missing_df is not None:
                from .annotate import annotate
                annotate(fig, missing_df, col, start, end, xref=f"x{i}")
            if col in zero_cols:
                fig.add_hline(y=0, line_dash="dot", line_color=theme.ZERO_LINE,
                              row=i, col=1)
            if log_y:
                fig.update_yaxes(type="log", row=i, col=1)

    fig.update_layout(template="plotly_white", height=260 * n + 80,
                      showlegend=False,
                      margin=dict(l=60, r=60, t=60, b=40))
    return fig


# =====================================================================
# M3 关联分析四图（2026-08-27 续作）
# 共同铁律：
#   - 散点/热力图/前向收益的横轴是"变量值"不是时间，标题显式标注
#     "（非时间）"（用户原则：趋势图横轴默认时间，非时间须标注）
#   - 配对统计只基于两变量共同有效月（诚实 n），缺失点不画
#   - 纯函数，零 Streamlit 依赖
# =====================================================================

import numpy as _np


def _year_frac(index):
    """时间着色用：Timestamp 索引 → 年份小数（2008.0 ~ 2026.5）。"""
    return [t.year + (t.month - 1) / 12.0 for t in index]


def _scatter_hover(cd, name_x, name_y):
    """散点 hover 模板：月份/两值/PIT 发布日/源文件。"""
    return ("<b>%{fullData.name}</b><br>月份 %{customdata[0]}"
            "<br>%{customdata[4]} = %{x:.3f}（发布 %{customdata[1]}）"
            "<br>%{customdata[5]} = %{y:.3f}（发布 %{customdata[2]}）"
            "<br>源 %{customdata[3]}<extra></extra>")


def scatter_chart(df, col_x, name_x, col_y, name_y, start=None, end=None,
                  color_mode="time", pit_meta=None, missing_df=None):
    """散点 + 时间着色（T3.1）：两变量月度关系 + 时序演化。

    - 只画两变量共同有效月（缺失点不画，标题标注有效 n）
    - 时间着色：点色=年份小数（色阶 Viridis，colorbar 标时间）
    - 叠加 OLS 拟合线 + Pearson r 注解（视觉直觉，非统计检验）
    - hover：月份/两值/各自发布日/源文件（PIT 溯源）
    """
    data = _slice(df, start, end)[[col_x, col_y]].dropna()
    n = len(data)
    cd = None
    hover = None
    if pit_meta:
        cd = []
        for ts in data.index:
            m = ts.strftime("%Y-%m")
            mx = pit_meta.get((col_x, m), {})
            my = pit_meta.get((col_y, m), {})
            cd.append([
                m,
                mx.get("avail", ""), my.get("avail", ""),
                (mx.get("source", "") or my.get("source", "")),
                name_x, name_y,
            ])
        hover = _scatter_hover(cd, name_x, name_y)

    fig = go.Figure(layout=BASE_LAYOUT)
    if color_mode == "time":
        fig.add_trace(go.Scatter(
            x=data[col_x], y=data[col_y], mode="markers", name="样本点",
            marker=dict(
                size=8, color=_year_frac(data.index),
                colorscale="Viridis", showscale=True,
                colorbar=dict(title="时间", thickness=12, len=0.7),
                line=dict(color="white", width=0.5),
            ),
            customdata=cd, hovertemplate=hover,
        ))
    else:  # na_reason 模式（任一变量缺失月份按原因着色；M2 语义复用）
        colors = []
        for ts in data.index:
            m = ts.strftime("%Y-%m")
            r1 = (pit_meta or {}).get((col_x, m), {}).get("na_reason", "")
            r2 = (pit_meta or {}).get((col_y, m), {}).get("na_reason", "")
            colors.append(theme.AXIS if (r1 or r2) else PALETTE[0])
        fig.add_trace(go.Scatter(
            x=data[col_x], y=data[col_y], mode="markers", name="样本点",
            marker=dict(size=8, color=colors),
            customdata=cd, hovertemplate=hover,
        ))

    # OLS 拟合线 + r 注解（共同有效月）
    if n >= 3:
        k, b = _np.polyfit(data[col_x], data[col_y], 1)
        xs = _np.linspace(data[col_x].min(), data[col_x].max(), 50)
        fig.add_trace(go.Scatter(
            x=xs, y=k * xs + b, mode="lines", name="OLS 拟合",
            line=dict(color=theme.FIT_LINE, width=2, dash="dash"),
            hoverinfo="skip",
        ))
        r = data[col_x].corr(data[col_y])
        fig.add_annotation(
            x=0.02, y=0.98, xref="paper", yref="paper", showarrow=False,
            align="left", text=f"Pearson r = {r:.3f}<br>共同有效月 n = {n}",
            font=dict(size=12), bgcolor=theme.NOTE_BG,
            bordercolor=theme.NOTE_BORDER, borderwidth=1,
        )

    fig.update_layout(
        title=f"{name_x} × {name_y} · 散点（时间着色）",
        xaxis_title=f"{name_x} 数值（非时间）",
        yaxis_title=f"{name_y} 数值（非时间）",
    )
    if missing_df is not None and pit_meta is None:
        # 无 PIT 时的降级：仍叠加缺失色带（双变量）
        from .annotate import annotate
        for c in (col_x, col_y):
            annotate(fig, missing_df, c, start, end)
    return fig


def rolling_corr_chart(df, col_a, name_a, col_b, name_b, start=None, end=None,
                       window=24, missing_df=None, pit_meta=None):
    """滚动相关系数（T3.2）：两变量在 N 月窗口内的 Pearson 相关时序。

    - 严格 min_periods=window（开头不足 N 月显示 NaN，不画，统计诚实）
    - 参考线：0（中灰实线）+ ±0.5（浅灰虚线，实用相关判定）
    - 叠加两变量缺失色带；标题标注窗口与有效点数
    """
    data = _slice(df, start, end)[[col_a, col_b]].dropna()
    corr = data[col_a].rolling(window=window, min_periods=window).corr(data[col_b])
    n_valid = int(corr.notna().sum())
    cd = None
    hover = None
    if pit_meta:
        cd = []
        for ts in corr.index:
            m = ts.strftime("%Y-%m")
            ma = pit_meta.get((col_a, m), {})
            mb = pit_meta.get((col_b, m), {})
            cd.append([m, ma.get("avail", ""), mb.get("avail", ""),
                       (ma.get("source", "") or mb.get("source", "")),
                       name_a, name_b])
        hover = ("<b>%{fullData.name}</b><br>月份 %{customdata[0]}"
                 "<br>相关 %{y:.3f}"
                 "<br>%{customdata[4]} 发布 %{customdata[1]}"
                 "<br>%{customdata[5]} 发布 %{customdata[2]}"
                 "<br>源 %{customdata[3]}<extra></extra>")

    fig = go.Figure(layout=BASE_LAYOUT)
    fig.add_trace(go.Scatter(
        x=corr.index, y=corr.values, mode="lines", name=f"相关（{window}月）",
        line=dict(color=PALETTE[0], width=2), connectgaps=False,
        customdata=cd, hovertemplate=hover,
    ))
    for y, style in ((0.0, "solid"), (0.5, "dot"), (-0.5, "dot")):
        fig.add_hline(y=y, line_dash=style,
                      line_color=theme.ZERO_LINE if y == 0 else "#d8d0c4",
                      line_width=1)
    fig.update_layout(
        title=f"{name_a} × {name_b} · 滚动相关（窗口 {window} 月，有效 {n_valid} 点）",
        yaxis_title="Pearson 相关",
        yaxis=dict(range=[-1.05, 1.05]),
    )
    if missing_df is not None:
        from .annotate import annotate
        for c in (col_a, col_b):
            annotate(fig, missing_df, c, start, end)
    return fig


def corr_heatmap(df, ids, names, start=None, end=None, missing_df=None):
    """相关系数矩阵热力图（T3.3）：跨组多变量的两两 Pearson 相关。

    - pairwise 完整观测相关（每对变量用各自共同有效月，non-global-dropna）
    - 格子显示数值（.2f）+ 色阶 RdBu_r（红正蓝负），z∈[-1,1]
    - hover：变量A×变量B + 相关值 + 配对有效月数 n
    """
    data = _slice(df, start, end)[ids]
    z = data.corr()  # pandas 默认 pairwise complete obs
    n_mat = data.notna().T @ data.notna().astype(int)
    labels = {i: names[idx] for idx, i in enumerate(ids)}

    hover = ("<b>%{x}</b> × <b>%{y}</b><br>相关 %{z:.3f}"
             "<br>配对有效月 %{customdata}<extra></extra>")
    fig = go.Figure(layout=BASE_LAYOUT)
    fig.add_trace(go.Heatmap(
        z=z.values, x=[labels[i] for i in ids], y=[labels[i] for i in ids],
        zmin=-1, zmax=1, colorscale="RdBu_r",
        text=_np.round(z.values, 2),
        texttemplate="%{text}",
        customdata=n_mat.values,
        hovertemplate=hover,
        colorbar=dict(title="相关", thickness=12, len=0.7),
    ))
    n_vars = len(ids)
    if start is None or end is None:
        span = "全期"
    else:
        span = f"{start:%Y-%m}~{end:%Y-%m}"
    fig.update_layout(
        title=f"相关系数矩阵（{n_vars} 个变量，样本期 {span}）",
        xaxis=dict(title="变量（非时间）", tickangle=-35),
        yaxis=dict(title="变量（非时间）", autorange="reversed"),
        height=max(420, 120 + 46 * n_vars),
    )
    return fig


def _parse_horizon(target_id):
    """target_id 'forward_36m_state' → 36；loss_flag_36m → 36。"""
    import re
    mm = re.search(r"(\d+)m", target_id)
    return int(mm.group(1)) if mm else None


def forward_return_chart(df, col_x, name_x, targets, target_id, target_name,
                         start=None, end=None, color_mode="loss",
                         size_mdd=False, pit_meta=None):
    """前向收益对照（T3.4）：状态变量 X vs 未来 h 月收益（Phase 6 直觉）。

    - Y = targets_long 中 target_id（forward_{h}m_state/execution）按
      decision_month 对齐
    - color_mode=loss：盈利红（#e74c3c）/亏损绿（#27ae60）——A 股习惯
      红涨绿跌（M4 统一视觉常量前先用此语义）
    - color_mode=time：点色=年份小数（时间演化）
    - size_mdd：气泡大小=|future_max_drawdown_{h}m|（风险叠加）
    - hover：决策月/收益/状态值/路径起止/观测数
    - 横轴=状态变量（非时间），标注有效 n
    """
    h = _parse_horizon(target_id)
    sub = targets[targets["target_id"] == target_id].set_index("decision_month")
    y = sub["value"]
    x = df[col_x].copy()
    # 对齐：以 df.index（决策月）为准，target 缺失月 → NaN
    y_aligned = y.reindex([t.strftime("%Y-%m") for t in x.index])
    pair = pd.DataFrame({
        "x": x.values, "y": y_aligned.values,
        "loss": _np.nan, "mdd": _np.nan,
    }, index=x.index)
    # loss_flag 对齐（同期限）
    if h is not None:
        lf = targets[targets["target_id"] == f"loss_flag_{h}m"]
        if len(lf):
            lf = lf.set_index("decision_month")["value"]
            pair["loss"] = lf.reindex(
                [t.strftime("%Y-%m") for t in pair.index]).values
    # MDD 对齐（同期限，风险叠加用；与 pair 同索引，dropna 后自然对齐）
    if h is not None:
        mdf = targets[targets["target_id"] == f"future_max_drawdown_{h}m"]
        if len(mdf):
            mdf = mdf.set_index("decision_month")["value"]
            pair["mdd"] = mdf.reindex(
                [t.strftime("%Y-%m") for t in pair.index]).values
    pair = pair.dropna(subset=["x", "y"])
    # targets_long 读入时 keep_default_na=False 全列为 str，显式转数值
    # （'0.1037' → 0.1037；空串/缺失 → NaN；loss 0/1 同理）
    for c in ("y", "loss", "mdd"):
        pair[c] = pd.to_numeric(pair[c], errors="coerce")
    pair = pair.dropna(subset=["x", "y"])
    pair = _slice(pair, start, end)
    n = len(pair)

    cd = None
    hover = None
    if pit_meta:
        cd = []
        for ts in pair.index:
            m = ts.strftime("%Y-%m")
            mx = pit_meta.get((col_x, m), {})
            cd.append([m, mx.get("avail", ""), mx.get("source", "")])
        hover = ("<b>%{fullData.name}</b><br>决策月 %{customdata[0]}"
                 f"<br>前向收益 %{{y:.3f}}（{h or 0} 个月）"
                 "<br>%{customdata[2]} = %{x:.3f}（发布 %{customdata[1]}）"
                 "<extra></extra>")

    fig = go.Figure(layout=BASE_LAYOUT)
    size = [None] * n
    if size_mdd and pair["mdd"].notna().any():
        # 气泡大小 = |MDD| 缩放（MDD<=0，绝对值 0.1~0.7 → 6~24px）
        abs_mdd = pair["mdd"].abs().clip(0.05, 0.8)
        size = (6 + 22 * (abs_mdd - abs_mdd.min())
                / (abs_mdd.max() - abs_mdd.min() + 1e-9)).values

    if color_mode == "time":
        fig.add_trace(go.Scatter(
            x=pair["x"], y=pair["y"], mode="markers",
            name=target_name,
            marker=dict(size=size if size_mdd else 9,
                        color=_year_frac(pair.index),
                        colorscale="Viridis", showscale=True,
                        colorbar=dict(title="时间", thickness=12, len=0.7),
                        line=dict(color="white", width=0.5)),
            customdata=cd, hovertemplate=hover,
        ))
    else:  # loss 红涨绿跌（气泡模式也保留红绿，避免图例与实际颜色脱节）
        colors = [theme.UP_RED if (v == 0) else theme.DOWN_GREEN
                  for v in pair["loss"]]
        fig.add_trace(go.Scatter(
            x=pair["x"], y=pair["y"], mode="markers", name=target_name,
            marker=dict(size=size if size_mdd else 9,
                        color=colors,
                        line=dict(color="white", width=0.5)),
            customdata=cd, hovertemplate=hover,
        ))
        # 图例补充（loss 模式无连续色阶，用注解说明）
        fig.add_annotation(
            x=0.98, y=0.98, xref="paper", yref="paper", showarrow=False,
            align="right",
            text=(f"<span style='color:{theme.UP_RED}'>■</span> 盈利 "
                  f"<span style='color:{theme.DOWN_GREEN}'>■</span> 亏损"
                  + ("<br>气泡大小=|未来最大回撤|" if size_mdd else "")),
            font=dict(size=12), bgcolor=theme.NOTE_BG,
            bordercolor=theme.NOTE_BORDER, borderwidth=1,
        )
    fig.add_hline(y=0, line_dash="dot", line_color=theme.ZERO_LINE, line_width=1)
    fig.update_layout(
        title=f"{name_x} × {target_name}（有效 n = {n}）",
        xaxis_title=f"{name_x} 数值（非时间）",
        yaxis_title=f"未来 {h or ''} 个月收益",
    )
    return fig
