#!/usr/bin/env python3
"""Stitches Gemini Enterprise demo screen recordings for Demand Sensing and Promo ROI Simulator,
overlays synchronized AI voiceover narration, encodes web-optimized 1080p MP4s (<35MB),
and embeds them into the Supply Chain Transformation portal.
"""

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

REPO_ROOT = Path(__file__).resolve().parent.parent
VIDEOS_DIR = REPO_ROOT / "videos"
TEMP_DIR = Path("/tmp/video_build")
GENERATE = "/google/bin/releases/gemini-agents-generate/generate"

# Input source videos (from Drive)
DS_CLIPS = [
    Path("/tmp/raw_videos/ds1.mov"),
    Path("/tmp/raw_videos/ds2.mov"),
    Path("/tmp/raw_videos/ds3.mov"),
]

PROMO_CLIPS = [
    Path("/tmp/raw_videos/promo1.mov"),
    Path("/tmp/raw_videos/promo2.mov"),
    Path("/tmp/raw_videos/promo3.mov"),
]

DS_NARRATION = [
    ("ds_01", 2.0, "Here, we are testing the Demand Sensing Agent in Gemini Enterprise. We select the first starter prompt to review customer demand trends across active products and regions."),
    ("ds_02", 20.0, "The agent dynamically queries live point-of-sale data, distributor orders, and weather feeds, cross-referencing regional baseline sales."),
    ("ds_03", 38.0, "In the response, it delivers a clear breakdown of demand shifts, imputes lost sales from stockouts, and flags an unverified thirty-five percent manual sales override on sparkling water."),
    ("ds_04", 60.0, "Next, we select Mode Two, asking for a visual comparison chart of our sensed demand against the current baseline plan across top products."),
    ("ds_05", 82.0, "The agent generates an interactive visualization directly within the chat surface, highlighting the gap between static forecasts and real-time sensed demand."),
    ("ds_06", 108.0, "This visual comparison makes it easy for demand planners to identify upcoming stockout risks and adjust replenishment buffers before shortages impact customer service."),
    ("ds_07", 139.0, "Finally, in Mode Three, we request an executive briefing note for leadership summarizing the key demand shifts and recommended forecast updates."),
    ("ds_08", 162.0, "The agent synthesizes the analysis into a concise, leadership-ready memo detailing forecast adjustments, protected revenue, and recommended next steps."),
    ("ds_09", 188.0, "With twenty-four percent lower forecast error and automated consensus, planners can act immediately with full confidence.")
]

PROMO_NARRATION = [
    ("promo_01", 2.0, "In this demo, we explore the Promo ROI Simulator agent in Gemini Enterprise. We select the first starter prompt to evaluate upcoming retail price promotions and identify which ones are truly profitable."),
    ("promo_02", 22.0, "The agent evaluates planned trade promotions across key retail accounts, modeling promotional lift, forward-buying behavior, and cross-product cannibalization."),
    ("promo_03", 46.0, "The operational review reveals that while most campaigns generate positive lift, a planned twenty percent discount on family packs results in margin loss due to high trade spend and product cannibalization."),
    ("promo_04", 74.0, "Switching to Mode Two, we ask for a visual chart comparing expected sales lift against net profit impact across all planned campaigns."),
    ("promo_05", 90.0, "The agent renders a visual matrix plotting volume lift against profit margin, clearly separating value-accretive promotions from margin-dilutive ones."),
    ("promo_06", 110.0, "In Mode Three, we request a trade promotion review note for Sales and Finance, outlining which campaigns to fund and which to restructure."),
    ("promo_07", 130.0, "The agent drafts an executive memorandum recommending approval for high-performing promotions and proposing a bundled offer to protect profitability on the family pack campaign."),
    ("promo_08", 152.0, "This demonstrates how enterprise teams can optimize multi-million dollar trade budgets quickly, maximizing both volume and operating margin.")
]


def ensure_tts(out_path: Path, text: str, retries: int = 3) -> bool:
    if out_path.exists() and out_path.stat().st_size > 1000:
        print(f"  [TTS] Already exists: {out_path.name}")
        return True
    out_path.parent.mkdir(parents=True, exist_ok=True)
    for attempt in range(retries):
        print(f"  [TTS] Synthesizing {out_path.name} (attempt {attempt+1})...", flush=True)
        res = subprocess.run(
            [GENERATE, f"-output={out_path}", "tts", "--voice=Puck", text],
            capture_output=True,
            text=True
        )
        if res.returncode == 0 and out_path.exists() and out_path.stat().st_size > 1000:
            print(f"  [TTS] OK: {out_path.name} ({out_path.stat().st_size} bytes)")
            time.sleep(1.0)
            return True
        print(f"  [TTS] Error: {res.stderr.strip()}", flush=True)
        time.sleep(2.0 * (attempt + 1))
    return False


def get_clip_duration(path: Path) -> float:
    res = subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "json", str(path)
    ])
    return float(json.loads(res)["format"]["duration"])


def assemble_audio_track(narration_list, total_duration: float, out_wav: Path):
    """Build a single synchronized audio track using adelay and amix."""
    inputs = []
    filter_delays = []
    for idx, (name, start_sec, text) in enumerate(narration_list):
        wav_file = (TEMP_DIR / f"tts_{name.split('_')[0]}" / f"{name}.wav")
        inputs.extend(["-i", str(wav_file)])
        delay_ms = int(start_sec * 1000)
        filter_delays.append(f"[{idx}:a]adelay={delay_ms}|{delay_ms},aformat=sample_fmts=fltp:sample_rates=44100:channel_layouts=stereo[a{idx}]")

    mix_inputs = "".join(f"[a{i}]" for i in range(len(narration_list)))
    filter_complex = f"{';'.join(filter_delays)};{mix_inputs}amix=inputs={len(narration_list)}:normalize=0,loudnorm=I=-16:TP=-1.0:LRA=11[outa]"

    cmd = ["ffmpeg", "-y"] + inputs + [
        "-filter_complex", filter_complex,
        "-map", "[outa]",
        "-t", f"{total_duration:.2f}",
        str(out_wav)
    ]
    print(f"  [Audio Assembly] Executing FFmpeg audio mix -> {out_wav}...")
    subprocess.run(cmd, check=True)
    print(f"  [Audio Assembly] Finished: {out_wav.name} ({out_wav.stat().st_size} bytes)")


def stitch_and_encode(clips, audio_track: Path, total_duration: float, output_mp4: Path):
    """Stitches video clips, rescales to 1920x1104 30fps, attaches audio track, encodes H.264 mp4."""
    inputs = []
    filter_scale = []
    for idx, clip in enumerate(clips):
        inputs.extend(["-i", str(clip)])
        filter_scale.append(f"[{idx}:v]scale=1920:1104,setsar=1,fps=30[v{idx}]")

    concat_inputs = "".join(f"[v{i}]" for i in range(len(clips)))
    filter_complex = f"{';'.join(filter_scale)};{concat_inputs}concat=n={len(clips)}:v=1:a=0[vout]"

    cmd = [
        "ffmpeg", "-y"
    ] + inputs + [
        "-i", str(audio_track),
        "-filter_complex", filter_complex,
        "-map", "[vout]",
        "-map", f"{len(clips)}:a",
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "23",
        "-c:a", "aac",
        "-b:a", "128k",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        "-t", f"{total_duration:.2f}",
        str(output_mp4)
    ]
    print(f"  [Video Render] Rendering {output_mp4.name} (target ~25MB)...", flush=True)
    subprocess.run(cmd, check=True)
    size_mb = output_mp4.stat().st_size / (1024 * 1024)
    print(f"  [Video Render] SUCCESS: {output_mp4.name} -> {size_mb:.2f} MB", flush=True)


def main():
    print("=" * 70)
    print("🎥 Supply Chain Demo Video Stitcher & Voiceover Producer")
    print("=" * 70)
    VIDEOS_DIR.mkdir(parents=True, exist_ok=True)
    TEMP_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Check input videos
    for c in DS_CLIPS + PROMO_CLIPS:
        if not c.exists():
            print(f"ERROR: Missing source clip {c}")
            sys.exit(1)

    ds_dur = sum(get_clip_duration(c) for c in DS_CLIPS)
    promo_dur = sum(get_clip_duration(c) for c in PROMO_CLIPS)
    print(f"✓ Demand Sensing clips total duration: {ds_dur:.2f}s ({ds_dur/60:.2f} min)")
    print(f"✓ Promo ROI clips total duration: {promo_dur:.2f}s ({promo_dur/60:.2f} min)")

    # 2. Generate TTS clips
    print("\n--- Generating Demand Sensing Voiceover ---")
    for name, sec, text in DS_NARRATION:
        p = TEMP_DIR / "tts_ds" / f"{name}.wav"
        ensure_tts(p, text)

    print("\n--- Generating Promo ROI Voiceover ---")
    for name, sec, text in PROMO_NARRATION:
        p = TEMP_DIR / "tts_promo" / f"{name}.wav"
        ensure_tts(p, text)

    # 3. Assemble Audio Tracks
    print("\n--- Assembling Synchronized Audio Tracks ---")
    ds_audio = TEMP_DIR / "demand_sensing_voice.wav"
    promo_audio = TEMP_DIR / "promo_roi_voice.wav"
    assemble_audio_track(DS_NARRATION, ds_dur, ds_audio)
    assemble_audio_track(PROMO_NARRATION, promo_dur, promo_audio)

    # 4. Stitch, scale and encode videos
    print("\n--- Stitching and Encoding Web-Optimized Videos ---")
    ds_final = VIDEOS_DIR / "demand_sensing_demo.mp4"
    promo_final = VIDEOS_DIR / "promo_lift_simulator_demo.mp4"

    stitch_and_encode(DS_CLIPS, ds_audio, ds_dur, ds_final)
    stitch_and_encode(PROMO_CLIPS, promo_audio, promo_dur, promo_final)

    # Also make a copy named promo_roi_demo.mp4 for convenience
    promo_alias = VIDEOS_DIR / "promo_roi_demo.mp4"
    shutil.copy2(promo_final, promo_alias)

    # 5. Distribute to all twin and docs directories
    print("\n--- Distributing Videos Across Web Targets ---")
    dist_targets = [
        REPO_ROOT / "docs" / "videos",
        REPO_ROOT / "zipline_dist" / "videos",
    ]
    for d in (REPO_ROOT / "dist").glob("*/videos"):
        dist_targets.append(d)

    for target in dist_targets:
        target.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ds_final, target / "demand_sensing_demo.mp4")
        shutil.copy2(promo_final, target / "promo_lift_simulator_demo.mp4")
        shutil.copy2(promo_alias, target / "promo_roi_demo.mp4")
        print(f"  ✓ Synced to {target.relative_to(REPO_ROOT)}")

    print("\n✅ All demo videos stitched, voiced over, compressed, and distributed!")


if __name__ == "__main__":
    main()
