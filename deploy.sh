#!/bin/bash

# Deploy agents, commands, and skills to global Claude config

set -e

CLAUDE_CONFIG_DIR="$HOME/.claude"
BACKUP_DIR="$HOME/claude-backups"
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

echo "Deploying Claude configuration..."
echo "Source: $PROJECT_DIR"
echo "Target: $CLAUDE_CONFIG_DIR"
echo ""

# Backup existing configuration if it exists
if [ -d "$CLAUDE_CONFIG_DIR" ]; then
    echo "Backing up existing configuration..."
    mkdir -p "$BACKUP_DIR"
    BACKUP_PATH="$BACKUP_DIR/claude_backup_$TIMESTAMP"
    cp -r "$CLAUDE_CONFIG_DIR" "$BACKUP_PATH"
    echo "✓ Backup created at: $BACKUP_PATH"
    echo ""
fi

# Create target directory if it doesn't exist
mkdir -p "$CLAUDE_CONFIG_DIR"

# Copy directories
echo "Copying agents..."
cp -r "$PROJECT_DIR/agents" "$CLAUDE_CONFIG_DIR/"

echo "Copying commands..."
cp -r "$PROJECT_DIR/commands" "$CLAUDE_CONFIG_DIR/"

echo "Copying skills..."
cp -r "$PROJECT_DIR/skills" "$CLAUDE_CONFIG_DIR/"

echo ""
echo "✓ Deployment complete!"
echo "Configuration deployed to: $CLAUDE_CONFIG_DIR"

