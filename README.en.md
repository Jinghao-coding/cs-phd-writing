# CS PhD Writing

[简体中文](README.md) | English

An agent skill for writing and reviewing Chinese doctoral dissertations in computer science, designed for Codex and Claude Code. It helps organize English research papers into a Chinese dissertation and improve technical prose while preserving the research meaning and evidence.

[Download a release](https://github.com/Jinghao-coding/cs-phd-writing/releases/latest) · [Changelog](CHANGELOG.md) · [Detailed installation guide, in Chinese](references/install-and-update.md)

The skill provides instructions and reference guides. Reading PDFs, editing Word documents, compiling LaTeX, and searching literature require tools in your agent environment. The operational guides remain in Chinese; this English README provides installation and usage guidance. Installing the upstream skills separately is unnecessary.

## What it does

| Task | Focus |
| --- | --- |
| Organize research contributions | Research questions, chapter roles, and conference/extended-version relationships without inventing dependencies |
| Rewrite and polish Chinese prose | Grammar, references, condition scope, terminology, and paragraph flow while preserving formulas and facts |
| Explain systems mechanisms | Actual entities, states, events, interfaces, and evidence rather than generic substitutions |
| Restructure chapters and surveys | Titles that match content, concepts introduced before their use, and comparisons around shared problems |
| Expand research chapters | Supported definitions, design rationale, derivations, examples, and evaluation analysis without invented results |
| Review manuscripts and figures | Consistency, citation support, figure purpose, readability, and project-specific source-format requirements |
| Verify and adapt references | University rules, authentic metadata, author order, stable citation keys, and software/web citations |
| Maintain writing context and explain agent systems | Current decisions, evidence provenance, execution objects, memory, and resource semantics |
| Configure a thesis project | Separate university rules, reference-thesis observations, and personal preferences |

Inputs can be pasted text, PDF, DOCX, or single-file and multi-file LaTeX projects. See [input reading](references/input-reading.md) for scope and tool requirements.

## Recent changes

Version 0.5.0 adds [writing context](references/writing-context.md), [agent systems prose](references/agent-systems-expression.md), and [bibliography validation](references/bibliography-validation.md). Imported BibTeX is checked against source metadata and the university’s existing bibliography setup; full authorship is preserved separately from display formatting. These are agent workflows, not an installed automatic verification service.

The v0.4 series adds stronger Chinese-language checks, chapter restructuring, and context-sensitive systems writing. The [systems prose guide](references/systems-context-expression.md) analyzes selected passages from six papers and provides independently written examples. It distinguishes concepts such as freeing device memory versus deleting cached state, submission versus completion, and atomicity versus exactly-once behavior. Version 0.4.2 adds bilingual READMEs and refreshed installation guidance; see the [changelog](CHANGELOG.md).

## Installation

Choose one installation method to avoid duplicate copies for the same agent.

### skills CLI

Requires Node.js and npm. Run the command for your agent:

```bash
# Codex: user-wide installation
npx skills@latest add Jinghao-coding/cs-phd-writing --skill cs-phd-writing --agent codex --global

# Claude Code: user-wide installation
npx skills@latest add Jinghao-coding/cs-phd-writing --skill cs-phd-writing --agent claude-code --global
```

Use `--agent codex claude-code` for both agents. Omit `--global` while in your thesis project for a project installation. Use `--copy` for independent copies. Repository installation may include changes on the default branch that are not yet packaged in a release; use a release ZIP to pin a version. See the [skills CLI documentation](https://github.com/vercel-labs/skills).

### Release ZIP

1. Open [Releases](https://github.com/Jinghao-coding/cs-phd-writing/releases) and download `cs-phd-writing-vX.Y.Z.zip` for the desired version.
2. Extract the complete `cs-phd-writing/` folder into one of the locations below. `SKILL.md` must be directly inside that folder, without an extra nesting level.
3. Keep all supporting files, including `references/`, `assets/`, `agents/`, and licenses. `SHA256SUMS.txt` checks the ZIP and manifest; `file-manifest.json` lists hashes of files inside the package.

| Agent | User-wide location | Project location |
| --- | --- | --- |
| Codex | `~/.agents/skills/cs-phd-writing/` | `<project>/.agents/skills/cs-phd-writing/` |
| Claude Code | `~/.claude/skills/cs-phd-writing/` | `<project>/.claude/skills/cs-phd-writing/` |

Locations were checked on 2026-10-04 against the official [Codex](https://developers.openai.com/codex/skills/) and [Claude Code](https://code.claude.com/docs/en/skills) documentation. For an existing client-managed installation, check its actual location before moving it or adding another copy. On Windows, replace `~` with your user directory; the shell examples below target macOS/Linux.

### Git clone

These examples require that the destination directory does not already exist:

```bash
# Codex
mkdir -p "$HOME/.agents/skills"
git clone https://github.com/Jinghao-coding/cs-phd-writing.git "$HOME/.agents/skills/cs-phd-writing"

# Claude Code
mkdir -p "$HOME/.claude/skills"
git clone https://github.com/Jinghao-coding/cs-phd-writing.git "$HOME/.claude/skills/cs-phd-writing"
```

A clone follows the default branch. See [installation and updates](references/install-and-update.md) for more details.

## Usage

Start a task in your thesis project and specify the scope. Invoke `$cs-phd-writing` in Codex or `/cs-phd-writing` in Claude Code.

**Polish prose in context:**

```text
Use $cs-phd-writing to polish the method explanation in the current chapter.
Read adjacent paragraphs, symbol definitions, and the relevant algorithm first.
Check entities, states, actions, and conditions. Return usable Chinese replacement text.
Explain substantive technical corrections separately; do not invent mechanisms.
```

**Review without editing:**

```text
Use $cs-phd-writing to review Chapter 3 without modifying files.
Identify factual, logical, and language issues with source locations.
Distinguish definite errors from optional style changes.
```

**Organize English papers into a dissertation:**

```text
Use $cs-phd-writing to propose a Chinese dissertation structure from the indexed papers.
Distinguish conference papers from extended versions. Explain each chapter's question,
evidence, and relationship to the others. Do not draft the manuscript yet.
```

In Claude Code, replace the invocation prefix with `/cs-phd-writing`. Discussion, review, and manuscript editing have different scopes; invoking the skill does not authorize a full rewrite.

## Connect your thesis project

Keep university requirements, private materials, and preferences in the thesis project. Read existing `AGENTS.md`, `CLAUDE.md`, and project configuration first; do not overwrite them with blank templates.

```text
Use $cs-phd-writing to organize this project's university requirements,
reference theses, and writing preferences. Create or update
docs/thesis-writing-profile.md while preserving confirmed information and material paths.
Record the sources of official rules, reference observations, and personal decisions.
Do not edit the manuscript in this task.
```

Choose only the files you need from the [project templates](assets/project-template/):

| File | Purpose |
| --- | --- |
| `docs/thesis-writing-profile.md` | Entry file, confirmed information, material pointers, preferences, and chapter constraints |
| `docs/university-writing-spec.md` | Official sources, versions, and rule locations |
| `docs/reference-thesis-notes.md` | Observed writing practices and how they apply to this project |
| `docs/paper-to-thesis-map.md` | Paper versions, questions, evidence, and chapter mapping |

Merge the applicable [project instructions snippet](assets/project-template/project-instructions.snippet.md) into `AGENTS.md` or `CLAUDE.md`. A thesis title, university rule, or page target is not inherited from the skill's installation directory. See [project configuration](references/project-profile.md).

## Updates and troubleshooting

For a user-wide CLI installation, update only this skill:

```bash
npx skills@latest update cs-phd-writing --global
```

Use `--project` for project installations. For a Git installation, confirm you are in the skill's own repository, preserve local changes, then run `git pull --ff-only`. For ZIP installations, preserve the old copy and replace the complete skill directory. Check each independent copy if multiple agents are installed. Updating the skill does not rewrite your thesis or replace its configuration.

- **Skill not found:** Check the directory nesting, `SKILL.md`, agent, and installation scope. Start a new task or restart the client if needed.
- **Old instructions still used:** Check the actual loaded path and version, remove ambiguity from duplicate installations, and ask the agent to reread the relevant guides.
- **Document or compilation tools unavailable:** Work with accessible content and report uncompleted checks. This skill does not install document runtimes.
- **Pinned versions and notifications:** Use a specific release and subscribe to Releases in GitHub's Watch settings. The default branch and release package may differ.

## Reference import example

```text
Use $cs-phd-writing to review this imported BibTeX batch.
Read the university rules and current bibliography setup first. Verify the original
sources, complete author order, and support for the cited claims. Preserve the
project's key convention; synchronize all affected references if keys change.
Keep verified software versions and web access dates, and report missing evidence.
```

## Guides and validation

[SKILL.md](SKILL.md) routes tasks to the necessary references. Useful entry points include [Chinese expression](references/chinese-expression.md), [systems prose in context](references/systems-context-expression.md), [paragraph functions](references/paragraph-functions.md), [paper-to-thesis integration](references/paper-to-thesis.md), and [manuscript review](references/manuscript-audit.md). These guides are in Chinese and do not all need to be loaded for every task.

[evals/](evals/) contains 42 synthetic cases, acceptance criteria, and versioned self-review records. Format checks, link checks, and maintainer self-reviews are not independent blind model evaluations or guarantees of performance across all domains and models. Paper analysis covers the recorded passages, not full-paper proofreading or experiment reproduction.

## Sources and license

This project adapts selected guidance from two upstream skills:

| Upstream and pinned revision | Adapted guidance |
| --- | --- |
| [doctoral-dissertation-skills](https://github.com/syc9336-rgb/doctoral-dissertation-skills/tree/95b0af625e34e4d26835e719352c52c2e907a43c) | Research-driven organization, chapter and paragraph roles, evidence, and separation of manuscript text from editing commentary |
| [dissertation-polisher-zh](https://github.com/ChipsAhoyM/dissertation-polisher-zh/tree/e88ee2b1746e3c90c48ec16c9b98b4be3ac33ef4) | Chapter review, scope of author references, terminology and symbol consistency, and located review feedback |

The adapted instructions are included in this package; upstream skills are not runtime dependencies and updates are not automatically imported. Upstream paragraph, style, and expression-pattern references are reorganized into the local guides. Patterns are prompts for contextual review, not prohibited-word lists. Mathematical reasoning, necessary qualifications, and useful navigation are preserved.

A supplementary Wikipedia writing-observations reference is documented in [prose quality](references/prose-quality.md); it is neither a thesis standard nor an AI-authorship detector. The systems-paper sources and inspected passages are recorded in [systems prose](references/systems-context-expression.md). External papers retain their own rights and are not bundled.

See [adaptation history](references/upstream-adaptation.md), the [source manifest](references/upstream-manifest.json), and [NOTICE](NOTICE.md) for provenance and attribution. This skill is distributed under [Apache License 2.0](LICENSE), with the upstream [NOTICE](licenses/doctoral-dissertation-NOTICE.txt) and [MIT license](licenses/dissertation-polisher-zh-MIT.txt) retained.
