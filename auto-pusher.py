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
import sys
import requests
from datetime import datetime

# === CONFIG ===
USERNAME = "GITEA USERNAME"
TOKEN = "GITA TOKEN"  # 🔐 Gitea token http://192.168.XXX.XXX:PORT/user/settings/applications
GITEA_HOST = "192.168.XXX.XXX:PORT"
BRANCH = "main"
SLEEP_INTERVAL = 300  # 5 minutes
INITIAL_COMMIT_MESSAGE = "Initial auto-commit on startup"
COMMIT_MESSAGE = "Auto-commit: changes detected"

# === DYNAMIC PROJECT DIR & NAME ===
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_NAME = os.path.basename(SCRIPT_DIR)
PROJECT_DIR = SCRIPT_DIR
REPO_PATH = f"{USERNAME}/{PROJECT_NAME}"
REMOTE_URL = f"http://{USERNAME}:{TOKEN}@{GITEA_HOST}/{REPO_PATH}"

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

# === GITEA API: Create Repo if Missing ===
def create_gitea_repo():
    api_url = f"http://{GITEA_HOST}/api/v1/user/repos"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"token {TOKEN}"
    }

    check_url = f"http://{GITEA_HOST}/api/v1/repos/{REPO_PATH}"
    check = requests.get(check_url, headers=headers)

    if check.status_code == 200:
        print(f"[{datetime.now()}] 📦 Repo '{REPO_PATH}' already exists on Gitea.")
        return

    print(f"[{datetime.now()}] 🚧 Repo not found. Creating repo '{REPO_PATH}'...")
    payload = {
        "name": PROJECT_NAME,
        "private": True,
        "auto_init": False,
        "default_branch": BRANCH
    }

    response = requests.post(api_url, json=payload, headers=headers)

    if response.status_code == 201:
        print(f"[{datetime.now()}] ✅ Successfully created private repo '{REPO_PATH}'.")
    else:
        print(f"[{datetime.now()}] ❌ Failed to create repo: {response.status_code} - {response.text}")
        raise Exception("Could not create repo on Gitea")

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

def has_changes():
    return bool(run_git_command(["git", "status", "--porcelain"]).stdout.strip())

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

def commit_and_push(message=COMMIT_MESSAGE):
    print(f"[{datetime.now()}] 🔧 Committing changes...")
    start = time.time()
    run_git_command(["git", "add", "."])
    run_git_command(["git", "commit", "-m", message])
    show_loading_bar(2.5)
    run_git_command(["git", "push", "origin", BRANCH])
    print(f"[{datetime.now()}] ✅ Commit pushed in {round(time.time() - start, 2)}s.")

def setup_repo_and_push():
    print(f"[{datetime.now()}] 🧪 Initializing new Git repo...")
    run_git_command(["git", "init"])
    run_git_command(["git", "branch", "-M", BRANCH])
    run_git_command(["git", "add", "."])
    run_git_command(["git", "commit", "-m", INITIAL_COMMIT_MESSAGE])
    run_git_command(["git", "remote", "add", "origin", REMOTE_URL])
    run_git_command(["git", "push", "-u", "origin", BRANCH])
    print(f"[{datetime.now()}] 🚀 Initial push complete.")

def setup_remote():
    print(f"[{datetime.now()}] 🔌 Setting up remote origin...")
    if not remote_exists():
        run_git_command(["git", "remote", "add", "origin", REMOTE_URL])
    run_git_command(["git", "branch", "-M", BRANCH])
    run_git_command(["git", "add", "."])
    run_git_command(["git", "commit", "-m", INITIAL_COMMIT_MESSAGE])
    run_git_command(["git", "push", "-u", "origin", BRANCH])
    print(f"[{datetime.now()}] 🌐 Remote linked and initial push done.")

# === MAIN ===
if __name__ == "__main__":
    print_banner()
    print(f"[{datetime.now()}] 💫 Auto Git Pusher started for: {PROJECT_DIR}")

    try:
        create_gitea_repo()

        if not is_git_repo():
            setup_repo_and_push()
        elif not remote_exists():
            setup_remote()
        else:
            log = run_git_command(["git", "log"])
            if not log.stdout.strip():
                print(f"[{datetime.now()}] 🧾 No commits found. Doing initial commit...")
                run_git_command(["git", "add", "."])
                status = run_git_command(["git", "status", "--short"])
                if status.stdout.strip():
                    run_git_command(["git", "commit", "-m", INITIAL_COMMIT_MESSAGE])
                    run_git_command(["git", "push", "-u", "origin", BRANCH])
                else:
                    print(f"[{datetime.now()}] ⚠️ Nothing to commit after add.")
            elif has_changes():
                commit_and_push(INITIAL_COMMIT_MESSAGE)
            else:
                print(f"[{datetime.now()}] 🧼 Clean start — nothing to commit.")

        while True:
            if has_changes():
                commit_and_push()
            else:
                print(f"[{datetime.now()}] 💤 No changes. Sleeping...")
            time.sleep(SLEEP_INTERVAL)

    except Exception as e:
        print(f"[{datetime.now()}] ❌ Fatal error: {e}")
