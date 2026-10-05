<div align="center">

# CS PhD Writing

**把真实研究写清楚，把多篇成果组织成一篇博士论文。**

面向计算机学科的中文博士论文写作与审阅技能，适用于 Codex 和 Claude Code。

[![Release](https://img.shields.io/github/v/release/Jinghao-coding/cs-phd-writing?style=flat-square&label=release&color=2563eb)](https://github.com/Jinghao-coding/cs-phd-writing/releases/latest)
[![License](https://img.shields.io/badge/license-Apache--2.0-64748b?style=flat-square)](LICENSE)
[![Codex](https://img.shields.io/badge/agent-Codex-0f766e?style=flat-square)](https://developers.openai.com/codex/skills/)
[![Claude Code](https://img.shields.io/badge/agent-Claude_Code-b45309?style=flat-square)](https://code.claude.com/docs/en/skills)

**简体中文** · [English](README.en.md)

[快速开始](#quick-start) · [使用示例](#examples) · [项目接入](#project-setup) · [指南导航](#guides) · [版本记录](CHANGELOG.md)

</div>

---

## 从研究材料到论文正文

围绕研究问题组织章节，结合技术上下文改进中文表述，并逐项核对事实、术语和引文。学校规范、研究材料与个人偏好由当前论文项目提供，适配不同学校、学院和学位类型。

| 你正在做什么 | 技能如何帮助你 |
| :--- | :--- |
| **整合多篇英文论文** | 梳理研究主线、成果版本和章节关系，重组为中文学位论文 |
| **润色中文与解释机制** | 检查主谓宾、指代和逻辑关系，写清对象、状态、动作与执行条件 |
| **展开研究章与文献综述** | 补足定义、设计理由、推导和结果分析，围绕问题比较相关方法 |
| **整理参考文献** | 核验真实来源、完整作者顺序与正文支持，适配学校样式及 BibTeX 字段 |
| **审阅全文与配图** | 核对跨章术语、论据、图文关系、公式引用和提交材料 |
| **持续修订与 Agent 系统写作** | 维护有效决定和证据版本，准确区分角色、调用、记忆与资源管理 |

**支持材料：** 粘贴文本、PDF、DOCX、LaTeX 单文件及多文件工程。文件读取、编辑、检索和编译由运行环境中的工具执行；技能提供写作规则与操作指南。

> **主分支 v0.7.0** · [下载正式版](https://github.com/Jinghao-coding/cs-phd-writing/releases/tag/v0.7.0) · [变更记录](CHANGELOG.md)

<a id="quick-start"></a>
## 快速开始

### 1. 安装到你的助手

使用 skills CLI，需要 Node.js 与 npm。选择对应平台执行：

**Codex**

```bash
npx skills@latest add Jinghao-coding/cs-phd-writing --skill cs-phd-writing --agent codex --global
```

**Claude Code**

```bash
npx skills@latest add Jinghao-coding/cs-phd-writing --skill cs-phd-writing --agent claude-code --global
```

同时安装到两者可用 `--agent codex claude-code`。在论文项目目录中省略 `--global` 可作项目级安装。参数见 [skills CLI](https://github.com/vercel-labs/skills)。

### 2. 在论文项目中发起任务

```text
使用 $cs-phd-writing，润色第三章的方法说明。
先读相邻段落、符号定义和相关算法，检查对象、状态、动作与条件。
给出可用替换文本；涉及技术含义的更正，单独说明依据。
```

Claude Code 使用 `/cs-phd-writing` 替换示例中的 `$cs-phd-writing`。

<details>
<summary><strong>其他安装方式：Release ZIP / Git</strong></summary>

**固定版本安装**

从 [Releases](https://github.com/Jinghao-coding/cs-phd-writing/releases) 下载 `cs-phd-writing-vX.Y.Z.zip`，将完整的 `cs-phd-writing/` 目录放入对应位置：

| 平台 | 用户级目录 | 项目级目录 |
| :--- | :--- | :--- |
| Codex | `~/.agents/skills/cs-phd-writing/` | `<project>/.agents/skills/cs-phd-writing/` |
| Claude Code | `~/.claude/skills/cs-phd-writing/` | `<project>/.claude/skills/cs-phd-writing/` |

`SKILL.md` 应直接位于该目录下，保留全部配套文件。使用附件 `SHA256SUMS.txt` 校验 ZIP 与文件清单。已有安装先确认实际路径；Windows 将 `~` 替换为用户目录。

**Git 安装：跟随主分支**

以下 macOS / Linux 示例适用于目标目录尚不存在的情况：

```bash
# Codex
mkdir -p "$HOME/.agents/skills"
git clone https://github.com/Jinghao-coding/cs-phd-writing.git "$HOME/.agents/skills/cs-phd-writing"

# Claude Code
mkdir -p "$HOME/.claude/skills"
git clone https://github.com/Jinghao-coding/cs-phd-writing.git "$HOME/.claude/skills/cs-phd-writing"
```

目录依据 [Codex](https://developers.openai.com/codex/skills/) 与 [Claude Code](https://code.claude.com/docs/en/skills) 官方文档。更多安装选项见[详细指南](references/install-and-update.md)。

</details>

<a id="examples"></a>
## 常用场景

### 整合成果，规划论文

```text
使用 $cs-phd-writing，根据材料索引中的英文论文提出博士论文组织方案。
区分会议版与扩展稿，说明各章的研究问题、证据和相互关系。
本次只给组织方案，暂不写正文。
```

### 审阅章节，定位问题

```text
使用 $cs-phd-writing，审阅第三章，不修改文件。
按原文位置说明事实、逻辑和语言问题，区分确定错误与可选风格建议。
```

### 核验引用，整理 BibTeX

```text
使用 $cs-phd-writing，整理本次导入的 BibTeX。
先读取学校规范和当前样式，核对原始来源、完整作者顺序及所引论断。
沿用项目引用键约定；改键时同步受影响引用。
软件与网页保留可核验的版本和实际访问日期，缺项单独列出。
```

<a id="project-setup"></a>
## 接入自己的论文项目

每个论文项目维护自己的学校要求、研究资料和写作约定。技能读取已有的 `AGENTS.md`、`CLAUDE.md` 及项目配置，按当前任务选用相关规则。

```text
使用 $cs-phd-writing，读取学校规范、学院补充要求和现有论文配置。
按我的学位类型与适用批次整理条款，记录原文位置和需要确认的差异。
更新 docs/thesis-writing-profile.md，保留已确认内容；本次不改正文。
```

按需选用[项目模板](assets/project-template/)：

| 项目文件 | 保存什么 |
| :--- | :--- |
| `docs/thesis-writing-profile.md` | 论文入口、材料指针、写作偏好与章节约束 |
| `docs/university-writing-spec.md` | 正式规范、版本、条款位置与文献配置 |
| `docs/reference-thesis-notes.md` | 范文的写作方法、采用理由及适用范围 |
| `docs/paper-to-thesis-map.md` | 成果版本、研究问题、证据与章节对应 |

配置方法见[项目接入指南](references/project-profile.md)，也可将[项目说明片段](assets/project-template/project-instructions.snippet.md)合并到现有项目说明中。

<a id="guides"></a>
## 指南导航

[SKILL.md](SKILL.md) 是执行入口，按任务加载相关指南。

| 主题 | 解决什么问题 | 参考指南 |
| :--- | :--- | :--- |
| **中文语法与搭配** | 定位语病、歧义与可选风格，保留正确文本 | [中文表达](references/chinese-expression.md) · [修订流程](references/revision-workflow.md) |
| **段落与英中转写** | 连接句间信息，梳理论证，转写自然中文 | [段落功能](references/paragraph-functions.md) · [衔接与转写](references/cohesion-and-translation.md) |
| **学术语气与简洁表达** | 减少空泛、重复和自评，保持论断强度 | [学术表述](references/prose-quality.md) |
| **技术语义与上下文** | 保持对象、动作、条件、数字和证据含义 | [语义核对](references/revision-workflow.md) · [系统机制](references/systems-context-expression.md) · [Agent 系统](references/agent-systems-expression.md) · [持续上下文](references/writing-context.md) |
| **结构与研究** | 组织章节、整合成果，围绕问题综合文献 | [论文结构](references/thesis-structure.md) · [小论文整合](references/paper-to-thesis.md) · [文献综合](references/research-and-synthesis.md) |
| **证据与引用** | 核验事实、作者顺序、引用支持与学校样式 | [事实与术语](references/evidence-and-terms.md) · [文献校验](references/bibliography-validation.md) |
| **阅读与交付** | 读取材料，规划图文，核对全文 | [输入读取](references/input-reading.md) · [配图规划](references/figure-design.md) · [全文审阅](references/manuscript-audit.md) |
| **工具与修订评估** | 比较公式、引用和数字，检查术语候选与过度修改 | [工具入口](references/language-tools.md) · [评估方法](evals/revision-evaluation.md) · [研究来源](references/language-research-sources.md) |

[评估目录](evals/)提供 **62 个合成案例**、**2 个公开真实修订分析切片**、多参考验收要求及版本记录。两个真实切片来自同一篇论文，分别讨论清晰性修改和科学含义变化。评估分开检查问题修复、含义保持、可读性、过度修改和文档完整性。

只读辅助检查使用 Python 标准库，无额外依赖：

```bash
python3 <skill-dir>/scripts/check_revision.py before.tex after.tex
```

脚本输出公式、引用和数字差异；可用 `--glossary glossary.json` 加载项目词表。使用方法与可选 textlint、Vale 等工具见[工具入口](references/language-tools.md)。

## 更新与帮助

CLI 用户级安装可执行：

```bash
npx skills@latest update cs-phd-writing --global
```

项目级安装使用 `--project`。Git 安装在技能独立仓库中处理好本地修改后执行 `git pull --ff-only`；ZIP 安装使用新版完整目录替换。详细操作见[安装与更新](references/install-and-update.md)。

<details>
<summary><strong>找不到技能或仍在使用旧版本？</strong></summary>

- 核对目录层级、`SKILL.md`、目标平台和安装范围。
- 核对实际加载路径，检查同名副本和所用版本。
- 更新后重新读取技能，或开启新任务；必要时重启客户端。
- 需要 PDF、DOCX 编辑或 LaTeX 编译时，确认助手环境有相应工具。
- 在 GitHub 的 **Watch → Custom → Releases** 中订阅版本通知。

</details>

## 来源与许可

本项目整合并改写了两个上游技能的部分规则，配套指南已包含在本仓库中：

| 上游 | 采用内容 |
| :--- | :--- |
| [doctoral-dissertation-skills · 95b0af6](https://github.com/syc9336-rgb/doctoral-dissertation-skills/tree/95b0af625e34e4d26835e719352c52c2e907a43c) | 研究驱动的章节组织、段落功能与证据规则 |
| [dissertation-polisher-zh · e88ee2b](https://github.com/ChipsAhoyM/dissertation-polisher-zh/tree/e88ee2b1746e3c90c48ec16c9b98b4be3ac33ef4) | 章节审阅、作者自指范围、术语一致性与定位反馈 |

系统论文、Agent 教程及文献工具的阅读范围记录在对应指南中。完整来源见[改写记录](references/upstream-adaptation.md)、[来源清单](references/upstream-manifest.json)和[署名说明](NOTICE.md)。

以 [Apache License 2.0](LICENSE) 发布，保留上游 [NOTICE](licenses/doctoral-dissertation-NOTICE.txt) 与 [MIT 许可证](licenses/dissertation-polisher-zh-MIT.txt)。
