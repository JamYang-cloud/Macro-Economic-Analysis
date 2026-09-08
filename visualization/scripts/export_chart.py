#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
export_chart.py — HTML → PNG 渲染脚本（宏观股市罗盘 · 可视化系统）

用法：python3 scripts/export_chart.py <html路径> <png输出路径> [宽度] [高度]

用 playwright headless chromium 打开本地 HTML，等 plotly 渲染完成后
对图表区域截图。device_scale_factor=2 输出 2x 清晰度（公众号配图可用）。
中文依赖浏览器系统字体（WSL 下为 Windows 微软雅黑），无 matplotlib
字体问题（chart-pipeline 已验证）。

依赖：playwright + chromium 已装（~/.cache/ms-playwright/）。
"""

import sys
from playwright.sync_api import sync_playwright


def main() -> int:
    if len(sys.argv) < 3:
        print("用法: export_chart.py <html> <png> [width] [height]", file=sys.stderr)
        return 2
    html_path, png_path = sys.argv[1], sys.argv[2]
    width = int(sys.argv[3]) if len(sys.argv) > 3 else 1200
    height = int(sys.argv[4]) if len(sys.argv) > 4 else 700

    from pathlib import Path
    url = Path(html_path).resolve().as_uri()

    with sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            page = browser.new_page(
                viewport={"width": width, "height": height},
                device_scale_factor=2,   # 2x 清晰度
            )
            page.goto(url, wait_until="networkidle", timeout=60000)
            # 等 plotly 渲染帧稳定（SVG 节点出现后再等一拍）
            page.wait_for_selector(".plotly-graph-div svg", timeout=30000)
            page.wait_for_timeout(800)
            # 只截图表区域（不含页面留白）
            page.locator(".plotly-graph-div").screenshot(path=png_path)
        finally:
            browser.close()
    print(f"OK: {png_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
