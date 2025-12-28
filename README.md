# magentaa11y-mcp

MCP server providing accessibility testing documentation from T-Mobile's [MagentaA11y project](https://github.com/tmobile/magentaA11y).

## Quick Start

1. **Fork or clone this repository**
   ```bash
   git clone https://github.com/joe-watkins/magentaa11y-fastmcp.git
   cd magentaa11y-fastmcp
   ```

2. **Deploy to FastMCP Cloud**
   - Visit [fastmcp.cloud](https://fastmcp.cloud/) and sign in with GitHub
   - Click "New Server" and select your forked/cloned repository
   - Set entrypoint to `server.py:mcp` (usually auto-detected)
   - Click "Deploy"

3. **Add to your MCP client**
   
   Copy the provided URL and add to your MCP settings:
   
   ```json
   {
     "mcpServers": {
       "magentaa11y": {
         "type": "http",
         "url": "https://your-project-name.fastmcp.app/mcp"
       }
     }
   }
   ```

**Auto-updates:** Your server automatically updates weekly with the latest MagentaA11y documentation via GitHub Actions.

## Usage

Example prompts:
- "Get me the Button component for native in Gherkin format"
- "Show me accessibility documentation for web forms"
- "What's the iOS-specific guidance for switches?"

## Links

- [MagentaA11y](https://www.magentaa11y.com/) | [GitHub](https://github.com/tmobile/magentaA11y)
- [FastMCP](https://github.com/jlowin/fastmcp) | [Cloud](https://fastmcp.cloud/)
- [Model Context Protocol](https://modelcontextprotocol.io/)