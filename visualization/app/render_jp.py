#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
render_jp.py — 日本数据模块（M2，中日可视化扩展 P3/v3）

v3：应「数据源三选一 → 统一变量池」需求——state/序列库/早期段/股市全部并入
一个选择空间（约 49 列、1949-05 ~ 2026-07 统一月首轴），变量自由组合同图，
如「M2同比 vs 日经225」直接可比。数据层走 core/country.load_jp_pool()
（data_snapshot + early_history 只读副本；6 条与 state 同源的 PIT 原始序列已隐藏）。

工具：数据浏览（主池）/ 日经225分析（日次·重基·12m 视角）/ PIT 序列下钻 /
      12-target 视图 / 当前读数。JP 增值：政策 regime 底色。用户可见名中文。
"""

import math
import os
import re
from datetime import datetime

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from core import charts, country, loader

JP_TOOLS = ["数据浏览(统一池)", "日经225分析", "PIT 序列下钻", "12-target 视图", "当前读数"]


@st.cache_data
def _pool_cached(_sig):
    return country.load_jp_pool()


def cached_pool():
    # data_sig：JP-HIST 注册表内容变更自动失效（2026-09-08）
    return _pool_cached(loader.data_sig())


@st.cache_data
def cached_state(branch):
    return country.load_jp_state(branch)


@st.cache_data
def cached_targets():
    return country.load_jp_targets()


@st.cache_data
def cached_descriptive():
    return country.load_jp_descriptive()


def add_regime_bands(fig, bands, start=None, end=None, visible=True):
    """政策 regime 底色：每段自起画到下一段起（末段至窗口末）。"""
    if not visible or not bands:
        return fig
    lo = pd.Timestamp(start) if start is not None else None
    hi = pd.Timestamp(end) if end is not None else None
    starts = [ts for ts, _ in bands]
    for i, (ts, _n) in enumerate(bands):
        x0 = ts if lo is None else max(ts, lo)
        x1 = starts[i + 1] if i + 1 < len(starts) else hi
        if x1 is None or x1 <= x0:
            continue
        fig.add_vrect(x0=x0, x1=x1, fillcolor="rgba(128,128,128,0.07)",
                      line_width=0, layer="below")
    return fig


def regime_band_annotations(bands, start, end):
    lo, hi = pd.Timestamp(start), pd.Timestamp(end)
    segs = []
    for i, (ts, name) in enumerate(bands):
        x0 = max(ts, lo)
        x1 = bands[i + 1][0] if i + 1 < len(bands) else hi
        if x1 <= x0:
            continue
        segs.append(f"{name}（{x0.strftime('%Y-%m')}~{x1.strftime('%Y-%m')}）")
    return segs


def _month_options(df):
    return [d.strftime("%Y-%m") for d in df.index]


def _summary_table(sub, sel, meta, label):
    rows = []
    for c in sel:
        s = sub[c].dropna()
        if len(s) == 0:
            rows.append({"变量": meta[c]["name_cn"], "单位": meta[c]["unit"],
                         "有效月数": 0, "最新值": "", "最小@月": "", "最大@月": ""})
            continue
        rows.append({"变量": meta[c]["name_cn"], "单位": meta[c]["unit"],
                     "有效月数": len(s), "最新值": round(float(s.iloc[-1]), 3),
                     "最小@月": f"{s.min():.3f}@{s.idxmin().strftime('%Y-%m')}",
                     "最大@月": f"{s.max():.3f}@{s.idxmax().strftime('%Y-%m')}"})
    st.caption(label)
    st.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True)


def _chart(df, sel, labels, start, end, scale, mode, chart_type,
           right_var, log_y):
    if mode == "叠加":
        if chart_type == "折线":
            return charts.line_chart(df, sel, [labels[c] for c in sel],
                                     start, end, scale=scale, log_y=log_y)
        if chart_type == "面积":
            return charts.area_chart(df, sel, [labels[c] for c in sel],
                                     start, end, scale=scale, log_y=log_y)
        if chart_type == "阶梯":
            return charts.step_chart(df, sel, [labels[c] for c in sel],
                                     start, end, scale=scale, log_y=log_y)
        if chart_type == "双轴" and right_var is not None and right_var != sel[0]:
            return charts.dual_axis(df, sel[0], labels[sel[0]],
                                    right_var, labels[right_var], start, end,
                                    scale=scale, log_y=log_y)
    else:
        return charts.facet_figures(df, [(c, labels[c], "折线") for c in sel],
                                    start, end, scale=scale, log_y=log_y)
    return None


def render_jp():
    """日本数据模块：统一变量池主浏览 + 5 个分析工具。"""
    df, meta = cached_pool()
    level_note = {"state": "决策网格口径", "pit": "PIT 月度化",
                  "early": "早期段(COMPARISON-ONLY)", "market": "股市(代理)",
                  "jphist": "补充数据·年度(每年12月落点)",
                  "h6b": "补充数据·季度(季首落点)"}
    st.subheader("日本数据模块 · 统一变量池（1949-05 ~ 2026-07，月首轴）")
    st.caption("池 = 月度状态面板(7 MODEL_X+3审计) ∪ PIT 序列库(33) ∪ 早期段(5) ∪ 日经225 全史 ∪ "
               "补充数据·年度(8，每年12月单点) ∪ 补充数据·季度(11，季首单点)。"
               "所有变量同一选择空间自由组合——例：M2同比 与 日经225 同图。"
               "level 标注：state=决策网格 / pit=PIT月度化 / early=比对专用 / market=股价代理 / "
               "jphist=补充数据·年度 / h6b=补充数据·季度（冻结链副本，展示专用）。")

    with st.sidebar:
        groups_all = sorted({m["group"] for m in meta.values()})
        audit_groups = [g for g in groups_all if "审计" in g]
        hide_groups = [g for g in groups_all if "序列库-其他" == g]
        # 默认全开（审计组收起），让用户看到全部家底
        sel_groups_default = [g for g in groups_all if g not in audit_groups]
        sel_groups = st.multiselect("数据分组", groups_all,
                                    default=sel_groups_default, key="jp_groups")
        feats = [c for c in df.columns if c in meta and meta[c]["group"] in sel_groups]
        if not feats:
            st.warning("请至少选择一个分组"); st.stop()
        order = [c for c in df.columns if c in feats]
        labels = {c: meta[c]["name_cn"] for c in order}
        hint = [c for c in ("m2_yoy_canonical", "日经225收盘价(月末·全史proxy)",
                            "tankan_mfg_di", "JGB10Y_FRED")
                if c in order][:3]
        sel = st.multiselect("选择变量（同图组合）", order, default=hint,
                             format_func=lambda c: labels[c])
        if not sel:
            st.info("请选择至少一个变量"); st.stop()
        scale = st.radio("观察尺度", ["月", "季", "年"], horizontal=True,
                         key="jp_scale")
        mode = st.radio("图表模式", ["叠加", "分面"], horizontal=True,
                        key="jp_mode")
        chart_type = st.radio("图形类型", ["折线", "双轴", "面积", "阶梯"],
                              key="jp_chart")
        right_var = None
        if chart_type == "双轴" and len(sel) >= 2:
            right_var = st.selectbox("右轴变量", [c for c in sel if c != sel[0]],
                                     format_func=lambda c: labels[c])
        log_y = st.checkbox("对数轴") if chart_type in ("折线", "面积", "阶梯") else False
        regime_on = st.checkbox("显示政策 regime 底色", value=True)
        months = _month_options(df)
        m_start = st.selectbox("起始月", months, index=months.index("1995-01"),
                               key="jp_mstart")
        m_end = st.selectbox("结束月", months, index=len(months) - 1,
                             key="jp_mend")
        if m_start > m_end:
            m_start, m_end = m_end, m_start
        tool = st.radio("日本分析工具", JP_TOOLS, index=0)
        do_export = st.button("导出 PNG", width="stretch", key="jp_export")

    start, end = pd.Timestamp(m_start), pd.Timestamp(m_end)
    st.caption(" | ".join(f"{c}：{level_note.get(meta[c].get('level',''),'')}"
                          for c in sel[:6]) or "")

    if tool.startswith("数据浏览"):
        fig = _chart(df, sel, labels, start, end, scale, mode, chart_type,
                     right_var, log_y)
        if fig is None:
            st.info("请选择变量/图形类型")
            return
        if regime_on:
            fig = add_regime_bands(fig, country.load_jp_regime_df_for_axis(),
                                   start, end)
        st.plotly_chart(fig, width="stretch")
        if regime_on:
            st.caption("政策 regime： " + " ｜ ".join(
                regime_band_annotations(country.load_jp_regime_df_for_axis(),
                                        m_start, m_end)))
        _summary_table(df.loc[start:end, sel], sel, meta,
                       f"数据摘要（{m_start} ~ {m_end}；缺失=该月无发布/不可知）")
        if do_export:
            _export_jp(fig, " / ".join([labels[c] for c in sel]),
                       m_start, m_end)
    elif tool.startswith("日经225分析"):
        _tool_nikkei()
    elif tool.startswith("PIT"):
        _tool_pit()
    elif tool.startswith("12-target"):
        _tool_targets()
    else:
        _tool_descriptive()


def _tool_nikkei():
    """日经225 分析视角（日次/重基/12m 变化）——与主池的月末列互补。"""
    with st.sidebar:
        src = st.radio("股价范围", ["1985-2026（FROZEN 副本）", "1949-2026（全史 early）"],
                       index=0)
        view = st.radio("呈现", ["收盘价", "对数收盘", "相对1990年初(重基100)",
                                "12个月变化"], index=0)
        months_show = st.radio("数据频率", ["月末", "全部交易日"], index=0)
        regime_on = st.checkbox("显示政策 regime 底色", value=False)
    use_full = src.startswith("1949")
    s = country.load_jp_nikkei_monthly("full" if use_full else "snapshot")
    st.caption("日经225（Nikkei 225，PRICE PROXY）：官方源=日経平均；FRED 镜像日次收盘。"
               "2023-2026 与日経官网直链 899 交易日 0 mismatch（JP1.9 审计）。"
               "TOPIX 配当込み（TRI）Gate C 未解 → 一律标注代理。"
               "锚点：1989-12 泡沫顶 38,915 → 2009-03 谷底 7,054 → 2024-02 新高 39,098。")
    if months_show.startswith("全部"):
        base = s
        title_ext, pc_periods = "日次收盘", 252
    else:
        base = s.resample("M").last()
        title_ext, pc_periods = "月末收盘", 12
    base = base.dropna()
    if view.startswith("对数"):
        y = base.apply(math.log)
        ylabel, t2 = "log(点)", "对数收盘"
    elif view.startswith("相对"):
        ref = base[base.index >= "1990-01"].iloc[0]
        y = base / ref * 100
        ylabel, t2 = "指数(1990-01=100)", "重基100"
    elif view.startswith("12"):
        y = base.pct_change(pc_periods) * 100
        ylabel, t2 = "%", "12个月变化"
    else:
        y = base
        ylabel, t2 = "点", "收盘价"
    f = go.Figure(go.Scatter(x=y.index, y=y.values, mode="lines",
                             line=dict(color="#c0392b", width=1.5),
                             name="日经225"))
    if regime_on:
        f = add_regime_bands(f, country.load_jp_regime_df_for_axis(),
                             y.index[0], y.index[-1])
    f.update_layout(template="plotly_white",
                    title=f"日经225 · {t2}（{title_ext}，{y.index[0].date()} ~ {y.index[-1].date()}）",
                    margin=dict(l=60, r=40, t=60, b=40), hovermode="x unified",
                    yaxis_title=ylabel)
    st.plotly_chart(f, width="stretch")
    rows = []
    for d in ("1989-12-29", "2009-03-10", "2024-02-22"):
        try:
            v = s.loc[d] if d in s.index else s.asof(d)
            rows.append({"锚点日期": d, "日经225收盘(最近可知)": round(float(v), 2)})
        except Exception:  # noqa: BLE001
            pass
    st.caption("锚点核对：1989-12-29=38,915.87（泡沫顶）/ 2009-03-10=7,054.98（谷底）/ 2024-02-22=39,098.68（新高）")
    st.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True)


def _tool_pit():
    series_list = country.list_jp_pit_series()
    with st.sidebar:
        sid = st.selectbox("PIT 序列", series_list, index=0)
    st.caption("39 条 PIT 冻结序列（JP1.6 FROZEN 副本）：官方/镜像、vintage 元数据随序列附。")
    ps = country.load_jp_pit_series(sid)
    if ps is None or ps["value"].dropna().empty:
        st.warning("序列为空"); return
    a = ps.attrs
    st.caption(f"{sid} ｜ vintage={a.get('vintage_type', '')} ｜ 源：{a.get('source_file', '')}")
    s2 = ps["value"].dropna()
    f2 = go.Figure(go.Scatter(x=s2.index, y=s2.values, mode="lines",
                              line=dict(color="#c0392b", width=1.6),
                              connectgaps=False, name=sid))
    f2.update_layout(template="plotly_white",
                     title=f"{sid} · 原始 PIT 值（{s2.index[0].date()} ~ {s2.index[-1].date()}）",
                     margin=dict(l=60, r=40, t=60, b=40), hovermode="x unified")
    st.plotly_chart(f2, width="stretch")


def _tool_targets():
    st.caption("NIKKEI225 PRICE PROXY 12-target（代理；TOPIX TRI canonical Gate C 未解）。"
               "h = 未来 36/60/120 月；state=决策月口径，exec=下一实际交易日执行口径。")
    tdf = cached_targets()
    with st.sidebar:
        tkind = st.radio("target 类型", ["state", "exec", "loss", "mdd"],
                         format_func=lambda t: {
                             "state": "未来收益 State", "exec": "执行收益 Exec",
                             "loss": "亏损标记 Loss", "mdd": "最大回撤 MDD"}[t])
    cols = [f"fwd{h}m_{tkind}" for h in (36, 60, 120)
            if f"fwd{h}m_{tkind}" in tdf.columns]
    if not cols:
        st.info("该类型无列"); return
    f3 = go.Figure(layout=dict(template="plotly_white",
                               margin=dict(l=60, r=40, t=60, b=40)))
    pal = ["#c0392b", "#2471a3", "#1e8449"]
    for i, c in enumerate(cols):
        s = tdf[c].dropna()
        f3.add_trace(go.Scatter(x=s.index, y=s.values, mode="lines",
                                name=f"{c.split('m_')[0]}个月"
                                + ("" if tkind != "loss" else " 1=亏损"),
                                line=dict(color=pal[i], width=1.8),
                                connectgaps=False))
    f3.update_layout(title=f"日经225(代理) 未来收益/回撤 · {tkind}",
                     hovermode="x unified", yaxis_title="% (loss 为 0/1)")
    st.plotly_chart(f3, width="stretch")


def _tool_descriptive():
    desc = cached_descriptive()
    st.caption("当前状态快照（2026-09-05）：最新可知值 + 陈旧度。终止/停更镜像标注陈旧，不当作当前读数。")
    rows = []
    for _, r in desc.iterrows():
        rows.append({"特征": r["feature_id"], "值日期": r["value_date"],
                     "值": r["value"],
                     "状态": f"{r['series_status']}(陈旧{r['stale_age_months']}月)"
                             if str(r.get("is_stale")).lower() == "true"
                             else r["series_status"],
                     "vintage": str(r["vintage_note"])[:44]})
    st.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True)


def _export_jp(fig, fig_title, m_start, m_end):
    try:
        from core import export as _e
        out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                           "exports")
        os.makedirs(out, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        topic = re.sub(r'[\\/:*?"<>|]', "_", fig_title)
        png = os.path.join(out, f"JP_{ts}_{topic}.png")
        _e.export_png(fig, png, title=f"{fig_title}  {m_start} ~ {m_end}")
        st.success(f"已导出: {png}")
        with open(png, "rb") as f:
            st.download_button("下载 PNG", f.read(),
                               file_name=os.path.basename(png), mime="image/png")
    except Exception as e:  # noqa: BLE001
        st.error(f"导出失败: {e}")
