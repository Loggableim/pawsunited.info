#!/usr/bin/env python3
"""Wrapper that runs live_status.py and pushes changes to GitHub."""
import subprocess, sys, os, json

SCRIPT = r"E:\Pawsunited\scripts\live_status.py"
WORKDIR = r"E:\Pawsunited"
TOKEN_FILE = r"C:\Users\logga\discord_token.txt"

# Read token
with open(TOKEN_FILE) as f:
    token = f.read().strip()

# Run live_status.py
env = os.environ.copy()
env["DISCORD_BOT_TOKEN"] = token

result = subprocess.run(
    [sys.executable, SCRIPT],
    cwd=WORKDIR, env=env, capture_output=True, text=True, timeout=30
)
print(result.stdout)
if result.returncode != 0:
    print(f"ERROR: {result.stderr}", flush=True)
    sys.exit(1)

# Check if live-status.json actually changed
status_file = os.path.join(WORKDIR, "assets/data/live-status.json")
if not os.path.exists(status_file):
    print("No live-status.json found")
    sys.exit(0)

# Git: commit+push only if changed
git_cmd = ["git", "-C", WORKDIR]
diff = subprocess.run(git_cmd + ["diff", "--quiet", "assets/data/live-status.json"],
                      capture_output=True, timeout=10)
if diff.returncode == 0:
    print("No changes to live-status.json")
    sys.exit(0)

print("Changes detected, committing...", flush=True)
subprocess.run(git_cmd + ["add", "assets/data/live-status.json"], check=True, timeout=10)
subprocess.run(git_cmd + ["commit", "-m", "chore: update live status [skip ci]"],
               capture_output=True, timeout=10)
push = subprocess.run(git_cmd + ["push"], capture_output=True, text=True, timeout=30)
print(push.stdout[-200:] if push.stdout else push.stderr[-200:], flush=True)
