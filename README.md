# CS PhD Writing

简体中文 | [English](README.en.md)

面向计算机学科的中文博士学位论文写作与审阅技能，适用于 Codex 与 Claude Code。将英文研究成果组织为中文学位论文，结合技术上下文改进表述，并核对研究对象、机制和证据是否一致。

[下载正式版本](https://github.com/Jinghao-coding/cs-phd-writing/releases/latest) · [变更记录](CHANGELOG.md) · [详细安装与更新](references/install-and-update.md)

本仓库提供写作指令与参考指南。实际读取 PDF、编辑 Word、编译 LaTeX 或检索文献的能力由运行环境提供；不需要另行安装两个上游技能。操作指南以中文维护，英文 README 用于介绍、安装和使用导航。

## 能做什么

| 任务 | 交付与判断重点 |
| --- | --- |
| 组织多篇研究成果 | 研究主线、章节对应、会议版与扩展稿归并，不虚构章间依赖 |
| 中文转写与润色 | 主谓与动宾搭配、指代、条件和量词作用域、段落衔接；保留公式和事实 |
| 解释系统机制 | 根据实际对象、状态、事件顺序和接口语义改写，不套用其他系统的机制 |
| 重组章节与综述 | 标题与内容对应、概念引入顺序、同问题方法比较，避免碎片化和重复 |
| 展开研究章 | 补足定义、设计理由、推导、运行示例和已有结果分析，不编造实验 |
| 审阅全文和配图 | 跨章术语与贡献、引文支持、图文关系和可读性；图源形式遵循项目要求 |
| 校验与整理参考文献 | 学校规范、真实来源、完整作者顺序、BibTeX适配、引用键迁移及软件/网站引用 |
| 维护上下文与描述Agent系统 | 有效决定、证据来源、执行对象、记忆与资源语义 |
| 接入论文项目 | 学校规范、范文经验与个人偏好分别保存在项目配置中 |

支持粘贴文本、PDF、DOCX、LaTeX 单文件及多文件工程。阅读范围和工具条件见 [输入读取](references/input-reading.md)。

## 近期更新

v0.5.0 增加[写作上下文](references/writing-context.md)、[Agent系统表述](references/agent-systems-expression.md)和[文献校验与格式适配](references/bibliography-validation.md)。导入BibTeX先核验原始元数据，再适配学校现有样式；完整作者信息与最终显示格式分别处理。这些是供助手执行的流程，不是已安装的自动核验服务。

v0.4 系列补强了中文表述、章节重组和系统上下文判断。新增指南参考六篇系统论文的指定段落，并提供独立编写的对照示例：释放显存与删除缓存、提交与完成、原子性与恰好一次等概念不能混用。见 [系统上下文表达](references/systems-context-expression.md)。v0.4.2 补充双语 README 并更新安装导航，具体变化见 [CHANGELOG](CHANGELOG.md)。

## 安装

选择一种安装方式，避免在同一平台重复安装同名副本。

### 使用 skills CLI

需要 Node.js 与 npm。在终端按目标平台执行：

```bash
# Codex：用户级安装
npx skills@latest add Jinghao-coding/cs-phd-writing --skill cs-phd-writing --agent codex --global

# Claude Code：用户级安装
npx skills@latest add Jinghao-coding/cs-phd-writing --skill cs-phd-writing --agent claude-code --global
```

同时安装到两者可用 `--agent codex claude-code`。在论文项目目录中去掉 `--global` 可作项目级安装；`--copy` 使用独立副本。仓库安装可能取得尚未打包发布的默认分支内容；需要固定版本时使用下方 Release ZIP。参数见 [skills CLI 官方说明](https://github.com/vercel-labs/skills)。

### 使用 Release ZIP

1. 打开 [Releases](https://github.com/Jinghao-coding/cs-phd-writing/releases)，下载该版本的 `cs-phd-writing-vX.Y.Z.zip`。
2. 解压，将完整的 `cs-phd-writing/` 文件夹放入以下一个位置。`SKILL.md` 应直接位于该文件夹下，不多嵌套一层。
3. 保留 `references/`、`assets/`、`agents/`、许可证等配套文件。附件中的 `SHA256SUMS.txt` 校验 ZIP 与文件清单；`file-manifest.json` 记录包内各文件。

| 平台 | 用户级目录 | 项目级目录 |
| --- | --- | --- |
| Codex | `~/.agents/skills/cs-phd-writing/` | `<project>/.agents/skills/cs-phd-writing/` |
| Claude Code | `~/.claude/skills/cs-phd-writing/` | `<project>/.claude/skills/cs-phd-writing/` |

路径依据 [Codex 官方文档](https://developers.openai.com/codex/skills/) 与 [Claude Code 官方文档](https://code.claude.com/docs/en/skills)，核对日期为 2026-10-04。既有安装若由客户端或安装器管理，应先确认实际位置，不直接迁移或再装一份。Windows 将 `~` 换为用户目录；以下 Shell 示例面向 macOS/Linux。

### 使用 Git

以下示例要求目标目录尚不存在：

```bash
# Codex
mkdir -p "$HOME/.agents/skills"
git clone https://github.com/Jinghao-coding/cs-phd-writing.git "$HOME/.agents/skills/cs-phd-writing"

# Claude Code
mkdir -p "$HOME/.claude/skills"
git clone https://github.com/Jinghao-coding/cs-phd-writing.git "$HOME/.claude/skills/cs-phd-writing"
```

Git 克隆跟随默认分支。固定版本、更新已有副本等操作见 [安装与更新](references/install-and-update.md)。

## 开始使用

安装后，在论文项目中发起任务并明确修改范围。Codex 使用 `$cs-phd-writing`，Claude Code 使用 `/cs-phd-writing`。

**结合上下文润色：**

```text
使用 $cs-phd-writing，润色当前章节的方法说明。
先读相邻段落、符号定义和相关算法，检查对象、状态、动作与条件。
给出可用替换文本；若技术含义需更正，单独说明依据，不补造机制。
```

**导入并核验参考文献：**

```text
使用 $cs-phd-writing，整理本次导入的BibTeX。
先读取学校规范和当前样式，核对原始来源、完整作者顺序及所引论断。
沿用项目引用键约定；需要改键时同步所有受影响引用。
软件与网页保留可核验的版本和访问日期，缺项不要猜填，报告未完成检查。
```

**只审不改：**

```text
使用 $cs-phd-writing，审阅第三章，不修改文件。
按原文位置说明事实、逻辑和语言问题，区分确定错误与可选风格建议。
```

**英文成果整合：**

```text
使用 $cs-phd-writing，根据材料索引中的英文论文提出中文博士论文组织方案。
区分会议版与扩展稿，说明各章问题、证据和联系，暂不写正文。
```

Claude Code 将这些请求中的调用前缀换成 `/cs-phd-writing`。正文修改与讨论方案分别处理，不因调用技能自动扩展到全文重写。

## 接入自己的论文项目

学校规范、个人材料与偏好应留在论文项目内。已有 `AGENTS.md`、`CLAUDE.md` 或项目配置时先读取，不用空白模板覆盖。

```text
使用 $cs-phd-writing，为当前论文整理学校规范、参考范文和写作偏好。
建立或更新 docs/thesis-writing-profile.md，保留已确认内容和现有材料路径。
区分正式规范、范文观察和个人安排，记录来源；本次不改正文。
```

按需使用 [项目模板](assets/project-template/)：

| 文件 | 内容 |
| --- | --- |
| `docs/thesis-writing-profile.md` | 论文入口、已确认信息、材料指针、偏好与章节约束 |
| `docs/university-writing-spec.md` | 官方规范的来源、版本和条款定位 |
| `docs/reference-thesis-notes.md` | 范文观察、拟采用方式和适用章节 |
| `docs/paper-to-thesis-map.md` | 多篇成果的版本、问题、证据和章节对应 |

将 [项目说明片段](assets/project-template/project-instructions.snippet.md) 中适用内容合并进 `AGENTS.md` 或 `CLAUDE.md`。学校要求、论文题目、固定页数等不会从技能安装目录继承。详见 [项目接入](references/project-profile.md)。

## 更新与常见问题

CLI 用户级安装可只更新本技能：

```bash
npx skills@latest update cs-phd-writing --global
```

项目级安装使用 `--project`。Git 克隆在确认是技能独立仓库、保留本地修改后执行 `git pull --ff-only`；ZIP 安装保留旧副本后替换完整技能目录。独立复制安装需核对每个平台的实际副本。更新技能不会自动改写论文或覆盖项目配置。

- **找不到技能：** 核对目录层级和 `SKILL.md`，确认安装到了当前平台与作用域；重新开始任务，必要时重启客户端。
- **仍在使用旧规则：** 检查实际读取路径与版本，避免重复副本；要求重新读取技能入口及相关指南。
- **PDF、DOCX或编译工具不可用：** 按已有工具处理可读内容，明确未完成的检查；技能本身不安装文档运行时。
- **想固定版本或获知更新：** 使用指定 Release，在 GitHub 的 Watch 设置中订阅 Releases。默认分支与发布包可能不同。

## 指南与验证

入口 [SKILL.md](SKILL.md) 按任务选择参考文件，不要求每次加载全部指南。可直接查阅 [中文表达](references/chinese-expression.md)、[系统上下文表达](references/systems-context-expression.md)、[段落功能](references/paragraph-functions.md)、[小论文整合](references/paper-to-thesis.md) 和 [全文审阅](references/manuscript-audit.md)。

[evals/](evals/) 提供42个合成案例、验收要求和分版本自检记录。结构校验、链接检查与维护助手自检不等同于独立模型盲测，也不能证明所有领域和模型上的效果。论文样本只分析登记的段落，不声称全文审校或实验复现。

## 来源与许可证

### 两个上游具体如何使用

本项目读取并改写了下列上游版本中的相关规则，按中文博士论文的写作与审阅任务重新组织。

| 上游与采用版本 | 采用的内容 | 本项目中的主要位置 |
| --- | --- | --- |
| [doctoral-dissertation-skills](https://github.com/syc9336-rgb/doctoral-dissertation-skills)，[95b0af6](https://github.com/syc9336-rgb/doctoral-dissertation-skills/tree/95b0af625e34e4d26835e719352c52c2e907a43c) | 根据实际研究组织章节；区分章、节、段落的论证功能；用证据支撑结论；清理修稿过程和提前辩护式表述 | [论文结构](references/thesis-structure.md)、[事实与术语](references/evidence-and-terms.md)、[写作与审阅](references/writing-and-review.md) |
| [dissertation-polisher-zh](https://github.com/ChipsAhoyM/dissertation-polisher-zh)，[e88ee2b](https://github.com/ChipsAhoyM/dissertation-polisher-zh/tree/e88ee2b1746e3c90c48ec16c9b98b4be3ac33ef4) | 按章阅读；校准“本文、本章、本节”的作用域；检查跨章术语和符号一致性；提供有原文定位的审阅意见 | [中文表达](references/chinese-expression.md)、[写作与审阅](references/writing-and-review.md) |

改写后的规则已包含在本仓库的 `SKILL.md` 和 `references/` 中。使用时只需调用 `$cs-phd-writing`，无需另行安装或调用这两个上游技能。这里没有导入它们的全部工作流，也不会自动跟随上游更新；后续采用新版本时需重新核对规则并更新来源记录。

doctoral-dissertation-skills 中三个参考文件的具体分工与本项目的对应关系如下：

| 上游文件 | 解决的问题 | 本项目对应内容 |
| --- | --- | --- |
| `paragraph_functions.md` | 段落如何完成背景、方法、证据、讨论等论证功能 | [段落功能](references/paragraph-functions.md)：按计算机研究整理为 24 类，补充算法、证明、实现和消融等内容 |
| `language_style.md` | 全文如何保持自然、精确、稳定的学术表达 | [中文表达](references/chinese-expression.md)：中文句法、术语、逻辑关系和证据强度 |
| `forbidden_patterns.md` | 哪些表达需要重点复核 | [中文表达](references/chinese-expression.md) 与 [学术表述检查](references/prose-quality.md)：提前辩护、夸大、空泛分析和正文残留，按语境判断 |

上游的表达模式是复核线索，不是见词即删的黑名单。本项目保留数学证明、必要限定和有实际作用的章节导引。

补充阅读参考为 [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)。其观察用于提醒检查具体写作与来源问题，不作为学位论文规范或 AI 作者判定标准。阅读版本与独立编写的中文检查流程见 [学术表述检查](references/prose-quality.md)。

### 本项目的补充与调整

- 强化中文主谓宾、指代、修饰范围和比较关系检查，逐项核对改写是否改变研究含义。
- 补充事实与词汇依据检查，区分误差和准确率、百分比和百分点、计划与已完成工作；对新术语核查定义和使用依据。
- 清理防御性表述时保留必要的数学推导、研究条件和真实局限；正常连接词和中文承前省略根据上下文判断。
- 学校规范与个人偏好由当前论文项目提供，不把上游个案中的固定章数、页数或强制递进关系设为通用要求；提供 [合成案例](evals/cases.md) 检查事实、语言、修改范围和跨项目使用。

完整的采用范围与改写说明见 [改写记录](references/upstream-adaptation.md)，上游文件、固定提交与校验信息见 [来源清单](references/upstream-manifest.json)。

### 许可证与署名

本项目以 [Apache License 2.0](LICENSE) 发布，保留 doctoral-dissertation-skills 的 [原始 NOTICE](licenses/doctoral-dissertation-NOTICE.txt) 和 dissertation-polisher-zh 的 [MIT 许可证](licenses/dissertation-polisher-zh-MIT.txt)。作者署名、第三方通知及适用范围见 [NOTICE](NOTICE.md)。
