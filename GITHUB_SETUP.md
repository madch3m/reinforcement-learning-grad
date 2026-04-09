# 🚀 GitHub Setup Guide

This guide walks you through publishing your Traffic Signal RL project to GitHub.

## 📋 Prerequisites

- Git installed on your computer ([Download Git](https://git-scm.com/downloads))
- GitHub account ([Sign up](https://github.com/join))
- The `traffic-signal-rl-complete` folder

## 🎯 Quick Start (5 minutes)

### Step 1: Create GitHub Repository

1. Go to [GitHub](https://github.com)
2. Click the **+** icon (top right) → **New repository**
3. Fill in:
   - **Repository name**: `traffic-signal-rl`
   - **Description**: "Traffic signal optimization using reinforcement learning"
   - **Visibility**: Public ✅ (or Private)
   - **Initialize**: ❌ Do NOT check any boxes (no README, no .gitignore, no license)
4. Click **Create repository**

### Step 2: Initialize Local Repository

Open terminal/command prompt in the `traffic-signal-rl-complete` folder:

**Mac/Linux:**
```bash
cd path/to/traffic-signal-rl-complete

# Initialize git repository
git init

# Add all files
git add .

# Make first commit
git commit -m "Initial commit: Traffic Signal RL project"

# Set main branch
git branch -M main

# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/traffic-signal-rl.git

# Push to GitHub
git push -u origin main
```

**Windows (PowerShell):**
```powershell
cd path\to\traffic-signal-rl-complete

# Initialize git repository
git init

# Add all files
git add .

# Make first commit
git commit -m "Initial commit: Traffic Signal RL project"

# Set main branch
git branch -M main

# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/traffic-signal-rl.git

# Push to GitHub
git push -u origin main
```

### Step 3: Verify Upload

1. Go to your repository: `https://github.com/YOUR_USERNAME/traffic-signal-rl`
2. You should see all your files!
3. The README.md will display automatically

🎉 **Done!** Your project is now on GitHub!

---

## 📝 Detailed Instructions

### Using GitHub Desktop (Easier Alternative)

If you prefer a GUI:

1. **Download GitHub Desktop**: https://desktop.github.com/
2. **Install and sign in** to GitHub
3. **Add repository**:
   - File → Add Local Repository
   - Choose `traffic-signal-rl-complete` folder
   - Click "Create Repository"
4. **Publish**:
   - Click "Publish repository"
   - Uncheck "Keep this code private" (unless you want it private)
   - Click "Publish Repository"

### First-Time Git Configuration

If this is your first time using Git:

```bash
# Set your name
git config --global user.name "Your Name"

# Set your email (use GitHub email)
git config --global user.email "your.email@example.com"
```

---

## 🔄 Making Updates

### After Making Changes

```bash
# Check what changed
git status

# Add changed files
git add .

# Or add specific files
git add filename.py

# Commit with message
git commit -m "Add SUMO integration"

# Push to GitHub
git push
```

### Quick Update Script

**update.sh** (Mac/Linux):
```bash
#!/bin/bash
git add .
git commit -m "$1"
git push
```

Usage:
```bash
chmod +x update.sh
./update.sh "Your commit message"
```

**update.bat** (Windows):
```batch
@echo off
git add .
git commit -m "%~1"
git push
```

Usage:
```batch
update.bat "Your commit message"
```

---

## 🌿 Branch Management

### Creating a Branch

```bash
# Create and switch to new branch
git checkout -b feature/new-feature

# Make changes, then commit
git add .
git commit -m "Add new feature"

# Push branch to GitHub
git push -u origin feature/new-feature
```

### Merging Branches

```bash
# Switch to main
git checkout main

# Merge your branch
git merge feature/new-feature

# Push to GitHub
git push
```

---

## 🔐 Authentication

### Using Personal Access Token (Recommended)

GitHub no longer accepts passwords. Use a Personal Access Token:

1. **Generate Token**:
   - GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Click "Generate new token (classic)"
   - Select scopes: `repo`, `workflow`
   - Generate and **copy the token**

2. **Use Token**:
   - When git asks for password, paste the token instead
   - Or configure credential helper:
     ```bash
     # Mac
     git config --global credential.helper osxkeychain
     
     # Windows
     git config --global credential.helper wincred
     
     # Linux
     git config --global credential.helper cache
     ```

### Using SSH (Alternative)

1. **Generate SSH key**:
   ```bash
   ssh-keygen -t ed25519 -C "your.email@example.com"
   ```

2. **Add to GitHub**:
   - Copy public key: `cat ~/.ssh/id_ed25519.pub`
   - GitHub → Settings → SSH and GPG keys → New SSH key
   - Paste key and save

3. **Use SSH URL**:
   ```bash
   git remote set-url origin git@github.com:YOUR_USERNAME/traffic-signal-rl.git
   ```

---

## 📊 GitHub Features to Enable

### 1. GitHub Actions (CI/CD)

Your project includes a `.github/workflows/ci.yml` file that:
- Runs tests automatically
- Checks code quality
- Tests on multiple Python versions

To enable:
1. Go to repository → Actions tab
2. GitHub will detect the workflow automatically
3. Workflows run on every push/PR

### 2. Issues

Enable issue tracking:
1. Repository → Settings → Features
2. Check "Issues"
3. Users can report bugs and suggest features

### 3. Discussions

Enable community discussions:
1. Repository → Settings → Features
2. Check "Discussions"
3. Great for Q&A and community engagement

### 4. GitHub Pages (Optional)

Host documentation:
1. Create `docs/` folder with `index.html`
2. Repository → Settings → Pages
3. Select source: `main` branch, `/docs` folder
4. Your docs will be at: `https://YOUR_USERNAME.github.io/traffic-signal-rl/`

### 5. Topics/Tags

Add topics for discoverability:
1. Repository main page → ⚙️ (next to About)
2. Add topics: `reinforcement-learning`, `traffic-signal`, `machine-learning`, `gradio`, `python`

---

## 🏷️ Releases

### Creating a Release

```bash
# Tag a version
git tag -a v1.0.0 -m "Version 1.0.0: Initial release"

# Push tag
git push origin v1.0.0
```

On GitHub:
1. Repository → Releases → Create a new release
2. Choose tag: v1.0.0
3. Add release notes
4. Attach compiled files if needed
5. Publish release

---

## 📢 Promoting Your Repository

### README Badges

Add badges to your README:

```markdown
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/YOUR_USERNAME/traffic-signal-rl.svg)](https://github.com/YOUR_USERNAME/traffic-signal-rl/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/YOUR_USERNAME/traffic-signal-rl.svg)](https://github.com/YOUR_USERNAME/traffic-signal-rl/network)
```

### Social Sharing

1. **Twitter/X**: Share with hashtags #MachineLearning #ReinforcementLearning
2. **LinkedIn**: Post about your project
3. **Reddit**: r/MachineLearning, r/reinforcementlearning
4. **Dev.to**: Write a blog post about the project
5. **Hacker News**: Share on Show HN

### GitHub Features

1. **Star your own repo** (why not? 😄)
2. **Watch** your repo for notifications
3. **Add topics** for discoverability
4. **Complete profile README** at `YOUR_USERNAME/YOUR_USERNAME`

---

## 🔧 Troubleshooting

### "Permission denied"
- Check your authentication (token or SSH)
- Verify repository URL: `git remote -v`

### "Repository not found"
- Verify repository name
- Check repository visibility (private vs public)

### "Large files"
GitHub has a 100MB file limit. For large files:
```bash
# Install Git LFS
git lfs install

# Track large files
git lfs track "*.zip"
git lfs track "models/*"

# Add .gitattributes
git add .gitattributes
```

### "Merge conflicts"
```bash
# Pull latest changes
git pull origin main

# Resolve conflicts in files
# Edit files to fix conflicts

# Add resolved files
git add .

# Commit merge
git commit -m "Resolve merge conflicts"

# Push
git push
```

---

## 📚 Useful Git Commands

```bash
# View status
git status

# View commit history
git log

# View changes
git diff

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Discard local changes
git checkout -- filename.py

# View remote URL
git remote -v

# Update remote URL
git remote set-url origin NEW_URL

# Create .gitignore from template
curl https://raw.githubusercontent.com/github/gitignore/main/Python.gitignore > .gitignore
```

---

## 🎓 Learning Resources

- **Git Basics**: https://git-scm.com/book/en/v2
- **GitHub Guides**: https://guides.github.com/
- **Interactive Tutorial**: https://learngitbranching.js.org/
- **Git Cheat Sheet**: https://education.github.com/git-cheat-sheet-education.pdf

---

## ✅ Checklist

Before publishing:
- [ ] Update README with your information
- [ ] Replace placeholders (YOUR_USERNAME, YOUR_NAME)
- [ ] Test all scripts work
- [ ] Add LICENSE file
- [ ] Create meaningful .gitignore
- [ ] Write clear commit messages
- [ ] Add repository description
- [ ] Add topics/tags
- [ ] Enable issues and discussions
- [ ] Review code for sensitive data (API keys, passwords)

After publishing:
- [ ] Share on social media
- [ ] Submit to awesome lists
- [ ] Write a blog post
- [ ] Add to your portfolio
- [ ] Keep it updated!

---

**Happy Publishing! 🚀**

Your project will help others learn about reinforcement learning and traffic optimization!
