# Git Repository Sync Guide

This guide demonstrates how to clone from GitHub and sync changes between two remote versions of the same repository.

## Overview

When working with multiple remote repositories (e.g., a main repository and a fork, or syncing between different hosting platforms), you need to manage multiple remotes and keep them synchronized.

## Initial Setup

### 1. Clone the Repository from GitHub

```bash
# Clone the repository from GitHub
git clone https://github.com/rutzsco/agent-hub-python.git
cd agent-hub-python

# Check current remotes
git remote -v
```

This will show:
```
origin  https://github.com/rutzsco/agent-hub-python.git (fetch)
origin  https://github.com/rutzsco/agent-hub-python.git (push)
```

### 2. Add a Second Remote

Add another remote repository (e.g., a different hosting platform, fork, or backup location):

```bash
# Add a second remote (replace with your actual URL)
git remote add secondary https://gitlab.com/username/agent-hub-python.git

# Or for Azure DevOps:
# git remote add secondary https://dev.azure.com/organization/project/_git/agent-hub-python

# Or for a different GitHub account/organization:
# git remote add secondary https://github.com/otheraccount/agent-hub-python.git

# Verify remotes
git remote -v
```

Now you'll see:
```
origin      https://github.com/rutzsco/agent-hub-python.git (fetch)
origin      https://github.com/rutzsco/agent-hub-python.git (push)
secondary   https://gitlab.com/username/agent-hub-python.git (fetch)
secondary   https://gitlab.com/username/agent-hub-python.git (push)
```

## Syncing Changes Between Remotes

### Scenario 1: Push Changes to Both Remotes

When you make local changes and want to push to both repositories:

```bash
# Make your changes and commit
git add .
git commit -m "Your commit message"

# Push to the primary remote (GitHub)
git push origin main

# Push to the secondary remote
git push secondary main
```

### Scenario 2: Sync Changes from Primary to Secondary

When changes are made to the primary repository (origin) and you want to sync them to the secondary:

```bash
# Fetch latest changes from primary remote
git fetch origin

# Ensure you're on the main branch
git checkout main

# Pull changes from primary
git pull origin main

# Push changes to secondary remote
git push secondary main
```

### Scenario 3: Sync Changes from Secondary to Primary

When changes are made to the secondary repository and you want to sync them to the primary:

```bash
# Fetch latest changes from secondary remote
git fetch secondary

# Pull changes from secondary
git pull secondary main

# Push changes to primary remote
git push origin main
```

### Scenario 4: Bidirectional Sync (Manual)

When both repositories have new changes:

```bash
# Fetch from both remotes
git fetch origin
git fetch secondary

# Check for differences
git log origin/main..secondary/main  # Changes in secondary not in origin
git log secondary/main..origin/main  # Changes in origin not in secondary

# If there are conflicts, you may need to merge
git merge secondary/main  # Merge secondary changes into local main
git push origin main      # Push merged changes to origin
git push secondary main   # Push to secondary to keep in sync
```

## Automated Sync Scripts

### PowerShell Script for Windows

Create a `sync-repos.ps1` file:

```powershell
#!/usr/bin/env pwsh

param(
    [string]$Direction = "both",
    [string]$Branch = "main"
)

Write-Host "Syncing repositories..." -ForegroundColor Green

# Fetch from all remotes
Write-Host "Fetching from all remotes..." -ForegroundColor Yellow
git fetch --all

# Checkout target branch
git checkout $Branch

switch ($Direction) {
    "to-secondary" {
        Write-Host "Syncing from origin to secondary..." -ForegroundColor Cyan
        git pull origin $Branch
        git push secondary $Branch
    }
    "to-origin" {
        Write-Host "Syncing from secondary to origin..." -ForegroundColor Cyan
        git pull secondary $Branch
        git push origin $Branch
    }
    "both" {
        Write-Host "Syncing both directions..." -ForegroundColor Cyan
        git pull origin $Branch
        git push secondary $Branch
        Write-Host "Sync complete!" -ForegroundColor Green
    }
    default {
        Write-Host "Invalid direction. Use: to-secondary, to-origin, or both" -ForegroundColor Red
        exit 1
    }
}

Write-Host "Repository sync completed!" -ForegroundColor Green
```

Usage:
```bash
# Sync from origin to secondary
.\sync-repos.ps1 -Direction "to-secondary"

# Sync from secondary to origin
.\sync-repos.ps1 -Direction "to-origin"

# Sync both (default)
.\sync-repos.ps1
```

### Bash Script for Linux/macOS

Create a `sync-repos.sh` file:

```bash
#!/bin/bash

DIRECTION=${1:-both}
BRANCH=${2:-main}

echo "Syncing repositories..."

# Fetch from all remotes
echo "Fetching from all remotes..."
git fetch --all

# Checkout target branch
git checkout $BRANCH

case $DIRECTION in
    "to-secondary")
        echo "Syncing from origin to secondary..."
        git pull origin $BRANCH
        git push secondary $BRANCH
        ;;
    "to-origin")
        echo "Syncing from secondary to origin..."
        git pull secondary $BRANCH
        git push origin $BRANCH
        ;;
    "both")
        echo "Syncing both directions..."
        git pull origin $BRANCH
        git push secondary $BRANCH
        echo "Sync complete!"
        ;;
    *)
        echo "Invalid direction. Use: to-secondary, to-origin, or both"
        exit 1
        ;;
esac

echo "Repository sync completed!"
```

Usage:
```bash
chmod +x sync-repos.sh

# Sync from origin to secondary
./sync-repos.sh to-secondary

# Sync from secondary to origin
./sync-repos.sh to-origin

# Sync both (default)
./sync-repos.sh
```

## CI/CD Integration

### GitHub Actions for Auto-Sync

Create `.github/workflows/sync-repos.yml`:

```yaml
name: Sync with Secondary Repository

on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Setup Git
        run: |
          git config user.name "GitHub Actions Bot"
          git config user.email "actions@github.com"

      - name: Add secondary remote
        run: |
          git remote add secondary ${{ secrets.SECONDARY_REPO_URL }}

      - name: Push to secondary
        run: |
          git push secondary main
        env:
          GITHUB_TOKEN: ${{ secrets.SECONDARY_REPO_TOKEN }}
```

## Best Practices

### 1. Use Different Branch Names for Testing
```bash
# Create feature branches for testing sync
git checkout -b feature/sync-test
git push origin feature/sync-test
git push secondary feature/sync-test
```

### 2. Handle Merge Conflicts
```bash
# If conflicts occur during sync
git status
# Resolve conflicts manually
git add .
git commit -m "Resolve sync conflicts"
git push origin main
git push secondary main
```

### 3. Verify Sync Status
```bash
# Check if repositories are in sync
git fetch --all
git log --oneline --graph --all
```

### 4. Set Up Different Default Remotes per Branch
```bash
# Set different upstream for different branches
git branch --set-upstream-to=origin/main main
git branch --set-upstream-to=secondary/develop develop
```

## Troubleshooting

### Issue: Authentication Errors
```bash
# For HTTPS remotes, use personal access tokens
git remote set-url secondary https://username:token@gitlab.com/username/repo.git

# For SSH, ensure SSH keys are properly configured
git remote set-url secondary git@gitlab.com:username/repo.git
```

### Issue: Divergent Histories
```bash
# If repositories have divergent histories
git pull --rebase secondary main
# Or allow merge commits
git pull --no-rebase secondary main
```

### Issue: Large File Sync Issues
```bash
# For repositories with Git LFS
git lfs fetch --all
git lfs push secondary --all
```

## Security Considerations

1. **Secrets Management**: Store credentials in environment variables or CI/CD secrets
2. **Access Control**: Ensure proper permissions on both repositories
3. **Audit Trail**: Monitor sync activities for security compliance
4. **Branch Protection**: Consider different protection rules for different remotes

## Example Workflow

Here's a complete example workflow for this repository:

```bash
# 1. Clone from GitHub
git clone https://github.com/rutzsco/agent-hub-python.git
cd agent-hub-python

# 2. Add secondary remote (example: GitLab)
git remote add gitlab https://gitlab.com/username/agent-hub-python.git

# 3. Push initial code to both
git push origin main
git push gitlab main

# 4. Make changes
echo "# New feature" >> NEW_FEATURE.md
git add NEW_FEATURE.md
git commit -m "Add new feature documentation"

# 5. Sync to both remotes
git push origin main
git push gitlab main

# 6. Later, sync changes from secondary back
git fetch gitlab
git pull gitlab main
git push origin main
```

This ensures both repositories stay synchronized and changes can flow bidirectionally as needed.
