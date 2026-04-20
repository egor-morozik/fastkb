# Client Configuration

FastKB runs as a local `stdio` server. Add this configuration to your AI client:

## Claude Desktop

Edit `claude_desktop_config.json` (`~/Library/Application Support/Claude/` on macOS, `%APPDATA%\Claude\` on Windows):

```json
{
  "mcpServers": {
    "fastkb": {
      "command": "python3",
      "args": ["-m", "fastkb.mcp_server"],
      "env": {
        "FASTKB_DB_PATH": "/absolute/path/to/your/fastkb.db"
      }
    }
  }
}
```

## Cursor / VS Code (Continue, Cline, Roo Code)

In your MCP settings (`Settings > MCP > Add Server`):

- **Name**: `fastkb`
- **Type**: `stdio`
- **Command**: `python3 -m fastkb.mcp_server`
- **Env**: `FASTKB_DB_PATH=/absolute/path/to/fastkb.db`

> **Always use absolute paths.** AI clients run in isolated workspaces where relative paths resolve incorrectly.

## Tool Specification

FastKB exposes a single typed tool to the AI:

| Tool     | Signature                | Description                                     |
| -------- | ------------------------ | ----------------------------------------------- |
| `search` | `search(query, limit=5)` | Runs FTS5 search and returns structured results |

**Response Format:**

```json
[
  {
    "path": "/absolute/path/to/file.py",
    "matching_lines": [12, 45, 89],
    "preview": "def handle_timeout(request): ..."
  }
]
```
