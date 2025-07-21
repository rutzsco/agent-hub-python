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

