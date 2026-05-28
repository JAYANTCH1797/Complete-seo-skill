"""Semrush API wrapper for SEO Suite.

This script wraps Semrush MCP tools for use from the command line.
In practice, the Semrush MCP tools are called directly by Claude Code.
This file serves as documentation of available endpoints and as a
fallback for direct API calls if needed.

Available Semrush MCP tools:
- keyword_research: search volume, difficulty, intent, related keywords
- organic_research: domain's organic keyword rankings and traffic
- backlink_research: backlink profile, referring domains, anchor text
- overview_research: domain overview (traffic, keywords, authority)
- url_research: single URL metrics
- siteaudit_research: site-wide technical audit data
- tracking_research: rank tracking data
- trends_research: keyword trend data
- subdomain_research: subdomain analysis
- subfolder_research: subfolder analysis
"""

# TODO: Implement direct Semrush API calls as fallback when MCP is unavailable.
# For now, all Semrush data access goes through the MCP tools.
