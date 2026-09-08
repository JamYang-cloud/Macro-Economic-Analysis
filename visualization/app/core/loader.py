#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core/loader.py — 数据加载层（宏观股市罗盘 · 可视化系统）

职责：只读加载 data_snapshot/ 下的冻结产物，统一解析为 DataFrame。
铁律：
  - 只读快照目录，绝不触碰 02_清洗标准化/ 源目录（冻结铁律）
  - 纯函数，零 Streamlit 依赖（未来换壳复用）
  - 缺失处理：源 CSV 缺失用空字符串（项目铁律 keep_default_na=False），
    数值列显式 pd.to_numeric(errors="coerce") 转 NaN
  - 统一 utf-8-sig 读取（BOM 坑，见 RECORD M0 第七节）

调用方（app.py）自行加 @st.cache_data 缓存；本层不做缓存。
"""

import os
import re

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
VIS_DIR = os.path.dirname(os.path.dirname(HERE))          # 08_可视化/
# M3 起数据源切 data_snapshot_v2/（Phase 2 重清洗后 84 变量冻结产物，
# manifest 33 条全 OK；v1 data_snapshot/ 冻结保留不再读取）
SNAPSHOT_DIR = os.path.join(VIS_DIR, "data_snapshot_v2")
CATALOG_NAME = "catalog_v2.csv"
# JP-HIST 年度长史 展示快照（08_可视化/data_snapshot_annual/，只读副本+manifest）
ANNUAL_DIR = os.path.join(VIS_DIR, "data_snapshot_annual")
ANNUAL_REGISTRY = {c: f"registry_{c}.csv" for c in ("cn", "jp")}

# JP-HIST H6-B 季度机制/通缩 展示快照（08_可视化/data_snapshot_h6/，只读副本+manifest；
# registry_q.csv 双国合一，country 列区分；文件= h6q_<side>_*.csv 单序列）
H6_DIR = os.path.join(VIS_DIR, "data_snapshot_h6")
H6_REGISTRY_NAME = "registry_q.csv"

# JP-HIST 原始层精选 展示快照（08_可视化/data_snapshot_h6raw/，月度网格；源零写入）
H6RAW_DIR = os.path.join(VIS_DIR, "data_snapshot_h6raw")
H6RAW_REGISTRY_NAME = "registry_raw.csv"

# 年度/季度行映射到 catalog_v2 同 schema 的字段（用户可见层）
_ANNUAL_CAT_FIELDS = ["variable_id", "display_name", "group", "layer",
                      "economic_block", "frequency", "unit", "model_tier",
                      "persistence_policy", "observed_start", "observed_end",
                      "coverage_rate", "risk", "na_summary", "notes"]

# 月度面板 63 个 RAW_STATE 变量列（与 missing_matrix 前 63 列对齐）
PANEL_VARIABLE_COLS = None  # 运行时从表头自动推导


def _read_csv(name, index_col=None):
    """统一 CSV 读取：utf-8-sig（剥 BOM）+ keep_default_na=False（保真）。"""
    path = os.path.join(SNAPSHOT_DIR, name)
    return pd.read_csv(path, encoding="utf-8-sig", keep_default_na=False,
                       index_col=index_col)


def _to_numeric(df, cols):
    """把指定列批量转数值，无法解析的（含空串）→ NaN。"""
    for c in cols:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    return df


def _month_index(df):
    """decision_month 'YYYY-MM' → Timestamp 索引（每月 1 日），供时间切片。
    显式 drop 列再设索引（set_index(Series) 的隐式 drop 在部分 pandas
    版本不可靠，实测 2.1.4 上列残留导致 join 报 columns overlap）。"""
    df = df.copy()
    idx = pd.to_datetime(df["decision_month"], format="%Y-%m")
    df = df.drop(columns=["decision_month"])
    df.index = idx
    df.index.name = "decision_month"
    return df


def load_panel():
    """月度原始状态面板：223 月 × 63 数值列，index=Timestamp。"""
    df = _read_csv("monthly_raw_state_panel.csv")
    global PANEL_VARIABLE_COLS
    PANEL_VARIABLE_COLS = [c for c in df.columns
                           if c not in ("decision_month", "decision_date")]
    df = _month_index(df)
    df = df.drop(columns=["decision_date"], errors="ignore")
    return _to_numeric(df, PANEL_VARIABLE_COLS)


def load_feature_panel():
    """特征面板：223 月 × 10 派生特征，index=Timestamp。"""
    df = _read_csv("feature_panel.csv")
    feat_cols = [c for c in df.columns if c != "decision_month"]
    df = _month_index(df)
    return _to_numeric(df, feat_cols)


def load_combined():
    """合并面板：63 RAW_STATE + 10 FEATURE = 73 数值列（与 missing_matrix 对齐）
    + JP-HIST CN 年度长史（hjy 展示列，Dec 月锚点；索引随之外扩到最早年度 1978-12）。"""
    panel = load_panel()
    feat = load_feature_panel()
    df = panel.join(feat, how="outer")
    ann, _ = load_annual_dec_monthly("cn")
    if ann is not None and len(ann.columns):
        df = df.join(ann, how="outer")
    qw, _ = load_h6_series_wide("cn")
    if qw is not None and len(qw.columns):
        df = df.join(qw, how="outer")
    rw, _ = load_h6raw_monthly_wide("cn")
    if rw is not None and len(rw.columns):
        df = df.join(rw, how="outer")
    # 补充数据低频列 held-last 填充：年/季度列在月轴是孤立单点（charts connectgaps=False
    # → 月尺度下不可见）；ffill 成平台（与 JP 池 PIT 季频处理同构），切「季/年」观察尺度
    # 重采样取周期末值=原始真实值，不改变语义。
    for _c in df.columns:
        if _c.startswith(("hjy_", "h6q_", "h6r_")):
            df[_c] = df[_c].ffill()
    return df


# ---------------- JP-HIST 年度长史（M1/M2/M3 数据展示层） ----------------
def load_annual_registry(country="cn"):
    """年度序列注册表（data_snapshot_annual/registry_<c>.csv → DataFrame）。"""
    path = os.path.join(ANNUAL_DIR, ANNUAL_REGISTRY[country])
    if not os.path.isfile(path):
        return pd.DataFrame()
    return _read_annual(path)


def _read_annual(path):
    return pd.read_csv(path, encoding="utf-8-sig", keep_default_na=False)


def load_annual_series_wide(country="cn"):
    """年度序列宽表：index=year(int)，列=variable_id（只含有效年；值 NaN 保留为 NaN）。"""
    reg = load_annual_registry(country)
    if reg.empty:
        return pd.DataFrame(), reg
    out = {}
    for _, r in reg.iterrows():
        p = os.path.join(ANNUAL_DIR, country, os.path.basename(str(r.source_file)))
        if not os.path.isfile(p):
            continue
        df = _read_annual(p)
        s = pd.to_numeric(df["value"], errors="coerce")
        out[r.variable_id] = pd.Series(s.values, index=df["year"].astype(int))
    wide = pd.DataFrame(out).sort_index()
    return wide, reg


def load_annual_dec_monthly(country="cn"):
    """年度序列 → 月度（每年 12-01 单点）宽表：与月频快照同轴可 join。
    观察尺度=年时每年落点即该值；月尺度只显示 12 月点（与季度/年度存量变量惯例一致）。"""
    wide, reg = load_annual_series_wide(country)
    if wide.empty:
        return None, reg
    idx = pd.to_datetime(wide.index.astype(str) + "-12-01")
    dec = wide.set_index(idx)
    dec.index.name = "decision_month"
    return dec, reg


# ---------------- JP-HIST H6-B 季度机制/通缩（M1/M2/M3 数据展示层） ----------------
def load_h6_registry():
    """H6-B 季度注册表（data_snapshot_h6/registry_q.csv → DataFrame；双国合一）。"""
    path = os.path.join(H6_DIR, H6_REGISTRY_NAME)
    if not os.path.isfile(path):
        return pd.DataFrame()
    return pd.read_csv(path, encoding="utf-8-sig", keep_default_na=False)


def _parse_quarter(qstr):
    """'YYYY-Qn' → (year, q)。"""
    y, q = str(qstr).strip().split("-Q")
    return int(y), int(q)


def data_sig():
    """展示数据源变更签名：关键文件 (name, size, mtime_ns) → hash。

    用法：上层 @st.cache_data 缓存函数把 `data_sig()` 并入参数（如
    `_cached(_sig)`），注册表/快照 CSV 内容一变（改名/加行/改值）签名即变，
    缓存自动失效——解决"registry 内容变更但长跑进程缓存不刷新"导致的
    组名漂移/分组消失（2026-09-08）。
    """
    paths = []
    # CN 月频面板 + 目录（combined/catalog 依赖）
    paths.append(os.path.join(VIS_DIR, "catalog", CATALOG_NAME))
    paths.append(os.path.join(SNAPSHOT_DIR, "monthly_raw_state_panel.csv"))
    paths.append(os.path.join(SNAPSHOT_DIR, "feature_panel.csv"))
    # JP-HIST 三批展示快照注册表（年度/季度/原始；内容变更均需使缓存失效）
    paths.append(os.path.join(ANNUAL_DIR, "registry_cn.csv"))
    paths.append(os.path.join(ANNUAL_DIR, "registry_jp.csv"))
    paths.append(os.path.join(H6_DIR, H6_REGISTRY_NAME))
    paths.append(os.path.join(H6RAW_DIR, H6RAW_REGISTRY_NAME))
    sig = []
    for p in paths:
        try:
            st_ = os.stat(p)
            sig.append((os.path.basename(p), st_.st_size, st_.st_mtime_ns))
        except OSError:
            sig.append((os.path.basename(p), -1, -1))
    return hash(tuple(sig))


def load_h6_series_wide(country="cn"):
    """H6-B 季度序列宽表：index=季首 Timestamp（1/4/7/10 月 1 日），列=variable_id
    （country 筛选后）。返回 (df, registry)。与年度层同构；季首单点，不 ffill。"""
    reg = load_h6_registry()
    if reg.empty:
        return None, reg
    out = {}
    for _, r in reg.iterrows():
        if str(r["country"]).strip().lower() != country.lower():
            continue
        p = os.path.join(H6_DIR, f"{r.variable_id}.csv")
        if not os.path.isfile(p):
            continue
        df = pd.read_csv(p, encoding="utf-8-sig", keep_default_na=False)
        vals = pd.to_numeric(df["value"], errors="coerce")
        idx = pd.to_datetime([f"{_parse_quarter(q)[0]}-{(_parse_quarter(q)[1]-1)*3+1:02d}-01"
                              for q in df["quarter"]], errors="coerce")
        s = pd.Series(vals.values, index=idx).sort_index()
        s = s[~s.index.duplicated(keep="last")]
        out[r.variable_id] = s
    wide = pd.DataFrame(out).sort_index()
    wide.index.name = "decision_month"
    return wide, reg


# ---------------- JP-HIST 原始层精选（月度网格；M1 展示层） ----------------
def load_h6raw_registry():
    """原始层精选注册表（data_snapshot_h6raw/registry_raw.csv → DataFrame）。"""
    path = os.path.join(H6RAW_DIR, H6RAW_REGISTRY_NAME)
    if not os.path.isfile(path):
        return pd.DataFrame()
    return pd.read_csv(path, encoding="utf-8-sig", keep_default_na=False)


def load_h6raw_monthly_wide(country="cn"):
    """原始层精选宽表：index=月首 Timestamp（值=该月月末/月内值），列=variable_id。
    文件列 month='YYYY-MM'。返回 (df, registry)。"""
    reg = load_h6raw_registry()
    if reg.empty:
        return None, reg
    out = {}
    for _, r in reg.iterrows():
        if str(r["country"]).strip().lower() != country.lower():
            continue
        p = os.path.join(H6RAW_DIR, f"{r.variable_id}.csv")
        if not os.path.isfile(p):
            continue
        df = pd.read_csv(p, encoding="utf-8-sig", keep_default_na=False)
        vals = pd.to_numeric(df["value"], errors="coerce")
        idx = pd.to_datetime(df["month"] + "-01", format="%Y-%m-%d", errors="coerce")
        s = pd.Series(vals.values, index=idx).sort_index()
        s = s[~s.index.duplicated(keep="last")]
        out[r.variable_id] = s
    wide = pd.DataFrame(out).sort_index()
    wide.index.name = "decision_month"
    return wide, reg


def load_missing():
    """缺失矩阵：223 月 × 73 列，每格 NA reason 代码或空串（空=有值）。"""
    df = _read_csv("missing_matrix.csv")
    return _month_index(df)


def load_catalog():
    """变量目录 v2：84 变量 × 15 列（含四组/中文名/单位/覆盖/缺失摘要）
    + JP-HIST CN 年度长史（data_snapshot_annual registry，同 schema 并入 → 与月频同一选择器）。"""
    df = _read_csv(os.path.join("..", "catalog", CATALOG_NAME))
    reg = load_annual_registry("cn")
    if reg.empty:
        return df
    ann = pd.DataFrame({f: "" for f in _ANNUAL_CAT_FIELDS}, index=range(len(reg)))
    for i, r in reg.iterrows():
        ann.at[i, "variable_id"] = r.variable_id
        ann.at[i, "display_name"] = r.display_name
        ann.at[i, "group"] = r.group_cn
        ann.at[i, "layer"] = "JP-HIST"
        ann.at[i, "frequency"] = "annual"
        ann.at[i, "unit"] = r.unit
        ann.at[i, "notes"] = r.notes
    # observed 起止（年-12 格式，与月面板口径一致）
    wide, _ = load_annual_series_wide("cn")
    if len(wide):
        for i, r in reg.iterrows():
            if r.variable_id in wide.columns:
                s = wide[r.variable_id].dropna()
                if len(s):
                    ann.at[i, "observed_start"] = f"{int(s.index.min())}-12"
                    ann.at[i, "observed_end"] = f"{int(s.index.max())}-12"
    ann = ann[df.columns]
    df = pd.concat([df, ann], ignore_index=True)

    # JP-HIST H6-B 季度机制/通缩（CN 侧）→ 同 schema 并入（独立季度组，月频池零改动）
    qreg = load_h6_registry()
    qcn = qreg[qreg["country"].astype(str).str.lower() == "cn"] if len(qreg) else pd.DataFrame()
    if len(qcn):
        qrows = pd.DataFrame({f: "" for f in _ANNUAL_CAT_FIELDS}, index=range(len(qcn)))
        for i, r in qcn.iterrows():
            qrows.at[i, "variable_id"] = r.variable_id
            qrows.at[i, "display_name"] = r.display_name
            qrows.at[i, "group"] = r.group_cn
            qrows.at[i, "layer"] = "H6-B"
            qrows.at[i, "frequency"] = "quarterly"
            qrows.at[i, "unit"] = r.unit
            qrows.at[i, "notes"] = r.notes
        qw2, _ = load_h6_series_wide("cn")
        if qw2 is not None and len(qw2.columns):
            for i, r in qcn.iterrows():
                if r.variable_id in qw2.columns:
                    s = qw2[r.variable_id].dropna()
                    if len(s):
                        qrows.at[i, "observed_start"] = (f"{s.index.min().year}-Q"
                                                         f"{(s.index.min().month-1)//3+1}")
                        qrows.at[i, "observed_end"] = (f"{s.index.max().year}-Q"
                                                       f"{(s.index.max().month-1)//3+1}")
        qrows = qrows[df.columns]
        df = pd.concat([df, qrows], ignore_index=True)

    # JP-HIST 原始层精选（CN 月度网格）→ 同 schema 并入
    rreg = load_h6raw_registry()
    rcn = rreg[rreg["country"].astype(str).str.lower() == "cn"] if len(rreg) else pd.DataFrame()
    if len(rcn):
        rrows = pd.DataFrame({f: "" for f in _ANNUAL_CAT_FIELDS}, index=range(len(rcn)))
        for i, r in rcn.iterrows():
            rrows.at[i, "variable_id"] = r.variable_id
            rrows.at[i, "display_name"] = r.display_name
            rrows.at[i, "group"] = r.group_cn
            rrows.at[i, "layer"] = "H6RAW"
            rrows.at[i, "frequency"] = "monthly"
            rrows.at[i, "unit"] = r.unit
            rrows.at[i, "notes"] = r.notes
        rw2, _ = load_h6raw_monthly_wide("cn")
        if rw2 is not None and len(rw2.columns):
            for i, r in rcn.iterrows():
                if r.variable_id in rw2.columns:
                    s = rw2[r.variable_id].dropna()
                    if len(s):
                        rrows.at[i, "observed_start"] = s.index.min().strftime("%Y-%m")
                        rrows.at[i, "observed_end"] = s.index.max().strftime("%Y-%m")
        rrows = rrows[df.columns]
        df = pd.concat([df, rrows], ignore_index=True)
    return df


def load_targets():
    """前向收益目标（M3 用）：targets_long.csv（v2，2,676 行 × 12 列）。"""
    return _read_csv("targets_long.csv")


def load_target_registry():
    """目标注册表（M3 用）：target_id → 中文名/期限/类型/公式。

    返回 DataFrame（target_registry.csv，12 目标），UI 下拉用它生成
    \"中文名（id）\"标签。
    """
    return _read_csv("target_registry.csv")


def load_current_state():
    """最新状态快照（2026-07）：current_state.csv。"""
    df = _read_csv("current_state.csv")
    return df


def load_model_input_registry():
    """14 个模型输入映射（含 economic_block）。"""
    df = _read_csv("model_input_registry.csv")
    return df


def load_pit_meta():
    """PIT 溯源字典（M2 hover 用）：{(variable_id, decision_month): meta}。

    meta = {avail, source, vintage, stale, ref, na_reason}
    来源 monthly_panel_long.csv（15k 行逐月逐变量溯源，Step 2.4 产物）。
    na_reason 为空串 = 该月有值。
    """
    df = _read_csv("monthly_panel_long.csv")
    meta = {}
    for row in df.itertuples(index=False):
        key = (row.variable_id, row.decision_month)
        meta[key] = {
            "avail": row.available_date_used or "",
            "source": row.source_file_used or "",
            "vintage": row.vintage_quality_used or "",
            "stale": row.stale_age_months or "",
            "ref": row.reference_period_used or "",
            "na_reason": row.na_reason or "",
        }
    return meta


def load_raw_source(variable_id, reg_row):
    """原始值下钻（M2）：读 data_snapshot/raw/<canonical_source>。

    返回 (df, info)：df 为 DataFrame(date, value)；
    info = {file, rows, date_col, value_col, parsed_ratio} 或 {error}。
    支持宽表（日期列+值列直接取）与长表（指标列按 series_filter 筛选）。
    日期解析宽容（pd.to_datetime coerce），解析比例在 info 中报告。
    """
    fname = (reg_row or {}).get("canonical_source", "")
    if not fname or str(fname).startswith("(derived)"):
        return None, {"error": "该变量无独立原始文件（派生变量）"}
    path = os.path.join(SNAPSHOT_DIR, "raw", fname)
    if not os.path.isfile(path):
        return None, {"error": f"原始文件未入快照: {fname}（运行 scripts/snapshot_sync.py 补拷）"}
    df = pd.read_csv(path, encoding="utf-8-sig", keep_default_na=False)

    date_col = (reg_row or {}).get("source_date_column", "") or ""
    value_col = (reg_row or {}).get("source_value_column", "") or ""
    series_filter = (reg_row or {}).get("series_filter", "") or ""

    # 长表模式：值列是"指标名"且文件中存在指标列 → 按 series_filter 筛选
    if value_col not in df.columns and series_filter:
        ind_col = None
        for c in df.columns:
            if df[c].astype(str).eq(series_filter).any():
                ind_col = c
                break
        if ind_col is not None:
            sub = df[df[ind_col].astype(str) == series_filter].copy()
            val = next((c for c in sub.columns
                        if c in ("今值", "数值", "value")), None)
            if val is None:
                cands = [c for c in sub.columns if c not in (date_col, ind_col)]
                val = cands[0] if cands else None
            df, value_col = sub, val

    # 日期列兜底（按常见列名）
    if date_col not in df.columns:
        for c in df.columns:
            if any(k in c for k in ("日期", "时间", "月份", "季度", "date", "period")):
                date_col = c
                break
    if not date_col or date_col not in df.columns:
        return None, {"error": f"无法定位日期列（{date_col or '未指定'}）"}
    if not value_col or value_col not in df.columns:
        return None, {"error": f"无法定位数值列（{value_col or '未指定'}）"}

    out = pd.DataFrame({
        "date": df[date_col].map(_parse_date),
        "value": pd.to_numeric(df[value_col], errors="coerce"),
    }).dropna(subset=["date"])
    parsed_ratio = round(len(out) / max(len(df), 1), 2)
    info = {"file": fname, "rows": len(out), "date_col": date_col,
            "value_col": value_col, "parsed_ratio": parsed_ratio}
    return out, info


def _parse_date(s):
    """宽容日期解析（下钻用）：处理中文格式与标准格式。

    覆盖 Phase 1 已知格式：
      '2008年01月份' / '2008年1月' / '2008年第1季度' / '2008年05月07日'
      '2008-01-02' / '2008-01' / '2008' / '2008.3'
    无法解析返回 NaT。
    """
    s = str(s).strip()
    m = re.match(r"(\d{4})年(\d{1,2})月份?", s)
    if m:
        return pd.Timestamp(int(m.group(1)), int(m.group(2)), 1)
    m = re.match(r"(\d{4})年第?(\d{1,2})季度", s)
    if m:
        return pd.Timestamp(int(m.group(1)), (int(m.group(2)) - 1) * 3 + 1, 1)
    m = re.match(r"(\d{4})年(\d{1,2})月(\d{1,2})日", s)
    if m:
        return pd.Timestamp(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    m = re.match(r"(\d{4})\.(\d{1,2})", s)
    if m:
        return pd.Timestamp(int(m.group(1)), int(m.group(2)), 1)
    return pd.to_datetime(s, errors="coerce")
