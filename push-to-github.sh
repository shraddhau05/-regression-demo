#!/bin/bash
cd "$(dirname "$0")"

if [ ! -d .git ] || [ ! -f .git/HEAD ]; then
  git init
  git add .
  git commit -m "Initial project files"
fi

git branch -M main

REMOTE_URL="https://github.com/shraddhau05/-regression-demo.git"
if ! git remote | grep -q '^origin$'; then
  git remote add origin "$REMOTE_URL"
fi

git add .
git commit -m "Update regression suite demo and custom agent" || true
git push -u origin main
