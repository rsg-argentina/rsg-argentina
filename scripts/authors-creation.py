import os
import pandas as pd
import requests

# === CONFIGURATION ===
CSV_FILE = "/mnt/data/authors-list.csv"  # Use cleaned CSV with columns: name, folder, photo_url
AUTHORS_DIR = os.path.join(os.getcwd(), "content", "authors")
DEFAULT_AVATAR = "https://www.gravatar.com/avatar/00000000000000000000000000000000?d=mp&f=y&s=200"

# === SETUP OUTPUT DIRECTORY ===
os.makedirs(AUTHORS_DIR, exist_ok=True)

# === LOAD CLEANED CSV ===
df = pd.read_csv(CSV_FILE)

# === PROCESS EACH AUTHOR ROW ===
for index, row in df.iterrows():
    name = str(row.get("name", "")).strip()
    folder = str(row.get("folder", "")).strip()
    photo_url = str(row.get("photo_url", "")).strip()

    # === CREATE FOLDER FOR AUTHOR ===
    author_dir = os.path.join(AUTHORS_DIR, folder)
    os.makedirs(author_dir, exist_ok=True)

    # === WRITE _index.md FILE ===
    index_md_path = os.path.join(author_dir, "_index.md")
    with open(index_md_path, "w", encoding="utf-8") as f:
        f.write(f"""+++
# Display name
title = "{name}"

# Author weight -- for sort purposes
weight = {(index + 1) * 10}

# Username (this should match the folder name)
authors = ["{folder}"]

# Role/position
role = "Member"

# Organizations/Affiliations
organizations = [{{ name = "RSG Argentina", url = "" }}]

# Short bio (displayed in user profile at end of posts)
bio = ""

# User groups
user_groups = ["Volunteers"]
+++

# About me
""")

    # === DOWNLOAD AVATAR ===
    avatar_path = os.path.join(author_dir, "avatar.jpg")
    avatar_downloaded = False

    if "drive.google.com" in photo_url:
        # Convert Google Drive link to direct download
        file_id = ""
        if "id=" in photo_url:
            file_id = photo_url.split("id=")[-1].split("&")[0]
        elif "/d/" in photo_url:
            file_id = photo_url.split("/d/")[-1].split("/")[0]
        if file_id:
            photo_url = f"https://drive.google.com/uc?export=download&id={file_id}"

    try:
        if photo_url.startswith("http"):
            response = requests.get(photo_url, timeout=10)
            if response.ok:
                with open(avatar_path, "wb") as img:
                    img.write(response.content)
                avatar_downloaded = True
    except Exception as e:
        print(f"⚠️ Error downloading avatar for {name}: {e}")

    # === FALLBACK TO DEFAULT AVATAR IF FAILED ===
    if not avatar_downloaded:
        try:
            response = requests.get(DEFAULT_AVATAR, timeout=10)
            if response.ok:
                with open(avatar_path, "wb") as img:
                    img.write(response.content)
        except Exception as e:
            print(f"⚠️ Failed to download fallback avatar for {name}: {e}")

    print(f"✅ Created author: {folder}")