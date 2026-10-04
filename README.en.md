<div align="center">

# CS PhD Writing

**Explain your research clearly. Bring your papers together into a coherent dissertation.**

A skill for writing and reviewing Chinese doctoral dissertations in computer science, for Codex and Claude Code.

[![Release](https://img.shields.io/github/v/release/Jinghao-coding/cs-phd-writing?style=flat-square&label=release&color=2563eb)](https://github.com/Jinghao-coding/cs-phd-writing/releases/latest)
[![License](https://img.shields.io/badge/license-Apache--2.0-64748b?style=flat-square)](LICENSE)
[![Codex](https://img.shields.io/badge/agent-Codex-0f766e?style=flat-square)](https://developers.openai.com/codex/skills/)
[![Claude Code](https://img.shields.io/badge/agent-Claude_Code-b45309?style=flat-square)](https://code.claude.com/docs/en/skills)

[简体中文](README.md) · **English**

[Quick start](#quick-start) · [Examples](#examples) · [Project setup](#project-setup) · [Guides](#guides) · [Changelog](CHANGELOG.md)

</div>

---

## From research materials to dissertation prose

Organize chapters around research questions, improve Chinese prose in its technical context, and check facts, terminology and citations. University rules, research materials and writing preferences come from the current thesis project, allowing the skill to adapt to different institutions and degree requirements.

| What you are working on | How the skill helps |
| :--- | :--- |
| **Integrating English papers** | Map research questions, publication versions and chapter relationships into a Chinese dissertation |
| **Polishing prose and explaining mechanisms** | Check grammar, references and logic; clarify entities, states, actions and execution conditions |
| **Developing chapters and literature reviews** | Explain definitions, design choices, derivations and results; compare approaches around shared problems |
| **Managing references** | Verify sources, complete author order and citation support; adapt BibTeX data to university styles |
| **Reviewing manuscripts and figures** | Check terminology, evidence, figures, equations, cross-references and submission materials |
| **Sustained revision and agent systems writing** | Track current decisions and evidence versions; distinguish roles, calls, memory and resource management |

**Supported inputs:** pasted text, PDF, DOCX, and single-file or multi-file LaTeX projects. The agent environment provides reading, editing, search and compilation tools; the skill provides writing guidance and workflows. Operational guides are maintained in Chinese.

> **Main branch v0.5.0** includes [writing context](references/writing-context.md), [agent systems prose](references/agent-systems-expression.md) and [bibliography validation](references/bibliography-validation.md). Install from the main branch for these additions, or choose a fixed version from [Releases](https://github.com/Jinghao-coding/cs-phd-writing/releases) and consult its release notes.

<a id="quick-start"></a>
## Quick start

### 1. Install for your agent

The skills CLI requires Node.js and npm. Choose your agent:

**Codex**

```bash
npx skills@latest add Jinghao-coding/cs-phd-writing --skill cs-phd-writing --agent codex --global
```

**Claude Code**

```bash
npx skills@latest add Jinghao-coding/cs-phd-writing --skill cs-phd-writing --agent claude-code --global
```

Use `--agent codex claude-code` for both. Omit `--global` in your thesis directory for a project installation. See the [skills CLI](https://github.com/vercel-labs/skills) for options.

### 2. Start a task in your thesis project

```text
Use $cs-phd-writing to polish the method explanation in Chapter 3.
Read adjacent paragraphs, symbol definitions and the relevant algorithm first.
Check entities, states, actions and conditions. Return usable Chinese replacement text.
Explain any substantive technical corrections separately, with their evidence.
```

In Claude Code, replace `$cs-phd-writing` with `/cs-phd-writing`.

<details>
<summary><strong>Other installation methods: Release ZIP / Git</strong></summary>

**Install a fixed version**

Download `cs-phd-writing-vX.Y.Z.zip` from [Releases](https://github.com/Jinghao-coding/cs-phd-writing/releases) and place the complete `cs-phd-writing/` folder in one of these locations:

| Agent | User-wide location | Project location |
| :--- | :--- | :--- |
| Codex | `~/.agents/skills/cs-phd-writing/` | `<project>/.agents/skills/cs-phd-writing/` |
| Claude Code | `~/.claude/skills/cs-phd-writing/` | `<project>/.claude/skills/cs-phd-writing/` |

Keep `SKILL.md` directly inside that folder, together with all supporting files. Use `SHA256SUMS.txt` to verify the ZIP and manifest. Check the actual path for existing installations. On Windows, replace `~` with your user directory.

**Install with Git to follow the main branch**

These macOS / Linux examples assume that the destination directory does not exist:

```bash
# Codex
mkdir -p "$HOME/.agents/skills"
git clone https://github.com/Jinghao-coding/cs-phd-writing.git "$HOME/.agents/skills/cs-phd-writing"

# Claude Code
mkdir -p "$HOME/.claude/skills"
git clone https://github.com/Jinghao-coding/cs-phd-writing.git "$HOME/.claude/skills/cs-phd-writing"
```

Locations follow the official [Codex](https://developers.openai.com/codex/skills/) and [Claude Code](https://code.claude.com/docs/en/skills) documentation. See the [detailed installation guide](references/install-and-update.md) for more options.

</details>

<a id="examples"></a>
## Common tasks

### Integrate papers and plan chapters

```text
Use $cs-phd-writing to propose a dissertation structure from the indexed English papers.
Distinguish conference and extended versions. Explain each chapter's research question,
evidence and relationship to the other chapters. Provide a plan only for this task.
```

### Review a chapter and locate issues

```text
Use $cs-phd-writing to review Chapter 3 without modifying files.
Locate factual, logical and language issues in the source.
Distinguish definite errors from optional style changes.
```

### Verify citations and organize BibTeX

```text
Use $cs-phd-writing to organize this imported BibTeX batch.
Read the university rules and current style first. Verify original sources,
complete author order and support for the cited claims. Follow the project's key convention
and update affected references when keys change. Preserve verified software versions
and actual web access dates; list missing information separately.
```

<a id="project-setup"></a>
## Connect your thesis project

Each thesis project keeps its own university requirements, research materials and writing decisions. The skill reads existing `AGENTS.md`, `CLAUDE.md` and project configuration, then selects the guidance relevant to the current task.

```text
Use $cs-phd-writing to read the university rules, department requirements and thesis configuration.
Identify the rules for my degree type and submission cohort, with source locations
and differences requiring clarification. Update docs/thesis-writing-profile.md,
preserving confirmed information. Keep manuscript editing outside this task.
```

Choose the files you need from the [project templates](assets/project-template/):

| Project file | Contents |
| :--- | :--- |
| `docs/thesis-writing-profile.md` | Entry file, material pointers, writing preferences and chapter constraints |
| `docs/university-writing-spec.md` | Official rules, versions, source locations and bibliography configuration |
| `docs/reference-thesis-notes.md` | Observed writing methods, adoption rationale and scope |
| `docs/paper-to-thesis-map.md` | Publication versions, research questions, evidence and chapter mapping |

See [project configuration](references/project-profile.md), or merge the [project instructions snippet](assets/project-template/project-instructions.snippet.md) into your existing project instructions.

<a id="guides"></a>
## Guide directory

[SKILL.md](SKILL.md) is the execution entrypoint and routes each task to the relevant guides.

| Topic | Guides |
| :--- | :--- |
| **Language and argument** | [Chinese expression](references/chinese-expression.md) · [Paragraph functions](references/paragraph-functions.md) · [Academic prose](references/prose-quality.md) |
| **Structure and research** | [Thesis structure](references/thesis-structure.md) · [Paper integration](references/paper-to-thesis.md) · [Literature synthesis](references/research-and-synthesis.md) |
| **Technical context** | [Systems mechanisms](references/systems-context-expression.md) · [Agent systems](references/agent-systems-expression.md) · [Writing context](references/writing-context.md) |
| **Evidence and citations** | [Facts and terminology](references/evidence-and-terms.md) · [Bibliography validation](references/bibliography-validation.md) |
| **Reading and delivery** | [Input reading](references/input-reading.md) · [Figure planning](references/figure-design.md) · [Manuscript review](references/manuscript-audit.md) |

The [evaluation directory](evals/) contains **42 synthetic cases**, acceptance criteria and versioned manual self-review records covering language, facts, context, references and editing scope.

## Updates and help

For a user-wide CLI installation:

```bash
npx skills@latest update cs-phd-writing --global
```

Use `--project` for project installations. For Git installations, resolve local changes in the skill's own repository and run `git pull --ff-only`. For ZIP installations, replace the complete directory with the new version. See [installation and updates](references/install-and-update.md).

<details>
<summary><strong>Skill missing or an older version still loading?</strong></summary>

- Check folder nesting, `SKILL.md`, the target agent and installation scope.
- Verify the loaded path, duplicate copies and version.
- Reread the skill after updating, or start a new task; restart the client if needed.
- Ensure your agent environment has the tools needed for PDF, DOCX editing or LaTeX compilation.
- Subscribe through GitHub's **Watch → Custom → Releases** for release notifications.

</details>

## Sources and license

This project adapts selected guidance from two upstream skills. The adapted guides are included in this repository:

| Upstream | Adapted guidance |
| :--- | :--- |
| [doctoral-dissertation-skills · 95b0af6](https://github.com/syc9336-rgb/doctoral-dissertation-skills/tree/95b0af625e34e4d26835e719352c52c2e907a43c) | Research-driven chapter organization, paragraph functions and evidence rules |
| [dissertation-polisher-zh · e88ee2b](https://github.com/ChipsAhoyM/dissertation-polisher-zh/tree/e88ee2b1746e3c90c48ec16c9b98b4be3ac33ef4) | Chapter review, scope of author references, terminology consistency and located feedback |

Reading scope for systems papers, agent tutorials and bibliography tools is recorded in the relevant guides. See the [adaptation history](references/upstream-adaptation.md), [source manifest](references/upstream-manifest.json) and [attribution notice](NOTICE.md) for full provenance.

Distributed under [Apache License 2.0](LICENSE), retaining the upstream [NOTICE](licenses/doctoral-dissertation-NOTICE.txt) and [MIT license](licenses/dissertation-polisher-zh-MIT.txt).
