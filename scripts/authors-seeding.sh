#!/bin/bash
# RSG Argentina - Author Profile Generator (Updated for image and CSV)

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

# Step 3: Get column indices
HEADER=$(head -n 1 "$CSV_FILE")
IFS=',' read -ra COLUMNS <<< "$HEADER"

NAME_COL=0
PHOTO_COL=0

for i in "${!COLUMNS[@]}"; do
  col="${COLUMNS[$i]}"
  if [[ "$col" == *"Nombre/s y Apellido/s"* ]]; then
    NAME_COL=$((i + 1))
  elif [[ "$col" == *"Foto personal"* ]]; then
    PHOTO_COL=$((i + 1))
  fi
done

if [[ $NAME_COL -eq 0 ]]; then
  echo "Error: Could not find name column."
  exit 1
fi

echo "Found 'name' column at position: $NAME_COL"
echo "Found 'photo' column at position: $PHOTO_COL"

# Step 4: Process CSV
tail -n +2 "$CSV_FILE" | while IFS= read -r line; do
  name=$(echo "$line" | awk -F',' -v col="$NAME_COL" '{print $col}' | tr -d '"')
  photo=$(echo "$line" | awk -F',' -v col="$PHOTO_COL" '{print $col}' | tr -d '"')

  if [ -z "$name" ]; then
    continue
  fi

  folder_name=$(echo "$name" | tr -cd 'a-zA-Z0-9' | tr '[:upper:]' '[:lower:]')
  if [ -z "$folder_name" ] || [[ "$folder_name" =~ ^[0-9]+$ ]]; then
    echo "  Skipping: Could not create valid folder name"
    continue
  fi

  author_dir="$AUTHORS_DIR/$folder_name"
  mkdir -p "$author_dir"

  # Generate author profile
  cat > "$author_dir/_index.md" << EOF
+++
title = "$name"
authors = ["$folder_name"]
role = "Member"
organizations = [{ name = "RSG Argentina", url = "" }]
bio = ""
user_groups = ["Volunteers"]
+++

# About me
EOF

  # Download avatar
  AVATAR_PATH="$author_dir/avatar.jpg"
  if [[ "$photo" == *"drive.google.com"* ]]; then
    FILE_ID=$(echo "$photo" | grep -oE '[-\w]{25,}' | head -n1)
    if [ -n "$FILE_ID" ]; then
      curl -s -L "https://drive.google.com/uc?export=download&id=$FILE_ID" -o "$AVATAR_PATH"
    fi
  fi

  # Fallback avatar if download failed
  if [ ! -f "$AVATAR_PATH" ]; then
    curl -s "https://www.gravatar.com/avatar/00000000000000000000000000000000?d=mp&f=y&s=200" -o "$AVATAR_PATH"
  fi

  echo "  Created author: $folder_name"
done

echo "Author generation complete. Total authors: $(find "$AUTHORS_DIR" -mindepth 1 -maxdepth 1 -type d | wc -l)"
echo "Run 'hugo server -D' to preview your site."
