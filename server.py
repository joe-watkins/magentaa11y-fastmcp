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
def list_web_components() -> str:
    """
    Lists all available web accessibility components from MagentaA11y.
    
    Returns:
        Formatted list of all web components organized by type
    """
    items = DATA.get('web', [])
    count = count_templates(items)
    
    result = "# Web Accessibility Components\n\n"
    result += f"**Total components:** {count}\n\n"
    result += format_template_list(items, level=1)
    
    return result


@mcp.tool()
def get_web_component(component_name: str) -> str:
    """
    Gets detailed accessibility criteria for a web component.
    
    Args:
        component_name: Name of the component (e.g., 'button', 'modal-dialog', 'form')
    
    Returns:
        Complete component documentation including all available sections
    """
    items = DATA.get('web', [])
    template = find_template(items, component_name)
    
    if not template:
        return f"Web component '{component_name}' not found.\n\nUse list_web_components() to see available components."
    
    return format_component_details(template, 'web', component_name)


@mcp.tool()
def search_web_criteria(query: str) -> str:
    """
    Searches for web accessibility criteria by keyword.
    
    Args:
        query: Search term (searches in component names and labels)
    
    Returns:
        List of matching web components
    """
    items = DATA.get('web', [])
    matches = search_in_items(items, query.lower(), 'web')
    
    if not matches:
        return f"No web components found matching '{query}'."
    
    result = f"# Web Components matching '{query}'\n\n"
    result += f"Found {len(matches)} component(s):\n\n"
    
    for match in matches:
        result += f"• **{match['label']}** (`{match['name']}`)\n"
        if 'path' in match:
            result += f"  Path: {match['path']}\n"
        result += "\n"
    
    return result


@mcp.tool()
def list_native_components() -> str:
    """
    Lists all available native (iOS/Android) accessibility components.
    
    Returns:
        Formatted list of all native components organized by type
    """
    items = DATA.get('native', [])
    count = count_templates(items)
    
    result = "# Native Accessibility Components\n\n"
    result += f"**Total components:** {count}\n\n"
    result += format_template_list(items, level=1)
    
    return result


@mcp.tool()
def get_native_component(component_name: str) -> str:
    """
    Gets detailed accessibility criteria for a native iOS/Android component.
    
    Args:
        component_name: Name of the component (e.g., 'button', 'switch', 'picker')
    
    Returns:
        Complete component documentation including all available sections
    """
    items = DATA.get('native', [])
    template = find_template(items, component_name)
    
    if not template:
        return f"Native component '{component_name}' not found.\n\nUse list_native_components() to see available components."
    
    return format_component_details(template, 'native', component_name)


@mcp.tool()
def search_native_criteria(query: str) -> str:
    """
    Searches for native accessibility criteria by keyword.
    
    Args:
        query: Search term (searches in component names and labels)
    
    Returns:
        List of matching native components
    """
    items = DATA.get('native', [])
    matches = search_in_items(items, query.lower(), 'native')
    
    if not matches:
        return f"No native components found matching '{query}'."
    
    result = f"# Native Components matching '{query}'\n\n"
    result += f"Found {len(matches)} component(s):\n\n"
    
    for match in matches:
        result += f"• **{match['label']}** (`{match['name']}`)\n"
        if 'path' in match:
            result += f"  Path: {match['path']}\n"
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
def get_component_gherkin(category: str, component_name: str) -> str:
    """
    Gets Gherkin-style acceptance criteria for a component.
    
    Args:
        category: Component category ('web' or 'native')
        component_name: Name of the component
    
    Returns:
        Gherkin-style acceptance criteria formatted for BDD testing
    """
    items = DATA.get(category, [])
    template = find_template(items, component_name)
    
    if not template:
        return f"Component '{component_name}' not found in {category} category."
    
    result = f"# {template['label']} - Gherkin Acceptance Criteria\n\n"
    
    if 'gherkin' in template and template['gherkin']:
        result += template['gherkin']
    else:
        result += "No Gherkin criteria available for this component.\n"
        result += f"\nUse list_component_formats('{category}', '{component_name}') to see available formats."
    
    return result


@mcp.tool()
def get_component_condensed(category: str, component_name: str) -> str:
    """
    Gets condensed acceptance criteria for quick reference.
    
    Args:
        category: Component category ('web' or 'native')
        component_name: Name of the component
    
    Returns:
        Condensed acceptance criteria for quick testing reference
    """
    items = DATA.get(category, [])
    template = find_template(items, component_name)
    
    if not template:
        return f"Component '{component_name}' not found in {category} category."
    
    result = f"# {template['label']} - Condensed Criteria\n\n"
    
    if 'condensed' in template and template['condensed']:
        result += template['condensed']
    else:
        result += "No condensed criteria available for this component.\n"
        result += f"\nUse list_component_formats('{category}', '{component_name}') to see available formats."
    
    return result


@mcp.tool()
def get_component_developer_notes(category: str, component_name: str) -> str:
    """
    Gets developer implementation notes with code examples.
    
    Args:
        category: Component category ('web' or 'native')
        component_name: Name of the component
    
    Returns:
        Developer notes including code examples and implementation guidance
    """
    items = DATA.get(category, [])
    template = find_template(items, component_name)
    
    if not template:
        return f"Component '{component_name}' not found in {category} category."
    
    result = f"# {template['label']} - Developer Notes\n\n"
    
    if 'developerNotes' in template and template['developerNotes']:
        result += template['developerNotes']
    else:
        result += "No developer notes available for this component.\n"
        result += f"\nUse list_component_formats('{category}', '{component_name}') to see available formats."
    
    return result


@mcp.tool()
def get_component_native_notes(category: str, component_name: str, platform: str) -> str:
    """
    Gets platform-specific implementation notes for native components.
    
    Args:
        category: Component category (usually 'native')
        component_name: Name of the component
        platform: Platform ('ios' or 'android')
    
    Returns:
        Platform-specific developer notes and implementation guidance
    """
    items = DATA.get(category, [])
    template = find_template(items, component_name)
    
    if not template:
        return f"Component '{component_name}' not found in {category} category."
    
    result = f"# {template['label']} - {platform.upper()} Notes\n\n"
    
    key = 'iosDeveloperNotes' if platform.lower() == 'ios' else 'androidDeveloperNotes'
    
    if key in template and template[key]:
        result += template[key]
    else:
        result += f"No {platform.upper()} specific notes available for this component.\n"
        result += f"\nUse list_component_formats('{category}', '{component_name}') to see available formats."
    
    return result


@mcp.tool()
def list_component_formats(category: str, component_name: str) -> str:
    """
    Lists all available documentation formats for a specific component.
    
    Args:
        category: Component category ('web' or 'native')
        component_name: Name of the component
    
    Returns:
        List of available documentation sections for the component
    """
    items = DATA.get(category, [])
    template = find_template(items, component_name)
    
    if not template:
        return f"Component '{component_name}' not found in {category} category."
    
    result = f"# {template['label']} - Available Formats\n\n"
    result += f"**Category:** {category}\n"
    result += f"**Component:** {component_name}\n\n"
    
    sections = [
        ('generalNotes', 'General Notes'),
        ('gherkin', 'Gherkin Acceptance Criteria'),
        ('condensed', 'Condensed Criteria'),
        ('criteria', 'Detailed Criteria'),
        ('videos', 'Video Examples'),
        ('developerNotes', 'Developer Notes'),
        ('androidDeveloperNotes', 'Android Developer Notes'),
        ('iosDeveloperNotes', 'iOS Developer Notes'),
    ]
    
    available = []
    for key, title in sections:
        if key in template and template[key]:
            available.append(f"• **{title}** (`{key}`)")
    
    if available:
        result += "## Available Sections\n\n"
        result += "\n".join(available)
    else:
        result += "No documentation sections available for this component."
    
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


def format_component_details(template: Dict[str, Any], category: str, name: str) -> str:
    """Format complete component details"""
    result = f"# {template['label']}\n\n"
    result += f"**Category:** {category}\n"
    result += f"**Component:** {name}\n\n"
    
    sections = [
        ('generalNotes', 'General Notes'),
        ('gherkin', 'Gherkin Acceptance Criteria'),
        ('condensed', 'Condensed Criteria'),
        ('criteria', 'Detailed Criteria'),
        ('videos', 'Video Examples'),
        ('developerNotes', 'Developer Notes'),
        ('androidDeveloperNotes', 'Android Developer Notes'),
        ('iosDeveloperNotes', 'iOS Developer Notes'),
    ]
    
    for key, title in sections:
        if key in template and template[key]:
            result += f"## {title}\n\n{template[key]}\n\n"
    
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
def get_server_info() -> str:
    """
    Returns information about this MCP server.
    
    Returns:
        Server information and data source details
    """
    web_count = count_templates(DATA.get('web', []))
    native_count = count_templates(DATA.get('native', []))
    total_templates = web_count + native_count
    
    return f"""**MagentaA11y MCP Server** v1.0.0

This server provides accessibility testing documentation from T-Mobile's MagentaA11y project.

**Data Source:** https://github.com/tmobile/magentaA11y
**Total Components:** {total_templates}
  - Web: {web_count}
  - Native: {native_count}

MagentaA11y is a comprehensive accessibility testing documentation resource that provides:
- Detailed testing criteria for web and native components
- Code examples and developer notes
- Gherkin-style acceptance criteria
- Platform-specific implementation guidance

Available Tools:
- list_web_components() - List all web components
- get_web_component(name) - Get detailed web component criteria
- search_web_criteria(query) - Search web components
- list_native_components() - List all native components
- get_native_component(name) - Get detailed native component criteria
- search_native_criteria(query) - Search native components
- get_component_gherkin(category, name) - Get Gherkin criteria
- get_component_condensed(category, name) - Get condensed criteria
- get_component_developer_notes(category, name) - Get code examples
- get_component_native_notes(category, name, platform) - Get iOS/Android notes
- list_component_formats(category, name) - See available formats"""


if __name__ == "__main__":
    # Run the FastMCP server
    mcp.run()
