# Security & trust model

Agent Skills are **instructions plus optional scripts** that an AI agent may
execute with your permissions. Installing one is closer to installing a package
than to copying a prompt. Treat this catalog as a map, not as a certificate.

## What we actually verify

- The repository is public on GitHub and not archived.
- A file named exactly `SKILL.md` exists at the recorded path.
- We fetched that file and parsed its YAML frontmatter (`name`, `description`,
  optional `license`, `compatibility`, `allowed-tools`).
- Repository stars, forks, last push and license identifier come from the GitHub
  API at generation time.
- We deduplicate copies of the same skill published into several agent folders.
- We flag skills that ship sibling scripts, declare `allowed-tools`, or mention
  shell/network install commands (`curl`, `wget`, `sudo`, `rm -rf`, `eval`,
  `chmod +x`, `git clone`, `pip install`, `npm install`).
- We attach bilingual `safeUse[]` notes to security-oriented skills and to
  skills whose upstream description is primarily Chinese.

## What we explicitly do **not** do

- We do not execute, sandbox or behaviorally audit upstream skills.
- We do not guarantee that a skill is free of prompt injection, data exfiltration
  or destructive commands.
- We do not guarantee that a repository's license covers every bundled file.
- We do not vendor upstream skill bodies, so we cannot diff or sign them.
- `review.requiresReview === false` means *no heuristic signal was found*, not
  *safe*. `license.status === "clear"` means *GitHub reported an OSI license*,
  not *legal advice*.

## Before installing (recommended checklist)

1. Open the source `SKILL.md` and read the whole body, not just the description.
2. List the skill folder for `scripts/`, `references/`, `assets/`, binaries and
   post-install hooks.
3. Check `allowed-tools` and any `curl | bash`, `sudo`, `rm -rf`, credential or
   dotfile access.
4. Check the upstream `LICENSE`; `NOASSERTION`, per-skill licenses and missing
   licenses are flagged in this catalog.
5. Prefer official/vendor-maintained repositories and actively maintained ones.
6. Install into one project first (`npx skills add ...` without `-g`), then
   inspect what landed in `.agents/skills/` / `.claude/skills/`.
7. Pin a commit for production if the CLI supports it (`owner/repo@<tag|sha>`).
8. For security-oriented skills, test only systems you own or are explicitly
   authorized to test. Review/translate primarily Chinese descriptions before
   using them in an English or Polish workflow.

## Reporting a problem

Open a GitHub issue with the repository, skill path and a description of the
concern. For upstream skill content, report it to the upstream maintainer too;
we can remove or annotate the catalog entry but cannot patch someone else's repo.

## Our own code

The website makes no network requests except loading its own `data/catalog.js`.
There is no analytics, no telemetry, no cookies and no backend. Saved skills and
theme/language preferences live only in your browser's `localStorage`.
