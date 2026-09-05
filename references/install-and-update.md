# 安装、更新与版本发布

Codex 与 Claude Code 使用仓库根目录的同一份 `SKILL.md` 和配套资源。`agents/openai.yaml` 提供 Codex 显示信息；论文资料和个人配置放在论文项目内。

## 安装方式

### 使用 skills CLI

需要 Node.js 与 npm。按目标平台选择，`--global` 表示用户级安装；省略该选项则安装到当前项目。

```bash
npx skills@latest add Jinghao-coding/cs-phd-writing --skill cs-phd-writing --agent codex --global
```

```bash
npx skills@latest add Jinghao-coding/cs-phd-writing --skill cs-phd-writing --agent claude-code --global
```

需要两个平台时，可使用 `--agent codex claude-code`。具体目录和安装方式由安装器处理。参数依据 [skills CLI](https://github.com/vercel-labs/skills)。

### 使用 Git 独立克隆

macOS / Linux 的 Codex 用户目录示例：

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
git clone https://github.com/Jinghao-coding/cs-phd-writing.git "${CODEX_HOME:-$HOME/.codex}/skills/cs-phd-writing"
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
| Codex | 默认 `~/.codex/skills/`；设置了 `CODEX_HOME` 时使用其下的 `skills/` | `.agents/skills/` |
| Claude Code | `~/.claude/skills/` | `.claude/skills/` |

`~` 代表用户目录；Windows 手动复制时使用实际用户目录（PowerShell 中为 `$env:USERPROFILE`）。若环境自定义了技能路径，遵循其配置。Claude Code 的目录与调用方式参见 [官方技能文档](https://code.claude.com/docs/en/skills)。

## 如何获知新版本

在 [仓库](https://github.com/Jinghao-coding/cs-phd-writing) 的 **Watch → Custom → Releases** 中订阅发布通知。维护者发布 Release 后，GitHub 按使用者的账户通知设置投递；仅下载或安装技能不等于订阅。

每个发布版本提供版本号、[变更记录](../CHANGELOG.md) 和下载包。GitHub 支持只订阅 Release 事件，参见 [GitHub Releases 说明](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases)。维护者不能据此知道每个使用者是否已经看到或安装了更新。

## 如何更新已安装技能

| 原安装方式 | 更新方式 |
| --- | --- |
| skills CLI 安装 | 用户级安装执行下面的指定技能更新命令；项目级安装改用 `--project` |
| Git 独立克隆 | 在该技能自身的 Git 仓库中拉取更新；存在本地修改时先处理差异 |
| ZIP / 手动复制 | 从 Release 下载新版，保留旧版备份后替换完整技能目录 |
| 链接到自己维护的源码 | 更新链接指向的实际源码；发布者另外将审核后的技能文件提交到公开仓库 |

```bash
npx skills@latest update cs-phd-writing --global
```

Git 克隆安装的 Codex 示例，先检查该目录确实是独立仓库，避免误操作父目录中的论文仓库：

```bash
cs_phd_skill_dir="${CODEX_HOME:-$HOME/.codex}/skills/cs-phd-writing"
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
