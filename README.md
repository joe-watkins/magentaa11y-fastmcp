# magentaa11y-mcp

MagentaA11y MCP Server

A Model Context Protocol (MCP) server that provides accessibility testing documentation from T-Mobile's [MagentaA11y project](https://github.com/tmobile/magentaA11y).

## About MagentaA11y

MagentaA11y is an open-source accessibility testing documentation project by T-Mobile that provides comprehensive guidance for testing web and native applications for accessibility compliance. This MCP server makes that documentation easily accessible to AI assistants.

## Installation

Add this server to your MCP settings file:

**For Claude Desktop** (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS or `%APPDATA%/Claude/claude_desktop_config.json` on Windows):

```json
{
  "mcpServers": {
    "magentaa11y": {
      "type": "http",
      "url": "https://your-deployment-url.fastmcp.app/mcp"
    }
  }
}
```

**For Cline/VS Code** (`.vscode/mcp.json` or User settings):

```json
{
  "servers": {
    "magentaa11y": {
      "type": "http",
      "url": "https://your-deployment-url.fastmcp.app/mcp"
    }
  }
}
```

## Available Tools

This MCP server provides the following tools:

- **Component listings**: Browse all available web and native components
- **Component details**: Get comprehensive accessibility testing documentation
- **Search**: Find components by name or keywords
- **Multiple formats**:
  - **Developer notes**: Code examples and implementation guidance
  - **Test criteria**: Gherkin-style acceptance criteria and condensed test instructions

The data is automatically updated weekly via GitHub Actions.

## Deployment with FastMCP Cloud

1. **Prerequisites**
   - GitHub repository (public or private)
   - FastMCP Cloud account

2. **Deploy to FastMCP Cloud**
   - Visit [fastmcp.cloud](https://fastmcp.cloud/)
   - Connect your GitHub account
   - Select this repository
   - Click "Deploy"

3. **Connect to Your Server**
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

## Contributing

This server wrapper is maintained at [joe-watkins/magentaa11y-fastmcp](https://github.com/joe-watkins/magentaa11y-fastmcp).

To contribute to the MagentaA11y documentation itself, visit the [MagentaA11y repository](https://github.com/tmobile/magentaA11y). Changes to MagentaA11y will be automatically picked up by this server through the weekly update workflow.

## License

This MCP server wrapper is provided as-is. The MagentaA11y content is subject to its own license - see the [MagentaA11y repository](https://github.com/tmobile/magentaA11y) for details.