# WordPress.com MCP Reference

## Canonical Links

- WordPress.com connector announcement (Feb 5, 2026):
  - https://wordpress.com/blog/2026/02/05/claude-connector/
- WordPress.com MCP docs:
  - https://developer.wordpress.com/docs/mcp/
- Connect your MCP client:
  - https://developer.wordpress.com/docs/mcp/connect-your-mcp-client/

## Core Endpoints

- OAuth dynamic client registration:
  - `https://public-api.wordpress.com/oauth2-1/register`
- OAuth authorization endpoint:
  - `https://public-api.wordpress.com/oauth2-1/authorize`
- OAuth token endpoint:
  - `https://public-api.wordpress.com/oauth2-1/token`
- MCP endpoint (JSON-RPC style request body):
  - `POST https://public-api.wordpress.com/wpcom/v2/mcp/v1`

## REST Write Endpoints (Post Publishing)

- Create post:
  - `POST https://public-api.wordpress.com/rest/v1.1/sites/{site}/posts/new`
- Update post:
  - `POST https://public-api.wordpress.com/rest/v1.1/sites/{site}/posts/{post_id}`

## Auth/Protocol Notes

- Use OAuth 2.1 Authorization Code with PKCE (`code_challenge_method=S256`).
- Include `Authorization: Bearer <access_token>` for MCP calls.
- Use explicit API versions in request paths and avoid relying on defaults.

## Product Notes

- MCP support is available on paid WordPress.com plans.
- The WordPress.com connector post describes read-only access when connected in Claude.

## Sanity-check prompts

- `List my WordPress.com sites and IDs.`
- `Show the 5 most recent posts for <site>.`
- `List recent media uploads for <site>.`
