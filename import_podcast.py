import xml.etree.ElementTree as ET
from datetime import datetime
import os
import re

feed_file = '/mnt/user-data/uploads/feed.xml'
posts_dir = '/mnt/user-data/outputs/_posts'

os.makedirs(posts_dir, exist_ok=True)

# Parse the XML
tree = ET.parse(feed_file)
root = tree.getroot()

# Define namespaces
namespaces = {
    'itunes': 'http://www.itunes.com/dtds/podcast-1.0.dtd',
    'content': 'http://purl.org/rss/1.0/modules/content/'
}

# Find all items
items = root.findall('.//item')

for item in items:
    # Extract title
    title_elem = item.find('title')
    title = title_elem.text.strip() if title_elem is not None else "Untitled"
    
    # Extract date
    pub_date_elem = item.find('pubDate')
    if pub_date_elem is not None:
        # Parse RFC 2822 date format (handle both short and full month names)
        date_str = pub_date_elem.text
        try:
            date = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %Z')
        except ValueError:
            # Try with full month name
            date = datetime.strptime(date_str, '%a, %d %B %Y %H:%M:%S %Z')
        date_formatted = date.strftime('%Y-%m-%d')
        date_full = date.strftime('%Y-%m-%d %H:%M:%S -0500')
    else:
        continue
    
    # Create filename
    title_slug = re.sub(r'[^0-9A-Za-z\s-]', '', title)
    title_slug = re.sub(r'\s+', '-', title_slug).lower()
    filename = os.path.join(posts_dir, f'{date_formatted}-{title_slug}.md')
    
    # Skip if exists
    if os.path.exists(filename):
        print(f"Skipping (already exists): {filename}")
        continue
    
    # Extract enclosure
    enclosure = item.find('enclosure')
    if enclosure is not None:
        original_url = enclosure.get('url')
        # Extract filename from URL and convert to _assets path
        audio_filename = original_url.split('/')[-1]
        audio_url = f"https://shawkatya.github.io/closetalkers/_assets/{audio_filename}"
        file_size = enclosure.get('length')
    else:
        audio_url = ""
        file_size = "0"
    
    # Extract iTunes data
    duration_elem = item.find('itunes:duration', namespaces)
    duration = duration_elem.text if duration_elem is not None else "0"
    
    episode_type_elem = item.find('itunes:episodeType', namespaces)
    episode_type = episode_type_elem.text if episode_type_elem is not None else "full"
    
    season_elem = item.find('itunes:season', namespaces)
    season = season_elem.text if season_elem is not None else ""
    
    explicit_elem = item.find('itunes:explicit', namespaces)
    explicit = explicit_elem.text if explicit_elem is not None else "no"
    
    # Get GUID
    guid_elem = item.find('guid')
    guid = guid_elem.text if guid_elem is not None else ""
    
    # Get summary
    summary_elem = item.find('itunes:summary', namespaces)
    summary = summary_elem.text.strip() if summary_elem is not None else ""
    
    # Get description and clean HTML
    description_elem = item.find('description')
    if description_elem is not None:
        description = description_elem.text
        # Remove CDATA markers and HTML tags
        description = re.sub(r'<!\[CDATA\[|\]\]>', '', description)
        description = re.sub(r'<[^>]+>', '', description).strip()
    else:
        description = summary
    
    # Write markdown file
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('---\n')
        f.write('layout: post\n')
        f.write(f'title: "{title}"\n')
        f.write(f'date: {date_full}\n')
        f.write('podcast:\n')
        f.write(f'  audio_url: "{audio_url}"\n')
        f.write(f'  file_size: {file_size}\n')
        f.write(f'  duration: {duration}\n')
        f.write(f'  guid: "{guid}"\n')
        if season:
            f.write(f'  season: {season}\n')
        f.write(f'  episode_type: "{episode_type}"\n')
        f.write(f'  explicit: "{explicit}"\n')
        f.write(f'  summary: "{summary}"\n')
        f.write('  # image: "/assets/episode-cover.png"\n')
        f.write('---\n')
        f.write(description + '\n\n')
        f.write(f'[Listen to the episode]({audio_url})\n')
    
    print(f"Created: {filename}")

print(f"\nImport complete! Files created in {posts_dir}")
