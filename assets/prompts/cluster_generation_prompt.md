# Topic Cluster Generation Prompt

<!-- Reusable prompt for generating topic cluster structures -->

## Instructions

Given:
1. **Core topic / pillar keyword**
2. **Seed keywords list** (from keyword research)
3. **Existing content URLs** (if any)

Generate:

1. **Pillar page**: Define the broad topic, target keyword, and content structure
2. **Cluster pages**: Group related keywords into individual page topics
   - Each cluster page targets a specific long-tail keyword
   - Each links back to the pillar and to 2-3 related clusters
3. **Internal linking map**: Which pages link to which, with suggested anchor text
4. **Content gaps**: Cluster topics not yet covered by existing content
5. **Priority order**: Which cluster pages to create first (based on traffic potential + difficulty)

Output a structured map with keyword assignments, URL suggestions, and linking instructions.
