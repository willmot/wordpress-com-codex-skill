# WordPress.com MCP Skill

Connect Codex (and other MCP-capable clients) to WordPress.com using OAuth 2.1 + PKCE, then run site/content/account workflows through the official WordPress.com MCP server.

## What This Skill Covers

- Connect WordPress.com through MCP in Codex-compatible clients.
- Verify access with site and post discovery checks.
- Troubleshoot common OAuth and MCP session issues.
- Publish posts via WordPress.com REST API when MCP tools are read-only.

## Files

- `SKILL.md`: Main workflow and operational guidance.
- `references/endpoints.md`: Canonical MCP/OAuth/REST endpoints.
- `agents/openai.yaml`: Agent metadata and default prompt.
- `scripts/publish_post.py`: REST API fallback script for post publishing.

## Quick Start

1. Read `SKILL.md`.
2. Complete OAuth 2.1 + PKCE with the endpoints in `references/endpoints.md`.
3. Verify tools with:
   - `wpcom-mcp-user-sites`
   - `wpcom-mcp-posts-search`
4. If write tools are unavailable in MCP, use:
   - `scripts/publish_post.py`

## REST Publish Example

```bash
WPCOM_ACCESS_TOKEN='<token>' \
python3 scripts/publish_post.py \
  --site tomwillmot.com \
  --title "Hello from Codex" \
  --content "<p>Published via REST API fallback.</p>" \
  --status publish
```

## License

MIT
