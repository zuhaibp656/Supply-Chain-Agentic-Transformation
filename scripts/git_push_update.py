#!/usr/bin/env python3
import subprocess
import sys

def run(cmd):
    print(f"Running: {' '.join(cmd)}", flush=True)
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.stdout:
        print(res.stdout, flush=True)
    if res.stderr:
        print(res.stderr, flush=True)
    if res.returncode != 0:
        print(f"Command failed with code {res.returncode}", flush=True)
        sys.exit(res.returncode)

# Add changed core files, agents, docs, zipline, scripts, and deployment metadata
paths_to_add = [
    "agents",
    "scripts",
    "docs",
    "data",
    "index.html",
    "periodic_table.html",
    "mind_map.html",
    "agent_testing_and_video_playbook.html",
    "AGENT_TESTING_AND_VIDEO_PLAYBOOK.md",
    "deployment_metadata.json",
    "zipline_dist",
    "supply_chain_zipline_bundle.zip",
    "Supply_Chain_Agentic_Portal.zip",
    "Zipline_Supply_Chain_Agentic_Portal.zip",
    "zipline",
    ".gitignore",
]

for p in paths_to_add:
    run(["git", "add", p])

run(["git", "commit", "-m", "Elevate 25 showcase agents with native interactive HTML dashboards, A2UI IFrameSrcdoc, and deployed filters"])
run(["git", "push", "origin", "main"])
print("SUCCESSFULLY COMMITTED AND PUSHED TO GITHUB MAIN!", flush=True)
