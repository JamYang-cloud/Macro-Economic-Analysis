#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
render_compare.py — 中日对比模块（M3，中日可视化扩展 P4）

crosswalk_v1 概念族对齐（首版可出图 12 族；pro.house_price 因 CN 房价未入
可视化快照面板而降级）。核心能力：
  - 双窗口 + 锚点对齐（用户例：CN 2015-2025 ↔ JP 1995-2005 同框叠合）
  - 对齐轴：两窗窗首=0，同图叠比较形态；hover 永远显示真实年月
  - 日历轴：上下对照双图（各自真实日历时间）
  - 尺度：直出（同单位%）/ 重基100（窗首=100）/ 双 Y 轴
  - 图注强制可比性声明（comparability A/B/C + 单位 + 源通道 + proxy 标注）
数据：CN = loader.load_combined()（data_snapshot_v2 只读）；JP = country 池/early。
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.subplots as sp
import streamlit as st

from core import country, loader

# CN registry id → 可视化快照实际列（registry 104 含未入 state 面板者；mean 版为面板列）
CN_COL_FIX = {"rate.fr007": "rate.fr007_mean", "rate.shibor_on": "rate.shibor_on_mean"}
# pro.house_price 无值列 → 首版降级（CN 房价未入可视化快照）

# JP crosswalk id → 取数通道（pool 列名 / early key / 特判）
def _jp_getter():
    return None  # 见 jp_series(id, pool)


def jp_series(jp_id, pool):
    """返回 (Series(月首), 说明)。"""
    if jp_id in pool.columns:
        return pool[jp_id].dropna(), "JP 池（state/pit 月度化）"
    early_map = {
        "ppi_manufacturing_1960": "ppi",
        "discount_rate_boj_1953": "discount_rate",
        "retail_sales_mom_1955": "retail_mom",
        "nikkei225_daily_full_1949": "nikkei225_full",
        "gdp_real_yoy_fy_1955_cao": "gdp_real_yoy",
    }
    if jp_id in early_map:
        s, em = country.load_jp_early(early_map[jp_id])
        key = early_map[jp_id]
        v = s.iloc[:, 0]          # early 文件第二列名各异（load_jp_early 保留原名）
        if key == "retail_mom":   # MoM% → 12m 连乘同比（crosswalk C 级标注）
            m = v / 100.0 + 1.0
            yoy = (m.rolling(12).apply(lambda x: x.prod(), raw=True) - 1.0) * 100.0
            s = pd.DataFrame({"value": yoy}, index=s.index)
            note = "JP 零售 MoM% 自算 12 月连乘同比（镜像）"
        elif key == "nikkei225_full":   # 日次 → 月末
            s = s.resample("M").last()
            note = "JP 日经225 日次→月末（全史 PRICE PROXY）"
        elif key == "gdp_real_yoy":     # FY 年度 → 月平台（直接读 real_yoy_pct 第4列）
            import os as _os
            gdf = pd.read_csv(_os.path.join(country.JP_EARLY, country.JP_EARLY_FILES["gdp_real_yoy"]),
                              encoding="utf-8-sig")
            gy = pd.to_numeric(gdf["real_yoy_pct"].astype(str).str.replace(",", "", regex=False),
                               errors="coerce")
            gidx = pd.to_datetime(gdf["fy_year"].astype(str), format="%Y", errors="coerce")
            s = pd.DataFrame({"value": gy.values}, index=gidx)
            s = s.resample("M").ffill()
            note = "JP 実質GDP FY年度增速（内閣府 1955-2022；年度值延展为月平台）"
        else:
            note = f"JP 早期段（{em['freq']}）"
        s = s.iloc[:, 0].dropna()
        s.index = s.index.to_period("M").to_timestamp()
        return s, note
    return None, ""


CN_SOURCE_NOTE = "CN 可视化快照（data_snapshot_v2，2008-01 起）"


@st.cache_data
def cached_crosswalk():
    return country.load_crosswalk()


@st.cache_data
def _cn_combined_cached(_sig):
    return loader.load_combined()


def cached_cn_combined():
    return _cn_combined_cached(loader.data_sig())


@st.cache_data
def _pool_c_cached(_sig):
    return country.load_jp_pool()


def cached_pool_c():
    return _pool_c_cached(loader.data_sig())


def available_families():
    """首版可出图族 + CN 面板可用性核对 → 仅返回 CN 面板有值列的族。"""
    cw = cached_crosswalk()
    comb = cached_cn_combined()
    fams = []
    for i, r in cw.iterrows():
        if str(r["m3_first_release"]).strip().upper() != "TRUE":
            continue
        cn_col = CN_COL_FIX.get(r["cn_variable_id"], r["cn_variable_id"])
        if cn_col in comb.columns:
            fams.append((i, r))
    return fams


def family_window(r, cn_col, cn_s, jp_s):
    """窗口统一长度：CN [cn_s, +L) / JP [jp_s, +L)；返回各自子序列+说明。"""
    return r, cn_s, jp_s


def render_compare():
    """中日对比（M3）三数据层：月频=原 crosswalk v1（零改动）；年度=JP-HIST 重点族（featured）；
    季度=H6-B 机制/通缩机制族（featured，季首落点）。"""
    st.subheader("中日对比模块（M3） · 三数据层：月频概念族 / 年度重点族（JP-HIST）/ 季度机制族（H6-B）")
    with st.sidebar:
        layer = st.radio("对比数据层", ["月频概念族（crosswalk v1）", "年度重点族（JP-HIST）",
                                      "季度机制族（H6-B）"], index=0, key="m3_layer")
    if layer.startswith("季度"):
        _quarterly_compare_view()
    elif layer.startswith("年度"):
        _annual_compare_view()
    else:
        _monthly_compare_view()


def _monthly_compare_view():
    st.caption("月频概念族（crosswalk v1）：把中国近年的形态与日本早 20-40 年的历史叠在一起看——锚点对齐后只比较形态与量级路径，"
               "不暗示因果。JP 侧代理/镜像/早期段均有标注；可比性等级 A=同口径直接可比 / "
               "B=近似可比 / C=形态可比（见 crosswalk notes）。")
    fams = available_families()
    comb = cached_cn_combined()
    pool, _ = cached_pool_c()

    fam_labels = []
    fam_idx = []
    for i, r in fams:
        fam_labels.append(f"{r['concept_family']}  [{r['comparability']}]"
                         f" CN:{r['cn_name']} ↔ JP:{r['jp_name']}")
        fam_idx.append(i)
    if not fam_labels:
        st.warning("crosswalk 无可比族（CN 面板可用列核对后为空）"); return
    st.caption("首版可出图 12 族（crosswalk m3_first_release=TRUE ∩ CN 面板有值）；"
               "房价族因 CN 房价未入可视化快照面板暂降级。")
    with st.sidebar:
        fam_sel = st.selectbox("概念族（crosswalk）", fam_labels, index=0)
        i = fam_idx[fam_labels.index(fam_sel)]
        r = cached_crosswalk().loc[i]
        length_y = st.radio("窗口长度", [5, 10, 15, 20], index=1, horizontal=True,
                            help="CN 与 JP 窗口取相同长度才可比")
        cn_col = CN_COL_FIX.get(r["cn_variable_id"], r["cn_variable_id"])
        cn_full = comb[cn_col].dropna()
        cn_start_opt = [d.strftime("%Y-%m") for d in cn_full.index[:-1]]
        jp_s, _note = jp_series(r["jp_series_id"], pool)
        jp_full = jp_s.dropna()
        jp_start_opt = [d.strftime("%Y-%m") for d in jp_full.index[:-1]]
        if not cn_start_opt or not jp_start_opt:
            st.warning("CN 或 JP 该族数据为空"); return
        # 默认锚点对：CN 起点=实际覆盖中部（默认 2015-01 附近），JP 起点=CN-20 年
        cn_def = min(cn_start_opt, key=lambda x: abs(pd.Timestamp(x) - pd.Timestamp("2015-01-01")))
        jp_def = min(jp_start_opt, key=lambda x: abs(pd.Timestamp(x) - (pd.Timestamp(cn_def) - pd.DateOffset(years=20))))
        cn_s = st.selectbox("中国窗口起点", cn_start_opt, index=cn_start_opt.index(cn_def))
        jp_s0 = st.selectbox("日本窗口起点（锚点）", jp_start_opt, index=jp_start_opt.index(jp_def))
        x_mode = st.radio("时间轴", ["对齐轴（锚点叠合）", "日历轴（上下对照）"], index=0)
        scale = st.radio("尺度", ["直出（同单位%）", "重基100（窗首=100）", "双 Y 轴"],
                         index=0 if r["normalization"] == "直出" else 1,
                         help="直出=同比%等同单位同轴；重基=水平/指数类窗首归一；双 Y=两国各用自己轴")

    # ---- 窗口数据 ----
    cn_col2 = CN_COL_FIX.get(r["cn_variable_id"], r["cn_variable_id"])
    cn_sr = comb[cn_col2].dropna()
    jp_sr, jp_note = jp_series(r["jp_series_id"], pool)
    cn_win = cn_sr.loc[pd.Timestamp(cn_s):]
    jp_win = jp_sr.loc[pd.Timestamp(jp_s0):]
    n_m = length_y * 12
    cn_win = cn_win.iloc[:n_m]
    jp_win = jp_win.iloc[:n_m]
    cn_end = cn_win.index[-1].strftime("%Y-%m")
    jp_end = jp_win.index[-1].strftime("%Y-%m")
    if len(cn_win) < 3 or len(jp_win) < 3:
        st.warning("窗口数据不足（起点太靠近末端）"); return

    rebase = scale.startswith("重基")
    dual = scale.startswith("双 Y")
    if rebase and (float(cn_win.iloc[0]) <= 0 or float(jp_win.iloc[0]) <= 0):
        st.warning("窗首为 0 或负值（如 GDP 负增速/零利率），不可用「重基100」，已切回直出")
        rebase = False
        scale = "直出（同单位%）"
    cn_y = (cn_win / cn_win.iloc[0] * 100) if rebase else cn_win
    jp_y = (jp_win / jp_win.iloc[0] * 100) if rebase else jp_win

    def rel_year(idx):
        return (idx - idx[0]).days / 365.25

    cn_x = rel_year(cn_win.index)
    jp_x = rel_year(jp_win.index)
    cn_txt = [d.strftime("%Y-%m") for d in cn_win.index]
    jp_txt = [d.strftime("%Y-%m") for d in jp_win.index]
    cn_name = f"🇨🇳中国 {r['cn_name']}"
    jp_name = f"🇯🇵日本 {r['jp_name']}"
    unit_txt = "指数(窗首=100)" if rebase else "%"

    # ---- 图 ----
    if x_mode.startswith("对齐"):
        fig = go.Figure(layout=dict(template="plotly_white",
                                    margin=dict(l=60, r=60, t=70, b=50)))
        fig.add_trace(go.Scatter(x=cn_x, y=cn_y.values, mode="lines",
                                 name=cn_name, line=dict(color="#c0392b", width=2),
                                 customdata=cn_txt,
                                 hovertemplate="%{customdata}（CN 相对窗首 %{x:.1f} 年）<br>%{y:.2f}%<extra></extra>"))
        jp_kw = {"yaxis": "y2"} if (dual and not rebase) else {}
        fig.add_trace(go.Scatter(x=jp_x, y=jp_y.values, mode="lines",
                                 name=jp_name, line=dict(color="#2471a3", width=2),
                                 customdata=jp_txt, **jp_kw,
                                 hovertemplate="%{customdata}（JP 相对窗首 %{x:.1f} 年）<br>%{y:.2f}%<extra></extra>"))
        layout = dict(title=f"⚖️ {r['concept_family']}：CN {cn_s}~{cn_end} ↔ JP {jp_s0}~{jp_end}（对齐轴）",
                      xaxis_title="相对锚点年数（两窗窗首=0）",
                      yaxis_title=unit_txt if not (dual and not rebase)
                      else f"🇨🇳 {unit_txt}",
                      hovermode="x unified", legend=dict(orientation="h", y=1.08))
        if dual and not rebase:
            layout["yaxis2"] = dict(title=f"🇯🇵 {unit_txt}", overlaying="y",
                                    side="right", showgrid=False)
        fig.update_layout(**layout)
    else:
        fig = sp.make_subplots(rows=2, cols=1, shared_xaxes=False,
                               subplot_titles=(f"🇨🇳中国 {r['cn_name']}（{cn_s}~{cn_end}）",
                                               f"🇯🇵日本 {r['jp_name']}（{jp_s0}~{jp_end}）"),
                               vertical_spacing=0.10)
        fig.add_trace(go.Scatter(x=cn_win.index, y=cn_y.values, mode="lines",
                                 name=cn_name, line=dict(color="#c0392b", width=1.8)),
                      row=1, col=1)
        fig.add_trace(go.Scatter(x=jp_win.index, y=jp_y.values, mode="lines",
                                 name=jp_name, line=dict(color="#2471a3", width=1.8)),
                      row=2, col=1)
        fig.update_layout(template="plotly_white", height=620,
                          margin=dict(l=60, r=30, t=70, b=50),
                          title=f"⚖️ {r['concept_family']}：日历轴对照")
        fig.update_yaxes(title_text=unit_txt, row=1, col=1)
        fig.update_yaxes(title_text=unit_txt, row=2, col=1)
    st.plotly_chart(fig, width="stretch")

    # ---- 可比性声明（强制图注） ----
    note_lines = [
        f"概念：{r['concept_family']} ｜ 可比性：{'A 同口径' if r['comparability']=='A' else ('B 近似' if r['comparability']=='B' else 'C 形态可比')}",
        f"🇨🇳 CN 序列：{r['cn_name']}（{cn_s}~{cn_end}，{CN_SOURCE_NOTE}）",
        f"🇯🇵 JP 序列：{r['jp_name']}（{jp_s0}~{jp_end}，{jp_note}）",
        f"窗口映射：中国 {cn_s}（锚点 0）↔ 日本 {jp_s0}（锚点 0），长度 {length_y} 年",
    ]
    if str(r["notes"]).strip() and str(r["notes"]) != "nan":
        note_lines.append(f"口径注：{r['notes']}")
    note_lines.append("⚠️ 时间移轴仅为形态比较（日本领先假设的视觉检验），两窗共长；JP 序列真实日期见 hover。")
    st.caption(" ｜ ".join(note_lines))

    # ---- 同窗对比摘要 ----
    rows = [
        {"国别": "中国", "窗口": f"{cn_s}~{cn_end}", "窗首": round(float(cn_y.iloc[0]), 2),
         "窗末": round(float(cn_y.iloc[-1]), 2),
         "区间最小": round(float(cn_y.min()), 2), "区间最大": round(float(cn_y.max()), 2),
         "末值相对窗首": f"{(float(cn_y.iloc[-1])/float(cn_y.iloc[0])-1)*100 if not rebase else float(cn_y.iloc[-1])-100:+.1f}%"},
        {"国别": "日本", "窗口": f"{jp_s0}~{jp_end}", "窗首": round(float(jp_y.iloc[0]), 2),
         "窗末": round(float(jp_y.iloc[-1]), 2),
         "区间最小": round(float(jp_y.min()), 2), "区间最大": round(float(jp_y.max()), 2),
         "末值相对窗首": f"{(float(jp_y.iloc[-1])/float(jp_y.iloc[0])-1)*100 if not rebase else float(jp_y.iloc[-1])-100:+.1f}%"},
    ]
    st.caption("同窗统计（重基模式=窗首100 后的水平；直出模式=同单位%）")
    st.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True)


# =====================================================================
# M3 年度重点族（JP-HIST · featured presets）——用户点名：CPI 等关键对比
# 数据：08_可视化/data_snapshot_annual（只读副本+manifest）；数字全部窗口实算；
# 纪律：只比形态/相对幅度，不做“日本化/滞后 N 年”断言（完整结论见 🧭 JP-HIST 结构发现）。
# =====================================================================
FAM = {
    "cpi_yoy": dict(label="CPI 同比", comp="A 同口径（两国官方 CPI 同比）",
                    ln=10, off=20, yoy=True,
                    note="日本 1999 起转负、2002 最深 −0.91；中国 2023-25 = 0.2/0.2/0.0 未转负——0 线=转负分界。"),
    "investment_gdp": dict(label="投资率（固定资本形成/GDP）", comp="B 近似（SNA 口径不同，绝对水平不可横比）",
                           ln=15, off=24, yoy=False,
                           note="2012 衔接断点≈2pp（四经普 SNA 修订）；比长下行斜率与平台期，不比绝对水平；"
                                "日本 2023 数据止（2008SNA 待更新）。"),
    "m2_yoy": dict(label="M2 同比", comp="B 近似（口径链有断）",
                   ln=15, off=25, yoy=True,
                   note="名义货币增速长下行对照；M2 通道在 M4 机制验证中为次级（held-out 方向一致，描述性）。"),
    "real_gdp_yoy": dict(label="实际GDP 同比", comp="B 近似（统计基准不同）",
                         ln=10, off=20, yoy=True,
                         note="增速台阶下移节奏对照（不预设对应年份）。"),
    "birth_rate": dict(label="出生率（每千人）", comp="A 同口径（每千人出生率）",
                       ln=15, off=15, yoy=False,
                       note="CN 2013-15 放开二孩短暂回升后再降；两国均为官方人口统计口径。"),
    "wage_yoy": dict(label="工资名义增速", comp="C 形态可比（两国口径不同，勿比绝对水平）",
                     ln=10, off=20, yoy=True,
                     note="CN=城镇单位/非私营口径，JP=FRED 雇佣报酬系列——只比形态。"),
}


@st.cache_data
def _annual_data(cc):
    wide, reg = loader.load_annual_series_wide(cc)
    return wide, reg


def _yopt(s, length):
    """起始年候选（保证窗口 [y, y+length) 全部落在有效年内）：s=dropna Series（int index）。"""
    yrs = sorted(int(y) for y in s.index if pd.notna(s.loc[y]))
    if len(yrs) < length:
        return []
    allowed = set(yrs)
    return [y for y in yrs if all(y + k in allowed for k in range(length))]


def _win(s, start, length):
    sub = s.loc[start:]
    return sub.iloc[:length]


def _round3(x):
    return round(float(x), 3) if pd.notna(x) else None


def _annual_compare_view():
    cnw, cnreg = _annual_data("cn")
    jpw, jpreg = _annual_data("jp")
    avail = [v for v in FAM
             if f"hjy_{v}" in cnw.columns and f"hjy_{v}" in jpw.columns]
    if not avail:
        st.warning("年度重点族数据缺失（data_snapshot_annual 未就绪）")
        return
    regidx = {r.variable_id: r for r in cnreg.itertuples()}
    fam_labels = [f"{i + 1}. {FAM[v]['label']}（CN 名：{regidx['hjy_' + v].display_name}）"
                  for i, v in enumerate(avail)]
    st.caption("年度重点族（JP-HIST featured）：每年 1 个观测（Dec 锚点）。选择概念族后，"
               "两侧窗口同长、锚点默认把「中国近年段 ↔ 日本更早段」叠合（offset 见各族预设），"
               "hover 永远显示真实年份。数值标注全部由窗口数据实算。")
    with st.sidebar:
        fam_lab = st.selectbox("重点族（featured）", fam_labels, index=0, key="m3a_fam")
        v = avail[fam_labels.index(fam_lab)]
        cfg = FAM[v]
        length = st.radio("窗口长度（年）", [5, 10, 15, 20], index=[5, 10, 15, 20].index(cfg["ln"]),
                          horizontal=True, key="m3a_len")
        cs = cnw[f"hjy_{v}"].dropna()
        js = jpw[f"hjy_{v}"].dropna()
        c_opts = _yopt(cs, length)
        j_opts = _yopt(js, length)
        if not c_opts or not j_opts:
            st.warning("该族有效年不足窗口长度"); return
        c_def = c_opts[-1]                       # 最近一个完整窗口
        j_def = min(j_opts, key=lambda y: abs(y - (c_def - cfg["off"])))
        c0 = st.selectbox("中国窗口起点年", c_opts, index=c_opts.index(c_def), key="m3a_c0")
        j0 = st.selectbox("日本窗口起点年（锚点）", j_opts, index=j_opts.index(j_def), key="m3a_j0")
        x_mode = st.radio("时间轴", ["对齐轴（锚点叠合）", "日历轴（上下对照）"], index=0, key="m3a_x")
        scale = st.radio("尺度", ["直出（同单位）", "重基（窗首=100）", "双 Y 轴"], index=0, key="m3a_scale")

    c_win = _win(cs, c0, length)
    j_win = _win(js, j0, length)
    if len(c_win) < 3 or len(j_win) < 3:
        st.warning("窗口数据不足"); return
    rebase = scale.startswith("重基")
    dual = scale.startswith("双 Y")
    if rebase and (float(c_win.iloc[0]) <= 0 or float(j_win.iloc[0]) <= 0):
        st.warning("窗首为 0 或负值，不可用「重基」，已切回直出")
        rebase, scale = False, "直出（同单位）"
    c_y = (c_win / c_win.iloc[0] * 100) if rebase else c_win
    j_y = (j_win / j_win.iloc[0] * 100) if rebase else j_win
    unit_txt = "指数(窗首=100)" if rebase else "单位见序列（多数 %）"
    c_name, j_name = f"🇨🇳中国 {regidx['hjy_' + v].display_name}", f"🇯🇵日本 {jpreg[jpreg.variable_id == 'hjy_' + v].iloc[0].display_name}"
    c1, j1 = int(c_win.index[0]), int(j_win.index[0])
    c_end, j_end = int(c_win.index[-1]), int(j_win.index[-1])

    if x_mode.startswith("对齐"):
        fig = go.Figure(layout=dict(template="plotly_white", margin=dict(l=60, r=60, t=80, b=50)))
        fig.add_trace(go.Scatter(x=(c_win.index - c1).astype(int), y=c_y.values, mode="lines+markers",
                                 name=c_name, line=dict(color="#c0392b", width=2), marker=dict(size=5),
                                 customdata=c_win.index,
                                 hovertemplate="%{customdata}年（CN 相对窗首 %{x} 年）<br>%{y:.2f}%<extra></extra>"))
        jk = {"yaxis": "y2"} if (dual and not rebase) else {}
        fig.add_trace(go.Scatter(x=(j_win.index - j1).astype(int), y=j_y.values, mode="lines+markers",
                                 name=j_name, line=dict(color="#2471a3", width=2), marker=dict(size=5),
                                 customdata=j_win.index, **jk,
                                 hovertemplate="%{customdata}年（JP 相对窗首 %{x} 年）<br>%{y:.2f}%<extra></extra>"))
        layout = dict(title=f"⚖️ {cfg['label']}（年度重点族）：CN {c1}~{c_end} ↔ JP {j1}~{j_end}（对齐轴）",
                      xaxis_title="相对锚点年数（两窗窗首=0）", hovermode="x unified",
                      legend=dict(orientation="h", y=1.12),
                      yaxis_title=unit_txt if not (dual and not rebase) else "🇨🇳 值")
        if dual and not rebase:
            layout["yaxis2"] = dict(title="🇯🇵 值", overlaying="y", side="right", showgrid=False)
        fig.update_layout(**layout)
        if cfg["yoy"]:
            fig.add_hline(y=0, line_color="#999", line_dash="dot")
        # 日本窗口负值区间（如 CPI 转负段）
        neg = j_win[j_win < 0]
        if len(neg):
            fig.add_vrect(x0=int(neg.index.min()) - j1, x1=int(neg.index.max()) + 1 - j1,
                          fillcolor="rgba(245,183,177,0.25)", line_width=0)
        # 峰值标注（投资率类）
        if v == "investment_gdp":
            for s, nm, col in ((c_win, "CN", "#c0392b"), (j_win, "JP", "#2471a3")):
                pk = s.idxmax()
                fig.add_annotation(x=int(pk) - (c1 if nm == "CN" else j1), y=float(s.loc[pk]),
                                   text=f"{nm}峰值 {int(pk)}:{float(s.loc[pk]):.1f}",
                                   showarrow=True, arrowhead=2, font=dict(size=10, color=col))
    else:
        fig = sp.make_subplots(rows=2, cols=1, subplot_titles=(f"🇨🇳 {regidx['hjy_' + v].display_name}（{c1}~{c_end}）",
                                                               f"🇯🇵 {jpreg[jpreg.variable_id == 'hjy_' + v].iloc[0].display_name}（{j1}~{j_end}）"),
                               vertical_spacing=0.12)
        fig.add_trace(go.Scatter(x=c_win.index, y=c_y.values, mode="lines+markers",
                                 name=c_name, line=dict(color="#c0392b", width=2), marker=dict(size=5)),
                      row=1, col=1)
        fig.add_trace(go.Scatter(x=j_win.index, y=j_y.values, mode="lines+markers",
                                 name=j_name, line=dict(color="#2471a3", width=2), marker=dict(size=5)),
                      row=2, col=1)
        fig.update_layout(template="plotly_white", height=620,
                          title=f"⚖️ {cfg['label']}：日历轴对照（年度重点族）",
                          margin=dict(l=60, r=30, t=70, b=50))
        fig.update_yaxes(title_text=unit_txt, row=1, col=1)
        fig.update_yaxes(title_text=unit_txt, row=2, col=1)
    st.plotly_chart(fig, width="stretch")

    # ---- 数据实算叙事（数字不手写） ----
    narr = []
    if v == "cpi_yoy":
        jmin_y, jmin_v = int(j_win.idxmin()), float(j_win.min())
        narr.append(f"🇯🇵 窗口内最低 {jmin_y} 年 {jmin_v:.2f}%")
        jneg = [int(y) for y in j_win.index if j_win.loc[y] < 0]
        narr.append(("🇯🇵 窗口内转负年份：" + (", ".join(map(str, jneg)))) if jneg else "🇯🇵 窗口内未转负")
        cl_y, cl_v = int(c_win.index[-1]), float(c_win.iloc[-1])
        narr.append(f"🇨🇳 窗末 {cl_y} 年 {cl_v:.2f}%——" + ("已转负" if cl_v < 0 else ("贴 0（未转负）" if cl_v < 1.5 else "仍在 0 线上方")))
    elif v == "investment_gdp":
        for s, nm in ((c_win, "🇨🇳"), (j_win, "🇯🇵")):
            pk = s.idxmax(); tr = s.index[-1]
            narr.append(f"{nm} 峰值 {int(pk)} 年 {float(s.loc[pk]):.1f}% → 窗末 {int(tr)} 年 {float(s.loc[tr]):.1f}%"
                        f"（{float(s.loc[tr] - s.loc[pk]):+.1f}pp）")
    elif v == "birth_rate":
        for s, nm in ((c_win, "🇨🇳"), (j_win, "🇯🇵")):
            narr.append(f"{nm} 窗首 {int(s.index[0])} {float(s.iloc[0]):.1f}‰ → 窗末 {int(s.index[-1])} {float(s.iloc[-1]):.1f}‰")
    else:
        for s, nm in ((c_win, "🇨🇳"), (j_win, "🇯🇵")):
            narr.append(f"{nm} 窗首 {int(s.index[0])} {float(s.iloc[0]):.2f} → 窗末 {int(s.index[-1])} {float(s.iloc[-1]):.2f}"
                        f"（Δ {float(s.iloc[-1] - s.iloc[0]):+.2f}）")
    note_lines = [
        f"概念：{cfg['label']} ｜ 可比性：{cfg['comp']}",
        f"🇨🇳 CN 序列：{regidx['hjy_' + v].display_name}（{c1}~{c_end}，JP-HIST 年度快照）",
        f"🇯🇵 JP 序列：{jpreg[jpreg.variable_id == 'hjy_' + v].iloc[0].display_name}（{j1}~{j_end}，JP-HIST 年度快照）",
        f"窗口映射：中国 {c1}（锚点 0）↔ 日本 {j1}（锚点 0），长度 {length} 年",
        "｜ ".join(narr),
    ]
    for side, rg in (("CN", cnreg), ("JP", jpreg)):
        row = rg[rg.variable_id == "hjy_" + v]
        if len(row) and str(row.iloc[0].notes).strip():
            note_lines.append(f"{side} 口径注：{row.iloc[0].notes}")
    if cfg.get("note"):
        note_lines.append(f"📌 {cfg['note']}")
    note_lines.append("⚠️ 时间移轴仅为形态/相对幅度比较（日本领先假设的视觉检验），两窗共长；"
                      "年度层=JP-HIST 冻结链副本（data_snapshot_annual + SHA manifest 可验证），"
                      "本页不做“日本化/固定滞后 N 年”断言——机制级结论见 🧭 JP-HIST 结构发现视图。")
    st.caption(" ｜ ".join(note_lines))

    rows = [{"国别": "中国", "窗口": f"{c1}~{c_end}", "窗首": _round3(c_y.iloc[0]),
             "窗末": _round3(c_y.iloc[-1]), "区间最小": _round3(c_y.min()),
             "区间最大": _round3(c_y.max()),
             "末值相对窗首": f"{(float(c_y.iloc[-1]) / float(c_y.iloc[0]) - 1) * 100 if not rebase else float(c_y.iloc[-1]) - 100:+.1f}%"},
            {"国别": "日本", "窗口": f"{j1}~{j_end}", "窗首": _round3(j_y.iloc[0]),
             "窗末": _round3(j_y.iloc[-1]), "区间最小": _round3(j_y.min()),
             "区间最大": _round3(j_y.max()),
             "末值相对窗首": f"{(float(j_y.iloc[-1]) / float(j_y.iloc[0]) - 1) * 100 if not rebase else float(j_y.iloc[-1]) - 100:+.1f}%"}]
    st.caption("同窗统计（重基=窗首 100 后水平；直出=原单位）")
    st.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True)


# =====================================================================
# M3 季度机制族（JP-HIST H6-B · featured presets）——用户拍板 6：四候选全进
# 数据：08_可视化/data_snapshot_h6（只读副本+SHA manifest；季首单点）
# 纪律：只比形态/相对幅度，不做“日本化/固定滞后 N 年”断言；口径注强制图下。
# =====================================================================
QFAM = [
    dict(key="core_cpi", short="core_cpi", label="核心CPI 同比（季均）",
         comp="B 近似（剔除范围不同：CN 不含食品能源 vs JP 除生鲜）",
         unit="% 同比", ln=10, off=22, yoy=True, rebase_def=False, dec=2,
         note="CN 2013Q1+ 官方核心 CPI 结构性起点（非缺口）；JP 1990s 转负区间已着色；"
              "CN 2023-25 ≈0/0.0 未转负——0 线=转负分界。"),
    dict(key="leverage", short="corp_leverage", label="企业杠杆（资产负债率·季末）",
         comp="C 形态可比（CN 规上工业 SECTOR_PROXY vs JP 法人全行业；禁绝对值横比）",
         unit="比值（负债/资产）", ln=15, off=0, yoy=False, rebase_def=False, dec=3,
         note="只比资产负债表周期形态：JP 1989-91 泡沫峰值后长去杠杆；CN 工业杠杆 2011+ "
              "高位缓慢下行（2007-10 口径 gap 已注）。"),
    dict(key="ppi", short="ppi", label="PPI 同比（季均）",
         comp="B 近似（CN NBS PPI vs JP CGPI）",
         unit="% 同比", ln=10, off=12, yoy=True, rebase_def=False, dec=2,
         note="JP 2022Q4 停更（镜像停更注）；CN 2006Q1+；比工业品价格周期相位。"),
    dict(key="housing", short="housing_starts", label="地产活动 · 住房新开工（形态示意）",
         comp="C 形态（CN 面积 vs JP 戸数 CONCEPT_PROXY；单位不同→默认重基100）",
         unit="规模（重基100 比较）", ln=15, off=10, yoy=False, rebase_def=True, dec=0,
         note="只比周期形态与峰谷节奏，不比绝对规模；CN 2000Q2-Q4 缺失、JP 2024 止均已注。"),
    dict(key="property", short="res_price", label="地产活动 · 住宅价格（形态示意）",
         comp="C 形态（概念/基准不同层；源文件无基准说明→禁绝对横比）",
         unit="指数（重基100 比较）", ln=15, off=15, yoy=False, rebase_def=True, dec=1,
         note="CN 2005Q2+（BIS 段）、JP 1955Q1+；指数基准未标，仅形态；红线=房价只作示意非投资信号。"),
]
QFAM_KEY2SHORT = {f["key"]: f["short"] for f in QFAM}


def _qkey(ts):
    return int(ts.year) * 4 + (int(ts.month) - 1) // 3


def _qfmt(ts):
    return f"{int(ts.year)}-Q{(int(ts.month) - 1) // 3 + 1}"


def _q_windows(s, n_q):
    """返回可作窗首的 qkey 列表（要求其后 n_q 个连续季度均有值）。"""
    keys = sorted({_qkey(ts) for ts in s.dropna().index})
    ks = set(keys)
    return [k for k in keys if all(k + i in ks for i in range(n_q))]


@st.cache_data
def _h6q(cc):
    w, reg = loader.load_h6_series_wide(cc)
    return w, reg


def _quarterly_compare_view():
    cnw, cnreg = _h6q("cn")
    jpw, jpreg = _h6q("jp")
    if cnw is None or jpw is None or not len(cnw.columns) or not len(jpw.columns):
        st.warning("H6-B 季度快照未就绪（data_snapshot_h6 缺失）")
        return
    cnregi = cnreg.set_index("variable_id")
    jpregi = jpreg.set_index("variable_id")
    avail = [f for f in QFAM
             if f"h6q_cn_{f['short']}" in cnw.columns and f"h6q_jp_{f['short']}" in jpw.columns]
    if not avail:
        st.warning("季度机制族无可用族（双侧缺序列）")
        return
    st.caption("季度机制族（H6-B featured，用户拍板全选）：H6-B 冻结机制/通缩变量（季首落点）叠合比较。"
               "选择概念族后，两侧窗口同长；默认锚点把「中国近年段 ↔ 日本更早段」叠合（offset 见各族预设，"
               "企业杠杆默认同期并列）。数值标注全部由窗口数据实算。")
    with st.sidebar:
        fam_lab = st.selectbox("机制族（H6-B featured）",
                               [f"{i+1}. {f['label']}" for i, f in enumerate(avail)],
                               index=0, key="m3q_fam")
        f = avail[[f"{i+1}. {x['label']}" for i, x in enumerate(avail)].index(fam_lab)]
        length = st.radio("窗口长度（年）", [5, 10, 15, 20],
                          index=[5, 10, 15, 20].index(f["ln"]), horizontal=True, key=f"m3q_len_{f['key']}")
        n_q = length * 4
        cs = cnw[f"h6q_cn_{f['short']}"]
        js = jpw[f"h6q_jp_{f['short']}"]
        c_ws = _q_windows(cs, n_q)
        j_ws = _q_windows(js, n_q)
        if not c_ws or not j_ws:
            st.warning("该族有效季度不足窗口长度")
            return
        c_ts = [cs.dropna().index[cs.dropna().index.map(_qkey).tolist().index(k)] for k in c_ws]
        j_ts = [js.dropna().index[js.dropna().index.map(_qkey).tolist().index(k)] for k in j_ws]
        c_labs = [_qfmt(t) for t in c_ts]
        j_labs = [_qfmt(t) for t in j_ts]
        c_def = c_ws[-1]
        j_def = min(j_ws, key=lambda k: abs(k - (c_def - f["off"] * 4)))
        c0 = st.selectbox("中国窗口起点（季）", c_labs, index=c_ws.index(c_def), key=f"m3q_c0_{f['key']}")
        j0 = st.selectbox("日本窗口起点（季，锚点）", j_labs, index=j_ws.index(j_def), key=f"m3q_j0_{f['key']}")
        x_mode = st.radio("时间轴", ["对齐轴（锚点叠合）", "日历轴（上下对照）"], index=0, key=f"m3q_x_{f['key']}")
        scale_opts = ["直出（同单位）", "重基100（窗首=100）", "双 Y 轴"]
        scale = st.radio("尺度", scale_opts,
                         index=1 if f["rebase_def"] else 0, key=f"m3q_scale_{f['key']}")

    c_start = c_ts[c_labs.index(c0)]
    j_start = j_ts[j_labs.index(j0)]
    c_win = cs.loc[c_start:].iloc[:n_q]
    j_win = js.loc[j_start:].iloc[:n_q]
    if len(c_win) < 3 or len(j_win) < 3:
        st.warning("窗口数据不足")
        return
    rebase = scale.startswith("重基")
    dual = scale.startswith("双 Y")
    if rebase and (float(c_win.iloc[0]) <= 0 or float(j_win.iloc[0]) <= 0):
        st.warning("窗首为 0 或负值，不可用「重基」，已切回直出")
        rebase, scale = False, "直出（同单位）"
    c_y = (c_win / c_win.iloc[0] * 100) if rebase else c_win
    j_y = (j_win / j_win.iloc[0] * 100) if rebase else j_win
    unit_txt = "指数(窗首=100)" if rebase else f["unit"]
    cn_id = f"h6q_cn_{f['short']}"
    jp_id = f"h6q_jp_{f['short']}"
    cn_name = "🇨🇳中国 " + str(cnregi.loc[cn_id]["display_name"])
    jp_name = "🇯🇵日本 " + str(jpregi.loc[jp_id]["display_name"])

    def _xrel(idx):
        return (idx - idx[0]).days / 365.25

    if x_mode.startswith("对齐"):
        fig = go.Figure(layout=dict(template="plotly_white", margin=dict(l=60, r=60, t=80, b=50)))
        cx = _xrel(c_win.index)
        jx = _xrel(j_win.index)
        fig.add_trace(go.Scatter(x=cx, y=c_y.values, mode="lines+markers",
                                 name=cn_name, line=dict(color="#c0392b", width=2), marker=dict(size=4),
                                 customdata=[_qfmt(t) for t in c_win.index],
                                 hovertemplate="%{customdata}（CN 相对窗首 %{x:.1f} 年）<br>%{y:.3f}<extra></extra>"))
        jk = {"yaxis": "y2"} if (dual and not rebase) else {}
        fig.add_trace(go.Scatter(x=jx, y=j_y.values, mode="lines+markers",
                                 name=jp_name, line=dict(color="#2471a3", width=2), marker=dict(size=4),
                                 customdata=[_qfmt(t) for t in j_win.index], **jk,
                                 hovertemplate="%{customdata}（JP 相对窗首 %{x:.1f} 年）<br>%{y:.3f}<extra></extra>"))
        layout = dict(title=f"⚖️ {f['label']}（季度机制族）：CN {_qfmt(c_win.index[0])}~{_qfmt(c_win.index[-1])}"
                             f" ↔ JP {_qfmt(j_win.index[0])}~{_qfmt(j_win.index[-1])}（对齐轴）",
                      xaxis_title="相对锚点年数（两窗窗首=0）", hovermode="x unified",
                      legend=dict(orientation="h", y=1.12),
                      yaxis_title=unit_txt if not (dual and not rebase) else "🇨🇳 值")
        if dual and not rebase:
            layout["yaxis2"] = dict(title="🇯🇵 值", overlaying="y", side="right", showgrid=False)
        fig.update_layout(**layout)
        if f["yoy"]:
            fig.add_hline(y=0, line_color="#999", line_dash="dot")
        neg = j_win[j_win < 0]
        if f["yoy"] and len(neg):
            x0 = _xrel(pd.DatetimeIndex([neg.index.min()]))[0]
            x1 = _xrel(pd.DatetimeIndex([neg.index.max()]))[0]
            fig.add_vrect(x0=x0, x1=x1 + 0.2, fillcolor="rgba(245,183,177,0.25)", line_width=0)
        if f["key"] == "leverage":
            for s, nm, col, base in ((c_win, "CN", "#c0392b", c_win.index[0]),
                                     (j_win, "JP", "#2471a3", j_win.index[0])):
                pk = s.idxmax()
                fig.add_annotation(x=_xrel(pd.DatetimeIndex([pk]))[0], y=float(s.loc[pk]),
                                   text=f"{nm} 峰值 {_qfmt(pk)}:{float(s.loc[pk]):.3f}",
                                   showarrow=True, arrowhead=2, font=dict(size=10, color=col))
    else:
        fig = sp.make_subplots(rows=2, cols=1, subplot_titles=(f"🇨🇳 {cn_name}（{_qfmt(c_win.index[0])}~{_qfmt(c_win.index[-1])}）",
                                                               f"🇯🇵 {jp_name}（{_qfmt(j_win.index[0])}~{_qfmt(j_win.index[-1])}）"),
                               vertical_spacing=0.12)
        fig.add_trace(go.Scatter(x=c_win.index, y=c_y.values, mode="lines+markers",
                                 name=cn_name, line=dict(color="#c0392b", width=2), marker=dict(size=4)),
                      row=1, col=1)
        fig.add_trace(go.Scatter(x=j_win.index, y=j_y.values, mode="lines+markers",
                                 name=jp_name, line=dict(color="#2471a3", width=2), marker=dict(size=4)),
                      row=2, col=1)
        fig.update_layout(template="plotly_white", height=620,
                          title=f"⚖️ {f['label']}：日历轴对照（季度机制族）",
                          margin=dict(l=60, r=30, t=70, b=50))
        fig.update_yaxes(title_text=unit_txt, row=1, col=1)
        fig.update_yaxes(title_text=unit_txt, row=2, col=1)
    st.plotly_chart(fig, width="stretch")

    # ---- 数据实算叙事 ----
    narr = []
    if f["key"] == "core_cpi":
        jmin_y, jmin_v = _qfmt(j_win.idxmin()), float(j_win.min())
        narr.append(f"🇯🇵 窗口内最低 {jmin_y} {jmin_v:.2f}%")
        jneg = [_qfmt(ts) for ts in j_win.index if j_win.loc[ts] < 0]
        narr.append("🇯🇵 窗口内转负季：" + ("、".join(jneg)) if jneg else "🇯🇵 窗口内未转负")
        cl_v = float(c_win.iloc[-1])
        narr.append(f"🇨🇳 窗末 {_qfmt(c_win.index[-1])} {cl_v:.2f}%——"
                    + ("已转负" if cl_v < 0 else ("贴 0（未转负）" if cl_v < 1.5 else "仍在 0 线上方")))
    elif f["key"] == "leverage":
        for s, nm in ((c_win, "🇨🇳"), (j_win, "🇯🇵")):
            d = float(s.iloc[-1] - s.iloc[0])
            narr.append(f"{nm} 窗首 {_qfmt(s.index[0])} {float(s.iloc[0]):.3f} → 窗末 "
                        f"{_qfmt(s.index[-1])} {float(s.iloc[-1]):.3f}（Δ {d:+.3f} 比值）")
    elif f["key"] == "housing":
        for s, nm in ((c_win, "🇨🇳"), (j_win, "🇯🇵")):
            pk = s.idxmax()
            pv = float(s.loc[pk])
            if rebase:
                narr.append(f"{nm} 峰值 {_qfmt(pk)}（窗首=100 后峰值水平 {pv:.0f}）")
            else:
                narr.append(f"{nm} 峰值 {_qfmt(pk)}（相对窗首 {pv / float(s.iloc[0]) * 100:.0f}%）")
    else:
        for s, nm in ((c_win, "🇨🇳"), (j_win, "🇯🇵")):
            narr.append(f"{nm} 窗首 {_qfmt(s.index[0])} {float(s.iloc[0]):.{f['dec']}f} → 窗末 "
                        f"{_qfmt(s.index[-1])} {float(s.iloc[-1]):.{f['dec']}f}"
                        f"（Δ {float(s.iloc[-1]-s.iloc[0]):+.{f['dec']}f}）")
    note_lines = [
        f"概念：{f['label']} ｜ 可比性：{f['comp']}",
        f"🇨🇳 CN 序列：{cn_name}（{_qfmt(c_win.index[0])}~{_qfmt(c_win.index[-1])}，H6-B 季度快照）",
        f"🇯🇵 JP 序列：{jp_name}（{_qfmt(j_win.index[0])}~{_qfmt(j_win.index[-1])}，H6-B 季度快照）",
        f"窗口映射：中国 {_qfmt(c_win.index[0])}（锚点 0）↔ 日本 {_qfmt(j_win.index[0])}（锚点 0），长度 {length} 年",
        "｜ ".join(narr),
    ]
    for side, rgi, vid in (("CN", cnregi, f"h6q_cn_{f['short']}"), ("JP", jpregi, f"h6q_jp_{f['short']}")):
        if vid in rgi.index and str(rgi.loc[vid].notes).strip():
            note_lines.append(f"{side} 口径注：{rgi.loc[vid].notes}")
    if f.get("note"):
        note_lines.append(f"📌 {f['note']}")
    note_lines.append("⚠️ 时间移轴仅为形态/相对幅度比较（日本领先假设的视觉检验），两窗共长；"
                      "季度层=H6-B 冻结机制变量副本（data_snapshot_h6 + SHA manifest 可验证），"
                      "本页不做“日本化/固定滞后 N 年”断言——机制级结论见 🧭 JP-HIST 结构发现视图。")
    st.caption(" ｜ ".join(note_lines))

    def _r3(x):
        return round(float(x), 3) if pd.notna(x) else None
    rows = [{"国别": "中国", "窗口": f"{_qfmt(c_win.index[0])}~{_qfmt(c_win.index[-1])}",
             "窗首": _r3(c_y.iloc[0]), "窗末": _r3(c_y.iloc[-1]),
             "区间最小": _r3(c_y.min()), "区间最大": _r3(c_y.max()),
             "末值相对窗首": f"{(float(c_y.iloc[-1])/float(c_y.iloc[0])-1)*100 if not rebase else float(c_y.iloc[-1])-100:+.1f}%"},
            {"国别": "日本", "窗口": f"{_qfmt(j_win.index[0])}~{_qfmt(j_win.index[-1])}",
             "窗首": _r3(j_y.iloc[0]), "窗末": _r3(j_y.iloc[-1]),
             "区间最小": _r3(j_y.min()), "区间最大": _r3(j_y.max()),
             "末值相对窗首": f"{(float(j_y.iloc[-1])/float(j_y.iloc[0])-1)*100 if not rebase else float(j_y.iloc[-1])-100:+.1f}%"}]
    st.caption("同窗统计（重基=窗首 100 后水平；直出=原单位）")
    st.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True)
