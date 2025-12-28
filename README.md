# magentaa11y-mcp

MagentaA11y MCP Server

A Model Context Protocol (MCP) server built with FastMCP 2.0 that provides accessibility testing documentation from T-Mobile's [MagentaA11y project](https://github.com/tmobile/magentaA11y).

## About MagentaA11y

MagentaA11y is an open-source accessibility testing documentation project by T-Mobile that provides comprehensive guidance for testing web and native applications for accessibility compliance. This MCP server makes that documentation easily accessible to AI assistants.

## Available Tools

This server includes the following tools:

| Tool | Description |
|------|-------------|
| `list_web_components` | Lists all available web accessibility components |
| `get_web_component` | Gets detailed accessibility criteria for a web component |
| `search_web_criteria` | Searches for web accessibility criteria by keyword |
| `list_native_components` | Lists all available native (iOS/Android) accessibility components |
| `get_native_component` | Gets detailed accessibility criteria for a native component |
| `search_native_criteria` | Searches for native accessibility criteria by keyword |
| `get_component_gherkin` | Gets Gherkin-style acceptance criteria for a component |
| `get_component_condensed` | Gets condensed acceptance criteria for quick reference |
| `get_component_developer_notes` | Gets developer implementation notes with code examples |
| `get_component_native_notes` | Gets platform-specific (iOS/Android) implementation notes |
| `list_component_formats` | Lists all available documentation formats for a component |
| `get_server_info` | Returns information about this MCP server |

## Data Source

This server uses data from the [MagentaA11y GitHub repository](https://github.com/tmobile/magentaA11y), which is included as a git submodule. The content includes:

- **Web accessibility patterns**: Buttons, forms, navigation, modals, etc.
- **Native mobile patterns**: iOS and Android accessibility patterns
- **How-to-test guides**: Step-by-step testing instructions
- **Developer notes**: Code examples and implementation guidance
- **Test criteria**: Gherkin-style acceptance criteria and condensed test instructions

### Automatic Updates

A GitHub Actions workflow automatically:
- Updates the MagentaA11y submodule weekly (every Sunday at 2 AM UTC)
- Rebuilds the content data from the latest documentation
- Commits and pushes the updates

You can also manually trigger updates from the GitHub Actions tab.

## Project Structure

- `server.py` - Main FastMCP server with accessibility tool definitions
- `requirements.txt` - Python dependencies
- `data/magentaA11y/` - Git submodule containing the MagentaA11y repository
  - `src/shared/content.json` - Generated content (used directly by the server)
- `.github/workflows/update-submodule.yml` - Weekly automated update workflow

## Local Development

### Prerequisites
- Python 3.8 or higher
- Node.js 18+ and npm (for building MagentaA11y content)
- Git

### Installation

1. Clone the repository with submodules:
```bash
git clone --recurse-submodules <your-repo-url>
cd magentaa11y-mcp

# Or if already cloned without submodules:
git submodule update --init --recursive
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Build the content data from MagentaA11y:
```bash
cd data/magentaA11y
npm install
npm run build
cd ../..
```

The server will use the generated `content.json` directly from the submodule at `data/magentaA11y/src/shared/content.json`.

### Running Locally

Start the FastMCP server:
```bash
python server.py
```

Or use the FastMCP CLI:
```bash
fastmcp run server.py:mcp
```

### Configure Claude Desktop (Local)

Add this to your Claude Desktop MCP settings:

```json
{
  "mcpServers": {
    "magentaa11y": {
      "command": "python",
      "args": ["c:/sites/mcp-test-with-fastmcp/server.py"]
    }
  }
}
```

Or if using the virtual environment:

```json
{
  "mcpServers": {
    "magentaa11y": {
      "command": "c:/sites/mcp-test-with-fastmcp/venv/Scripts/python.exe",
      "args": ["c:/sites/mcp-test-with-fastmcp/server.py"]
    }
  }
}
```

## Updating MagentaA11y Content

### Automatic Updates (Recommended)

The GitHub Actions workflow automatically updates the content weekly. You can also manually trigger it:

1. Go to your repository's Actions tab on GitHub
2. Select the "Update MagentaA11y Submodule" workflow
3. Click "Run workflow"

### Manual Updates

To manually update the MagentaA11y content:

```bash
# Update the submodule
git submodule update --remote --merge data/magentaA11y

# Rebuild the content
cd data/magentaA11y
npm install
npm run build
cd ../..

# Commit the changes (the submodule tracks the content.json file)
git add data/magentaA11y
git commit -m "chore: update MagentaA11y submodule"
git push
```

## Deployment to FastMCP Cloud

### Quick Start

1. **Visit FastMCP Cloud**
   - Navigate to [fastmcp.cloud](https://fastmcp.cloud/)
   - Sign in with your GitHub account

2. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/magentaa11y-mcp.git
   git push -u origin main
   ```

3. **Create a Project**
   - Click "Create a Project" in FastMCP Cloud
   - Choose your GitHub repository
   - Configure:
     - **Name**: `magentaa11y-mcp` (or your preferred name)
     - **Entrypoint**: `server.py:mcp`
     - **Authentication**: Choose public or private access
   - Click "Deploy"

4. **Connect to Your Server**
   Once deployed, your server is available at:
   ```
   https://your-project-name.fastmcp.app/mcp
   ```

   FastMCP Cloud provides instant connection configs for:
   - **Claude Desktop** - Copy/paste JSON config
   - **Cursor** - Connection settings
   - **Any MCP Client** - Use the provided URL

### Auto-Updates
- FastMCP Cloud monitors your `main` branch
- Automatic redeployment on every push
- PR builds get unique URLs for testing before production
- The weekly GitHub Action will automatically update your deployed server

### Pre-Deployment Checklist
- [x] Repository is on GitHub (public or private)
- [x] `server.py` contains FastMCP instance (`mcp = FastMCP(...)`)
- [x] `requirements.txt` includes `fastmcp>=2.0.0`
- [x] Data files are in the repository
- [x] Server uses relative paths (`Path(__file__).parent`)
- [x] All tools have docstrings and type hints
- [x] Server runs locally without errors
- [x] Submodule data is committed

### Verify Before Deployment
```bash
fastmcp inspect server.py:mcp
```

## Example Usage

Here are some example queries you can use with this MCP server:

```
# List all web components
list_web_components()

# Get detailed information about button accessibility
get_web_component("button")

# Search for form-related web components
search_web_criteria("form")

# List all native components
list_native_components()

# Get native switch component details
get_native_component("switch")

# Get Gherkin criteria for a web modal
get_component_gherkin("web", "modal-dialog")

# Get condensed test criteria for a button
get_component_condensed("web", "button")

# Get developer notes with code examples for forms
get_component_developer_notes("web", "form")

# Get iOS-specific implementation notes
get_component_native_notes("native", "button", "ios")

# See what formats are available for a component
list_component_formats("web", "navigation")
```

## Contributing to MagentaA11y

This server uses data from the [MagentaA11y project](https://github.com/tmobile/magentaA11y). If you find issues or want to contribute to the accessibility documentation:

1. Visit the [MagentaA11y repository](https://github.com/tmobile/magentaA11y)
2. Review their contributing guidelines
3. Submit issues or pull requests to improve the documentation

Changes to MagentaA11y will be automatically picked up by this server through the weekly update workflow.

## Learn More

- [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [FastMCP Cloud](https://fastmcp.cloud/)
- [MagentaA11y Project](https://www.magentaa11y.com/)
- [MagentaA11y GitHub](https://github.com/tmobile/magentaA11y)
- [Web Content Accessibility Guidelines (WCAG)](https://www.w3.org/WAI/WCAG22/quickref/)

## License

This MCP server wrapper is provided as-is. The MagentaA11y content is subject to its own license - see the [MagentaA11y repository](https://github.com/tmobile/magentaA11y) for details.
