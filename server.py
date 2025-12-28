"""
MagentaA11y MCP Server

A FastMCP server that exposes accessibility testing documentation and tools
from T-Mobile's MagentaA11y project.
"""

from fastmcp import FastMCP
import json
from pathlib import Path
from typing import Optional, List, Dict, Any

# Initialize FastMCP server
mcp = FastMCP("magentaa11y-mcp")

# Load data from JSON file built by MagentaA11y
DATA_PATH = Path(__file__).parent / "data" / "magentaA11y" / "src" / "shared" / "content.json"

def load_data():
    """Load data at module level for efficiency"""
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

DATA = load_data()


@mcp.tool()
def list_issue_templates() -> str:
    """
    Lists all available accessibility issue templates from MagentaA11y.
    
    Returns information about the different categories (web, native, how-to-test)
    and the types of accessibility issues documented.
    
    Returns:
        Formatted list of all available templates organized by category
    """
    result = "# MagentaA11y Accessibility Issue Templates\n\n"
    
    for category, items in DATA.items():
        result += f"## {category.upper()}\n\n"
        count = count_templates(items)
        result += f"Total templates: {count}\n\n"
        result += format_template_list(items, level=3)
        result += "\n"
    
    return result


def count_templates(items: List[Dict[str, Any]], count: int = 0) -> int:
    """Recursively count all template files"""
    for item in items:
        if item.get('type') == 'file':
            count += 1
        elif 'children' in item:
            count = count_templates(item['children'], count)
    return count


def format_template_list(items: List[Dict[str, Any]], level: int = 1) -> str:
    """Recursively format template list"""
    result = ""
    for item in items:
        indent = "  " * (level - 1)
        if item.get('type') == 'file':
            result += f"{indent}• {item['label']} (`{item['name']}`)\n"
        elif 'children' in item:
            result += f"{indent}**{item['label']}**\n"
            result += format_template_list(item['children'], level + 1)
    return result


@mcp.tool()
def get_issue_template(category: str, template_name: str) -> str:
    """
    Retrieves the content of a specific accessibility issue template.
    
    Args:
        category: The category (web, native, how-to-test)
        template_name: The name of the template (e.g., 'alert-notification', 'button')
    
    Returns:
        The full template content including all sections (general notes, gherkin, criteria, etc.)
    """
    items = DATA.get(category, [])
    template = find_template(items, template_name)
    
    if not template:
        return f"Template '{template_name}' not found in category '{category}'.\n\nUse list_issue_templates() to see available templates."
    
    result = f"# {template['label']}\n\n"
    result += f"**Category:** {category}\n"
    result += f"**Name:** {template['name']}\n\n"
    
    sections = [
        ('generalNotes', 'General Notes'),
        ('gherkin', 'Gherkin Acceptance Criteria'),
        ('condensed', 'Condensed Criteria'),
        ('criteria', 'Criteria'),
        ('videos', 'Videos'),
        ('androidDeveloperNotes', 'Android Developer Notes'),
        ('iosDeveloperNotes', 'iOS Developer Notes'),
        ('developerNotes', 'Developer Notes'),
    ]
    
    for key, title in sections:
        if key in template and template[key]:
            result += f"## {title}\n\n{template[key]}\n\n"
    
    return result


def find_template(items: List[Dict[str, Any]], name: str) -> Optional[Dict[str, Any]]:
    """Recursively find a template by name"""
    for item in items:
        if item.get('type') == 'file' and item.get('name') == name:
            return item
        elif 'children' in item:
            found = find_template(item['children'], name)
            if found:
                return found
    return None


@mcp.tool()
def search_templates(query: str, category: Optional[str] = None) -> str:
    """
    Searches for accessibility templates by keyword.
    
    Args:
        query: Search term (searches in template names and labels)
        category: Optional category filter (web, native, how-to-test)
    
    Returns:
        List of matching templates with their categories and names
    """
    query_lower = query.lower()
    results = []
    
    categories_to_search = [category] if category else DATA.keys()
    
    for cat in categories_to_search:
        if cat in DATA:
            matches = search_in_items(DATA[cat], query_lower, cat)
            results.extend(matches)
    
    if not results:
        return f"No templates found matching '{query}'."
    
    result = f"# Search Results for '{query}'\n\n"
    result += f"Found {len(results)} template(s):\n\n"
    
    for match in results:
        result += f"• **{match['label']}** ({match['category']}/{match['name']})\n"
        if 'path' in match:
            result += f"  Path: {match['path']}\n"
        result += "\n"
    
    return result


def search_in_items(items: List[Dict[str, Any]], query: str, category: str, path: str = "") -> List[Dict[str, Any]]:
    """Recursively search for templates"""
    results = []
    for item in items:
        current_path = f"{path}/{item['name']}" if path else item['name']
        
        if item.get('type') == 'file':
            if query in item['name'].lower() or query in item['label'].lower():
                results.append({
                    'name': item['name'],
                    'label': item['label'],
                    'category': category,
                    'path': current_path
                })
        elif 'children' in item:
            results.extend(search_in_items(item['children'], query, category, current_path))
    
    return results


@mcp.tool()
def get_category_info(category: str) -> str:
    """
    Gets information about a specific accessibility category.
    
    Args:
        category: The category name (web, native, how-to-test)
    
    Returns:
        Overview of the category and its templates
    """
    if category not in DATA:
        return f"Category '{category}' not found. Available categories: {', '.join(DATA.keys())}"
    
    items = DATA[category]
    count = count_templates(items)
    
    result = f"# {category.upper()} Accessibility Templates\n\n"
    result += f"**Total templates:** {count}\n\n"
    result += "## Structure\n\n"
    result += format_template_list(items, level=1)
    
    return result


@mcp.tool()
def get_developer_notes(category: str, template_name: str) -> str:
    """
    Gets just the developer notes section from a template.
    
    Args:
        category: The category (web, native, how-to-test)
        template_name: The name of the template
    
    Returns:
        Developer notes with code examples
    """
    items = DATA.get(category, [])
    template = find_template(items, template_name)
    
    if not template:
        return f"Template '{template_name}' not found in category '{category}'."
    
    result = f"# {template['label']} - Developer Notes\n\n"
    
    notes_sections = [
        ('developerNotes', 'Developer Notes'),
        ('androidDeveloperNotes', 'Android Developer Notes'),
        ('iosDeveloperNotes', 'iOS Developer Notes'),
    ]
    
    found_notes = False
    for key, title in notes_sections:
        if key in template and template[key]:
            result += f"## {title}\n\n{template[key]}\n\n"
            found_notes = True
    
    if not found_notes:
        result += "No developer notes available for this template.\n"
    
    return result


@mcp.tool()
def get_test_criteria(category: str, template_name: str, format: str = "condensed") -> str:
    """
    Gets testing criteria for an accessibility issue.
    
    Args:
        category: The category (web, native, how-to-test)
        template_name: The name of the template
        format: Format type - 'condensed', 'gherkin', or 'general' (default: 'condensed')
    
    Returns:
        Testing criteria in the requested format
    """
    items = DATA.get(category, [])
    template = find_template(items, template_name)
    
    if not template:
        return f"Template '{template_name}' not found in category '{category}'."
    
    result = f"# {template['label']} - Test Criteria\n\n"
    
    format_key = {
        'condensed': 'condensed',
        'gherkin': 'gherkin',
        'general': 'generalNotes'
    }.get(format, 'condensed')
    
    if format_key in template and template[format_key]:
        result += template[format_key]
    else:
        result += f"No {format} criteria available for this template.\n"
        result += "\nAvailable formats:\n"
        for key in ['condensed', 'gherkin', 'generalNotes']:
            if key in template and template[key]:
                result += f"• {key}\n"
    
    return result


@mcp.tool()
def list_categories() -> str:
    """
    Lists all available accessibility documentation categories.
    
    Returns:
        List of categories with template counts
    """
    result = "# MagentaA11y Categories\n\n"
    
    for category, items in DATA.items():
        count = count_templates(items)
        result += f"• **{category}**: {count} templates\n"
    
    result += "\nUse get_category_info(category) to see details about a specific category.\n"
    
    return result


@mcp.tool()
def get_server_info() -> str:
    """
    Returns information about this MCP server.
    
    Returns:
        Server information and data source details
    """
    total_templates = sum(count_templates(items) for items in DATA.values())
    
    return f"""**MagentaA11y MCP Server** v1.0.0

This server provides accessibility testing documentation from T-Mobile's MagentaA11y project.

**Data Source:** https://github.com/tmobile/magentaA11y
**Total Templates:** {total_templates}
**Categories:** {', '.join(DATA.keys())}

MagentaA11y is a comprehensive accessibility testing documentation resource that provides:
- Detailed testing criteria for web and native components
- Code examples and developer notes
- Gherkin-style acceptance criteria
- How-to-test guides

Use list_issue_templates() to explore available templates."""


if __name__ == "__main__":
    # Run the FastMCP server
    mcp.run()
