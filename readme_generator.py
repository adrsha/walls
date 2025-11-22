#!/usr/bin/env python3

import os
import sys
from pathlib import Path
from typing import List

# Configuration
WALLPAPER_DIRS   = ['wallpapers', 'images', '.']
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'}
OUTPUT_FILE      = 'README.md'
IMAGES_PER_ROW   = 3
THUMBNAIL_WIDTH  = 300

def find_images(directory: str) -> List[str]:
    """
    Recursively find all image files in a directory.
    Returns list of relative paths from the directory.
    """
    if not os.path.exists(directory):
        return []
    
    images = []
    
    try:
        for root, dirs, files in os.walk(directory):
            # Skip hidden directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'node_modules']
            
            for file in files:
                # Skip hidden files and README
                if file.startswith('.') or file == 'README.md':
                    continue
                
                file_ext = os.path.splitext(file)[1].lower()
                if file_ext in IMAGE_EXTENSIONS:
                    full_path     = os.path.join(root, file)
                    relative_path = os.path.relpath(full_path, directory)
                    images.append(relative_path)
    
    except Exception as e:
        print(f"Error reading directory {directory}: {e}", file=sys.stderr)
    
    return sorted(images)

def generate_image_row(images: List[str], start_index: int) -> str:
    """
    Generate a markdown table row with images.
    """
    row_images = images[start_index:start_index + IMAGES_PER_ROW]
    
    if not row_images:
        return ''
    
    # Create image cells
    cells = []
    for img_path in row_images:
        img_name     = os.path.splitext(os.path.basename(img_path))[0]
        encoded_path = img_path.replace('\\', '/').replace(' ', '%20')
        cell         = f'<img src="{encoded_path}" width="{THUMBNAIL_WIDTH}" alt="{img_name}">'
        cells.append(cell)
    
    # Fill remaining cells if needed
    while len(cells) < IMAGES_PER_ROW:
        cells.append('')
    
    table_row = f"| {' | '.join(cells)} |\n"
    
    return table_row

def generate_readme(images: List[str], repo_name: str) -> str:
    """
    Generate complete README content.
    """
    if not images:
        return f"""# {repo_name}

No wallpapers found in this repository.

---
*This README was automatically generated*
"""
    
    content = f"""# Wallpapers: adrsha/{repo_name}

A collection of {len(images)} wallpapers.

## Gallery

"""
    
    # Generate table header
    header_cells = [''] * IMAGES_PER_ROW
    separator    = ['---'] * IMAGES_PER_ROW
    
    content += f"| {' | '.join(header_cells)} |\n"
    content += f"| {' | '.join(separator)} |\n"
    
    # Generate image rows
    for i in range(0, len(images), IMAGES_PER_ROW):
        content += generate_image_row(images, i)
    
    content += f"""

---

**Total wallpapers:** {len(images)}

*This README was automatically generated*
"""
    
    return content

def main():
    """
    Main function to generate README.
    """
    # Determine which directory to scan
    scan_dir = '.'
    for directory in WALLPAPER_DIRS:
        if os.path.exists(directory) and directory != '.':
            scan_dir = directory
            break
    
    print(f"Scanning directory: {scan_dir}")
    
    # Find all images
    images = find_images(scan_dir)
    
    if not images:
        print("Warning: No images found!", file=sys.stderr)
    else:
        print(f"Found {len(images)} images")
    
    # Get repository name
    repo_name = os.path.basename(os.path.abspath('.'))
    if repo_name == '':
        repo_name = 'Wallpapers'
    
    # Generate README content
    readme_content = generate_readme(images, repo_name)
    
    # Write to file
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        print(f"Successfully generated {OUTPUT_FILE}")
    except Exception as e:
        print(f"Error writing {OUTPUT_FILE}: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main();
