# 安装、更新与版本发布

支持Agent Skills的工具使用仓库根目录的同一份 `SKILL.md` 和配套资源；可通过 [skills CLI支持列表](https://github.com/vercel-labs/skills#supported-agents)确认当前工具及安装标识。`agents/openai.yaml` 提供 Codex 显示信息；论文资料和个人配置放在论文项目内。

安装入口：[中文 README](../README.md) · [English README](../README.en.md)。2026-10-04 按 [Codex 官方文档](https://developers.openai.com/codex/skills/) 与 [Claude Code 官方文档](https://code.claude.com/docs/en/skills) 核对下列目录。既有安装先确认实际位置，不因文档更新自动迁移或重复安装。

## 让Agent识别环境并安装

可直接使用README的[安装请求](../README.md#quick-start)。执行安装的Agent应先识别当前宿主和已有安装，再查宿主配置或官方说明确定技能目录；目录未知时不能直接套用Codex或Claude Code路径。

原生支持技能时，沿宿主已有管理方式或skills CLI安装完整目录；多工具共享安装优先复用同一份源文件，仅在宿主支持时使用链接，避免为每个工具重复创建Git仓库。安装现有技能时先读取本地状态，保留作者修改，沿原安装方式更新。

没有原生技能发现机制但能读取文件时，将完整包放在一个稳定目录，并在任务中明确要求读取该目录的SKILL.md及相关指南。只有文本输入能力时，可向其提供当前任务所需指南内容；本地读写和编译由用户或外部工具完成。不要把存放文件等同于宿主已经注册技能。

安装后分别确认文件存在、技能名称与版本、宿主实际发现或加载结果，并给出该宿主的调用方式。按宿主需要刷新技能或开启新任务。技能自身无需模型服务；修订检查脚本需要Python，skills CLI需要Node.js/npm，缺少运行时可改用Release ZIP安装。本文列出的Codex/Claude Code目录是具体示例，其他工具以当时配置和官方说明为准。

2026-10-05核对了 [Agent Skills介绍](https://agentskills.io/home)及 [skills CLI官方README](https://github.com/vercel-labs/skills)的跨工具安装入口与共享目录方式。

## 安装方式

### 使用 skills CLI

需要 Node.js 与 npm。按目标平台选择，`--global` 表示用户级安装；省略该选项则安装到当前项目。

```bash
npx skills@latest add Jinghao-coding/cs-phd-writing --skill cs-phd-writing --agent codex --global
```

```bash
npx skills@latest add Jinghao-coding/cs-phd-writing --skill cs-phd-writing --agent claude-code --global
```

需要两个平台时，可使用 `--agent codex claude-code`。安装器默认通过共享技能目录和链接提供文件；选择 `--copy` 时，各平台获得独立副本，更新时也需要覆盖这些副本。具体目录和安装方式由安装器处理。参数依据 [skills CLI](https://github.com/vercel-labs/skills)。

### 使用 Git 独立克隆

macOS / Linux 的 Codex 用户目录示例：

```bash
mkdir -p "$HOME/.agents/skills"
git clone https://github.com/Jinghao-coding/cs-phd-writing.git "$HOME/.agents/skills/cs-phd-writing"
```

Claude Code 用户目录示例：

```bash
mkdir -p "$HOME/.claude/skills"
git clone https://github.com/Jinghao-coding/cs-phd-writing.git "$HOME/.claude/skills/cs-phd-writing"
```

### 手动复制

从 [Releases](https://github.com/Jinghao-coding/cs-phd-writing/releases) 下载技能 ZIP，解压后将整个 `cs-phd-writing/` 放入目标平台的技能目录。保留 `SKILL.md`、`references/`、`assets/`、许可证及其他随包文件。

| 平台 | 用户级目录 | 当前项目内目录 |
| --- | --- | --- |
| Codex | `~/.agents/skills/` | `.agents/skills/` |
| Claude Code | `~/.claude/skills/` | `.claude/skills/` |

`~` 代表用户目录；Windows 手动复制时使用实际用户目录（PowerShell 中为 `$env:USERPROFILE`）。若环境自定义了技能路径，遵循其配置。Claude Code 的目录与调用方式参见 [官方技能文档](https://code.claude.com/docs/en/skills)。

## 如何获知新版本

在 [仓库](https://github.com/Jinghao-coding/cs-phd-writing) 的 **Watch → Custom → Releases** 中订阅发布通知。维护者发布 Release 后，GitHub 按使用者的账户通知设置投递；仅下载或安装技能不等于订阅。

每个发布版本提供版本号、[变更记录](../CHANGELOG.md) 和下载包。GitHub 支持只订阅 Release 事件，参见 [GitHub Releases 说明](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases)。维护者不能据此知道每个使用者是否已经看到或安装了更新。

## 如何更新已安装技能

| 原安装方式 | 更新方式 |
| --- | --- |
| skills CLI 安装 | 用户级安装执行下面的指定技能更新命令；项目级安装改用 `--project`；复制安装按下文明确指定平台重新安装 |
| Git 独立克隆 | 在该技能自身的 Git 仓库中拉取更新；存在本地修改时先处理差异 |
| ZIP / 手动复制 | 从 Release 下载新版，保留旧版备份后替换完整技能目录 |
| 链接到自己维护的源码 | 更新链接指向的实际源码；发布者另外将审核后的技能文件提交到公开仓库 |

```bash
npx skills@latest update cs-phd-writing --global
```

更新后核对目标平台实际读取的 `SKILL.md` 版本及配套文件。如果使用 `--copy`，或安装器未识别某个平台，重复执行带 `--agent` 的安装命令；保留自己的改动后，再覆盖技能副本。两个平台的复制安装示例：

```bash
npx skills@latest add Jinghao-coding/cs-phd-writing --skill cs-phd-writing --agent codex claude-code --global --copy
```

项目级复制安装去掉 `--global`。2026-09-05 使用 skills CLI 1.5.23 实测时，指定技能的项目更新只刷新了共享目录，Claude Code 的独立副本仍为旧版；明确指定两个平台重新安装可覆盖这些副本。因此，不能只根据安装器的成功提示判断所有平台都已更新。

Git 克隆安装的 Codex 示例，先检查该目录确实是独立仓库，避免误操作父目录中的论文仓库：

```bash
cs_phd_skill_dir="$HOME/.agents/skills/cs-phd-writing"
if [ -d "$cs_phd_skill_dir/.git" ]; then
  git -C "$cs_phd_skill_dir" pull --ff-only
else
  printf '%s\n' '此目录不是独立 Git 克隆，请按原安装方式更新。'
fi
```

从默认分支安装或更新会取得最新源码，可能包含尚未单独发布的修改。需要固定版本时使用对应 Release 下载包，并在论文项目中记录所用技能版本。个人偏好、学校要求和范文笔记留在论文项目中，不通过修改技能包来保存。

更新后重新调用技能；当前任务仍使用旧内容时，明确要求重新读取 `SKILL.md` 及所需参考文件，或开启新任务。更新不会自动替你改写论文。

## 维护者如何发布

1. 在技能源码中修改通用规则或文档，保留上游来源与许可；学校、作者和具体研究配置继续留在论文项目中。
2. 更新 `SKILL.md` 的版本号、改写记录及 `CHANGELOG.md`，说明变化、实际验证和是否需要调整项目配置。修正文档或规则可递增补丁号，新增能力可递增次版本；改变使用方式时写明迁移步骤。
3. 检查技能格式、链接和所影响的行为；涉及安装方式时用隔离目录验证。只把技能文件提交到公开仓库。
4. 针对已验证的提交创建版本标签与 GitHub Release，附上完整技能 ZIP 和校验信息。推送代码本身不是一次 Release 发布。
5. 核对 Release 指向的提交、版本号和附件。订阅者之后可按通知决定是否更新。

发布是明确的维护操作，不由普通论文润色任务自动触发。具体发布操作参见 [GitHub 发布指南](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository)。

本地维护先执行[维护说明](../MAINTAINING.md)中的标准库校验命令；CI运行相同确定性检查。模型行为评测按发布前需要另行执行并保存实际补丁。
