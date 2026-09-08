#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core/export.py — 图表导出层（宏观股市罗盘 · 可视化系统）

职责：
  1) fig_to_html：Plotly Figure → 自包含 HTML（plotly.js 内联，离线可用）
  2) export_png：调用 scripts/export_chart.py（playwright 渲染）出 PNG

设计：
  - 浏览器渲染（playwright）而非 kaleido：浏览器吃 Windows 系统字体，
    中文无豆腐块（chart-pipeline 已验证）；kaleido 独立渲染器中文字体是坑
  - HTML 内联 plotly.js（include_plotlyjs=True）：不依赖 CDN，截图不白屏
  - 零 Streamlit 依赖；导出目录由调用方（app.py）决定
"""

import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
VIS_DIR = os.path.dirname(os.path.dirname(HERE))       # 08_可视化/
RENDER_SCRIPT = os.path.join(VIS_DIR, "scripts", "export_chart.py")

# 完整版 plotly.js（本地注入用）。来源：cdn.jsdelivr.net/npm/plotly.js-dist@2.24.1
# /plotly.min.js，2026-08-27 下载（3.59MB）。
# 背景：plotly.py 5.15 的 to_html(include_plotlyjs=True) 内联的是 partial
# bundle（2.71MB，heatmap 模块缺失）→ heatmap trace 在浏览器被降级渲染成
# scatter 折线（M3 实测：无 heatmaplayer 层、画 8 圆点+对角线）。streamlit
# 页面正常（前端是另一套完整 plotly.js），仅导出路径受影响。手动注入完整
# bundle 修复，同时保留离线渲染能力。
PLOTLYJS_PATH = os.path.join(VIS_DIR, "scripts", "plotly-2.24.1.min.js")


def fig_to_html(fig, title="", width=1200, height=700):
    """Figure → 自包含 HTML 字符串（完整 plotly.js 内联、隐藏 modebar、无水印）。

    include_plotlyjs=False + 手动注入本地完整 bundle（见 PLOTLYJS_PATH 注释）。
    导出前统一应用标题样式（M4 视觉常量）。
    """
    from . import charts  # 延迟 import（防循环依赖）
    fig = charts.style_title(fig)
    html = fig.to_html(
        full_html=True,
        include_plotlyjs=False,      # 手动注入完整 bundle（partial bundle 缺 heatmap）
        config={"displayModeBar": False, "responsive": True},
        default_width=f"{width}px",
        default_height=f"{height}px",
    )
    if os.path.isfile(PLOTLYJS_PATH):
        with open(PLOTLYJS_PATH, encoding="utf-8") as f:
            js = f.read()
        html = html.replace(
            "</head>",
            f"<script type=\"text/javascript\">{js}</script></head>", 1)
    if title:
        html = html.replace("<title>Plot</title>", f"<title>{title}</title>", 1)
    return html


def export_png(fig, png_path, title="", width=1200, height=700):
    """Figure → PNG。先生成临时 HTML，再调 playwright 渲染脚本截图。

    返回：png_path（成功）或抛 RuntimeError（渲染失败）。
    """
    html_str = fig_to_html(fig, title=title, width=width, height=height)
    with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as f:
        tmp_html = f.name
        f.write(html_str.encode("utf-8"))
    try:
        cmd = [sys.executable, RENDER_SCRIPT, tmp_html, png_path,
               str(width), str(height)]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if proc.returncode != 0:
            raise RuntimeError(f"export_chart.py 失败: {proc.stderr[-800:]}")
    finally:
        os.unlink(tmp_html)
    if not os.path.isfile(png_path) or os.path.getsize(png_path) == 0:
        raise RuntimeError("PNG 输出为空或未生成")
    return png_path
