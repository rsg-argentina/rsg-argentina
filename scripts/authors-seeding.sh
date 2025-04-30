#!/bin/bash
# RSG Argentina - Author Profile Generator (Cleaned CSV Version)

# Define paths
PROJECT_ROOT="$(pwd)"
CSV_FILE="$PROJECT_ROOT/authors-list.csv"
AUTHORS_DIR="$PROJECT_ROOT/content/authors"

echo "=== RSG Argentina Author Generator ==="
echo "Project root: $PROJECT_ROOT"
echo "CSV file: $CSV_FILE"
echo "Authors directory: $AUTHORS_DIR"

# Step 1: Clean authors directory
echo "Cleaning authors directory..."
rm -rf "$AUTHORS_DIR"
mkdir -p "$AUTHORS_DIR"

# Step 2: Check if CSV exists
if [ ! -f "$CSV_FILE" ]; then
  echo "Error: CSV file not found at $CSV_FILE"
  exit 1
fi

# Step 3: Process cleaned CSV (assumes columns: name,folder,photo_url)
tail -n +2 "$CSV_FILE" | while IFS=',' read -r name folder photo; do
  name=$(echo "$name" | tr -d '"')
  folder=$(echo "$folder" | tr -d '"')
  photo=$(echo "$photo" | tr -d '"')

  if [ -z "$name" ] || [ -z "$folder" ]; then
    continue
  fi

  author_dir="$AUTHORS_DIR/$folder"
  mkdir -p "$author_dir"

  # Generate author profile
  cat > "$author_dir/_index.md" << EOF
+++
# Display name
title = "$name"

# Author weight -- for sort purposes
weight = 10

# Username (this should match the folder name)
authors = ["$folder"]

# Role/position
role = "Member"

# Organizations/Affiliations
organizations = [{ name = "RSG Argentina", url = "" }]

# Short bio (displayed in user profile at end of posts)
bio = ""

# User groups
user_groups = ["Volunteers"]
+++

# About me
EOF

  # Download avatar image
  AVATAR_PATH="$author_dir/avatar.jpg"
  if [[ "$photo" == *"drive.google.com"* ]]; then
    FILE_ID=$(echo "$photo" | grep -oE '[-\w]{25,}' | head -n1)
    if [ -n "$FILE_ID" ]; then
      curl -s -L "https://drive.google.com/uc?export=download&id=$FILE_ID" -o "$AVATAR_PATH"
    fi
  elif [[ "$photo" == http* ]]; then
    curl -s -L "$photo" -o "$AVATAR_PATH"
  fi

  # Fallback avatar if download failed
  if [ ! -s "$AVATAR_PATH" ]; then
    curl -s "https://www.gravatar.com/avatar/00000000000000000000000000000000?d=mp&f=y&s=200" -o "$AVATAR_PATH"
  fi

  echo "✅ Created author: $folder"
done

echo "Author generation complete. Total authors: $(find "$AUTHORS_DIR" -mindepth 1 -maxdepth 1 -type d | wc -l)"
echo "Run 'hugo server -D' to preview your site."
