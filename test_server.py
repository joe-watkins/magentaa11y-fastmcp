"""
Test script for magentaa11y-mcp FastMCP server

This script validates that the data is loaded correctly.
"""

import json
from pathlib import Path

# Load data to test against
DATA_PATH = Path(__file__).parent / "data" / "magentaA11y" / "src" / "shared" / "content.json"

def test_data_file_exists():
    """Test that data file exists"""
    assert DATA_PATH.exists(), f"Data file not found at {DATA_PATH}"
    print("✓ Data file exists")


def test_data_structure():
    """Test data structure"""
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    assert isinstance(data, dict), "Data should be a dictionary"
    assert len(data) > 0, "Data should not be empty"
    
    print(f"✓ Data loaded successfully with {len(data)} categories")


def test_categories():
    """Test categories exist"""
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    expected_categories = ['web', 'native', 'how-to-test']
    for category in expected_categories:
        assert category in data, f"Expected category '{category}' in data"
    
    print(f"✓ All expected categories found: {', '.join(expected_categories)}")


def test_templates_structure():
    """Test that templates have expected structure"""
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Count templates
    def count_files(items):
        count = 0
        for item in items:
            if item.get('type') == 'file':
                count += 1
            elif 'children' in item:
                count += count_files(item['children'])
        return count
    
    total = sum(count_files(items) for items in data.values())
    assert total > 0, "Should have at least one template"
    
    print(f"✓ Found {total} templates across all categories")


def test_server_import():
    """Test that server can be imported"""
    try:
        import server
        assert hasattr(server, 'mcp'), "Server should have mcp instance"
        assert hasattr(server, 'DATA'), "Server should have DATA loaded"
        print("✓ Server module imported successfully")
    except Exception as e:
        raise AssertionError(f"Failed to import server: {e}")


if __name__ == "__main__":
    print("Testing magentaa11y-mcp server...\n")
    
    try:
        test_data_file_exists()
        test_data_structure()
        test_categories()
        test_templates_structure()
        test_server_import()
        
        print("\n✅ All tests passed!")
        print("\nTo test the server with an MCP client:")
        print("  python server.py")
        print("\nOr use FastMCP CLI:")
        print("  fastmcp run server.py:mcp")
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        exit(1)
