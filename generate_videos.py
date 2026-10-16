"""Generate crisp H.264 MP4 demo videos for Supply Chain Agentic Transformation portal."""

from __future__ import annotations

import math
import os
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

OUT_DIR = Path(__file__).resolve().parent / "videos"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Add loadpilot-dispatch-agent to sys.path so we can render the real 3D LIFO truck video too
LP_ROOT = Path("/usr/local/google/home/zuhaibp/high-code-agents/loadpilot-dispatch-agent")
if str(LP_ROOT) not in sys.path:
    sys.path.insert(0, str(LP_ROOT))


def _font(size: int, bold: bool = True) -> ImageFont.ImageFont:
    candidates = (
        ("DejaVuSans-Bold.ttf", "LiberationSans-Bold.ttf", "Arial Bold.ttf")
        if bold
        else ("DejaVuSans.ttf", "LiberationSans-Regular.ttf", "Arial.ttf")
    )
    for name in candidates:
        try:
            return ImageFont.truetype(name, size)
        except Exception:
            continue
    return ImageFont.load_default()


def _write_mp4(frames: list[Image.Image], out_path: Path, fps: int = 20) -> None:
    w, h = frames[0].size
    gen = imageio_ffmpeg.write_frames(
        str(out_path),
        (w, h),
        fps=fps,
        codec="libx264",
        pix_fmt_in="rgb24",
        pix_fmt_out="yuv420p",
         ffmpeg_log_level="error",
        output_params=["-movflags", "+faststart", "-crf", "21"],
    )
    gen.send(None)
    for im in frames:
        gen.send(im.convert("RGB").tobytes())
    gen.close()
    print(f"Wrote {out_path.name} ({out_path.stat().st_size // 1024} KB)")


def build_fleetflow_video() -> None:
    """Use the real FleetFlow 3D isometric LIFO loader engine from loadpilot-dispatch-agent."""
    from app.data.demo_mmr import HUBS, build_demo_stops
    from app.integration.tools import params_from_state
    from app.optim.dispatch import plan_dispatch
    from app.render.video_mp4 import render_loading_frames

    params = params_from_state({})
    hub = HUBS[params.hub_id]
    stops = build_demo_stops(seed=42)
    plan = plan_dispatch(hub, stops, params)
    route = max(plan.routes, key=lambda r: len(r.stops))
    lp = plan.loads[route.truck_id]
    frames = list(render_loading_frames(route, lp, width=1280, height=720, fps=20, seconds=7.0))
    out = OUT_DIR / "fleetflow_dispatch_demo.mp4"
    _write_mp4(frames, out, fps=20)


def build_ormwo_video() -> None:
    """Render 1280x720 animated Offshore Rig Mobilization & Metocean Radar MP4."""
    W, H = 1280, 720
    frames: list[Image.Image] = []
    f_title = _font(28, True)
    f_sub = _font(16, False)
    f_mono = _font(15, True)
    f_big = _font(36, True)
    f_sm = _font(13, False)

    total = 100
    for t in range(total):
        p = t / (total - 1)
        im = Image.new("RGB", (W, H), (5, 10, 20))
        d = ImageDraw.Draw(im)

        # Subtle CAD grid
        for gx in range(0, W, 40):
            d.line([(gx, 0), (gx, H)], fill=(12, 22, 40), width=1)
        for gy in range(0, H, 40):
            d.line([(0, gy), (W, gy)], fill=(12, 22, 40), width=1)

        # Header bar
        d.rectangle([0, 0, W, 76], fill=(8, 15, 30), outline=(30, 50, 85))
        d.text((36, 16), "ORMWO · Offshore Rig Mobilization & Weather Optimizer", fill=(248, 250, 252), font=f_title)
        d.text((36, 48), "Gemini Enterprise · DeepMind WeatherNext · DNV-ST-N001 Naval Physics Engine", fill=(0, 210, 180), font=f_sub)
        d.rounded_rectangle([W - 310, 20, W - 36, 56], radius=18, fill=(10, 45, 40), outline=(0, 210, 180), width=2)
        d.text((W - 290, 29), "● DNV-ST-N001 APPROVED · GO", fill=(94, 234, 212), font=f_mono)

        # Left Panel: Animated Jack-Up Rig & Ocean Swell CAD
        d.rounded_rectangle([36, 98, 760, 680], radius=16, fill=(8, 16, 32), outline=(35, 60, 100), width=2)
        d.text((58, 116), "CAD BLUEPRINT // SAGAR SAMRAT (300-FT JACK-UP) · MUMBAI HIGH", fill=(138, 180, 248), font=f_mono)

        # Seabed
        seabed_y = 560
        d.line([(60, seabed_y), (736, seabed_y)], fill=(148, 163, 184), width=3)
        d.text((68, seabed_y + 10), "SEABED SILT HORIZON // -76.0m DEPTH · 24H PRELOAD VERIFIED", fill=(148, 163, 184), font=f_sm)

        # Animated sea surface wave
        msl_y = 390
        wave_pts = []
        for wx in range(60, 736, 8):
            wy = msl_y + math.sin(wx * 0.035 + t * 0.22) * 11 + math.cos(wx * 0.018 - t * 0.15) * 5
            wave_pts.append((wx, wy))
        for i in range(len(wave_pts) - 1):
            d.line([wave_pts[i], wave_pts[i + 1]], fill=(0, 210, 180), width=3)
        d.text((68, msl_y - 28), f"LIVE SIGNIFICANT WAVE HEIGHT Hs = {1.15 + 0.08 * math.sin(t * 0.1):.2f}m  (LIMIT <= 1.50m)", fill=(0, 210, 180), font=f_mono)

        # 3 Lattice Truss Legs (jacking animation)
        hull_y = int(260 + 25 * math.sin(p * math.pi))
        for lx in (190, 360, 530):
            d.rectangle([lx, 175, lx + 28, seabed_y], outline=(56, 139, 253), width=2)
            for zy in range(180, seabed_y - 16, 22):
                d.line([(lx, zy), (lx + 28, zy + 11)], fill=(56, 139, 253), width=2)
                d.line([(lx + 28, zy + 11), (lx, zy + 22)], fill=(56, 139, 253), width=2)
            # Spudcan
            d.polygon([(lx - 12, seabed_y), (lx + 14, seabed_y + 22), (lx + 40, seabed_y)], fill=(30, 80, 160), outline=(96, 165, 250))

        # Rig Hull
        d.rounded_rectangle([150, hull_y, 585, hull_y + 48], radius=6, fill=(15, 28, 55), outline=(96, 165, 250), width=3)
        d.text((235, hull_y + 15), "SAGAR SAMRAT TRI-HULL · AIR GAP 24.5m", fill=(255, 255, 255), font=f_mono)

        # Derrick
        d.polygon([(470, hull_y), (495, hull_y - 85), (512, hull_y - 85), (535, hull_y)], outline=(251, 188, 4), width=2)

        # Animated AHTS Escort Tug steaming right
        tug_x = int(590 + 45 * math.sin(t * 0.12))
        tug_y = int(msl_y - 14 + 5 * math.sin(t * 0.22))
        d.line([(585, hull_y + 30), (tug_x, tug_y + 8)], fill=(251, 188, 4), width=2)
        d.polygon([(tug_x, tug_y), (tug_x + 70, tug_y), (tug_x + 84, tug_y + 16), (tug_x + 10, tug_y + 16)], fill=(245, 158, 11), outline=(255, 255, 255))
        d.text((575, tug_y + 24), "3x AHTS ESCORT (150T PULL)", fill=(251, 188, 4), font=f_sm)

        # Right Panel: Metocean Telemetry & Capital Impact
        d.rounded_rectangle([784, 98, 1244, 375], radius=16, fill=(8, 16, 32), outline=(35, 60, 100), width=2)
        d.text((808, 118), "48-HR METOCEAN SWELL CORRIDOR", fill=(0, 210, 180), font=f_mono)
        # Forecast chart
        cx0, cy0, cw, ch = 812, 165, 404, 165
        d.rectangle([cx0, cy0, cx0 + cw, cy0 + ch], fill=(5, 10, 22), outline=(30, 48, 80))
        limit_y = cy0 + 48
        d.line([(cx0, limit_y), (cx0 + cw, limit_y)], fill=(234, 67, 53), width=2)
        d.text((cx0 + 10, limit_y - 18), "DNV Jacking Limit: 1.50m Hs", fill=(242, 139, 130), font=f_sm)

        f_pts = []
        for idx in range(48):
            fx = cx0 + int(idx / 47 * cw)
            val = 1.15 + 0.18 * math.sin(idx * 0.22 + t * 0.08)
            fy = cy0 + ch - int((val / 2.0) * ch)
            f_pts.append((fx, fy))
        for i in range(len(f_pts) - 1):
            d.line([f_pts[i], f_pts[i + 1]], fill=(52, 168, 83), width=3)

        # Scan cursor on chart
        scan_x = cx0 + int(p * cw)
        d.line([(scan_x, cy0), (scan_x, cy0 + ch)], fill=(251, 188, 4), width=2)

        # Bottom Right Panel: Capital & NPT Impact
        d.rounded_rectangle([784, 398, 1244, 680], radius=16, fill=(8, 16, 32), outline=(35, 60, 100), width=2)
        d.text((808, 418), "SOVEREIGN CAPITAL PROTECTION", fill=(251, 188, 4), font=f_mono)
        d.text((808, 452), "Rs 1.20 Cr / Day", fill=(0, 210, 180), font=f_big)
        d.text((808, 498), "Idle Rig Non-Productive Time (NPT) Avoided", fill=(200, 212, 230), font=f_sub)

        steps_txt = [
            ("Spudcan Preload (24h Ballast)", "VERIFIED", (52, 168, 83)),
            ("3x AHTS Bollard Pull (150T)", "LOCKED", (52, 168, 83)),
            ("48h Swell Window (Hs <= 1.32m)", "CLEAR", (52, 168, 83)),
            ("MWS Tow Certificate #MH-04", "ISSUED", (66, 133, 244)),
        ]
        for idx, (lbl, st, col) in enumerate(steps_txt):
            sy = 538 + idx * 32
            d.text((808, sy), f"• {lbl}", fill=(180, 195, 215), font=f_sm)
            d.text((1120, sy), st, fill=col, font=f_mono)

        frames.append(im)

    _write_mp4(frames, OUT_DIR / "ormwo_rig_nav_demo.mp4", fps=20)


def build_pipeline_video(filename: str, title: str, subtitle: str, accent: tuple[int, int, int], stages: list[tuple[str, str, str]]) -> None:
    """Render an animated 6-stage pipeline execution video for F2F, O2D, Demand Sensing, or Warehouse."""
    W, H = 1280, 720
    frames: list[Image.Image] = []
    f_title = _font(26, True)
    f_sub = _font(15, False)
    f_mono = _font(14, True)
    f_card = _font(17, True)
    f_sm = _font(13, False)

    total = 96
    for t in range(total):
        p = t / (total - 1)
        active_idx = min(int(p * len(stages)), len(stages) - 1)
        im = Image.new("RGB", (W, H), (6, 9, 17))
        d = ImageDraw.Draw(im)

        # Grid
        for gx in range(0, W, 48):
            d.line([(gx, 0), (gx, H)], fill=(14, 20, 34), width=1)
        for gy in range(0, H, 48):
            d.line([(0, gy), (W, gy)], fill=(14, 20, 34), width=1)

        # Header
        d.rectangle([0, 0, W, 82], fill=(10, 15, 28), outline=(35, 50, 80))
        d.text((40, 18), title, fill=(248, 250, 252), font=f_title)
        d.text((40, 50), subtitle, fill=accent, font=f_sub)
        d.rounded_rectangle([W - 290, 22, W - 40, 58], radius=18, fill=(16, 28, 48), outline=accent, width=2)
        d.text((W - 270, 32), f"STAGE 0{active_idx + 1} / 0{len(stages)} ACTIVE", fill=accent, font=f_mono)

        # 6 Stage Cards (2 rows of 3)
        cw, ch = 376, 235
        for idx, (st_name, st_sys, st_out) in enumerate(stages):
            row, col = divmod(idx, 3)
            x0 = 40 + col * (cw + 36)
            y0 = 115 + row * (ch + 42)
            done = idx < active_idx
            curr = idx == active_idx

            border_col = accent if curr else ((52, 168, 83) if done else (38, 52, 78))
            bg_col = (16, 26, 46) if curr else ((10, 20, 32) if done else (10, 14, 24))
            d.rounded_rectangle([x0, y0, x0 + cw, y0 + ch], radius=16, fill=bg_col, outline=border_col, width=3 if curr else 2)

            # Top badge
            st_badge = f"STAGE 0{idx + 1} · {'COMPLETED ✓' if done else ('EXECUTING ●' if curr else 'QUEUED')}"
            d.text((x0 + 20, y0 + 18), st_badge, fill=border_col, font=f_mono)
            d.text((x0 + 20, y0 + 46), st_name, fill=(248, 250, 252), font=f_card)
            d.rounded_rectangle([x0 + 20, y0 + 78, x0 + 260, y0 + 104], radius=6, fill=(20, 30, 50))
            d.text((x0 + 28, y0 + 84), st_sys, fill=(148, 163, 184), font=f_sm)

            # Golden thread output box
            d.rounded_rectangle([x0 + 20, y0 + 118, x0 + cw - 20, y0 + ch - 18], radius=10, fill=(8, 13, 24), outline=(30, 45, 70))
            # Wrap text
            words = st_out.split()
            lines, cur_l = [], ""
            for w_str in words:
                if len(cur_l + " " + w_str) <= 42:
                    cur_l = (cur_l + " " + w_str).strip()
                else:
                    lines.append(cur_l)
                    cur_l = w_str
            if cur_l:
                lines.append(cur_l)
            for li, ln in enumerate(lines[:4]):
                d.text((x0 + 30, y0 + 128 + li * 20), ln, fill=(210, 225, 245) if (done or curr) else (100, 115, 135), font=f_sm)

            # Connector arrow
            if col < 2:
                ax0 = x0 + cw + 4
                ay = y0 + ch // 2
                d.line([(ax0, ay), (ax0 + 28, ay)], fill=accent if done else (50, 65, 95), width=3)

        # Bottom Golden Thread Progress Bar
        d.rounded_rectangle([40, 648, W - 40, 692], radius=12, fill=(10, 16, 30), outline=(35, 55, 90))
        bar_w = int((W - 100) * p)
        d.rounded_rectangle([50, 658, 50 + max(bar_w, 24), 682], radius=8, fill=accent)
        d.text((64, 662), f"GOLDEN THREAD CONTEXT SYNC: {int(p * 100)}% COMPLETE · ZERO MANUAL HANDOFFS", fill=(255, 255, 255), font=f_mono)

        frames.append(im)

    _write_mp4(frames, OUT_DIR / filename, fps=20)


if __name__ == "__main__":
    build_fleetflow_video()
    build_ormwo_video()
    build_pipeline_video(
        "o2d_suite_demo.mp4",
        "Order-to-Delivery (O2D) Autonomous Logistics Suite",
        "Plan BHW-20261015-01 · 70 Retail Drops · 840 Cartons · 10 -> 8 Trucks (-29% Cost)",
        (251, 188, 4),
        [
            ("01 Multimodal Order Intake", "SAP S/4HANA · Model Armor", "Ingests 70 store orders (840 cartons); Cloud DLP masks PII in <15ms."),
            ("02 Dock QR Vision Validator", "OpenCV ArUco · Gemini 3.7", "Decodes 840/840 thermal QR labels in 1.8s; flags 2 crushed cartons."),
            ("03 Polar Corridor & CVRPTW", "Google OR-Tools · Maps API v2", "Pins Ravi to West (T14-1); compresses fleet from 10 to 8 trucks."),
            ("04 3D Height-Map LIFO Packer", "1x1cm Grid · CMVR Rule 93", "Packs Stop 8 at cab, Stop 1 at door (0-75cm); 100% axle balance."),
            ("05 Driver Edge PWA & GPS", "Zero-Login App · WhatsApp", "Pushes 1-tap Google Maps voice nav & printable LR Challan to drivers."),
            ("06 Touchless Freight Audit", "SAP TM · GPS Geofence POD", "Auto-approves Rs 45,700 base haulage; blocks Rs 6,400 false detention."),
        ],
    )
    build_pipeline_video(
        "f2f_fleet_demo.mp4",
        "Forecast-to-Fulfill (F2F) Autonomous Planning Fleet",
        "Cycle 2026-W42 · +38% Festive Surge · 99.4% OTIF · -22% Safety Stock",
        (52, 168, 83),
        [
            ("01 Multi-Signal Demand Sense", "BigQuery · IMD Weather · POS", "Detects +62,400 case West/South surge; strips 9.2k forward-buy noise."),
            ("02 BOM & Raw Material Netting", "SAP Ariba · Multi-Tier BOM", "Flags 14T PET resin gap at Silvassa; triggers secondary vendor VND-1108."),
            ("03 Multi-Echelon MEIO Transfer", "SAP S/4HANA MM · OR-Tools", "Reallocates 18,400 surplus cases from Nagpur via STO-2026-8841."),
            ("04 Finite MPS Line Sequencer", "SAP PP/DS · MILP Solver", "Clusters flavours on Pune Line 3; cuts CIP washout from 6.5h to 2.0h."),
            ("05 Executive S&OP Conductor", "Gemini 3.7 · Margin Bridge", "Approves Scenario B (+Rs 1.84 Cr net margin) over air-freight."),
            ("06 Real-Time ATP & WMS Wave", "SAP ATP · Manhattan EWM", "Locks Tier-1 Modern Trade allocations & releases WAVE-BHW-1015."),
        ],
    )
    build_pipeline_video(
        "demand_sensing_demo.mp4",
        "Multi-Signal Demand Sensing & S&OP Scenario Agent",
        "50,000+ SKU-Locations · POS + Weather + Promo Elasticity · -24% WAPE Error",
        (16, 185, 129),
        [
            ("01 POS & DMS Ingestion", "BigQuery · 600 Outlets", "Streams daily secondary sales & modern trade EDI 852 velocity feeds."),
            ("02 Weather & Event Fusion", "IMD Hyper-Local · Calendar", "Correlates +4.2C heatwave & Diwali shift with regional beverage lift."),
            ("03 Stockout Distortion Scrub", "Vertex AI Imputation", "Reconstructs unconstrained demand across 14 stockout-affected DCs."),
            ("04 Cannibalization Matrix", "Halo & Elasticity ML", "Isolates 18% pack-size cannibalization on 500ml vs 1L promotional SKUs."),
            ("05 Bayesian Bias Correction", "SAP IBP Forecast Lock", "Trims chronic +22% regional sales over-forecast bias automatically."),
            ("06 QoQ Margin & Volume Bridge", "Executive S&OP Brief", "Generates cited P&L and safety-stock bridge in 45 seconds."),
        ],
    )
    build_pipeline_video(
        "smart_warehouse_demo.mp4",
        "Dock Vision QR, Dynamic Slotting & MEIO Agent",
        "SAP EWM · Manhattan Active WM · <2 Sec Pallet QR Scan · -35% Picker Travel",
        (66, 133, 244),
        [
            ("01 Smartphone Dock Capture", "Staging Bay Camera / Mobile", "Captures multi-carton pallet photo at Bhiwandi Inbound Gate 04."),
            ("02 ArUco & QR Vision Decode", "OpenCV + Gemini 3.7 Vision", "Decodes 48 carton labels simultaneously; flags 1 torn barcode."),
            ("03 ASN & SAP EWM Tie-Out", "SAP MIGO / EWM Inbound", "Auto-posts Goods Receipt GR-88412 and prints putaway pallet tags."),
            ("04 Dynamic ABC Velocity Slot", "Heatmap Slotting Optimizer", "Moves 18 high-turn festive SKUs to golden waist-level pick bins."),
            ("05 Zero-Walk Wave Release", "Manhattan Wave Engine", "Clusters 420 outbound store picks into 12 optimal MHE forklift paths."),
            ("06 3D LIFO Bay Staging", "FleetFlow Dock Handshake", "Stages pallets in strict reverse-drop sequence at Outbound Doors 1-8."),
        ],
    )
