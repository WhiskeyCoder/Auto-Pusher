```
       d8888          888                   8888888b.                    888                       
      d88888          888                   888   Y88b                   888                       
     d88P888          888                   888    888                   888                       
    d88P 888 888  888 888888 .d88b.         888   d88P 888  888 .d8888b  88888b.   .d88b.  888d888 
   d88P  888 888  888 888   d88""88b        8888888P"  888  888 88K      888 "88b d8P  Y8b 888P"   
  d88P   888 888  888 888   888  888 888888 888        888  888 "Y8888b. 888  888 88888888 888     
 d8888888888 Y88b 888 Y88b. Y88..88P        888        Y88b 888      X88 888  888 Y8b.     888     
d88P     888  "Y88888  "Y888 "Y88P"         888         "Y88888  88888P' 888  888  "Y8888  888
                            💻 Auto-Pusher for Gitea 💻
```


# 🧠 Auto-Pusher for Gitea

A fully-automated, zero-click Git auto-committing and pushing system — perfect for homelabbers, lone-wolf devs, and anyone working outside bloated IDEs.

### 💻 Features

- 📦 Automatically detects changes in a local project folder
- 💨 Commits and pushes every X minutes (default: 5 min)
- 🧪 Initializes Git and sets remote if missing
- 🧠 Tracks first commit if the repo is clean
- 🌈 ASCII banners, progress bars, and sexy logging
- 🧾 Self-hosted Git support (Gitea, GitLab, etc.)

### 📋 Requirements

- Python 3.8+
- Git installed and available in your PATH
- A Gitea repo URL and an API token

### 🚀 Setup

1. Clone your project locally
2. Configure the script variables at the top:
   - `PROJECT_DIR`
   - `USERNAME`, `TOKEN`, `GITEA_HOST`, `REPO_PATH`

3. Set your Git identity (one-time):
```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

4. Run the script:
```python auto-pusher.py```


💡 Why This Script?
Most IDEs like PyCharm are deeply tied to GitHub or GitLab and don’t handle self-hosted Gitea smoothly. 

This script:
Works with any Git server
Doesn’t need manual commits or GUIs
Is easy to drop into multiple folders for version control


 
