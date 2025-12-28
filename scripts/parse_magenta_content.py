"""
Parse MagentaA11y markdown documentation files and generate content.json

This script reads markdown files from the MagentaA11y submodule and creates
a structured JSON file that can be used by the MCP server tools.
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, List, Any, Optional


def format_label(name: str) -> str:
    """Format a filename to a readable label."""
    return name.replace('-', ' ').replace('.md', '').title()


def extract_sections(content: str) -> Dict[str, Optional[str]]:
    """
    Extract sections from markdown content based on H2 headings.
    
    Sections include:
    - General Notes
    - Gherkin
    - Condensed
    - Criteria
    - Videos
    - Android Developer Notes
    - iOS Developer Notes
    - Developer Notes (other content)
    """
    sections = {
        'generalNotes': None,
        'gherkin': None,
        'condensed': None,
        'criteria': None,
        'videos': None,
        'androidDeveloperNotes': None,
        'iosDeveloperNotes': None,
        'developerNotes': None,
    }
    
    # Split content by H2 headings
    lines = content.split('\n')
    current_section = 'developerNotes'
    current_content = []
    
    for line in lines:
        # Check if line is an H2 heading
        h2_match = re.match(r'^##\s+(.+)$', line)
        if h2_match:
            # Save previous section if it has content
            if current_content:
                content_text = '\n'.join(current_content).strip()
                if content_text:
                    sections[current_section] = content_text
                current_content = []
            
            # Determine new section
            heading = h2_match.group(1).lower()
            if 'general notes' in heading:
                current_section = 'generalNotes'
            elif 'gherkin' in heading:
                current_section = 'gherkin'
            elif 'condensed' in heading:
                current_section = 'condensed'
            elif 'criteria' in heading:
                current_section = 'criteria'
            elif 'videos' in heading:
                current_section = 'videos'
            elif 'android developer notes' in heading:
                current_section = 'androidDeveloperNotes'
            elif 'ios developer notes' in heading:
                current_section = 'iosDeveloperNotes'
            else:
                current_section = 'developerNotes'
                current_content.append(line)
        elif not line.startswith('# '):  # Skip H1 headings
            current_content.append(line)
    
    # Save final section
    if current_content:
        content_text = '\n'.join(current_content).strip()
        if content_text:
            sections[current_section] = content_text
    
    return sections


def process_markdown_file(filepath: Path) -> Dict[str, Any]:
    """Process a single markdown file and extract its content."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        sections = extract_sections(content)
        
        result = {
            'label': format_label(filepath.stem),
            'name': filepath.stem,
            'type': 'file',
        }
        
        # Only include non-null sections
        for key, value in sections.items():
            if value is not None:
                result[key] = value
        
        return result
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return None


def get_directory_structure(dir_path: Path) -> List[Dict[str, Any]]:
    """Recursively get the directory structure and process markdown files."""
    items = []
    
    try:
        for item in sorted(dir_path.iterdir()):
            if item.is_dir():
                children = get_directory_structure(item)
                if children:  # Only include directories with content
                    items.append({
                        'label': format_label(item.name),
                        'name': item.name,
                        'children': children,
                    })
            elif item.is_file() and item.suffix == '.md':
                file_data = process_markdown_file(item)
                if file_data:
                    items.append(file_data)
    except Exception as e:
        print(f"Error processing directory {dir_path}: {e}")
    
    return items


def generate_content_data():
    """Generate content.json from MagentaA11y markdown documentation."""
    # Define paths
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    documentation_dir = project_root / 'data' / 'magentaA11y' / 'public' / 'content' / 'documentation'
    output_path = project_root / 'data' / 'content.json'
    
    if not documentation_dir.exists():
        print(f"Documentation directory not found: {documentation_dir}")
        print("Make sure the MagentaA11y submodule is initialized.")
        return
    
    print(f"Processing documentation from: {documentation_dir}")
    
    # Process each category
    content_data = {}
    
    # Define expected categories in order
    categories = ['web', 'native', 'how-to-test']
    
    for category in categories:
        category_path = documentation_dir / category
        if category_path.exists() and category_path.is_dir():
            print(f"Processing category: {category}")
            content_data[category] = get_directory_structure(category_path)
    
    # Write output file
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(content_data, f, indent=2, ensure_ascii=False)
        print(f"\n✓ Content data generated successfully: {output_path}")
        print(f"  Categories: {len(content_data)}")
        for category, items in content_data.items():
            print(f"  - {category}: {len(items)} items")
    except Exception as e:
        print(f"Error writing output file: {e}")


if __name__ == '__main__':
    generate_content_data()
