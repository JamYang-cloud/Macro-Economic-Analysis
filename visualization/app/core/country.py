#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core/country.py — 多国注册与日本数据加载通道（中日可视化扩展 P2）

职责：
  - COUNTRIES 注册表（cn/jp；未来 us 加一行）
  - JP 侧只读加载：state 面板 / regime / targets / pit 序列 / early_history，
    统一产出与 CN loader 同构的对象（DatetimeIndex×数值列宽表 + missing + registry）
  - 铁律：只读 宏观股市罗盘_日本/06_可视化/{data_snapshot,early_history} 副本，
    绝不触碰 FROZEN 原件；所有加载为纯函数（调用方自加 @st.cache_data）
  - M3 关键对齐：两国时间索引统一为「月首日」（CN decision_month 惯例），
    JP 月末日期映射为月首（如 2026-07-31 → 2026-07-01）

文件名/ID 约定与跨平台：Windows 目录含中文，统一用绝对路径常量。
"""

import os

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
VIS_DIR = os.path.dirname(os.path.dirname(HERE))            # 宏观股市罗盘/08_可视化
JP_PROJ = os.path.abspath(os.path.join(VIS_DIR, "..", "data", "japan"))  # 仓库 data/japan
JP_SNAPSHOT = os.path.join(JP_PROJ, "data_snapshot")
JP_EARLY = os.path.join(JP_PROJ, "early_history")
JP_CROSSWALK = os.path.join(JP_PROJ, "crosswalk_v1.csv")

COUNTRIES = {
    "cn": {
        "name": "中国",
        "flag": "🇨🇳",
        "snapshot": os.path.join(VIS_DIR, "data_snapshot_v2"),
        "registry": "variable_registry_v2.csv",
    },
    "jp": {
        "name": "日本",
        "flag": "🇯🇵",
        "snapshot": JP_SNAPSHOT,
        "names_file": "jp_viz_feature_names.csv",
        "registry": "jp17_feature_registry_v1.csv",
    },
    # 预留：us 接入时加一行（数据目录/registry 对齐 crosswalk 多国扩展）
}

# JP 面板文件名（data_snapshot/ 副本，FROZEN 语义）
JP_STATE_FILES = {
    "primary": "state_monthly_primary.csv",
    "sensitivity": "state_monthly_sensitivity.csv",
    "equity_primary": "state_equity_primary.csv",
    "equity_sensitivity": "state_equity_sensitivity.csv",
}
JP_ID_COL = "date"
JP_REGIME_FILE = "policy_regime_11段.csv"
JP_TARGET_FILE = "target_monthly_v2.csv"
JP_TARGET_REGISTRY = "jp18_target_registry_v3.csv"
JP_DESCRIPTIVE = "state_descriptive_current.csv"
JP_PIT_DIR = "pit"
# 早期段（COMPARISON-ONLY）
JP_EARLY_FILES = {
    "nikkei225_full": "nikkei225_daily_full_1949.csv",
    "discount_rate": "discount_rate_boj_1953.csv",
    "retail_mom": "retail_sales_mom_1955.csv",
    "ppi": "ppi_manufacturing_1960.csv",
    "gdp_real_yoy": "gdp_real_yoy_fy_1955_cao.csv",
    "aging_65plus": "aging_65plus_share_1950_soumu.csv",
}
JP_EARLY_NAMES = {
    "nikkei225_full": "日经225收盘价（全史 PRICE PROXY）",
    "discount_rate": "公定歩合贴现率（早期政策利率）",
    "retail_mom": "零售销售环比（镜像）",
    "ppi": "制造业PPI（镜像）",
    "gdp_real_yoy": "実質GDP增速（FY 年度）",
    "aging_65plus": "65岁以上人口占比",
}
JP_EARLY_UNITS = {
    "nikkei225_full": "点", "discount_rate": "%", "retail_mom": "% 环比",
    "ppi": "指数(2015=100)", "gdp_real_yoy": "% 同比", "aging_65plus": "%",
}


def _read_csv(path):
    return pd.read_csv(path, encoding="utf-8-sig", keep_default_na=False)


def _to_month_start(series_or_df):
    """月末日期（YYYY-MM-DD）→ 月首 Timestamp，与 CN 面板同轴。"""
    if isinstance(series_or_df, pd.Series):
        dt = pd.to_datetime(series_or_df, errors="coerce")
        return dt.dt.to_period("M").dt.to_timestamp()
    df = series_or_df.copy()
    dt = pd.to_datetime(df[JP_ID_COL], errors="coerce")
    df.index = dt.dt.to_period("M").dt.to_timestamp()
    df.index.name = "decision_month"
    return df.drop(columns=[JP_ID_COL])


def _wide_to_numeric(df, cols):
    for c in cols:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    return df


# ---------------- JP 元数据 ----------------
def load_jp_names():
    """feature_id → 中文可读名/单位/分组（用户可见层，唯一权威）。"""
    df = _read_csv(os.path.join(JP_SNAPSHOT, "jp_viz_feature_names.csv"))
    return df


def load_jp_registry():
    """JP17 feature registry（FROZEN 副本）。"""
    return _read_csv(os.path.join(JP_SNAPSHOT, "jp17_feature_registry_v1.csv"))


def jp_name_map():
    df = load_jp_names()
    return dict(zip(df["feature_id"], df["中文名"]))


def jp_unit_map():
    df = load_jp_names()
    return dict(zip(df["feature_id"], df["单位"]))


def jp_group_map():
    df = load_jp_names()
    return dict(zip(df["feature_id"], df["分组"]))


# ---------------- JP 月度状态面板（M2 主数据） ----------------
def load_jp_state(branch="sensitivity"):
    """JP 月度 state 宽表 → 与 CN combined 同构：
    index=月首 Timestamp；列=特征（含 policy_regime_id 文本列剔除）；
    返回 (df, col_meta)。col_meta={col: {name_cn, unit, group}}（仅数值特征）。
    """
    path = os.path.join(JP_SNAPSHOT, JP_STATE_FILES[branch])
    df = _read_csv(path)
    date_cols = [c for c in df.columns if c not in (JP_ID_COL, "policy_regime_id")]
    df = _to_month_start(df)
    df = df.drop(columns=["policy_regime_id"], errors="ignore")
    # 清理 AUDIT 三列保留（m2_yoy 等）但 numeric
    df = _wide_to_numeric(df, date_cols)
    names = jp_name_map()
    units = jp_unit_map()
    groups = jp_group_map()
    meta = {c: {"name_cn": names.get(c, c), "unit": units.get(c, ""),
                "group": groups.get(c, "未分组")} for c in date_cols}
    return df, meta


def jp_missing(df):
    """由 state 宽表空值构造缺失矩阵（reason='NA'；空串=有值）——与 CN missing 同构。"""
    out = df.copy().astype(object)
    out[df.isna()] = "JP:未发布(空值)"
    out[df.notna()] = ""
    return out


def load_jp_regime():
    """policy regime 11 段：regime_start → regime_id（M2 时间轴底色）。"""
    df = _read_csv(os.path.join(JP_SNAPSHOT, JP_REGIME_FILE))
    return df


def load_jp_regime_df_for_axis():
    """返回 [(start_ts, regime_id)] 供底色分带。"""
    df = load_jp_regime()
    out = []
    for _, r in df.iterrows():
        ts = pd.to_datetime(r["regime_start"]).to_period("M").to_timestamp()
        out.append((ts, r["regime_id"]))
    return out


# ---------------- JP targets / descriptive ----------------
def load_jp_targets():
    """12-target 长表（379 决策月 × 14 列）。index=月首。"""
    df = _read_csv(os.path.join(JP_SNAPSHOT, JP_TARGET_FILE))
    return _to_month_start(df)


def load_jp_target_registry():
    return _read_csv(os.path.join(JP_SNAPSHOT, JP_TARGET_REGISTRY))


def load_jp_descriptive():
    return _read_csv(os.path.join(JP_SNAPSHOT, JP_DESCRIPTIVE))


# ---------------- JP PIT 序列（下钻 / 早期段对比数据源） ----------------
def load_jp_pit_series(series_id):
    """读取 data_snapshot/pit/pit_<series_id>__<FREQ>.csv（唯一匹配），
    返回 DataFrame：index=原始日期（月/季末 Timestamp 保留原义），列 value。
    供下钻与 M3 早期窗口取数（含 PIT 18 列元数据经 .attrs 附上）。
    """
    pit_dir = os.path.join(JP_SNAPSHOT, JP_PIT_DIR)
    cands = [f for f in os.listdir(pit_dir)
             if f.startswith(f"pit_{series_id}__") and f.endswith(".csv")]
    if not cands:
        return None
    df = _read_csv(os.path.join(pit_dir, sorted(cands)[0]))
    attrs = {c: df[c].iloc[0] for c in df.columns} if len(df) else {}
    value = pd.to_numeric(df["value"], errors="coerce")
    out = pd.DataFrame({"value": value.values},
                       index=pd.to_datetime(df["date"], errors="coerce"))
    out.index.name = "date"
    out.attrs = attrs
    return out


def list_jp_pit_series():
    pit_dir = os.path.join(JP_SNAPSHOT, JP_PIT_DIR)
    return sorted(f[4:].rsplit("__", 1)[0]
                  for f in os.listdir(pit_dir)
                  if f.startswith("pit_") and f.endswith(".csv")
                  and "release_calendar" not in f)


# PIT 序列中文名/单位（可视化层命名；code 自解释不足，人工映射 39 条）
PIT_NAMES = {
    "BOJ_ASSETS_FRED": ("BOJ总资产(镜像)", "亿日元"), "BOJ_TOTAL_ASSETS": ("日本银行总资产(官方)", "亿日元"),
    "CALL_UNC_BOJ_DAILY": ("无担保隔夜拆借利率日度", "%"), "CALL_UNC_MONTHLY_1985": ("拆借利率月均(镜像)", "%"),
    "CPI2025_ALL": ("CPI総合同比(2025基官方)", "%"), "CPI2025_CORECORE": ("CPI核心-核心同比(官方)", "%"),
    "CPI2025_CORE": ("CPI核心同比(官方)", "%"), "CPI2025_EXRENT": ("CPI除租金同比(官方)", "%"),
    "CPIALL_FRED": ("CPI同比(镜像,停2021)", "%"), "CPICORE_FRED_2015B": ("核心CPI(镜像,停2021)", "%同比/自算"),
    "CREDIT_HH_U": ("家庭部门信贷(BIS)", ""), "CREDIT_NFC_U": ("非金融企业信贷(BIS)", ""),
    "CREDIT_PNFS_A": ("私人非金融信贷总量年化(BIS)", ""), "CREDIT_PNFS_U": ("私人非金融部门信贷(BIS)", ""),
    "EXPORT_FRED_SA": ("出口(镜像SA)", ""), "IIP_FRED_MOM": ("工业生产环比(镜像)", "%环比"),
    "IMPORT_FRED_SA": ("进口(镜像SA)", ""), "JGB10Y_FRED": ("10年国债收益率(FRED镜像)", "%"),
    "M2_CURRENT_AVG": ("M2现行段平均(官方)", "万亿日元"), "M2_FRED_SA": ("M2(镜像SA,停2017)", ""),
    "M2_OLD_AVG": ("M2旧段平均(官方,停1999)", "万亿日元"), "M2_OLD_EOP": ("M2旧段期末(官方,停1999)", "万亿日元"),
    "M2_REF_AVG": ("M2参考段平均(官方)", "万亿日元"), "MONETARY_BASE": ("基础货币(官方)", "万亿日元"),
    "MONETARY_BASE_YOY": ("基础货币同比(官方)", "%同比"), "NETTRADE_FRED_SA": ("净出口(镜像SA)", ""),
    "PROP_NOMINAL": ("房价名义(BIS)", ""), "PROP_REAL": ("房价实际(BIS)", ""),
    "SPASTT01_FRED_MONTHLY": ("TOPIX月均(镜像proxy)", "点"), "TANKAN_MFG_DI": ("短观制造业DI", "DI"),
    "TANKAN_NONMFG_DI": ("短观非制造业DI", "DI"), "TOPIX_OFFICIAL_HIGH": ("TOPIX年内高(官方年度)", "点"),
    "TOPIX_OFFICIAL_LOW": ("TOPIX年内低(官方年度)", "点"), "TOPIX_OFFICIAL_YEAREND": ("TOPIX年末(官方年度)", "点"),
    "UNEMPLOY_ILO": ("失业率(ILO镜像)", "%"), "USDJPY_DAILY": ("美元兑日元日度", "日元/美元"),
    "USDJPY_MONTHLY_1957": ("美元兑日元月均(镜像)", "日元/美元"), "WAGE_MFG_HOURLY_FRED": ("制造业时薪(镜像)", "2015=100"),
    "WAGE_PRIVATE_FRED": ("私营月薪(镜像,停2023)", "2015=100"),
}


def load_jp_pit_wide():
    """39 条 PIT 序列 → 月度宽表（index=月首；日度→月末值、季频→月末+前向填充、
    月频原值；停更序列不 ffill）。返回 (df, meta)。供 JP 序列库浏览/M3 取数。"""
    pit_dir = os.path.join(JP_SNAPSHOT, JP_PIT_DIR)
    cols, meta = {}, {}
    for f in sorted(os.listdir(pit_dir)):
        if not (f.startswith("pit_") and f.endswith(".csv")) or "release_calendar" in f:
            continue
        sid = f[4:].rsplit("__", 1)[0]
        df = _read_csv(os.path.join(pit_dir, f))
        dt = pd.to_datetime(df["date"], errors="coerce")
        val = pd.to_numeric(df["value"], errors="coerce")
        s = pd.Series(val.values, index=dt).sort_index()
        s = s[~s.index.duplicated(keep="last")]
        # 频次判定（非空间隔中位）
        idx = s.dropna().index
        if len(idx) >= 2:
            med = int(pd.Series(idx).diff().dropna().median().days)
        else:
            med = 30
        if med >= 40:          # 季频/年频 → 月末 last + ffill
            s = s.resample("M").last().ffill()
        else:                   # 日度/月频 → 月末 last（月频无缺不受影响）
            s = s.resample("M").last()
        s.index = s.index.to_period("M").to_timestamp()
        name, unit = PIT_NAMES.get(sid, (sid, ""))
        meta[sid] = {"name_cn": name, "unit": unit, "group": "序列库(官方/镜像)"}
        cols[sid] = s
    wide = pd.DataFrame(cols).sort_index()
    wide.index.name = "decision_month"
    return wide, meta


def load_jp_nikkei_monthly(source="snapshot"):
    """日经225 收盘 → 月末序列（index=月首）。source=snapshot(1985+) / full(1949+)。"""
    if source == "full":
        p = os.path.join(JP_EARLY, JP_EARLY_FILES["nikkei225_full"])
    else:
        p = os.path.join(JP_SNAPSHOT, "nikkei225_daily_fred.csv")
    df = _read_csv(p)
    dt = pd.to_datetime(df[df.columns[0]], errors="coerce")
    val = pd.to_numeric(df[df.columns[1]], errors="coerce")
    s = pd.Series(val.values, index=dt).sort_index()
    s = s.resample("M").last()
    s.index = s.index.to_period("M").to_timestamp()
    return s


# state 层已有同源/决策口径的特征 → 池中隐藏对应 PIT 原始序列（防重复选择）
PIT_HIDE_DUP = {"CALL_UNC_BOJ_DAILY", "USDJPY_DAILY", "TANKAN_MFG_DI",
                "TANKAN_NONMFG_DI", "MONETARY_BASE_YOY", "BOJ_TOTAL_ASSETS"}
# PIT 序列族分组（可视化 UI 分组，替代笼统「序列库」）
PIT_GROUPS = {
    "利率": {"CALL_UNC_MONTHLY_1985", "JGB10Y_FRED"},
    "汇率": {"USDJPY_MONTHLY_1957"},
    "货币": {"M2_CURRENT_AVG", "M2_REF_AVG", "M2_OLD_AVG", "M2_OLD_EOP",
             "M2_FRED_SA", "MONETARY_BASE", "BOJ_ASSETS_FRED"},
    "信贷": {"CREDIT_HH_U", "CREDIT_NFC_U", "CREDIT_PNFS_A", "CREDIT_PNFS_U"},
    "价格": {"CPI2025_ALL", "CPI2025_CORE", "CPI2025_CORECORE", "CPI2025_EXRENT",
             "CPIALL_FRED", "CPICORE_FRED_2015B", "PROP_NOMINAL", "PROP_REAL"},
    "实体": {"UNEMPLOY_ILO", "WAGE_MFG_HOURLY_FRED", "WAGE_PRIVATE_FRED",
             "IIP_FRED_MOM", "PROP_NOMINAL", "PROP_REAL"},
    "贸易": {"EXPORT_FRED_SA", "IMPORT_FRED_SA", "NETTRADE_FRED_SA"},
    "股票": {"SPASTT01_FRED_MONTHLY", "TOPIX_OFFICIAL_HIGH",
             "TOPIX_OFFICIAL_LOW", "TOPIX_OFFICIAL_YEAREND"},
}
_GROUP_OWNER = {}
for _g, _codes in PIT_GROUPS.items():
    for _c in _codes:
        _GROUP_OWNER.setdefault(_c, _g)


def _pit_group(sid):
    return _GROUP_OWNER.get(sid, "序列库-其他")


def load_jp_pool():
    """JP 统一变量池（P3v2 用户需求：货币 vs 股市等任意组合同图）。

    合并 = state 月度面板(10 列, 1995+) ∪ PIT 序列库(39 - 6 同源隐藏 = 33)
           ∪ 早期段 5 序列 ∪ 日经225 全史月末(1949+)  →  约 49 列，统一月首轴。
    返回 (wide_df, meta)，meta[c]={name_cn, unit, group, level}。
    level: state=决策网格 / pit=原始PIT月度化 / early=COMPARISON-ONLY / market=股市。
    """
    wide, meta = load_jp_pit_wide()
    # 隐藏与 state 同源的 PIT 原始序列
    for h in PIT_HIDE_DUP:
        if h in wide:
            del wide[h]
            del meta[h]
    # state 面板并入（决策网格口径优先命名）
    sdf, smeta = load_jp_state("sensitivity")
    for c in sdf.columns:
        wide[c] = sdf[c]
        g = smeta[c]["group"]
        meta[c] = {"name_cn": smeta[c]["name_cn"], "unit": smeta[c]["unit"],
                   "group": g if g != "未分组" else "货币", "level": "state"}
    # 早期段 5 序列（日经除外——单独 market 列）
    for k, fname in JP_EARLY_FILES.items():
        if k == "nikkei225_full":
            continue
        s, em = load_jp_early(k)
        nm = em["name_cn"]
        s2 = s.resample("M").last() if em["freq"] == "monthly" else s
        wide[nm] = s2.reindex(wide.index.union(s2.index)).ffill().reindex(wide.index)
        grp = {"gdp_real_yoy": "实体", "aging_65plus": "实体",
               "ppi": "价格", "retail_mom": "实体", "discount_rate": "利率"}[k]
        meta[nm] = {"name_cn": nm, "unit": em["unit"], "group": grp,
                    "level": "early"}
    # 日经225 全史月末（股市通道，与宏观同池可比）
    nk = load_jp_nikkei_monthly("full").resample("M").last()
    nm = "日经225收盘价(月末·全史proxy)"
    wide[nm] = nk.reindex(wide.index.union(nk.index)).ffill().reindex(wide.index)
    meta[nm] = {"name_cn": nm, "unit": "点", "group": "股票", "level": "market"}
    # JP-HIST 年度长史（展示层并入：每年 12 月单点；meta level='jphist'）
    from . import loader as _ld
    _dec, _reg = _ld.load_annual_dec_monthly("jp")
    if _dec is not None and len(_dec.columns):
        _regi = _reg.set_index("variable_id") if len(_reg) else None
        for c in _dec.columns:
            wide[c] = _dec[c]
            if _regi is not None and c in _regi.index:
                row = _regi.loc[c]
                meta[c] = {"name_cn": row.display_name, "unit": row.unit,
                           "group": row.group_cn, "level": "jphist"}
    # JP-HIST H6-B 季度机制/通缩（展示层并入：季首单点；meta level='h6b'）
    _qw, _qreg = _ld.load_h6_series_wide("jp")
    if _qw is not None and len(_qw.columns):
        _qregi = _qreg.set_index("variable_id") if len(_qreg) else None
        for c in _qw.columns:
            wide[c] = _qw[c]
            if _qregi is not None and c in _qregi.index:
                row = _qregi.loc[c]
                meta[c] = {"name_cn": row.display_name, "unit": row.unit,
                           "group": row.group_cn, "level": "h6b"}
    # 补充数据低频列 held-last 填充（同 CN loader）：年度/季度列月轴单点孤立不可见，
    # ffill 成平台；池内 PIT 季频序列本来就是 ffill 月度化——语义一致。
    for _c in wide.columns:
        if _c in meta and meta[_c].get("level") in ("jphist", "h6b"):
            wide[_c] = wide[_c].ffill()
    wide = wide.sort_index()
    wide.index.name = "decision_month"
    return wide, meta


# ---------------- JP early_history（COMPARISON-ONLY） ----------------
def load_jp_early(key):
    """早期段比对序列 → (df, meta)。保留原始频率 index（annual=年首, monthly=月首,
    daily=原日）；year 列 int 需 str 化解析（避免被当纳秒戳）。"""
    fname = JP_EARLY_FILES[key]
    df = _read_csv(os.path.join(JP_EARLY, fname))
    date_col = df.columns[0]
    val_col = df.columns[1]
    raw = df[date_col].astype(str).str.strip()
    dt = pd.to_datetime(raw, errors="coerce")
    if (dt.dt.year.nunique() == dt.notna().sum() and
            (dt.dt.month == 1).all() and (dt.dt.day == 1).all()):
        freq = "annual"
    elif (dt - dt.dt.to_period("M").dt.to_timestamp()).dt.days.abs().max() <= 1:
        freq = "monthly"
    else:
        freq = "daily"
    out = pd.DataFrame({val_col: pd.to_numeric(df[val_col], errors="coerce").values},
                       index=dt)
    out.index.name = "date"
    meta = {"name_cn": JP_EARLY_NAMES[key], "unit": JP_EARLY_UNITS[key],
            "source": fname, "freq": freq}
    return out, meta


# ---------------- crosswalk（M3 概念对齐表） ----------------
def load_crosswalk():
    df = _read_csv(JP_CROSSWALK)
    return df


# ---------------- 自检（P2 验收：与 FREEZE 基线核对） ----------------
def verify_jp_state():
    """JP 面板加载自检：行数/特征非空 vs FREEZE_JP1.7 invariants。"""
    results = []
    df, meta = load_jp_state("sensitivity")
    results.append(("state_sensitivity 行数", len(df), 379))
    # FREEZE 基线非空（JP1.7 v3 invariants）
    baseline = {"call_unc_boj_m": 343, "usdjpy_m": 379, "m2_yoy_canonical": 379,
                "mb_yoy": 379, "boj_assets": 339, "tankan_mfg_di": 379,
                "tankan_nonmfg_di": 379}
    ok = True
    for col, exp in baseline.items():
        got = int(df[col].notna().sum())
        flag = got == exp
        ok &= flag
        results.append((f"非空 {col}", got, exp))
    # 中文名映射覆盖（MODEL_X 7 + AUDIT 3）
    names = jp_name_map()
    missing_names = [c for c in df.columns if c not in names and c != "policy_regime_id"]
    results.append(("中文名缺失特征", len(missing_names), 0))
    return results, ok
