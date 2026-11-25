# Offline shortlist

Use this only when the catalog JSON cannot be fetched. For live stars, licenses,
skill counts and exact paths, always prefer `data/catalog.json`.

## Reference / official

| Repository | Start with | Install |
| --- | --- | --- |
| `anthropics/skills` | `pdf`, `docx`, `pptx`, `xlsx`, `frontend-design`, `skill-creator` | `npx skills add anthropics/skills --skill pdf` |
| `anthropics/claude-plugins-official` | plugin marketplace, not plain skills | `/plugin marketplace add anthropics/claude-plugins-official` |
| `openai/skills` | `pdf`, `figma`, `security-threat-model`, `skill-creator` | `npx skills add openai/skills --skill skill-creator` |
| `google/skills` | `finding-google-skills`, `bigquery-basics`, `gcloud` | `npx skills add google/skills --skill finding-google-skills` |
| `googleworkspace/cli` | `gws-gmail-triage`, `gws-calendar`, `gws-docs` | `npx skills add googleworkspace/cli --skill gws-gmail-triage` |
| `github/awesome-copilot` | `code-review`, `agentic-workflows` | `npx skills add github/awesome-copilot --skill code-review` |
| `vercel-labs/agent-skills` | `react-best-practices`, `web-design-guidelines` | `npx skills add vercel-labs/agent-skills --skill react-best-practices` |
| `vercel-labs/skills` | `find-skills` (the CLI's own discovery skill) | `npx skills add vercel-labs/skills --skill find-skills` |
| `duckdb/duckdb-skills` | `query`, `read-file`, `convert-file` | `npx skills add duckdb/duckdb-skills --skill query` |
| `obsidianmd/obsidian-skills` | `obsidian-markdown`, `json-canvas` | `npx skills add obsidianmd/obsidian-skills --skill obsidian-markdown` |
| `cloudflare/security-audit-skill` | `security-audit` | `npx skills add cloudflare/security-audit-skill --skill security-audit` |
| `huggingface/skills` | `huggingface-datasets`, `huggingface-papers` | `npx skills add huggingface/skills --skill huggingface-datasets` |

## Expert collections

| Repository | Good for |
| --- | --- |
| `obra/superpowers` | TDD, systematic debugging, plans, code review, git worktrees |
| `mattpocock/skills` | diagnosing bugs, code review, domain modeling, specs, triage |
| `addyosmani/agent-skills` | production engineering: security, performance, CI/CD, review |
| `affaan-m/ECC` | very large harness-optimization library; review individual skills |
| `emilkowalski/skills` | UI animation and design craft |
| `K-Dense-AI/scientific-agent-skills` | 177+ validated science skills and databases |
| `coreyhaines31/marketingskills` | CRO, SEO, copywriting, ads, analytics |
| `phuryn/pm-skills` | PRDs, OKRs, experiments, roadmaps, product strategy |
| `trailofbits/skills` | professional security audit and vulnerability research |
| `OpenZeppelin/openzeppelin-skills` | secure smart-contract development |
| `ComposioHQ/awesome-claude-skills` | huge community catalog; verify individually |
| `sickn33/agentic-awesome-skills` | thousands of skills + catalog CLI; uneven quality |

## Starter bundles (conceptual)

- **Coding baseline**: `obra/superpowers` + `mattpocock/skills` + `addyosmani/agent-skills` + `cloudflare/security-audit-skill`
- **Frontend**: `anthropics/skills@frontend-design` + `vercel-labs/agent-skills@react-best-practices` + `emilkowalski/skills@animate` + `Nutlope/hallmark@hallmark`
- **Documents**: `anthropics/skills` (`pdf`, `docx`, `pptx`, `xlsx`) + `obsidianmd/obsidian-skills`
- **Security**: `cloudflare/security-audit-skill` + `trailofbits/skills` + `OpenZeppelin/openzeppelin-skills`
- **Data**: `K-Dense-AI/scientific-agent-skills` + `duckdb/duckdb-skills` + `firecrawl/skills`

For exact, copyable commands query the catalog's `packs[].script`.
