# magentaa11y-mcp

MCP server providing accessibility testing documentation from T-Mobile's [MagentaA11y project](https://github.com/tmobile/magentaA11y).

## Installation

Add to your MCP settings:

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

## Deployment

### FastMCP Cloud (Recommended)

1. Visit [fastmcp.cloud](https://fastmcp.cloud/) and sign in with GitHub
2. Click "New Server" and select this repository
3. Set entrypoint to `server.py:mcp` (usually auto-detected)
4. Click "Deploy" - your server will be live at `https://your-project-name.fastmcp.app/mcp`
5. Copy the provided config and add it to your MCP client settings

**Auto-updates:** Pushes to `main` automatically redeploy. Pull requests get preview URLs for testing.

### Local Development

```bash
pip install -r requirements.txt
fastmcp dev server.py:mcp
```

**Updating data:** The `data/content.json` file contains MagentaA11y documentation. To update it:

```bash
# Update submodule, build it, and copy content.json
git submodule update --init --remote
cd data/magentaA11y
npm ci && npm run build
cd ../..
python update_data.py
```

Or use the GitHub Actions workflow (runs weekly automatically).

## Usage

Example prompts:
- "Get me the Button component for native in Gherkin format"
- "Show me accessibility documentation for web forms"
- "What's the iOS-specific guidance for switches?"

## Links

- [MagentaA11y](https://www.magentaa11y.com/) | [GitHub](https://github.com/tmobile/magentaA11y)
- [FastMCP](https://github.com/jlowin/fastmcp) | [Cloud](https://fastmcp.cloud/)
- [Model Context Protocol](https://modelcontextprotocol.io/)