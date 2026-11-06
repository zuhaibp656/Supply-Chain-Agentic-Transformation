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

# Add changed core files directly to avoid recursive deep scanning of huge zip bundles
paths_to_add = [
    "README.md",
    "agents/README.md",
    "scripts/build_all_60_agent_readmes_and_renderers.py",
    "scripts/git_push_update.py",
]

for p in paths_to_add:
    run(["git", "add", p])

# Add all 60 agent READMEs and newly generated renderers directly via glob
run(["git", "add", "agents/*/README.md"])
run(["git", "add", "agents/*/app/render/interactive_html.py"])
run(["git", "add", "agents/*/app/render/surfaces.py"])
run(["git", "add", "agents/*/app/tools.py"])
run(["git", "add", "agents/*/app/agent.py"])

run(["git", "commit", "-m", "Publish 60 ASCM SCOR AI Agents: dedicated executive READMEs, interactive HTML cockpits, and unified 60-agent catalog"])
run(["git", "push", "origin", "main"])
print("SUCCESSFULLY COMMITTED AND PUSHED TO GITHUB MAIN!", flush=True)
