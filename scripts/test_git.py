#!/usr/bin/env python3
import sys
import subprocess
import time

print("Script started!", flush=True)

for cmd in [
    ["echo", "quick test"],
    ["/usr/bin/git", "--version"],
]:
    t0 = time.time()
    print(f"Running: {' '.join(cmd)}", flush=True)
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        print(f"Finished in {time.time()-t0:.2f}s, out: {res.stdout.strip()}", flush=True)
    except Exception as e:
        print(f"Failed: {e}", flush=True)

print("Done!", flush=True)
