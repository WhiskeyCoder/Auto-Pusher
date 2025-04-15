#!/usr/bin/env python3
# ==============================
# 💻 Auto-Pusher by Whiskey and Mrs Whiskey
# ==============================
# A zero-click Git auto-committing and pushing script for Gitea.
# Perfect for self-hosted devs, home-labbers, and lone-wolf operators.
#
# 🔥 Make sure to configure your Git user info:
# git config --global user.name "Your Name"
# git config --global user.email "your@email.com"
#
# 🧠 Why? So your commits don't scream "WHO AM I?!"
# ===============================================

import os
import subprocess
import time
from datetime import datetime
import sys

# === CONFIG ===
PROJECT_DIR = r"ENTER THE FULL LOCATION OF THE FOLDER"
USERNAME = "GITEA USERNAME"
TOKEN = "GITA TOKEN"  # 🔐 Gitea token http://192.168.XXX.XXX:PORT/user/settings/applications
GITEA_HOST = "192.168.XXX.XXX:PORT"
REPO_PATH = "USERNAME/PROJECT_NAME"

REMOTE_URL = f"http://{USERNAME}:{TOKEN}@{GITEA_HOST}/{REPO_PATH}"
BRANCH = "main"
COMMIT_MESSAGE = "Auto-commit: changes detected"
INITIAL_COMMIT_MESSAGE = "Initial auto-commit on startup"
SLEEP_INTERVAL = 300  # 5 minutes

# === ASCII HEADER ===
def print_banner():
    banner = r"""
       d8888          888                   8888888b.                    888                       
      d88888          888                   888   Y88b                   888                       
     d88P888          888                   888    888                   888                       
    d88P 888 888  888 888888 .d88b.         888   d88P 888  888 .d8888b  88888b.   .d88b.  888d888 
   d88P  888 888  888 888   d88""88b        8888888P"  888  888 88K      888 "88b d8P  Y8b 888P"   
  d88P   888 888  888 888   888  888 888888 888        888  888 "Y8888b. 888  888 88888888 888     
 d8888888888 Y88b 888 Y88b. Y88..88P        888        Y88b 888      X88 888  888 Y8b.     888     
d88P     888  "Y88888  "Y888 "Y88P"         888         "Y88888  88888P' 888  888  "Y8888  888     
                                                                                             
               💻 Auto-Pusher for Gitea 💻
    """
    print(banner)

# === GIT HELPERS ===
def run_git_command(cmd):
    result = subprocess.run(
        cmd,
        cwd=PROJECT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    if result.stdout.strip():
        print(f"[{datetime.now()}] 📤 STDOUT: {result.stdout.strip()}")
    if result.stderr.strip():
        print(f"[{datetime.now()}] ❗ STDERR: {result.stderr.strip()}")
    return result

def is_git_repo():
    return run_git_command(["git", "rev-parse", "--is-inside-work-tree"]).returncode == 0

def remote_exists():
    return "origin" in run_git_command(["git", "remote"]).stdout

def show_loading_bar(duration=3):
    bar_length = 30
    print(f"[{datetime.now()}] ⏳ Pushing to remote...", end="\r")
    for i in range(bar_length + 1):
        percent = int((i / bar_length) * 100)
        bar = "=" * i + "-" * (bar_length - i)
        sys.stdout.write(f"\r[{datetime.now()}] ⏳ [{bar}] {percent}%")
        sys.stdout.flush()
        time.sleep(duration / bar_length)
    print("")

# === CORE GIT FLOW ===
def setup_repo_and_push():
    print(f"[{datetime.now()}] 🧪 Initializing new Git repo...")
    run_git_command(["git", "init"])
    run_git_command(["git", "branch", "-M", BRANCH])
    run_git_command(["git", "add", "."])
    run_git_command(["git", "commit", "-m", INITIAL_COMMIT_MESSAGE])
    run_git_command(["git", "remote", "add", "origin", REMOTE_URL])
    run_git_command(["git", "push", "-u", "origin", BRANCH])
    print(f"[{datetime.now()}] ✅ Repo initialized and pushed.")

def setup_remote():
    print(f"[{datetime.now()}] 🚀 Setting up remote origin...")
    if not remote_exists():
        run_git_command(["git", "remote", "add", "origin", REMOTE_URL])
    run_git_command(["git", "branch", "-M", BRANCH])
    run_git_command(["git", "add", "."])
    run_git_command(["git", "commit", "-m", INITIAL_COMMIT_MESSAGE])
    run_git_command(["git", "push", "-u", "origin", BRANCH])
    print(f"[{datetime.now()}] ✅ Remote setup complete.")

def has_changes():
    return bool(run_git_command(["git", "status", "--porcelain"]).stdout.strip())

def commit_and_push(message=COMMIT_MESSAGE):
    print(f"[{datetime.now()}] Changes detected. Committing...")
    start = time.time()
    run_git_command(["git", "add", "."])
    run_git_command(["git", "commit", "-m", message])
    show_loading_bar(2.5)
    run_git_command(["git", "push", "origin", BRANCH])
    duration = round(time.time() - start, 2)
    print(f"[{datetime.now()}] ✅ Commit pushed. Took {duration}s.")

def log_no_changes():
    print(f"[{datetime.now()}] No changes detected.")

# === MAIN LOOP ===
if __name__ == "__main__":
    print_banner()
    print("💫 Auto Git Pusher started. Watching for changes...")

    if not is_git_repo():
        setup_repo_and_push()
    elif not remote_exists():
        setup_remote()
    else:
        log = run_git_command(["git", "log"])
        if not log.stdout.strip():
            print(f"[{datetime.now()}] 📦 No commits found. Trying initial commit...")
            run_git_command(["git", "add", "."])
            status = run_git_command(["git", "status", "--short"])
            if status.stdout.strip():
                print(f"[{datetime.now()}] 📋 {len(status.stdout.strip().splitlines())} file(s) staged for commit.")
                run_git_command(["git", "commit", "-m", INITIAL_COMMIT_MESSAGE])
                run_git_command(["git", "push", "-u", "origin", BRANCH])
                print(f"[{datetime.now()}] ✅ First commit done.")
            else:
                print(f"[{datetime.now()}] ⚠️ Nothing to commit even after git add.")
        elif has_changes():
            commit_and_push(INITIAL_COMMIT_MESSAGE)
        else:
            print(f"[{datetime.now()}] 🧼 Clean on startup, nothing to commit.")

    while True:
        try:
            if has_changes():
                commit_and_push()
            else:
                log_no_changes()
        except Exception as e:
            print(f"[{datetime.now()}] ❌ Error: {e}")
        time.sleep(SLEEP_INTERVAL)
