#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 2 ]; then
  echo "Usage: ./scripts/create_topic.sh <section-folder> <topic-name>"
  echo "Example: ./scripts/create_topic.sh 02-implementation new-camera-node"
  exit 1
fi

SECTION="$1"
TOPIC="$2"
DIR="$SECTION/$TOPIC"

mkdir -p "$DIR/assets/images" "$DIR/assets/diagrams" "$DIR/assets/tables" "$DIR/assets/exports"
cat > "$DIR/index.qmd" <<EOF
---
title: "$TOPIC"
description: "TBD"
categories: []
status: draft
---

# $TOPIC

## Mục tiêu

## Nội dung chính

## Liên kết liên quan
EOF

echo "Created $DIR"
