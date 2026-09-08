#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""render_jphist.py — JP-HIST 结构发现（M4）视图：把 JP-HIST H0-H5 冻结发现系统化呈现。
数据：08_可视化/data_snapshot_jphist/（只读快照，SHA manifest 可验证；FROZEN 原件不被触碰）。
纪律：每条图下方自动图注（发现/口径/禁读句）；hover 永远真实年份/编号。
"""
from pathlib import Path

import pandas as pd
import streamlit as st

from core import charts
from jphist_charts import (fig_g1_timeline, fig_g2_mapping, fig_g3_transition,
                           fig_g4a_yearly_lag, fig_g4b_window_norm_heatmap, fig_g5_forest,
                           fig_g6_cpi_collapse, fig_g7_paths, fig_g8_profiles,
                           fig_g9a_module_heat, fig_g9b_discrimination, fig_g10_evidence,
                           fig_g11_cn_cpi_recent, fig_g11_cn_investment)

SNAP = Path(__file__).resolve().parent.parent / "data_snapshot_jphist"
_CSV = {"state_seq": "h5_state_sequence.csv", "sanity": "h5_sanity_vs_cluster.csv",
        "jgap": "h5final_jgap_sequence.csv", "level": "h5_h51_summary_level_by_regime.csv",
        "discrim": "h5_h51_summary_discrimination.csv", "lomo": "h5_h51_summary_lomo.csv",
        "profiles_jp": "h5_regime_profiles_jp.csv", "contrast": "h5_regime_profile_contrast.csv",
        "cf": "h5_cf_flip_summary.csv", "dirscores": "h5final_direction_scores.csv",
        "paths": "h5final_eventtime_paths.csv", "grid": "h4v03e_grid.csv",
        "evidence": "evidence_matrix.csv", "kf": "key_figures.csv",
        "cn_cpi": "annual_CN_cpi_yoy.csv", "cn_inv": "annual_CN_investment_gdp.csv",
        "cn_m2": "annual_CN_m2_yoy.csv"}


@st.cache_data(show_spinner=False)
def _read(fn):
    return pd.read_csv(SNAP / fn, encoding="utf-8-sig")


def load_data():
    d = {}
    for k, fn in _CSV.items():
        d[k] = _read(fn)
    n = _read("jphist_notes.csv")
    d["notes"] = {r.key: r for r in n.itertuples()}
    for k in ["state_seq", "jgap"]:
        d[k] = d[k][d[k].cn_year.notna()].copy()
    return d


def _n(d, key):
    row = d["notes"].get(key)
    return row.value if row is not None else ""


def show(fig):
    st.plotly_chart(charts.style_title(fig), width="stretch")


def note_caption(d, keys):
    for k in keys:
        row = d["notes"].get(k)
        if row is not None:
            st.caption(f"🔖 {row.value}（{row.source}）")


def render_jphist():
    st.subheader("🧭 JP-HIST 结构发现（长期结构比较层 H0-H5 · 全链冻结）")
    st.caption("回顾性结构态比较（非 PIT/非预测/非投资信号）：以日本 1970-2025 为参照系，看中国 2000-2025 的宏观结构态"
               "落在日本的哪个结构段（regime）、相似背后有没有可独立验证的机制。结论与数字全部来自冻结链"
               "FREEZE_H0..H5 与报告；图表数据只读 data_snapshot_jphist/（SHA manifest 可验证）。")
    d = load_data()

    t1, t2, t3, t4, t5 = st.tabs(
        ["总览与证据矩阵", "时间轴与状态归属", "滞后与窗口模式", "机制验证（held-out）", "路径与监测"])

    # ---------------- tab1 总览 ----------------
    with t1:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("两法归属一致", "13 / 13", "2013-2025 逐年")
        c2.metric("最相似日本段", "J90 ×7 · J00 ×4", "另 2 年落 JGAP 过渡带")
        c3.metric("persistent J00", "无", "P(J00→J00)=0 · 2024 回落 JGAP")
        c4.metric("held-out 机制通道", "1 + 1", "investment（核心）· M2（次级）")
        st.markdown("**核心结论一览**：① 无稳健单一固定滞后（30-40 年/22 年均只局部成立）；② 中国像的是“两个日本”"
                    "（1991-98 停滞主体 × 2003-11 通缩段）且在两态间摆动，非单调推进；③ 低通胀/近零 CPI 本身不足以证明日本化"
                    "（CPI 是分类铰链而非独立机制，2023-25 未转负）；④ 唯一 held-out 同向复现=投资率通道（+M2 次级，均描述性）；"
                    "⑤ 广泛共同机制对应未获支持=主结论。")
        show(fig_g10_evidence(d))
        note_caption(d, ["discipline"])

    # ---------------- tab2 时间轴与归属 ----------------
    with t2:
        show(fig_g1_timeline(d))
        st.caption("上轨=日本 1970-2025 的结构段色带（J90/JGAP/J00/OTHER）；下轨=中国每年最相似的日本结构段，"
                   "点上方数字为该年最相似的日本年份。色块一致的颜色=属于同一结构段——直观看出“两个日本 + 摆动”。")
        show(fig_g2_mapping(d))
        st.caption("2013-2025 主窗：每一年→最相似日本年份。7 年落 J90、4 年落 J00、2 年（2015/2024）落 JGAP 过渡带；"
                   "2024 → 2002（日本 CPI 最深 −0.91% 之年）。阴影带=日本结构段年份区间。")
        show(fig_g3_transition(d))
        note_caption(d, ["mixed_13", "q3_no_persist", "jgap_diag"])

    # ---------------- tab3 滞后与窗口 ----------------
    with t3:
        show(fig_g4a_yearly_lag(d))
        st.caption("每个窗口内，逐年最优滞后在 10-45 年间漂移（无稳定平台）——这是“没有单一固定滞后”的逐年视角证据。")
        show(fig_g4b_window_norm_heatmap(d))
        note_caption(d, ["b_window_l22", "d_window_p", "no_robust_single_lag"])
        st.caption("读法：22 年只在 B 窗（cross-metric 4/4）与 D 窗（MANHATTAN p=0.0009）等特定窗口×口径下出现；"
                   "换标准化口径/窗口即漂移。禁止外推成“中国滞后日本 N 年”。")

    # ---------------- tab4 机制验证 ----------------
    with t4:
        show(fig_g5_forest(d))
        st.caption("横轴=把该通道移出分类器后重新分类的两组（CN→J90 vs CN→J00）在该通道上的组均差（D_CN,−v）；"
                   "空心菱形=日本两态的参照差（D_JP）；✗=方向与日本相反。绿色实心=方向一致且 bootstrap 90% CI 不含 0"
                   "（held-out 方向性复现，perm p 未达 10%，描述性）。")
        show(fig_g6_cpi_collapse(d))
        show(fig_g8_profiles(d))
        show(fig_g9a_module_heat(d))
        show(fig_g9b_discrimination(d))
        note_caption(d, ["cpi_hinge", "inv_replication", "m2_secondary"])

    # ---------------- tab5 路径与监测 ----------------
    with t5:
        show(fig_g7_paths(d))
        st.caption("CPI：日本 1999 起转负、2002 最深 −0.91%；中国 2023-2025 = 0.2/0.2/0.0 未转负（阴影=日本负区间）。"
                   "投资率：日本峰值 1990 31.7%→2000 25.6%（−19.3%）；中国峰值 2011 48.3%→2024 40.5%（−16.2%，未止跌）——"
                   "同为高平台后长下行；两国 SNA/绝对水平不可横比，只比相对形态。")
        st.markdown("**监测面板**（数据止于 2025 · 时间戳化 · 非交易信号）：")
        cpi = d["cn_cpi"]; inv = d["cn_inv"]
        cpi_l = cpi.sort_values("year").iloc[-1]
        cpi_23 = float(cpi[cpi.year == 2023].value.iloc[0]) if (cpi.year == 2023).any() else None
        inv_l = inv.sort_values("year").iloc[-1]
        inv_pk = inv.loc[inv.value.idxmax()]
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("CPI（最近年）", f"{float(cpi_l.value):.1f}%", "2023-25: 0.2/0.2/0.0 · 未转负")
        m2.metric("距转负分界", "0 线上方", "日本 1999 转负 · 2002 −0.91%")
        m3.metric("投资率（最近年）", f"{float(inv_l.value):.1f}%",
                  f"距峰值({int(inv_pk.year)} {float(inv_pk.value):.1f}%) −{float(inv_pk.value - inv_l.value):.1f}pp")
        st_c = d["state_seq"]
        last = st_c.sort_values("cn_year").iloc[-1]
        m4.metric("2025 状态归属", str(last.assigned_regime), f"→ JP {int(last.rep_jp_year)} 年")
        show(fig_g11_cn_cpi_recent(d))
        show(fig_g11_cn_investment(d))
        st.caption("关键分界：未来值得警惕的不是“低通胀”本身，而是「CPI 持续转负 + 投资率与 M2 同向走低」的组合——"
                   "那才接近日本 2000 年代结构的信号；M2 最新读数与完整货币序列请在 M3/🇯🇵 视图对照（本快照不含现值面板）。")
        note_caption(d, ["cn_cpi_near0", "cn_inv_path"])
