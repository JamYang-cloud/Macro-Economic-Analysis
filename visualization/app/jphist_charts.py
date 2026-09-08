#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""jphist_charts.py — JP-HIST 结构发现（M4）图表构建器（纯 plotly，无 streamlit 依赖）。

数据：render_jphist 一次性读入 snapshot 并传 dict `d`；本模块只画图。
纪律：凡“复现”= held-out 描述性方向复现；regime 为分类结论；hover 永远真实年份。
颜色约定：CN #c0392b / JP #2471a3；J90 #a93226 / J00 #e59866 亮amber 改 #d68910 / JGAP #7d6608 / OTHER #d5d8dc。
"""
import re
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ---------- 常量与辅助 ----------
REG4 = [("J90", 1991, 1998), ("JGAP", 1999, 2002), ("J00", 2003, 2011)]
REG_COLOR = {"J90": "#a93226", "JGAP": "#7d6608", "J00": "#d68910", "OTHER": "#c5c8cc"}
REG_CN = {"J90": "J90 日本1991-98·泡沫破裂停滞", "JGAP": "JGAP 过渡带1999-2002",
          "J00": "J00 日本2003-11·通缩低增长", "OTHER": "OTHER 其余可达段"}
CN_C, JP_C = "#c0392b", "#2471a3"
VAR_CN = {"real_gdp_yoy": "实际GDP增速", "iip_yoy": "工业产出增速", "investment_gdp": "投资率(GDP占比)",
          "cpi_yoy": "CPI 同比", "m2_yoy": "M2 同比", "export_yoy": "出口同比", "reer": "实际有效汇率",
          "wage_yoy": "工资增速", "birth_rate": "出生率变化(ΔCBR)"}
WINDOW_START = {"A": 2000, "B": 2005, "C": 2010, "D": 2015}
FONT = dict(family="Microsoft YaHei, PingFang SC, Noto Sans CJK SC, sans-serif")


def regime4_of(y):
    for r, lo, hi in REG4:
        if lo <= y <= hi:
            return r
    return "OTHER"


def note(d, key):
    """从 jphist_notes.csv 取 (value, source)。"""
    row = d["notes"].get(key)
    return (row["value"], row["source"]) if row is not None else ("", "")


def base_layout(title, height=460, **extra):
    lay = dict(template="plotly_white", title=title, height=height,
               margin=dict(l=70, r=70, t=64, b=44), font=FONT, **extra)
    return go.Figure(layout=lay)


def _ci_bounds(s):
    """'[a,b]' → (a,b)；空 → None。"""
    if not isinstance(s, str) or not s.startswith("["):
        return None
    m = re.match(r"\[([-\d.]+)\s*,\s*([-\d.]+)\]", s)
    return (float(m.group(1)), float(m.group(2))) if m else None


# ---------- G1 全景时间轴（JP 结构段色带 + CN 逐年归属） ----------
def fig_g1_timeline(d):
    seq = d["state_seq"]
    years = list(range(1970, 2026))
    codes = {r: i for i, r in enumerate(["OTHER", "J90", "JGAP", "J00"])}
    zrow = [codes[regime4_of(y)] for y in years]
    names = [REG_CN[regime4_of(y)] for y in years]
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.2, 0.8],
                        vertical_spacing=0.02,
                        subplot_titles=("🇯🇵 日本 1970-2025：结构段色带（J90/JGAP/J00/OTHER）",
                                        "🇨🇳 中国 2000-2025：逐年最相似日本结构段（hover=代表日本年）"))
    fig.add_trace(go.Heatmap(x=years, y=["JP"], z=[zrow], zmin=0, zmax=3,
                             colorscale=[[0, REG_COLOR["OTHER"]], [1 / 3, REG_COLOR["J90"]],
                                         [2 / 3, REG_COLOR["JGAP"]], [1, REG_COLOR["J00"]]],
                             showscale=False, customdata=[names], name="",
                             hovertemplate="%{x}年<br>%{customdata}<extra></extra>",
                             xgap=1), row=1, col=1)
    for _, r in seq.iterrows():
        fig.add_trace(go.Scatter(x=[int(r.cn_year)], y=[0], mode="markers+text",
                                 marker=dict(color=REG_COLOR[r.assigned_regime], size=11,
                                             line=dict(color="white", width=1)),
                                 text=[str(int(r.rep_jp_year))], textposition="top center",
                                 textfont=dict(size=9, color="#333"),
                                 customdata=[[f"{REG_CN[r.assigned_regime]}", int(r.rep_jp_year),
                                              round(float(r.S_total), 3)]],
                                 hovertemplate="%{x}年 · CN→JP %{customdata[1]} 年（%{customdata[0]}）"
                                               "<br>S_total=%{customdata[2]}<extra></extra>",
                                 showlegend=False, name=""), row=2, col=1)
    fig.update_xaxes(range=[1970, 2027], dtick=5, row=1, col=1)
    fig.update_xaxes(dtick=5, row=2, col=1)
    fig.update_yaxes(visible=False, row=1, col=1)
    fig.update_yaxes(visible=False, range=[-0.35, 1.15], row=2, col=1)
    fig.update_layout(title="两国结构态全景：日本的结构段 × 中国年份的归属（混合态、摆动）",
                      height=560, margin=dict(l=40, r=30, t=70, b=44), font=FONT)
    return fig


# ---------- G2 逐 CN 年 → 最相似日本年映射（2013-2025 主窗） ----------
def fig_g2_mapping(d):
    seq = d["state_seq"]
    sub = seq[(seq.cn_year >= 2013)].sort_values("cn_year")
    fig = base_layout("逐年中国年份 → 最相似日本年份（2013-2025 主窗；两法 13/13 一致）",
                      height=470)
    for r0, lo, hi, colr in [("J90", 1991, 1998, "#f5b7b1"), ("JGAP", 1999, 2002, "#d9d4c0"),
                             ("J00", 2003, 2011, "#f8c471")]:
        fig.add_hrect(y0=lo, y1=hi + 0.98, fillcolor=colr, opacity=0.35, line_width=0,
                      annotation_text=r0, annotation_position="right",
                      annotation_font=dict(color="#7b7b7b", size=11))
    fig.add_trace(go.Scatter(x=sub.cn_year, y=sub.rep_jp_year, mode="markers",
                             marker=dict(color=[REG_COLOR[r] for r in sub.assigned_regime],
                                         size=13, line=dict(color="white", width=1.2)),
                             customdata=[[f"{REG_CN[r]}", round(float(s), 3)]
                                         for r, s in zip(sub.assigned_regime, sub.S_total)],
                             hovertemplate="CN %{x} → JP %{y} 年<br>%{customdata[0]}"
                                           "<br>S_total=%{customdata[1]}<extra></extra>",
                             showlegend=False))
    fig.add_trace(go.Scatter(x=sub.cn_year, y=sub.rep_jp_year, mode="text",
                             text=sub.rep_jp_year.astype(int).astype(str),
                             textposition="top center", textfont=dict(size=10, color="#333"),
                             showlegend=False))
    fig.update_yaxes(title="最相似日本年份（regime-level argmax）", range=[1988.5, 2012.5])
    fig.update_xaxes(title="中国年份", dtick=1, range=[2012.4, 2026])
    fig.add_annotation(x=2025.6, y=1999.2, text="7/13 J90 · 4/13 J00 · 2/13 过渡带",
                       showarrow=False, font=dict(size=12, color="#333"))
    return fig


# ---------- G3 状态转移（4 态，含 JGAP） ----------
def fig_g3_transition(d):
    jg = d["jgap"].sort_values("cn_year").reset_index(drop=True)
    jg = jg[jg.cn_year >= 2013]
    sts = list(jg.state4)
    labels4 = ["J90", "JGAP", "J00", "OTHER"]
    links = {f"{a}->{b}": 0 for a in labels4 for b in labels4}
    for a, b in zip(sts[:-1], sts[1:]):
        links[f"{a}->{b}"] += 1
    src, tgt, val, colors = [], [], [], []
    for k, v in links.items():
        if v:
            a, b = k.split("->")
            src.append(labels4.index(a)); tgt.append(labels4.index(b)); val.append(v)
            colors.append(REG_COLOR[a])
    node_colors = [REG_COLOR[l] for l in labels4]
    fig = go.Figure(go.Sankey(
        arrangement="snap",
        node=dict(pad=18, thickness=22, line=dict(color="#fff", width=1),
                  label=[f"{l}<br>{REG_CN[l].split('·')[0]}" for l in labels4],
                  color=node_colors),
        link=dict(source=src, target=tgt, value=val, color=colors)))
    fig.update_layout(title="中国结构态逐年转移（2013-2025，4 态含 JGAP）——摆动而非推进",
                      height=470, margin=dict(l=20, r=20, t=64, b=40), font=FONT)
    return fig


# ---------- G4 滞后剖面与窗口模式（发现一） ----------
def _parse_lags(s):
    try:
        return [int(x) for x in str(s).split(",")]
    except Exception:
        return []


def fig_g4a_yearly_lag(d):
    grid = d["grid"]
    g = grid[(grid.metric == "MANHATTAN") & (grid.norm == "z1970-2025")].copy()
    fig = base_layout("逐年最相似滞后（MANHATTAN · z1970-2025 标定）：A-D 窗内 lag 的漂移",
                      height=420)
    for w in ["A", "B", "C", "D"]:
        row = g[g.window == w]
        if row.empty:
            continue
        lags = _parse_lags(row.iloc[0].all_lags)
        y0 = WINDOW_START[w]
        xs = [y0 + i for i in range(len(lags))]
        fig.add_trace(go.Scatter(x=xs, y=lags, mode="lines+markers", name=f"{w}窗(CN {y0}-{y0 + len(lags) - 1})",
                                 line=dict(width=1.6), marker=dict(size=5)))
    fig.add_hline(y=22, line_dash="dot", line_color="#888",
                  annotation_text="H4 中段候选 22 年（B 窗 cross-metric）", annotation_position="right")
    fig.update_xaxes(title="中国年份", dtick=2)
    fig.update_yaxes(title="最优滞后 lag（年）", range=[5, 50])
    return fig


def fig_g4b_window_norm_heatmap(d):
    grid = d["grid"]
    g = grid[grid.metric == "MANHATTAN"].copy()
    piv = g.pivot(index="window", columns="norm", values="best_lag_mode")
    piv = piv.reindex(index=["A", "B", "C", "D"])
    norms = [c for c in ["z1970-2000", "z1970-2025", "expanding_z", "rolling_z", "percentile"]
             if c in piv.columns]
    piv = piv[norms]
    fig = go.Figure(go.Heatmap(
        x=[f"{n}" for n in norms], y=[f"{w}窗" for w in ["A", "B", "C", "D"]],
        z=piv.values, text=piv.values.astype(int).astype(str), texttemplate="%{text}",
        textfont=dict(size=13, color="#333"), zmin=10, zmax=45,
        colorscale="YlOrRd", colorbar=dict(title="lag mode"),
        hovertemplate="%{y} × %{x}<br>best lag mode=%{text}<extra></extra>"))
    fig.update_layout(title="窗口 × 标准化口径 的 best-lag mode（MANHATTAN）——随 norm 漂移 ⇒ 无稳健单一滞后",
                      height=340, margin=dict(l=60, r=30, t=64, b=44), font=FONT)
    return fig


# ---------- G5 Held-out 机制验证森林图 ----------
def _ds_rows(d, norm="z1970-2025"):
    ds = d["dirscores"]
    return ds[ds.norm == norm].copy()


def fig_g5_forest(d):
    ds = _ds_rows(d)
    ds = ds.sort_values(["drop_type", "held_out_var"], kind="stable")
    ylab, yids = [], []
    for _, r in ds.iterrows():
        t = "通道" if str(r.drop_type) == "CHANNEL" else "变量级"
        ylab.append(f"{t}·{VAR_CN.get(str(r.held_out_var), r.held_out_var)}（{r.drop_id}）")
        yids.append(_)
    fig = base_layout("Held-out 机制验证：各通道退出分类器后的同向分离（主 norm z1970-2025）",
                      height=640)
    fig.add_vline(x=0, line_color="#999", line_width=1)
    for i, (yi, r) in enumerate(zip(yids, ds.itertuples())):
        ci = _ci_bounds(r.boot_ci90)
        if ci:
            lo, hi = ci
            fig.add_trace(go.Scatter(x=[lo, hi], y=[ylab[i], ylab[i]], mode="lines",
                                     line=dict(color="#666", width=5),
                                     showlegend=False, hoverinfo="skip"))
        col = {"Y": "#1e8449", "N": "#c0392b"}.get(str(r.sign_match), "#7f8c8d")
        marker = "diamond" if str(r.sign_match) == "Y" else ("x" if str(r.sign_match) == "N" else "circle")
        fig.add_trace(go.Scatter(x=[r.D_CN_negv], y=[ylab[i]], mode="markers",
                                 marker=dict(color=col, size=11, symbol=marker,
                                             line=dict(color="white", width=1)),
                                 customdata=[[r.held_out_var, r.D_JP,
                                              None if pd.isna(r.perm_p_2sided) else round(float(r.perm_p_2sided), 3),
                                              r.feasible, str(r.drop_id)]],
                                 hovertemplate=f"{VAR_CN.get(r.held_out_var, r.held_out_var)} · {r.drop_id}"
                                               "<br>D_CN(−v)=%{x:.3f}（D_JP 参照= %{customdata[1]:.3f}）"
                                               "<br>perm p=%{customdata[2]} · feasible=%{customdata[3]}"
                                               "<extra></extra>",
                                 showlegend=False, name=""))
        fig.add_trace(go.Scatter(x=[r.D_JP], y=[ylab[i]], mode="markers",
                                 marker=dict(color="#2471a3", size=6, symbol="diamond-open"),
                                 showlegend=False, hoverinfo="skip"))
    # 高亮核心三通道注释
    core_rows = ds[ds.drop_id.isin(["CH-CPI_YOY", "CH-INVESTMENT_GDP", "CH-REER"])]
    for r in core_rows.itertuples():
        fig.add_annotation(x=r.D_CN_negv, y=VAR_CN.get(r.held_out_var, r.held_out_var),
                           text="核心", showarrow=False,
                           font=dict(size=10, color="#2471a3"))
    fig.update_yaxes(autorange="reversed", title="")
    fig.update_xaxes(title="D = (CN→J90 组均值 − CN→J00 组均值) [robust-z 差]；实心=方向一致 · ✗=反向 · 空心菱=JP 参照")
    return fig


# ---------- G6 CPI 铰链坍缩对位 ----------
def fig_g6_cpi_collapse(d):
    ds = d["dirscores"]
    row = ds[(ds.drop_id == "CH-CPI_YOY") & (ds.norm == "z1970-2025")].iloc[0]
    jd = float(row.D_JP); cd = float(row.D_CN_negv)
    fig = base_layout("CPI 通道：分类器内最强分离 vs held-out 后坍缩（J90−J00 组均差）",
                      height=430)
    fig.add_trace(go.Bar(x=["JP 参照<br>J90 组 − J00 组", "CN held-out(−CPI)<br>重新分类后两组"],
                         y=[jd, cd], marker_color=["#2471a3", "#c0392b"],
                         text=[f"{jd:.3f}", f"{cd:.3f}"], textposition="outside",
                         textfont=dict(size=15, color="#333")))
    fig.add_annotation(x=1, y=max(jd, cd) * 0.4,
                       text=f"0.011 ≈ JP 差的 {cd / jd * 100:.1f}% · p=1.0 · CI 跨 0",
                       showarrow=False, font=dict(size=13, color="#a93226"))
    fig.add_annotation(x=0.5, y=-0.1,
                       text="近零 CPI 年份（2023/2025）的 J00 归属只靠 CPI 自身（自指铰链）——不是独立机制证据",
                       showarrow=False, font=dict(size=12, color="#333"))
    fig.update_yaxes(title="D（组均 robust-z 差）", range=[-0.35, 1.05])
    return fig


# ---------- G7 事件路径对照（CPI / 投资率） ----------
def fig_g7_paths(d):
    p = d["paths"]
    fig = make_subplots(rows=2, cols=1, shared_xaxes=False, vertical_spacing=0.12,
                        subplot_titles=("CPI 同比（%）：日本转负路径 vs 中国近零",
                                        "投资率（固定资本形成占 GDP，%）：高平台后长下行"))
    for (var, rowi) in [("cpi_yoy", 1), ("investment_gdp", 2)]:
        for country, colr, nm in [("JP", JP_C, "🇯🇵 日本"), ("CN", CN_C, "🇨🇳 中国")]:
            sub = p[(p.variable == var) & (p.country == country)].sort_values("year")
            fig.add_trace(go.Scatter(x=sub.year, y=sub.value, mode="lines+markers",
                                     name=f"{nm} {VAR_CN.get(var, var)}",
                                     line=dict(color=colr, width=2), marker=dict(size=4),
                                     hovertemplate=f"{nm} %{{x}}年：%{{y:.2f}}%<extra></extra>"),
                          row=rowi, col=1)
        if var == "cpi_yoy":
            fig.add_hline(y=0, line_color="#666", line_dash="dot", row=rowi, col=1)
            fig.add_vrect(x0=1999, x1=2005, fillcolor="#f5b7b1", opacity=0.15, line_width=0,
                          row=rowi, col=1)
            fig.add_annotation(x=2002, y=-1.15, text="JP 2002 −0.91%（最深）",
                               showarrow=False, font=dict(size=10, color="#a93226"), row=rowi, col=1)
            fig.add_annotation(x=2024, y=0.65, text="CN 0.2/0.2/0.0（未转负）",
                               showarrow=False, font=dict(size=10, color="#c0392b"), row=rowi, col=1)
    fig.update_layout(title="事件路径对照（只比形态/相对路径；两国 SNA 与绝对水平不可横比）",
                      height=640, margin=dict(l=60, r=30, t=70, b=44), font=FONT)
    fig.update_xaxes(title="年份", row=1, col=1)
    fig.update_xaxes(title="年份", row=2, col=1)
    return fig


# ---------- G8 两态机制画像（JP 侧 J90 vs J00 变量均差） ----------
def fig_g8_profiles(d):
    pj = d["profiles_jp"].copy()
    pj = pj.sort_values("diff_J90mJ00")
    ylab = [f"{VAR_CN.get(v, v)}（{m}）" for m, v in zip(pj.module, pj.variable)]
    fig = base_layout("JP 侧 J90 vs J00 变量画像（robust-z 组均值；分离轴 ≠ held-out 机制，对照机制验证 tab）",
                      height=560)
    fig.add_trace(go.Bar(x=pj.J90_mean, y=ylab, name="J90 (1991-98)", orientation="h",
                         marker_color="#a93226", opacity=0.85,
                         hovertemplate="%{y}<br>J90 mean z=%{x:.2f}<extra></extra>"))
    fig.add_trace(go.Bar(x=pj.J00_mean, y=ylab, name="J00 (2003-11)", orientation="h",
                         marker_color="#d68910", opacity=0.85,
                         hovertemplate="%{y}<br>J00 mean z=%{x:.2f}<extra></extra>"))
    fig.add_vline(x=0, line_color="#666", line_width=1)
    fig.update_layout(barmode="group", legend=dict(orientation="h", y=1.06))
    fig.update_xaxes(title="robust-z 均值（相对自身 1970-2025 全史）")
    return fig


# ---------- G9 模块分解 + 判别力 ----------
def fig_g9a_module_heat(d):
    lev = d["level"].copy()
    piv = lev.pivot(index="module", columns="regime_group", values="mean_Sm")
    piv = piv.reindex(index=["GROWTH", "INFLATION", "MONEY_CREDIT", "EXTERNAL", "DEMOGRAPHY_LABOR"],
                      columns=["J90", "J00", "OTHER"])
    fig = go.Figure(go.Heatmap(
        x=[f"{c}（CN→{c} 年组）" for c in ["J90", "J00", "OTHER"]],
        y=piv.index, z=piv.values,
        text=[[f"{v:.2f}" for v in row] for row in piv.values], texttemplate="%{text}",
        textfont=dict(size=13, color="white"), zmin=-1.5, zmax=0,
        colorscale="Reds_r", colorbar=dict(title="S_m（越近 0 越相似）"),
        hovertemplate="%{y} · %{x}<br>S_m=%{text}<extra></extra>"))
    fig.update_layout(title="模块水平相似度分解（S_total=(1/n)·ΣS_m；越近 0 越相似）——货币最似、人口/工资最不似",
                      height=340, margin=dict(l=40, r=30, t=64, b=44), font=FONT)
    return fig


def fig_g9b_discrimination(d):
    dm = d["discrim"].sort_values("mean_delta_m")
    fig = base_layout("J90 vs J00 判别力 Δ_m（各模块对‘分到哪一态’的区分贡献份额）",
                      height=330)
    fig.add_trace(go.Bar(x=dm.mean_delta_m, y=dm.module, orientation="h",
                         marker_color="#2471a3",
                         text=[f"{s * 100:.1f}%" for s in dm.delta_m_share],
                         textposition="outside",
                         hovertemplate="%{y}: mean Δ_m=%{x:.3f}<extra></extra>"))
    fig.add_annotation(x=0.47, y=4, text="单变量模块注：INFLATION=cpi_yoy、MONEY_CREDIT=m2_yoy",
                       showarrow=False, font=dict(size=11, color="#7f8c8d"))
    fig.update_xaxes(title="mean Δ_m（J90best−J00best 模块分差绝对值）")
    fig.update_yaxes(autorange="reversed")
    return fig


# ---------- G10 证据矩阵总览 ----------
_STATUS_COLOR = {"REJECTED": "#e6b0aa", "REJECTED AS GENERAL CLAIM": "#f5b7b1",
                 "NOT SUPPORTED": "#f5cba7", "SUPPORTED": "#a9dfbf",
                 "SUPPORTED DESCRIPTIVELY": "#f9e79f", "SECONDARY SUPPORT（non-gate）": "#aed6f1",
                 "CANDIDATE（偏弱）": "#d7bde2", "SUPPORTED（JP2 层）": "#aed6f1",
                 "DESCRIPTIVE（附录口径）": "#f9e79f"}


def fig_g10_evidence(d):
    ev = d["evidence"]
    fill = [_STATUS_COLOR.get(str(s), "#f0f3f4") for s in ev.status]
    fig = go.Figure(go.Table(
        header=dict(values=["ID", "结论（Claim）", "证据等级", "关键证据", "来源"],
                    fill_color="#2c3e50", font=dict(color="white", size=12),
                    align="left", height=30),
        cells=dict(values=[ev.claim_id, ev.claim, ev.status, ev.evidence_short, ev.freeze_ref],
                   fill_color=[["#fdfefe"] * len(ev), ["#fdfefe"] * len(ev), fill,
                               ["#fdfefe"] * len(ev), ["#fdfefe"] * len(ev)],
                   font=dict(size=11), align="left", height=26)))
    fig.update_layout(title="Evidence Matrix（E01-E19）——红=否定/不支持 · 绿=支持 · 黄=描述性",
                      height=760, margin=dict(l=10, r=10, t=60, b=20), font=FONT)
    return fig


# ---------- G11 监测（小图；指标卡在 render 层） ----------
def fig_g11_cn_cpi_recent(d):
    cpi = d["cn_cpi"]
    cpi = cpi[(cpi.year >= 2018)].sort_values("year")
    fig = base_layout("中国 CPI 同比（%）2018-2025：距 0 线（转负分界）还有多远", height=300)
    fig.add_trace(go.Bar(x=cpi.year, y=cpi.value, marker_color="#c0392b",
                         text=[f"{v:.1f}" for v in cpi.value], textposition="outside",
                         hovertemplate="%{x}年 CPI=%{y:.2f}%<extra></extra>"))
    fig.add_hline(y=0, line_color="#666", line_dash="dot",
                  annotation_text="转负分界（日本 1999 转负、2002 −0.91）", annotation_position="right")
    fig.update_yaxes(range=[-1.2, 3.6], title="%")
    return fig


def fig_g11_cn_investment(d):
    inv = d["cn_inv"].sort_values("year")
    fig = base_layout("中国投资率（占 GDP，%）2005-2024：峰值后长下行", height=300)
    fig.add_trace(go.Scatter(x=inv.year, y=inv.value, mode="lines+markers",
                             line=dict(color="#c0392b", width=2.2), marker=dict(size=5),
                             hovertemplate="%{x}年 %{y:.2f}%<extra></extra>"))
    pk = inv.loc[inv.value.idxmax()]
    fig.add_annotation(x=int(pk.year), y=float(pk.value), text=f"峰值 {int(pk.year)} {float(pk.value):.1f}%",
                       showarrow=True, arrowhead=2, font=dict(size=11, color="#a93226"))
    fig.update_yaxes(title="%")
    return fig
