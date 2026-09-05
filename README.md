# CS PhD Writing

An agent skill for writing and reviewing computer science PhD dissertations in Chinese.

面向计算机学科的中文博士学位论文写作与审阅，支持将多篇英文小论文组织、重写为中文毕业论文。

基于 [doctoral-dissertation-skills](https://github.com/syc9336-rgb/doctoral-dissertation-skills) 和 [dissertation-polisher-zh](https://github.com/ChipsAhoyM/dissertation-polisher-zh) 改写整合，保留上游署名与许可证。

## 适合哪些任务

| 任务 | 具体交付 |
| --- | --- |
| 从真实材料重建论文结构 | 研究主线、章与节的功能、问题与证据对应；按材料调整已有大纲 |
| 英文小论文转为中文学位论文 | 成果与章节对应、会议版与扩展版归并、内容重组、中文转写和来源记录 |
| 组织文献综述、理论框架和研究设计 | 按问题比较已有研究，明确概念与假设，区分实验计划和实际结果 |
| 组织方法、结果与讨论 | 说明做法、观察与解释各自的功能，核对结论是否有证据支持 |
| 检查中文与技术表达 | 主谓宾、指代、修饰范围、术语、因果与比较关系；清理防御性表述并保留必要条件 |
| 审阅章节或全文 | 有原文定位、依据和建议的修改意见，检查重复贡献及跨章一致性 |
| 核对图表、附录、脚注、引文和中英文版本 | 对象与引用是否对应、材料是否存在、数值与结论是否一致 |
| 接入学校规范、范文和个人偏好 | 论文项目内的配置与资料指针，区分正式规范、参考写法和个人安排 |
| 答辩或提交前检查 | 按项目正式要求核对组成部分、引用、已确认信息和实际导出文件 |

流程入口见 [SKILL.md](SKILL.md)。单段润色、只审不改和讨论大纲均按请求范围处理。

## 支持的输入

| 格式 | 读取逻辑 |
| --- | --- |
| PDF | 根据目录或书签按章节分批阅读；图表、公式和复杂排版查看对应页面 |
| DOCX | 按标题、段落与表格阅读，另行核对公式、图像、题注及修订状态 |
| LaTeX 单文件 | 读取实际启用的正文、定义、图表及文献 |
| LaTeX 多文件工程 | 定位主文件，按实际输入顺序、条件和路径规则追踪依赖 |
| 粘贴文本 | 直接处理片段，不据此声称已审阅全文 |

工具按运行环境选择；扫描件需要实际可用的 OCR 或视觉读取能力。具体策略与覆盖范围见 [输入读取](references/input-reading.md)。

## 安装与调用

仓库根目录是一份可供 Codex 和 Claude Code 使用的技能包，共用写作规则、参考文件和项目模板。

### 方法一：npx 安装

需要 Node.js 与 npm，按使用的平台选择：

```bash
# Codex
npx skills@latest add Jinghao-coding/cs-phd-writing --skill cs-phd-writing --agent codex --global

# Claude Code
npx skills@latest add Jinghao-coding/cs-phd-writing --skill cs-phd-writing --agent claude-code --global
```

同时安装到两者时，使用 `--agent codex claude-code`；去掉 `--global` 则安装到当前项目。安装器用法见 [skills CLI](https://github.com/vercel-labs/skills)。

### 方法二：Git 克隆或手动安装

将完整仓库克隆或将 Release 技能包解压到目标平台的技能目录，文件夹名为 `cs-phd-writing`。保留全部配套文件。路径和命令见 [安装与更新](references/install-and-update.md)。

| 平台 | 显式调用示例 |
| --- | --- |
| Codex | `使用 $cs-phd-writing，审阅当前论文第三章，只给修改建议。` |
| Claude Code | `/cs-phd-writing 审阅当前论文第三章，只给修改建议。` |

安装后重新调用技能；若当前任务未发现它，可指定 `SKILL.md` 路径读取或开启新任务。Claude Code 的调用约定见 [官方文档](https://code.claude.com/docs/en/skills)。

## 英文小论文如何转为毕业论文

按“选定稿件与版本 → 研究主线 → 成果与章节对应 → 内容重组与中文转写 → 跨稿事实、符号和引用检查”处理。多篇成果可以共同支撑一章，一篇成果也可承担多个论证功能；前期工作按其作用安排。

```text
使用 $cs-phd-writing，根据材料索引中的英文论文组织中文博士学位论文。
先给研究主线和成果与章节对应，不直接改正文。
区分会议版与扩展版，说明共享背景如何合并，并核对各章的证据。
```

后续可明确要求按已确认大纲转写某章。流程和边界见 [小论文到学位论文](references/paper-to-thesis.md)，对应表见 [模板](assets/project-template/docs/paper-to-thesis-map.md)。Claude Code 使用同样的请求内容，将调用前缀换成 `/cs-phd-writing`。

## 接入学校规范、范文分析及个人偏好

配置放在自己的论文项目里。首次接入可以直接提供原件、网页或已有资料路径，再提出：

```text
使用 $cs-phd-writing，为当前论文接入学校规范、参考范文和我的写作偏好。
建立或更新 docs/thesis-writing-profile.md，保留已有已确认内容。
区分正式规范、范文观察和个人安排，标明来源与版本；未确认项留空。
本次只整理项目配置，不改论文正文。
```

也可以从 [项目模板](assets/project-template/) 选择需要的文件：

| 放入论文项目的位置 | 内容 |
| --- | --- |
| `docs/thesis-writing-profile.md` | 学位类型、题目、材料指针、个人和导师偏好、章节约束 |
| `docs/university-writing-spec.md` | 官方来源、适用版本、条款定位与实际要求 |
| `docs/reference-thesis-notes.md` | 范文中观察到的做法、拟采用方式及适用理由 |
| `docs/paper-to-thesis-map.md` | 需要整合小论文时，登记版本、问题、证据和章节对应 |

将 [项目说明片段](assets/project-template/project-instructions.snippet.md) 合并到论文的 `AGENTS.md` 或 `CLAUDE.md`，让后续任务找到配置。已有文件只合并需要的内容，不用空白模板覆盖。

学校要求决定适用的格式约束，范文提供写作经验，个人偏好指导当前论文的选择；出现冲突时说明来源及影响。材料路径可以沿用现有目录。技能更新与论文配置分开维护，详情见 [项目接入](references/project-profile.md)。

## 获知更新与升级

在仓库 **Watch → Custom → Releases** 中订阅版本发布；通知投递由使用者自己的 GitHub 设置决定。发布内容见 [Releases](https://github.com/Jinghao-coding/cs-phd-writing/releases)，具体变化见 [CHANGELOG](CHANGELOG.md)。[GitHub 说明](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases)

通过 skills CLI 做用户级安装后，可以只更新本技能：

```bash
npx skills@latest update cs-phd-writing --global
```

项目级安装改用 `--project`。Git 克隆、手动复制和链接源码采用各自的更新方式，见 [安装、更新与维护者发布](references/install-and-update.md)。默认分支可能包含尚未单独发布的修改；需要固定版本时使用对应 Release。

## 来源与许可证

### 两个上游具体如何使用

本项目读取并改写了下列上游版本中的相关规则，按中文博士论文的写作与审阅任务重新组织。

| 上游与采用版本 | 采用的内容 | 本项目中的主要位置 |
| --- | --- | --- |
| [doctoral-dissertation-skills](https://github.com/syc9336-rgb/doctoral-dissertation-skills)，[95b0af6](https://github.com/syc9336-rgb/doctoral-dissertation-skills/tree/95b0af625e34e4d26835e719352c52c2e907a43c) | 根据实际研究组织章节；区分章、节、段落的论证功能；用证据支撑结论；清理修稿过程和提前辩护式表述 | [论文结构](references/thesis-structure.md)、[事实与术语](references/evidence-and-terms.md)、[写作与审阅](references/writing-and-review.md) |
| [dissertation-polisher-zh](https://github.com/ChipsAhoyM/dissertation-polisher-zh)，[e88ee2b](https://github.com/ChipsAhoyM/dissertation-polisher-zh/tree/e88ee2b1746e3c90c48ec16c9b98b4be3ac33ef4) | 按章阅读；校准“本文、本章、本节”的作用域；检查跨章术语和符号一致性；提供有原文定位的审阅意见 | [中文表达](references/chinese-expression.md)、[写作与审阅](references/writing-and-review.md) |

改写后的规则已包含在本仓库的 `SKILL.md` 和 `references/` 中。使用时只需调用 `$cs-phd-writing`，无需另行安装或调用这两个上游技能。这里没有导入它们的全部工作流，也不会自动跟随上游更新；后续采用新版本时需重新核对规则并更新来源记录。

### 本项目的补充与调整

- 强化中文主谓宾、指代、修饰范围和比较关系检查，逐项核对改写是否改变研究含义。
- 补充事实与词汇依据检查，区分误差和准确率、百分比和百分点、计划与已完成工作；对新术语核查定义和使用依据。
- 清理防御性表述时保留必要的数学推导、研究条件和真实局限；正常连接词和中文承前省略根据上下文判断。
- 学校规范与个人偏好由当前论文项目提供，不把上游个案中的固定章数、页数或强制递进关系设为通用要求；提供 [合成案例](evals/cases.md) 检查事实、语言、修改范围和跨项目使用。

完整的采用范围与改写说明见 [改写记录](references/upstream-adaptation.md)，上游文件、固定提交与校验信息见 [来源清单](references/upstream-manifest.json)。

### 许可证与署名

本项目以 [Apache License 2.0](LICENSE) 发布，保留 doctoral-dissertation-skills 的 [原始 NOTICE](licenses/doctoral-dissertation-NOTICE.txt) 和 dissertation-polisher-zh 的 [MIT 许可证](licenses/dissertation-polisher-zh-MIT.txt)。作者署名、第三方通知及适用范围见 [NOTICE](NOTICE.md)。

## 验证与适用范围

`evals/` 提供合成案例与验收要求。技能是供 Agent 执行的写作流程，实际读取和编辑能力取决于可用工具；安装成功、结构校验和个别案例审阅均不能证明所有格式、所有模型或全部学科场景下的效果。未读取或未验证的材料应明确说明，不以任意评分替代事实判断。
