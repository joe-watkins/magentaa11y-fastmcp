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

Deploy to [FastMCP Cloud](https://fastmcp.cloud/) or run locally:

```bash
pip install -r requirements.txt
fastmcp dev server.py
```

## Usage

Example prompts:
- "Get me the Button component for native in Gherkin format"
- "Show me accessibility documentation for web forms"
- "What's the iOS-specific guidance for switches?"

## Links

- [MagentaA11y](https://www.magentaa11y.com/) | [GitHub](https://github.com/tmobile/magentaA11y)
- [FastMCP](https://github.com/jlowin/fastmcp) | [Cloud](https://fastmcp.cloud/)
- [Model Context Protocol](https://modelcontextprotocol.io/)