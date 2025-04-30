import os
import csv
import requests
import re
import unicodedata
import random
import shutil
import sys  # Added for command line arguments

# === CONFIGURATION ===
# Parse command line arguments
USE_DEFAULT_IMAGES = False
DUMP_EXISTING_AUTHORS = False

for arg in sys.argv[1:]:
    if arg == "-noimg":
        USE_DEFAULT_IMAGES = True
        print("Running with default images only (no downloads)")
    elif arg == "-dump":
        DUMP_EXISTING_AUTHORS = True
        print("Will delete existing authors directory before creating new profiles")

# Path to CSV file in the scripts/author-seeding folder
CSV_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "authors-list.csv")
# Path to authors directory relative to the project root
AUTHORS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "content", "authors")
DEFAULT_AVATARS = [
    "https://randomuser.me/api/portraits/women/17.jpg",
    "https://randomuser.me/api/portraits/men/32.jpg",
    "https://randomuser.me/api/portraits/women/56.jpg",
    "https://randomuser.me/api/portraits/men/75.jpg",
    "https://randomuser.me/api/portraits/women/90.jpg",
    "https://randomuser.me/api/portraits/men/41.jpg"
]

# === HELPER FUNCTIONS ===

def generate_folder_name(name):
    """Generate a clean folder name from author name (slug)"""
    # Remove accents/diacritics
    name = ''.join(c for c in unicodedata.normalize('NFD', name)
                  if not unicodedata.combining(c))
    
    # Convert to lowercase, remove special chars, and remove spaces
    return re.sub(r'[^\w]', '', name.lower().replace(' ', ''))

def extract_google_drive_file_id(url):
    """Extract file ID from Google Drive URL"""
    if not url or 'google.com' not in url:
        return None
    
    file_id = None
    if '/open?id=' in url:
        file_id = url.split('/open?id=')[1].split('&')[0]
    elif '/d/' in url:
        file_id = url.split('/d/')[1].split('/')[0]
    elif 'id=' in url:
        file_id = url.split('id=')[1].split('&')[0]
    
    return file_id

def parse_affiliations(affiliation_text):
    """Parse affiliations from text format to structured format"""
    if not affiliation_text:
        return []
    
    # Split by dash or hyphen which separates different affiliations
    parts = [p.strip() for p in re.split(r'\s*-\s*', affiliation_text)]
    result = []
    
    for part in parts:
        # Try to extract URL if it exists within parentheses first
        url_match = re.search(r'\((https?://[^)]+)\)', part)
        
        # If no URL in parentheses, check for bare URLs
        if not url_match:
            url_match = re.search(r'(https?://\S+)', part)
        
        url = ""
        if url_match:
            url = url_match.group(1)
            # Remove trailing periods from URLs
            if url.endswith('.'):
                url = url[:-1]
        
        # Remove the URL part from the name
        if url_match:
            if '(' in part and ')' in part:
                name = re.sub(r'\s*\([^)]+\)', '', part).strip()
            else:
                # If URL is not in parentheses, just remove it from the string
                name = part.replace(url, '').strip()
                # Remove trailing/leading periods that might have been part of the sentence
                name = name.strip('.')
        else:
            name = part.strip()
        
        # Clean up the name - remove multiple spaces and ensure consistent spacing
        name = re.sub(r'\s+', ' ', name).strip()
        
        # Add to results if we have a valid name
        if name:
            result.append({"name": name, "url": url})
    
    return result

def get_weight_by_role(role):
    """Determine weight based on role"""
    # Leadership roles get weight 30
    leadership_roles = [
        "president", "vice-president", "secretary", "treasurer", 
        "scientific advisor", "faculty advisor", "committee coordinator"
    ]
    
    # Convert role to lowercase for case-insensitive comparison
    role_lower = role.lower()
    
    # Check for leadership roles (weight 30)
    for leadership_role in leadership_roles:
        if leadership_role in role_lower:
            return 30
    
    # Check for academic advisor (weight 10)
    if "academic advisor" in role_lower:
        return 10
    
    # Default weight for volunteers and other roles
    return 0

def get_user_group_by_role(role):
    """Determine user group based on role"""
    # Leadership roles go to Authorities group
    leadership_roles = [
        "president", "vice-president", "secretary", "treasurer", 
        "scientific advisor", "faculty advisor"
    ]
    
    # Convert role to lowercase for case-insensitive comparison
    role_lower = role.lower()
    
    # Check for leadership roles (Authorities group)
    for leadership_role in leadership_roles:
        if leadership_role in role_lower:
            return "Authorities"
    
    # Academic advisors get their own group
    if "academic advisor" in role_lower:
        return "Academic Advisors"
    
    # Default user group for everyone else
    return "Volunteers"

def parse_education(education_text):
    """Parse education from text to structured format"""
    if not education_text:
        return []
    
    # Split by comma, 'and', or semicolon to get multiple education entries
    parts = re.split(r',\s*|\s+y\s+|;\s*', education_text)
    result = []
    
    for part in parts:
        part = part.strip()
        if not part:
            continue
        
        # Default: treat the whole string as the course
        course = part
        institution = ""
        
        # Common keywords that indicate an institution
        institution_keywords = [
            'university', 'universidad', 'instituto', 'college', 
            'school', 'uba', 'unq', 'unnoba'
        ]
        
        # Try to find an institution name in the text
        for keyword in institution_keywords:
            if keyword.lower() in part.lower():
                # Find the part of the string containing the institution
                index = part.lower().find(keyword.lower())
                
                # Look for the beginning of the institution name
                start = index
                while start > 0 and part[start-1] not in ",.;()":
                    start -= 1
                
                # Look for the end of the institution name
                end = index + len(keyword)
                while end < len(part) and part[end] not in ",.;()":
                    end += 1
                
                # Extract the institution name
                institution = part[start:end].strip()
                
                # Remove the institution from the course
                course = part[:start] + part[end:]
                course = course.strip(" ,.;()-")
                break
        
        # If we didn't find a keyword but there's a pattern like "at XYZ"
        if not institution:
            match = re.search(r'(?:en|at|from|de|by)\s+(?:la\s+|the\s+)?([^(),;]+)', part, re.IGNORECASE)
            if match:
                institution = match.group(1).strip()
                course = part.replace(match.group(0), '').strip(" ,.;()-")
        
        # Clean up course description
        course = re.sub(r'^\s*[-:]\s*', '', course)  # Remove leading dash or colon
        
        # Add to results
        if course:  # Only add if we have a course
            result.append({
                "course": course,
                "institution": institution
            })
    
    return result

def parse_social_links(links_text):
    """Parse social links to determine icon and link type"""
    if not links_text:
        return []
    
    # Split by comma or spaces if multiple links
    links = [link.strip() for link in re.split(r',\s*|\s+', links_text) if link.strip()]
    result = []
    
    for link in links:
        # Determine the type of link
        icon = "link"
        icon_pack = "fas"
        
        if "linkedin.com" in link:
            icon = "linkedin"
            icon_pack = "fab"
        elif "github.com" in link:
            icon = "github"
            icon_pack = "fab"
        elif "twitter.com" in link or "x.com" in link:
            icon = "twitter"
            icon_pack = "fab"
        elif "scholar.google.com" in link:
            icon = "google-scholar"
            icon_pack = "ai"
        
        result.append({"icon": icon, "icon_pack": icon_pack, "link": link})
    
    return result

def parse_interests(interests_text):
    """Parse interests from comma-separated text to a list"""
    if not interests_text:
        return []
    
    # Split by comma
    return [interest.strip() for interest in interests_text.split(',') if interest.strip()]

# === SETUP OUTPUT DIRECTORY ===
# Check if we should remove the existing authors directory
if DUMP_EXISTING_AUTHORS and os.path.exists(AUTHORS_DIR):
    print(f"Removing existing authors directory: {AUTHORS_DIR}")
    try:
        shutil.rmtree(AUTHORS_DIR)
        print("✅ Successfully removed existing authors directory")
    except Exception as e:
        print(f"⚠️ Error removing authors directory: {e}")

# Create authors directory if it doesn't exist
os.makedirs(AUTHORS_DIR, exist_ok=True)
print(f"✅ Created/confirmed authors directory: {AUTHORS_DIR}")

# === LOAD CSV ===
authors = []
try:
    with open(CSV_FILE, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        authors = list(csv_reader)
    print(f"✅ Loaded CSV with {len(authors)} authors")
except Exception as e:
    print(f"❌ Error loading CSV: {e}")
    exit(1)

# === PROCESS EACH AUTHOR ROW ===
for index, row in enumerate(authors):
    try:
        # Extract basic information
        name = str(row.get("Nombre/s y Apellido/s", "")).strip()
        if not name:
            print(f"⚠️ Skipping row {index + 1} - no name provided")
            continue
            
        folder = generate_folder_name(name)
        photo_url = str(row.get("Foto personal", "")).strip()
        email = str(row.get("E-mail", "")).strip()
        about_me = str(row.get("About me (en inglés) ", "")).strip()
        mini_bio = str(row.get("Mini biografía", "")).strip()
        interests_text = str(row.get("Lista de intereses en bioinformática (en inglés)", "")).strip()
        role = str(row.get("Cargo que ocupa", "Volunteer")).strip()
        affiliations_text = str(row.get("Afiliación (Laboratorio, Instituto/ Universidad) - Incluir links", "")).strip()
        social_links_text = str(row.get("Link de Linkedin, github, twitter, ID, Google Scholar, otro", "")).strip()
        education_text = str(row.get("Título/Carrera", "")).strip()
        
        # Process structured information
        role = role.capitalize() if role else "Volunteer"
        # Get weight based on role
        weight = get_weight_by_role(role)
        # Get user group based on role
        user_group = get_user_group_by_role(role)
        
        affiliations = parse_affiliations(affiliations_text)
        social_links = parse_social_links(social_links_text)
        interests = parse_interests(interests_text)
        education = parse_education(education_text)

        # === CREATE FOLDER FOR AUTHOR ===
        author_dir = os.path.join(AUTHORS_DIR, folder)
        os.makedirs(author_dir, exist_ok=True)
        
        # === FORMAT THE TEMPLATE DATA ===
        
        # Format affiliations for template
        formatted_affiliations = []
        for aff in affiliations:
            # Escape quotes with a single backslash
            safe_name = aff["name"].replace('"', '\\"')
            safe_url = aff["url"].replace('"', '\\"')
            
            formatted_affiliations.append(f'{{ name = "{safe_name}", url = "{safe_url}" }}')
            
        if formatted_affiliations:
            formatted_affiliations_str = ", ".join(formatted_affiliations)
        else:
            formatted_affiliations_str = '{ name = "RSG Argentina", url = "" }'
            
        # Format education entries for template
        formatted_education = []
        for edu in education:
            # Escape quotes with a single backslash
            safe_course = edu["course"].replace('"', '\\"')
            safe_institution = edu["institution"].replace('"', '\\"')
            
            # Only add if we have a course
            if safe_course:
                formatted_education.append(
                    f'[[education.courses]]\ncourse = "{safe_course}"\ninstitution = "{safe_institution}"\n# year = 2021'
                )
            
        formatted_education_str = "\n\n".join(formatted_education)
        
        # Format interests for template
        formatted_interests = []
        for interest in interests:
            # Escape quotes with a single backslash
            safe_interest = interest.replace('"', '\\"')
            formatted_interests.append(f'"{safe_interest}"')
            
        formatted_interests_str = ", ".join(formatted_interests)
        
        # Format social links for template
        formatted_social_links = []
        for social in social_links:
            # Escape quotes with a single backslash
            safe_link = social["link"].replace('"', '\\"')
            formatted_social_links.append(
                f'[[social]]\n  icon = "{social["icon"]}"\n  icon_pack = "{social["icon_pack"]}"\n  link = "{safe_link}"'
            )
            
        formatted_social_links_str = "\n\n".join(formatted_social_links)

        # === WRITE _index.md FILE ===
        index_md_path = os.path.join(author_dir, "_index.md")
        with open(index_md_path, "w", encoding="utf-8") as f:
            # Escape special characters in content
            name_safe = name.replace('"', '\\"')
            about_me_safe = about_me.replace('"', '\\"')
            email_safe = email.replace('"', '\\"')
            
            # Format user groups based on role
            if user_group:
                user_groups_str = f'["{user_group}"]'
            else:
                user_groups_str = "[]"  # Empty array for academic advisors
                
            f.write(f"""+++
# Display name
title = "{name_safe}"

# Author weight -- for sort purposes
weight = {weight}

# Username (this should match the folder name)
authors = ["{folder}"]

# Author name (this is required for people without content)
{folder} = [""]

# Role/position
role = "{role}"

# Organizations/Affiliations
#   Separate multiple entries with a comma, using the form: `[ {{name="Org1", url=""}}, {{name="Org2", url=""}} ]`.
organizations = [ {formatted_affiliations_str} ]

# Short bio (displayed in user profile at end of posts)
bio = ""

# Enter email to display Gravatar (if Gravatar enabled in Config)
email = "{email_safe}"

# List (academic) interests or hobbies
interests = [{formatted_interests_str}]             

# Organizational groups that you belong to (for People widget)
#   Set this to `[]` or comment out if you are not using People widget.
user_groups = {user_groups_str}

# List qualifications (such as academic degrees)

{formatted_education_str}

# Social/Academic Networking
# For available icons, see: https://sourcethemes.com/academic/docs/widgets/#icons
#   For an email link, use "fas" icon pack, "envelope" icon, and a link in the
#   form "mailto:your-email@example.com" or "#contact" for contact widget.

{formatted_social_links_str}

+++

# About me 

{about_me_safe}
""")

        # === DOWNLOAD AVATAR ===
        avatar_path = os.path.join(author_dir, "avatar.jpg")
        avatar_downloaded = False
        
        # Only attempt to download user images if -noimg flag is not set
        if not USE_DEFAULT_IMAGES and photo_url:
            # Convert Google Drive link to direct download if needed
            file_id = extract_google_drive_file_id(photo_url)
            if file_id:
                download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
            else:
                download_url = photo_url

            try:
                if download_url.startswith(("http://", "https://")):
                    response = requests.get(download_url, timeout=15)
                    if response.ok:
                        with open(avatar_path, "wb") as img:
                            img.write(response.content)
                        avatar_downloaded = True
                        print(f"  ✓ Downloaded avatar from: {download_url}")
            except Exception as e:
                print(f"  ⚠️ Error downloading avatar: {e}")

        # Use default avatar if download failed or -noimg flag was set
        if not avatar_downloaded:
            try:
                # Choose a random avatar from our list
                random_avatar = random.choice(DEFAULT_AVATARS)
                response = requests.get(random_avatar, timeout=10)
                if response.ok:
                    with open(avatar_path, "wb") as img:
                        img.write(response.content)
                    if USE_DEFAULT_IMAGES:
                        print(f"  ✓ Used default avatar (as requested)")
                    else:
                        print(f"  ✓ Used fallback avatar: {random_avatar}")
                else:
                    print(f"  ⚠️ Failed to download default avatar: HTTP {response.status_code}")
            except Exception as e:
                print(f"  ⚠️ Failed to download default avatar: {e}")

        print(f"✅ Created author: {folder}")
        
    except Exception as e:
        print(f"❌ Error processing author {index + 1}: {e}")

print(f"\n✅ Completed processing {len(authors)} authors")