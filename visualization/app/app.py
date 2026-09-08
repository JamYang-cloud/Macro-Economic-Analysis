#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
app.py — 宏观股市罗盘 · 数据浏览器（Streamlit 壳，M3）

启动：cd 宏观股市罗盘 && streamlit run 08_可视化/app/app.py
架构：本文件只做 UI 编排；数据/图表/标注/推荐/导出逻辑全在 core/。
数据源：data_snapshot_v2/（M3 起，Phase 2 重清洗后 84 变量冻结产物）。

功能：
  M1.1 数据浏览（默认）：分组多选/观察尺度/叠加+分面/双轴/推荐规则/
        对数轴/一键导出 PNG
  M2   核查增强：PIT hover（发布日/源文件/vintage/陈旧月数/参考期/
        缺失原因）、原始值下钻（L0/L1 vs 月度面板）、箱线离群点月份、
        缺失原因分布
  M3   关联分析（新）：散点（时间着色）/滚动相关/相关热力图/
        前向收益对照（targets_long，Phase 6 条件分布直觉）
"""

import os
import re
import sys
import json
import subprocess
from datetime import datetime

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from core import loader, charts, export, presentation  # noqa: E402

VIS_DIR = os.path.dirname(HERE)
EXPORTS_DIR = os.path.join(VIS_DIR, "exports")
GROUPS = ["宏观", "货币金融", "资本", "居民", "补充数据·中国(年度)",
          "补充数据·中国(机制·季度)", "补充数据·中国(通缩·季度)",
          "补充数据·中国(原始月度)"]
OVERLAY_TYPES = ["折线", "双轴", "面积", "阶梯", "分布视图", "箱线图"]
FACET_TYPES = charts.CHART_TYPES
TIME_TYPES = {"折线", "双轴", "面积", "阶梯"}  # 时间轴图型（观察尺度生效）
ANALYZE_TOOLS = ["数据浏览", "散点", "滚动相关", "相关热力图", "前向收益"]

st.set_page_config(page_title="宏观股市罗盘 · 数据浏览器", layout="wide")


def run_qc(png_path):
    """导出后 GLM-4V 质检（T4.2）：调 verify_glm.py 回读，报告存导出目录。

    返回质检证据 dict；失败返回 {"error": ...}。质检报告保存为
    <png 同名>_qc.json。
    """
    script = os.path.join(VIS_DIR, "scripts", "verify_glm.py")
    if not os.path.isfile(script):
        return {"error": f"verify_glm.py 不存在: {script}"}
    try:
        proc = subprocess.run([sys.executable, script, png_path],
                              capture_output=True, text=True, timeout=150)
    except Exception as e:  # noqa: BLE001
        return {"error": f"质检进程失败: {e}"}
    if proc.returncode != 0:
        return {"error": f"质检失败 rc={proc.returncode}: {proc.stderr[-300:]}"}
    lines = [l for l in proc.stdout.strip().splitlines() if l.strip()]
    if not lines:
        return {"error": "质检无输出"}
    try:
        ev = json.loads(lines[-1])
    except Exception as e:  # noqa: BLE001
        return {"error": f"质检输出解析失败: {e}"}
    qc_path = os.path.splitext(png_path)[0] + "_qc.json"
    try:
        with open(qc_path, "w", encoding="utf-8") as f:
            json.dump(ev, f, ensure_ascii=False, indent=2)
    except Exception:  # noqa: BLE001
        pass
    return ev


def run_export(fig, fig_title, m_start, m_end, qc_check=False):
    """统一导出：PNG（playwright 2x）+ 可选 GLM 质检。

    目录约定（T4.1）：exports/YYYYMMDD_{中文主题}/HHMMSS.png，
    主题取自图标题（非法文件名字符替换为 _）。质检报告同目录 _qc.json。
    """
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    topic = fig_title.replace("/", "·").replace(" ", "")
    topic = re.sub(r'[\\/:*?"<>|]', "_", topic)
    out_dir = os.path.join(EXPORTS_DIR,
                           f"{datetime.now().strftime('%Y%m%d')}_{topic}")
    os.makedirs(out_dir, exist_ok=True)
    png_path = os.path.join(out_dir, f"{ts}.png")
    try:
        export.export_png(fig, png_path, title=f"{fig_title}  {m_start} ~ {m_end}")
        st.success(f"已导出: {png_path}")
        with open(png_path, "rb") as f:
            st.download_button("下载 PNG", f.read(),
                               file_name=os.path.basename(png_path),
                               mime="image/png")
        if qc_check:
            with st.spinner("GLM-4V 质检回读中…"):
                ev = run_qc(png_path)
            if "error" in ev:
                st.warning(f"质检失败: {ev['error']}")
            else:
                issues = ev.get("issues", [])
                st.caption(
                    f"质检：类型={ev.get('image_type')} | 标题={ev.get('title')} | "
                    f"问题={issues}")
                qc_path = os.path.splitext(png_path)[0] + "_qc.json"
                st.caption(f"质检报告: {qc_path}")
    except Exception as e:  # noqa: BLE001
        st.error(f"导出失败: {e}")


# ---------------- 缓存封装 ----------------
# 数据层缓存统一把 loader.data_sig()（注册表/面板文件 mtime 签名）并入 key：
# CSV 内容变更（组名/加行）→ 签名变 → 缓存自动失效，无需重启/清缓存。
@st.cache_data
def _combined_cached(_sig):
    return loader.load_combined()


def get_combined():
    return _combined_cached(loader.data_sig())


@st.cache_data
def get_missing():
    return loader.load_missing()


@st.cache_data
def _catalog_cached(_sig):
    return loader.load_catalog()


def get_catalog():
    return _catalog_cached(loader.data_sig())


@st.cache_data
def get_pit_meta():
    return loader.load_pit_meta()


@st.cache_data
def get_targets():
    return loader.load_targets()


@st.cache_data
def get_target_registry():
    return loader.load_target_registry()


def target_label(row):
    """target_registry 行 → 中文下拉标签（M3 前向收益）。"""
    h = charts._parse_horizon(row["target_id"])
    t = row["target_type"]
    name = {
        "STATE_RETURN": f"未来{h}个月收益·决策日口径",
        "EXECUTION_RETURN": f"未来{h}个月收益·次日入场口径",
        "LOSS_FLAG": f"{h}个月亏损标记(1=亏损)",
        "FUTURE_MDD": f"未来{h}个月最大回撤",
    }.get(t, row["target_id"])
    return f"{name}（{row['target_id']}）"


# 相关热力图默认变量（跨组核心：估值/利率/流动性/增长/市场）
HEAT_DEFAULT_HINTS = ["滚动市盈率TTM", "市净率", "10年期国债收益率",
                      "FR007月均", "CPI同比", "工业增加值同比", "M2同比",
                      "沪深300全收益(TRI)"]



# ============ 顶层：多国导航壳（M4 注册化） ============
# 国家视图由 core/country.COUNTRIES 注册表生成（加新国家：COUNTRIES 加行 +
# 新增 render_<cc>.py + 在底部路由加一个 elif 分支）。
# P1 扩展：CN=原逻辑包裹 render_cn（零改动）；JP/对比 在 P3/P4 已实装。
from core import country as _country

_VIEWS = [f"{_country.COUNTRIES[c]['flag']} {_country.COUNTRIES[c]['name']}数据"
          for c in _country.COUNTRIES] + ["⚖️ 中日对比", "🧭 JP-HIST 结构发现"]
with st.sidebar:
    st.title("宏观股市罗盘")
    st.caption("数据浏览器 · M3")
    PAGE = st.radio("视图", _VIEWS, index=0,
                    help="日本数据/中日对比为扩展模块（数据=两国 FROZEN 快照只读副本）。")


def render_cn():
    """中国数据页（M1）——原 app.py 全部逻辑，P1 包裹零改动。"""
    # ---------- 侧边栏（CN 页控件） ----------
    with st.sidebar:

        catalog = get_catalog()
        dup = catalog["display_name"].duplicated(keep=False)
        catalog["label"] = [
            r.display_name if not dup.iloc[i] else f"{r.display_name}（{r.variable_id}）"
            for i, r in catalog.iterrows()
        ]
        name_to_id = dict(zip(catalog["label"], catalog["variable_id"]))
        id_to_name = dict(zip(catalog["variable_id"], catalog["display_name"]))
        id_to_row = catalog.set_index("variable_id")

        # 分组多选（跨组 = 勾多个组，变量候选取并集；所有工具共用）
        # 选项直接取自 catalog 实际 group 值（四基组固定在前，其余按 catalog 出现顺序），
        # 避免硬编码 GROUPS 与 registry 组名漂移 → 勾了组却无可选变量（2026-09-08 修复）
        _base4 = ["宏观", "货币金融", "资本", "居民"]
        group_opts = _base4 + [g for g in catalog["group"].dropna().unique()
                               if g not in _base4]
        sel_groups = st.multiselect("数据分组", group_opts, default=group_opts)
        opts_df = catalog[catalog["group"].isin(sel_groups)]
        opts = opts_df["label"].tolist()
        if not opts:
            st.warning("请至少选择一个分组")
            st.stop()

        # 分析工具（M3；默认数据浏览 = 现有全部功能）
        tool = st.radio("分析工具", ANALYZE_TOOLS, index=0)

        # ---- 数据浏览专用控件（M1.1 原逻辑）----
        sel = []
        mode = "叠加"
        chart_type = "折线"
        right_var = None
        per_var = {}
        log_y = False
        scale = "月"

        if tool == "数据浏览":
            # 默认选中：沪深300全收益 + CPI同比（精确优先，子串兜底）
            def _pick(hint, opts):
                exact = [l for l in opts if l == hint]
                if exact:
                    return exact[0]
                subs = [l for l in opts if hint.split("(")[0] in l]
                return subs[0] if subs else None

            default_sel = [p for p in
                           [_pick("沪深300全收益(TRI)", opts), _pick("CPI同比", opts)]
                           if p][:2]
            sel = st.multiselect("选择变量", opts, default=default_sel)

            # 观察尺度（周期末值重采样，消除低频变量 forward-hold 阶梯）
            scale = st.radio("观察尺度", ["月", "季", "年"], horizontal=True)

            mode = st.radio("图表模式", ["叠加", "分面"], horizontal=True)
            if mode == "叠加":
                chart_type = st.radio("图形类型", OVERLAY_TYPES)
                if chart_type == "双轴":
                    right_opts = [l for l in sel if l != sel[0]]
                    if right_opts:
                        right_var = st.selectbox("右轴变量（从已选变量中挑）", right_opts)
                    else:
                        st.warning("双轴需要至少选择两个变量")
                if chart_type in TIME_TYPES:
                    log_y = st.checkbox("对数轴（长周期看增速）")
            else:  # 分面
                with st.expander("各变量呈现方式（默认=推荐规则，可改）",
                                 expanded=len(sel) <= 4):
                    for lbl in sel:
                        col = name_to_id[lbl]
                        row = id_to_row.loc[col].to_dict()
                        rec = presentation.default_presentation(col, row)
                        rec_idx = FACET_TYPES.index(rec["chart"])
                        per_var[col] = st.selectbox(f"{id_to_name[col]}",
                                                    FACET_TYPES, index=rec_idx)
                log_y = st.checkbox("对数轴（作用于折线/面积子图）")

        # 时间范围（全局，所有工具共用）
        df_all = get_combined()
        months = [d.strftime("%Y-%m") for d in df_all.index]
        _def_start = months.index("2008-01") if "2008-01" in months else 0
        m_start = st.selectbox("起始月", months, index=_def_start)
        m_end = st.selectbox("结束月", months, index=len(months) - 1)
        if m_start > m_end:
            st.warning("起始月晚于结束月，已自动交换")
            m_start, m_end = m_end, m_start

        # ---- M3 各分析工具控件 ----
        scatter_x = scatter_y = None
        scatter_color = "时间"
        corr_a = corr_b = None
        corr_window = 24
        heat_sel = []
        fwd_x = None
        fwd_tid_label = None
        fwd_color = "盈亏"
        fwd_size = False

        if tool == "散点":
            scatter_x = st.selectbox("X 变量", opts)
            scatter_y = st.selectbox("Y 变量", [o for o in opts if o != scatter_x])
            scatter_color = st.radio("点着色", ["时间", "缺失原因"],
                                     horizontal=True)
            st.caption("横轴=变量值（非时间）；点色=月份，看两变量关系随时序演化。")
        elif tool == "滚动相关":
            corr_a = st.selectbox("变量 A", opts)
            corr_b = st.selectbox("变量 B", [o for o in opts if o != corr_a])
            corr_window = st.selectbox("滚动窗口（月）", [12, 24, 36, 60], index=1)
            st.caption("Pearson 相关随时间的滚动变化（窗口内共同有效月）。")
        elif tool == "相关热力图":
            heat_sel = st.multiselect("选择变量（2-15 个，跨组可混选）",
                                      opts, default=[])
            if not heat_sel:
                # 默认：8 个跨组核心变量（按中文名 hint 匹配）
                defaults = []
                for hint in HEAT_DEFAULT_HINTS:
                    hit = [l for l in opts if hint.split("(")[0] in l]
                    if hit:
                        defaults.append(hit[0])
                heat_sel = st.multiselect("或直接用默认核心 8 变量", opts,
                                          default=defaults[:8])
            st.caption("两两 Pearson 相关（每对变量用各自共同有效月），"
                       "红=正相关、蓝=负相关。")
        elif tool == "前向收益":
            fwd_x = st.selectbox("状态变量（X）", opts)
            treg = get_target_registry()
            tlabels = [target_label(r) for _, r in treg.iterrows()]
            fwd_tid_label = st.selectbox("目标（Y，未来收益）", tlabels, index=0)
            fwd_color = st.radio("点着色", ["盈亏", "时间"], horizontal=True)
            fwd_size = st.checkbox("气泡大小 = 未来最大回撤", value=False)
            st.caption("X=决策月可见的状态值，Y=未来 h 个月全收益（targets_long，"
                       "PIT 对齐）；红=盈利、绿=亏损（A股习惯红涨绿跌）。")

        do_export = st.button("导出 PNG", width="stretch")
        qc_check = st.checkbox("导出后自动质检（GLM-4V 回读）", value=False)
    # ---------- 主区（原 M1.1/M2/M3 逻辑） ----------
    # ---------------- 主区 ----------------
    df = get_combined()
    missing = get_missing()
    pit_meta = get_pit_meta()
    start, end = pd.Timestamp(m_start), pd.Timestamp(m_end)

    if tool == "数据浏览":
        # ============ M1.1/M2 原逻辑（零改动） ============
        if not sel:
            st.info("请从左侧选择至少一个变量")
            st.stop()

        ids = [name_to_id[s] for s in sel]
        names = [id_to_name[i] for i in ids]
        zero_cols = presentation.ZERO_LINE

        # 推荐呈现提示条
        with st.expander("推荐呈现方式", expanded=len(sel) <= 3):
            for col in ids:
                row = id_to_row.loc[col].to_dict()
                st.caption(f"● {id_to_name[col]}：{presentation.recommend_text(col, row)}")

        # 图表
        fig = None
        if mode == "叠加":
            if chart_type == "折线":
                fig = charts.line_chart(df, ids, names, start, end, missing,
                                        scale=scale, log_y=log_y, zero_cols=zero_cols,
                                        pit_meta=pit_meta)
                if len(ids) > 1:
                    st.caption("提示：不同量纲的变量混画单轴会压扁小量纲序列，"
                               "对比趋势建议用「双轴」。")
            elif chart_type == "面积":
                fig = charts.area_chart(df, ids, names, start, end, missing,
                                        scale=scale, log_y=log_y, zero_cols=zero_cols,
                                        pit_meta=pit_meta)
            elif chart_type == "阶梯":
                fig = charts.step_chart(df, ids, names, start, end, missing,
                                        scale=scale, log_y=log_y, zero_cols=zero_cols,
                                        pit_meta=pit_meta)
            elif chart_type == "双轴":
                if right_var is None:
                    st.info("请再选择一个变量作为右轴")
                else:
                    rid, rname = name_to_id[right_var], id_to_name[name_to_id[right_var]]
                    fig = charts.dual_axis(df, ids[0], names[0], rid, rname,
                                           start, end, missing, scale=scale,
                                           log_y=log_y, zero_cols=zero_cols,
                                           pit_meta=pit_meta)
            elif chart_type == "分布视图":
                fig = charts.histogram(df, ids[0], names[0], start, end, missing)
            else:  # 箱线图
                fig = charts.box_chart(df, ids[0], names[0], start, end)
        else:  # 分面
            specs = [(col, id_to_name[col], per_var[col]) for col in ids]
            fig = charts.facet_figures(df, specs, start, end, missing,
                                       scale=scale, log_y=log_y, zero_cols=zero_cols,
                                       pit_meta=pit_meta)

        if fig is not None:
            st.plotly_chart(charts.style_title(fig), width="stretch")

            # 数据摘要表（月度口径，语义化：中文名 + 单位 + 极值所在月）
            sub = df.loc[start:end, ids]
            summary_rows = []
            for col in ids:
                s = sub[col].dropna()
                if len(s) == 0:
                    summary_rows.append({"变量": id_to_name[col],
                                         "单位": id_to_row.loc[col].get("unit", "") or "",
                                         "有效月数": 0, "均值": "", "最新值": "",
                                         "最新月": "", "最小@月": "", "最大@月": "",
                                         "缺失月数": len(sub)})
                    continue
                summary_rows.append({
                    "变量": id_to_name[col],
                    "单位": id_to_row.loc[col].get("unit", "") or "",
                    "有效月数": len(s),
                    "均值": round(float(s.mean()), 3),
                    "最新值": round(float(s.iloc[-1]), 3),
                    "最新月": s.index[-1].strftime("%Y-%m"),
                    "最小@月": f"{s.min():.3f} @ {s.idxmin().strftime('%Y-%m')}",
                    "最大@月": f"{s.max():.3f} @ {s.idxmax().strftime('%Y-%m')}",
                    "缺失月数": len(sub) - len(s),
                })
            st.caption(f"数据摘要（{m_start} ~ {m_end}，{len(sub)} 个月，月度口径）"
                       f"—— 最小/最大标注出现月份，便于核查异常点；"
                       f"缺失月数 = 区间内无值月份（原因见图上色带）")
            st.dataframe(pd.DataFrame(summary_rows), width="stretch",
                         hide_index=True)

            # ---- 原始值下钻（M2）：原始文件序列 vs 月度面板 ----
            with st.expander("原始值下钻（L0/L1 原始文件 vs 月度面板）"):
                drill_col = st.selectbox("选择要下钻的变量",
                                         [f"{id_to_name[c]}（{c}）" for c in ids])
                dcol = drill_col.split("（")[-1].rstrip("）")
                raw_df, info = loader.load_raw_source(dcol, id_to_row.loc[dcol].to_dict())
                if raw_df is None:
                    st.warning(info.get("error", "下钻失败"))
                else:
                    reg = id_to_row.loc[dcol]
                    st.caption(f"源文件 {info['file']}（{reg.get('source_owner','')} / "
                               f"{reg.get('definition_regime','')}）｜ 解析 {info['rows']} 行"
                               f"（{int(info['parsed_ratio']*100)}%）｜ "
                               f"日期列「{info['date_col']}」 值列「{info['value_col']}」")
                    fig_raw = go.Figure()
                    fig_raw.add_trace(go.Scatter(
                        x=raw_df["date"], y=raw_df["value"], name="原始值",
                        mode="lines", line=dict(color="#7f7f7f", width=1.5),
                        connectgaps=False))
                    ps = df[dcol].dropna()
                    fig_raw.add_trace(go.Scatter(
                        x=ps.index, y=ps.values, name="月度面板（清洗后）",
                        mode="lines", line=dict(color="#c0392b", width=2, dash="dash"),
                        connectgaps=False))
                    fig_raw.update_layout(
                        template="plotly_white",
                        title=f"{id_to_name[dcol]} · 原始值与月度面板对比",
                        legend=dict(orientation="h", yanchor="bottom", y=1.02,
                                    xanchor="left", x=0),
                        margin=dict(l=60, r=60, t=60, b=40),
                        hovermode="x unified")
                    st.plotly_chart(fig_raw, width="stretch")
                    st.caption("灰色=原始文件序列；红色虚线=月度面板（PIT 清洗后）。"
                               "两者应基本吻合，明显分歧处即值得核查的异常点。")

            # ---- 缺失原因分布（M2）----
            with st.expander("缺失原因分布（所选区间）"):
                miss_ids = [c for c in ids if c in missing.columns]
                miss = missing.loc[start:end, miss_ids]
                any_missing = False
                for col in miss_ids:
                    counts = miss[col].value_counts()
                    counts = counts[counts.index != ""]  # 有值（空串）不计
                    if len(counts) == 0:
                        st.caption(f"● {id_to_name[col]}：区间内无缺失")
                        continue
                    any_missing = True
                    st.caption(f"● {id_to_name[col]}：")
                    fig_m = go.Figure(go.Bar(
                        x=counts.index.tolist(), y=counts.values.tolist(),
                        marker_color="#c0392b"))
                    fig_m.update_layout(
                        template="plotly_white",
                        title=f"{id_to_name[col]} 缺失原因分布（{m_start}~{m_end}）",
                        yaxis_title="月数", xaxis_title="缺失原因（reason code）",
                        margin=dict(l=60, r=40, t=60, b=40))
                    st.plotly_chart(fig_m, width="stretch")
                if not any_missing:
                    st.caption("所有选中变量在所选区间内均无缺失。")
                if len(miss_ids) < len(ids):
                    st.caption("注：补充数据（年度/机制季度/通缩季度/原始月度）列无逐月缺失矩阵（非月频面板列），只显示月频列的缺失原因。")

            # 导出（数据浏览，M4：公共 run_export + 可选 GLM 质检）
            if do_export:
                run_export(fig, " / ".join(names[:2]), m_start, m_end,
                           qc_check=qc_check)

    else:
        # ============ M3 关联分析 ============
        fig = None
        fig_title = tool

        try:
            if tool == "散点" and scatter_x and scatter_y:
                id_x, id_y = name_to_id[scatter_x], name_to_id[scatter_y]
                color_mode = "time" if scatter_color == "时间" else "na_reason"
                fig = charts.scatter_chart(df, id_x, id_to_name[id_x],
                                           id_y, id_to_name[id_y], start, end,
                                           color_mode=color_mode, pit_meta=pit_meta,
                                           missing_df=missing)
                fig_title = f"散点 · {id_to_name[id_x]} × {id_to_name[id_y]}"

            elif tool == "滚动相关" and corr_a and corr_b:
                id_a, id_b = name_to_id[corr_a], name_to_id[corr_b]
                fig = charts.rolling_corr_chart(df, id_a, id_to_name[id_a],
                                                id_b, id_to_name[id_b], start, end,
                                                window=corr_window, missing_df=missing,
                                                pit_meta=pit_meta)
                fig_title = f"滚动相关 · {id_to_name[id_a]} × {id_to_name[id_b]}（{corr_window}月）"

            elif tool == "相关热力图" and heat_sel:
                heat_ids = [name_to_id[l] for l in heat_sel]
                heat_names = [id_to_name[i] for i in heat_ids]
                if len(heat_ids) < 2:
                    st.info("热力图至少选择 2 个变量")
                else:
                    fig = charts.corr_heatmap(df, heat_ids, heat_names, start, end,
                                              missing_df=missing)
                    fig_title = f"相关热力图 · {len(heat_ids)} 变量"

            elif tool == "前向收益" and fwd_x and fwd_tid_label:
                id_x = name_to_id[fwd_x]
                tid = fwd_tid_label.split("（")[-1].rstrip("）")
                treg = get_target_registry()
                trow = treg[treg["target_id"] == tid].iloc[0]
                tname = target_label(trow)
                color_mode = "loss" if fwd_color == "盈亏" else "time"
                targets = get_targets()
                fig = charts.forward_return_chart(df, id_x, id_to_name[id_x],
                                                  targets, tid, tname, start, end,
                                                  color_mode=color_mode,
                                                  size_mdd=fwd_size, pit_meta=pit_meta)
                fig_title = f"前向收益 · {id_to_name[id_x]} × {tname}"
        except Exception as e:  # noqa: BLE001
            st.error(f"图表生成失败: {e}")
            fig = None

        if fig is not None:
            st.plotly_chart(charts.style_title(fig), width="stretch")
            if do_export:
                run_export(fig, fig_title, m_start, m_end, qc_check=qc_check)
        else:
            st.info("请在左侧配置分析工具参数")


# ---------- 页面分发 ----------
if PAGE == _VIEWS[0]:
    render_cn()
elif PAGE == _VIEWS[1]:
    from render_jp import render_jp
    render_jp()
elif PAGE == "⚖️ 中日对比":
    from render_compare import render_compare
    render_compare()
else:
    from render_jphist import render_jphist
    render_jphist()