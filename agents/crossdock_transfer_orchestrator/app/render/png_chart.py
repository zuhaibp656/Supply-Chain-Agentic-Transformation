"""Self-contained Pillow high-resolution PNG executive chart generator (1200x640)."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    Image = None  # type: ignore


def _fmt_num(val: float) -> str:
    abs_v = abs(val)
    if abs_v >= 1_000_000:
        return f"{val / 1_000_000:.2f}M"
    if abs_v >= 10_000:
        return f"{val / 1_000:.1f}k"
    if abs_v >= 100:
        return f"{val:,.0f}"
    return f"{val:,.2f}"


def render_comparison_png(
    agent_id: str,
    title: str,
    subtitle: str,
    labels: List[str],
    series_a: List[float],
    series_a_label: str,
    series_b: List[float],
    series_b_label: str,
    y_title: str = "Value",
    output_path: Optional[Path] = None,
) -> Dict[str, Any]:
    """Renders a crisp 1200x640 grouped comparison chart PNG using Pillow and saves locally."""
    if output_path is None:
        pkg_root = Path(__file__).resolve().parent.parent.parent
        art_dir = pkg_root / "artifacts"
        try:
            art_dir.mkdir(parents=True, exist_ok=True)
            test_file = art_dir / ".write_check"
            test_file.write_text("ok", encoding="utf-8")
            test_file.unlink(missing_ok=True)
        except Exception:
            art_dir = Path(os.environ.get("TMPDIR", "/tmp")) / "supply_chain_artifacts"
            art_dir.mkdir(parents=True, exist_ok=True)
        output_path = art_dir / f"{agent_id}_analysis_chart.png"
    else:
        output_path.parent.mkdir(parents=True, exist_ok=True)

    svg_path = output_path.with_suffix(".svg")
    n_svg = min(len(labels), len(series_a), len(series_b), 8)
    if n_svg > 0:
        sa_v = [float(x) for x in series_a[:n_svg]]
        sb_v = [float(x) for x in series_b[:n_svg]]
        all_v = sa_v + sb_v + [0.0]
        mn_v, mx_v = min(all_v), max(all_v)
        sp_v = (mx_v - mn_v) if (mx_v - mn_v) > 1e-9 else 1.0
        pl, pr, pt, pb = 96, 1144, 158, 548
        ph, pw = pb - pt, pr - pl
        zy = int(pb - ((0.0 - mn_v) / sp_v) * ph)
        sw = pw / n_svg
        bw = max(14, int(sw * 0.30))
        svg_bars = []
        for idx_i in range(n_svg):
            cx = int(pl + (idx_i + 0.5) * sw)
            ya = int(pb - ((sa_v[idx_i] - mn_v) / sp_v) * ph)
            yb = int(pb - ((sb_v[idx_i] - mn_v) / sp_v) * ph)
            ta, ba = min(ya, zy), max(ya, zy)
            tb, bb = min(yb, zy), max(yb, zy)
            lbl_s = str(labels[idx_i])[-14:].replace("&", "&amp;").replace("<", "&lt;")
            svg_bars.append(
                f'<rect x="{cx - bw - 3}" y="{ta}" width="{bw}" height="{max(2, ba - ta)}" rx="3" fill="#64748b"/>'
                f'<text x="{cx - bw - 3}" y="{max(142, ta - 6)}" font-size="11" fill="#475569">{_fmt_num(sa_v[idx_i])}</text>'
                f'<rect x="{cx + 3}" y="{tb}" width="{bw}" height="{max(2, bb - tb)}" rx="3" fill="#2563eb"/>'
                f'<text x="{cx + 3}" y="{max(142, tb - 6)}" font-size="11" font-weight="600" fill="#1d4ed8">{_fmt_num(sb_v[idx_i])}</text>'
                f'<text x="{cx}" y="{pb + 22}" font-size="11" text-anchor="middle" fill="#1e293b">{lbl_s}</text>'
            )
        t_esc = title[:95].replace("&", "&amp;").replace("<", "&lt;")
        s_esc = subtitle[:115].replace("&", "&amp;").replace("<", "&lt;")
        la_esc = series_a_label[:42].replace("&", "&amp;").replace("<", "&lt;")
        lb_esc = series_b_label[:42].replace("&", "&amp;").replace("<", "&lt;")
        svg_doc = (
            '<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="640" viewBox="0 0 1200 640" font-family="Inter, system-ui, sans-serif">'
            '<rect width="1200" height="640" fill="#f8fafc"/>'
            '<rect x="20" y="20" width="1160" height="600" rx="16" fill="#ffffff" stroke="#e2e8f0" stroke-width="2"/>'
            '<rect x="20" y="20" width="1160" height="76" rx="16" fill="#0f172a"/>'
            f'<text x="48" y="52" font-size="18" font-weight="700" fill="#ffffff">{t_esc}</text>'
            f'<text x="48" y="76" font-size="12" fill="#94a3b8">{s_esc}</text>'
            f'<rect x="48" y="114" width="16" height="12" rx="2" fill="#64748b"/><text x="72" y="124" font-size="12" fill="#334155">{la_esc}</text>'
            f'<rect x="380" y="114" width="16" height="12" rx="2" fill="#2563eb"/><text x="404" y="124" font-size="12" fill="#334155">{lb_esc}</text>'
            f'<line x1="{pl}" y1="{zy}" x2="{pr}" y2="{zy}" stroke="#475569" stroke-width="1.5"/>'
            + "".join(svg_bars)
            + f'<text x="48" y="602" font-size="11" fill="#94a3b8">XYZ Global Industries Corp. (XYZ-CORP-01) · Deterministic Python Analytics · Agent: {agent_id}</text>'
            + "</svg>"
        )
        svg_path.write_text(svg_doc, encoding="utf-8")

    if Image is None:
        import struct
        import zlib

        w, h = 1200, 640
        bg = bytes((255, 255, 255))
        hdr = bytes((15, 23, 42))
        ca = bytes((100, 116, 139))
        cb = bytes((37, 99, 235))
        grid_c = bytes((226, 232, 240))
        buf = [bytearray(bg * w) for _ in range(h)]
        for y in range(20, 96):
            buf[y][20 * 3 : (w - 20) * 3] = hdr * (w - 40)
        for gy in (158, 255, 353, 450, 548):
            buf[gy][96 * 3 : 1144 * 3] = grid_c * (1144 - 96)
        if n_svg > 0:
            for idx_i in range(n_svg):
                cx = int(pl + (idx_i + 0.5) * sw)
                ya = int(pb - ((sa_v[idx_i] - mn_v) / sp_v) * ph)
                yb = int(pb - ((sb_v[idx_i] - mn_v) / sp_v) * ph)
                ta, ba = max(100, min(ya, zy)), min(h - 30, max(ya, zy) + 2)
                tb, bb = max(100, min(yb, zy)), min(h - 30, max(yb, zy) + 2)
                x1a, x2a = max(24, cx - bw - 3), min(w - 24, cx - 3)
                x1b, x2b = max(24, cx + 3), min(w - 24, cx + bw + 3)
                if x2a > x1a:
                    span_a = ca * (x2a - x1a)
                    for yy in range(ta, ba):
                        buf[yy][x1a * 3 : x2a * 3] = span_a
                if x2b > x1b:
                    span_b = cb * (x2b - x1b)
                    for yy in range(tb, bb):
                        buf[yy][x1b * 3 : x2b * 3] = span_b
        raw_scanlines = b"".join(b"\x00" + bytes(row) for row in buf)

        def _chunk(ctype: bytes, data: bytes) -> bytes:
            return struct.pack(">I", len(data)) + ctype + data + struct.pack(">I", zlib.crc32(ctype + data) & 0xFFFFFFFF)

        png_bytes = (
            b"\x89PNG\r\n\x1a\n"
            + _chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
            + _chunk(b"IDAT", zlib.compress(raw_scanlines, level=6))
            + _chunk(b"IEND", b"")
        )
        output_path.write_bytes(png_bytes)
        return {
            "status": "SUCCESS",
            "renderer": "stdlib_png_and_svg",
            "png_path": str(output_path),
            "svg_path": str(svg_path),
            "download_uri": f"file://{output_path}",
            "dimensions": "1200x640",
            "bars_rendered": n_svg,
        }

    width, height = 1200, 640
    img = Image.new("RGB", (width, height), (248, 250, 252))
    draw = ImageDraw.Draw(img)

    # Outer card
    draw.rounded_rectangle([(20, 20), (width - 20, height - 20)], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=2)

    font_sm = ImageFont.load_default()
    # Header Accent Strip
    draw.rounded_rectangle([(20, 20), (width - 20, 96)], radius=16, fill=(15, 23, 42))
    draw.rectangle([(20, 72), (width - 20, 96)], fill=(15, 23, 42))
    draw.text((48, 40), title[:95], fill=(255, 255, 255), font=font_sm)
    draw.text((48, 66), subtitle[:115], fill=(148, 163, 184), font=font_sm)

    # Legend pills
    col_a = (100, 116, 139)  # Slate baseline
    col_b = (37, 99, 235)    # Royal blue optimized
    draw.rectangle([(48, 114), (66, 128)], fill=col_a)
    draw.text((74, 115), series_a_label[:42], fill=(51, 65, 85), font=font_sm)
    draw.rectangle([(360, 114), (378, 128)], fill=col_b)
    draw.text((386, 115), series_b_label[:42], fill=(51, 65, 85), font=font_sm)
    draw.text((720, 115), f"Axis: {y_title[:45]}", fill=(100, 116, 139), font=font_sm)

    n = min(len(labels), len(series_a), len(series_b), 8)
    if n == 0:
        img.save(output_path, format="PNG")
        return {"status": "SAVED_EMPTY", "png_path": str(output_path), "download_uri": f"file://{output_path}"}

    labels = labels[:n]
    series_a = [float(x) for x in series_a[:n]]
    series_b = [float(x) for x in series_b[:n]]

    all_vals = series_a + series_b + [0.0]
    min_val = min(all_vals)
    max_val = max(all_vals)
    span = (max_val - min_val) if (max_val - min_val) > 1e-9 else 1.0

    plot_left, plot_right = 96, width - 56
    plot_top, plot_bottom = 158, height - 92
    plot_h = plot_bottom - plot_top
    plot_w = plot_right - plot_left

    zero_ratio = (0.0 - min_val) / span
    zero_y = int(plot_bottom - zero_ratio * plot_h)

    # Gridlines
    for step in range(5):
        frac = step / 4.0
        gy = int(plot_bottom - frac * plot_h)
        gval = min_val + frac * span
        draw.line([(plot_left, gy), (plot_right, gy)], fill=(226, 232, 240), width=1)
        draw.text((34, gy - 6), _fmt_num(gval), fill=(100, 116, 139), font=font_sm)

    draw.line([(plot_left, zero_y), (plot_right, zero_y)], fill=(71, 85, 105), width=2)

    slot_w = plot_w / n
    bar_w = max(14, int(slot_w * 0.30))

    for i in range(n):
        cx = int(plot_left + (i + 0.5) * slot_w)
        va = series_a[i]
        vb = series_b[i]

        ya = int(plot_bottom - ((va - min_val) / span) * plot_h)
        yb = int(plot_bottom - ((vb - min_val) / span) * plot_h)

        # Bar A
        x1a, x2a = cx - bar_w - 3, cx - 3
        top_a, bot_a = min(ya, zero_y), max(ya, zero_y)
        if bot_a - top_a < 2:
            top_a = bot_a - 2
        draw.rectangle([(x1a, top_a), (x2a, bot_a)], fill=col_a)
        draw.text((x1a, max(136, top_a - 14)), _fmt_num(va), fill=(71, 85, 105), font=font_sm)

        # Bar B
        x1b, x2b = cx + 3, cx + bar_w + 3
        top_b, bot_b = min(yb, zero_y), max(yb, zero_y)
        if bot_b - top_b < 2:
            top_b = bot_b - 2
        draw.rectangle([(x1b, top_b), (x2b, bot_b)], fill=col_b)
        draw.text((x1b, max(136, top_b - 14)), _fmt_num(vb), fill=(29, 78, 216), font=font_sm)

        lbl = str(labels[i])
        if len(lbl) > 15:
            lbl = lbl[-14:]
        draw.text((cx - bar_w - 4, plot_bottom + 14), lbl, fill=(30, 41, 59), font=font_sm)

    draw.text(
        (48, height - 46),
        f"XYZ Global Industries Corp. (XYZ-CORP-01) · Deterministic Python Analytics · Agent: {agent_id}",
        fill=(148, 163, 184),
        font=font_sm,
    )

    img.save(output_path, format="PNG")
    return {
        "status": "SUCCESS",
        "png_path": str(output_path),
        "download_uri": f"file://{output_path}",
        "dimensions": "1200x640",
        "bars_rendered": n,
    }
