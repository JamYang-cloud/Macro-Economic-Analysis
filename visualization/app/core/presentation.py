#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core/presentation.py — 推荐呈现规则引擎（宏观股市罗盘 · 可视化系统）

职责：根据变量性质推荐"呈现方式 + 理由"，供 UI 显示提示与分面默认值。
规则按数据性质分类（2026-08-27 用户确认的 7 类建议），显式可审计；
新增变量类型在此追加规则，不侵入图表层。

返回结构：
  {"chart": "折线|分布视图|箱线图|面积",
   "reason": "为什么推荐这个",
   "note": "补充提示（可为空）",
   "zero_line": bool,   # 是否自动加 0 轴参考线（差值/利差类）
   "suggest_scale": "月|季|年|None"}  # 建议观察尺度

零 Streamlit 依赖。
"""

# 波动/派生统计类：分布形态优先
VOLATILE = {"fr007_vol", "fr007_p90", "mkt.hs300_volume"}

# 差值/利差类：0 轴有经济含义
ZERO_LINE = {"m1_m2_gap", "term_spread", "pmi_gap", "eyg", "delta_pmi"}


def default_presentation(variable_id, cat_row):
    """推荐呈现方式。cat_row = catalog 行（dict，含 frequency/unit/layer）。"""
    freq = (cat_row or {}).get("frequency", "")

    if variable_id in VOLATILE:
        return {
            "chart": "分布视图",
            "reason": "波动/派生统计类：分布形态（尖峰厚尾）比趋势更重要",
            "note": "折线可辅助看压力区间随时间演化",
            "zero_line": False,
            "suggest_scale": None,
        }

    if variable_id in ZERO_LINE:
        return {
            "chart": "折线",
            "reason": "差值/利差类：正负分界有经济含义，已自动加 0 轴参考线",
            "note": "",
            "zero_line": True,
            "suggest_scale": None,
        }

    if freq in ("quarterly", "annual"):
        return {
            "chart": "折线",
            "reason": f"低频状态类（原始频率 {freq}）：建议切到季度/年度尺度消除阶梯",
            "note": "",
            "zero_line": False,
            "suggest_scale": "季" if freq == "quarterly" else "年",
        }

    if "_yoy" in variable_id or variable_id.startswith(("inf.", "gro.")):
        return {
            "chart": "折线",
            "reason": "同比/增速类：天然平稳，折线看周期最直观",
            "note": "分布视图可辅助核查离群点",
            "zero_line": False,
            "suggest_scale": None,
        }

    return {
        "chart": "折线",
        "reason": "存量/水平类：折线看趋势与周期位置最直观",
        "note": "怀疑异常时可切分布视图核查离群",
        "zero_line": False,
        "suggest_scale": None,
    }


def recommend_text(variable_id, cat_row):
    """UI 提示条文案：'推荐折线 —— 理由；补充'。"""
    rec = default_presentation(variable_id, cat_row)
    text = f"推荐 {rec['chart']} —— {rec['reason']}"
    if rec["note"]:
        text += f"；{rec['note']}"
    if rec["suggest_scale"]:
        text += f"（建议观察尺度：{rec['suggest_scale']}）"
    return text
