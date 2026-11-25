# Install Agent Skills into your AI agent

A skill is a **folder** containing `SKILL.md` (YAML frontmatter + Markdown
instructions) and optional `scripts/`, `references/` and `assets/`. The format
is shared by Claude Code, Codex, Cursor, Gemini CLI, GitHub Copilot, OpenCode,
Windsurf and many others — see the [open Agent Skills spec](https://agentskills.io).

> ⚠️ Read [SECURITY.md](../SECURITY.md) first. A skill can contain scripts and
> `allowed-tools` declarations. This catalog verifies metadata, not behavior.

## 0. Prerequisites

- Node.js **22.20+** for the [`npx skills` CLI](https://github.com/vercel-labs/skills)
- Or just `git` + `cp` for a fully manual install
- Or Python 3 for our helper: `python3 scripts/install.py search pdf`

## 1. One command (recommended)

Every skill card on the website has a copy button. The most robust form points
straight at the skill folder, which also works for nested plugin layouts:

```bash
npx skills add https://github.com/anthropics/skills/tree/main/skills/pdf
```

If the CLI can discover the repository's skills, the shorthand works too:

```bash
npx skills add anthropics/skills --skill pdf
```

Useful flags (from the [CLI reference](https://github.com/vercel-labs/skills/blob/main/docs/commands.md)):

| Flag | Meaning |
| --- | --- |
| `-g, --global` | Install for all projects instead of the current one |
| `-a, --agent <name>` | Target one agent, e.g. `-a claude-code` |
| `-s, --skill <name>` | Install a specific skill by name |
| `-l, --list` | List available skills without installing |
| `-y, --yes` | Skip prompts (CI-friendly) |
| `--copy` | Copy files instead of symlinking |
| `--rename <name>` | Resolve two skills with the same name |

```bash
# global, non-interactive, only Claude Code
npx skills add anthropics/skills --skill pdf -g -a claude-code -y

# try a skill once, without installing
npx skills use anthropics/skills@pdf

# see what a repository offers
npx skills add obra/superpowers --list
```

## 2. Where skills land

The CLI detects your installed agents. Common paths
([full table](https://github.com/vercel-labs/skills/blob/main/docs/agents.md)):

| Agent | Project path | Global path |
| --- | --- | --- |
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |
| Codex, GitHub Copilot, Gemini CLI, Cline, Pi, Zed | `.agents/skills/` | `~/.agents/skills/` |
| Cursor | `.agents/skills/` | `~/.cursor/skills/` |
| OpenCode / Amp / Replit | `.agents/skills/` | `~/.config/opencode/skills/` |
| Windsurf | `.windsurf/skills/` | `~/.codeium/windsurf/skills/` |
| OpenClaw | `skills/` | `~/.openclaw/skills/` |

`.agents/skills/` is the best vendor-neutral choice if your team uses several
agents. The CLI's symlink mode keeps one canonical copy.

## 3. Manual install (no Node.js)

```bash
git clone --depth 1 https://github.com/anthropics/skills.git /tmp/anthropics-skills
mkdir -p .agents/skills
cp -r /tmp/anthropics-skills/skills/pdf .agents/skills/pdf
```

The folder name must match the `name` field in `SKILL.md`. A common mistake is
an extra wrapper directory: `.agents/skills/repo-main/skills/pdf/SKILL.md`
will **not** be discovered. Correct: `.agents/skills/pdf/SKILL.md`.

Start a **new** agent session after installing; skills are discovered at startup.
In Claude Code, `/skills` or "What skills are available?" confirms detection.

## 4. Plugin marketplaces

Some repositories (e.g. `anthropics/claude-plugins-official`) ship Claude Code
**plugins**, not standalone skill folders. Use the plugin flow inside Claude Code:

```text
/plugin marketplace add anthropics/claude-plugins-official
/plugin install <plugin-name>@<marketplace-name>
```

The website marks these entries in their curator note. Running
`npx skills add` against a plugin-only repo may not find the skill you expect.

## 5. Starter packs

The website's **Packs** tab gives you a copyable multi-line script, e.g.:

```bash
npx skills add https://github.com/obra/superpowers/tree/main/skills/test-driven-development
npx skills add https://github.com/mattpocock/skills/tree/main/skills/engineering/code-review
npx skills add https://github.com/addyosmani/agent-skills/tree/main/skills/security-and-hardening
```

Review each command before running it. Install project-locally first, then
promote the ones you actually use to `-g`.

## 6. Troubleshooting

| Symptom | Fix |
| --- | --- |
| Skill not visible | Check `SKILL.md` sits **directly** inside the skill folder; restart the session |
| `name` mismatch | Folder name must equal the frontmatter `name` |
| CLI cannot find a nested skill | Use the full `/tree/<branch>/<path>` URL form |
| Two skills with the same name | Use `--rename` |
| Update an installed skill | Re-run `npx skills add ...`, then `npx skills check` / `update` |
| Corporate/air-gapped environment | Clone the repo manually and use the manual copy method above |

See also [docs/API.md](API.md) to query the catalog programmatically and
[`scripts/install.py`](../scripts/install.py) for a friendly local helper.
