# AI Integration via MCP

Connect FastKB to any MCP-compatible AI assistant (Claude Desktop, Cursor, Cline, Continue, etc.). Your local files become instantly searchable context for AI, **without sending data to external servers**.

## Quick Setup

```bash
pip install fastkb
```

## Client Configuration

FastKB runs as a local stdio server. Add this to your AI client's MCP config:

**Claude Desktop** (`~/Library/Application Support/Claude/claude_desktop_config.json` or `%APPDATA%\Claude\claude_desktop_config.json`):

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

**Cursor / VS Code (Continue, Cline, Roo Code)**:
Add to your MCP settings (`Settings > MCP > Add Server`):

- **Name**: `fastkb`
- **Type**: `stdio`
- **Command**: `python3 -m fastkb.mcp_server`
- **Env**: `FASTKB_DB_PATH=/absolute/path/to/fastkb.db`

> **Always use absolute paths for `command` and `env`.** AI clients run in isolated workspaces where relative paths resolve incorrectly.

### Exposed Tool Specification

FastKB exposes a single typed tool to the AI:

| Tool     | Signature                | Description                                     |
| -------- | ------------------------ | ----------------------------------------------- |
| `search` | `search(query, limit=5)` | Runs FTS5 search and returns structured results |

**Response format:**

```json
[
  {
    "path": "/absolute/path/to/file.py",
    "matching_lines": [12, 45, 89],
    "preview": "def handle_timeout(request): ..."
  }
]
```

### Example AI Prompts

Once connected, use natural language in your AI chat:

- `"Find where I handle JWT expiration in my codebase."`
- `"Search my notes for the OAuth callback setup steps."`
- `"Show me all config files that reference 'timeout' > 30."`

The AI will automatically call `fastkb.search()`, read the returned lines, and answer with precise file references.

### Security & Privacy

- **100% Local**: All indexing and search happens on your machine.
- **No Cloud Calls**: MCP communicates via `stdio` between your AI client and FastKB.
- **Zero Telemetry**: FastKB does not phone home, log queries, or store AI prompts.
- **Sandbox-Friendly**: Safe to run in CI, dev containers, or restricted environments.
