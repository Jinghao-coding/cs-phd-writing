# Chinese PhD Writing

An agent skill for evidence-based Chinese PhD dissertation writing and review.

面向中文博士学位论文的写作与审阅 Agent Skill。以真实研究为依据组织章节，检查中文语义、事实、术语、论证和跨章一致性。

## 能做什么

- 把多项研究组织成有明确问题和证据的学位论文。
- 逐句检查主谓宾搭配、指代、语序、因果与比较关系。
- 核对事实和术语依据，防止改写改变技术含义。
- 清理防御性、宣传性和写作过程表述，保留必要推导与研究条件。
- 接入当前论文的学校规范、范文分析及个人偏好。

学校、作者、题目、论文来源和篇幅目标保存在论文项目中。通用技能包不携带这些个人配置，也不默认指定学校或研究方向。

## 安装到 Codex

将仓库克隆到 Codex 的用户技能目录：

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
git clone https://github.com/Jinghao-coding/chinese-phd-writing.git "${CODEX_HOME:-$HOME/.codex}/skills/chinese-phd-writing"
```

也可以下载仓库，将完整目录命名为 `chinese-phd-writing/` 后放入用户技能目录（通常为 `~/.codex/skills/`）。保留 `references/`、许可证和其他随包文件。

开启一个新会话以刷新技能发现。也可以在现有会话中提供 `SKILL.md` 路径，明确要求读取后使用。

## 使用示例

```text
使用 $chinese-phd-writing，审阅第三章，只给修改建议。
重点检查中文主谓宾、指代、术语和实验结论，不改源码。
```

```text
使用 $chinese-phd-writing，根据材料索引和已完成研究调整大纲。
说明每章解决的问题及证据，不按论文数量决定章数。
```

```text
使用 $chinese-phd-writing，把这段英文方法说明改写成中文博士论文表述。
保留技术含义、公式和引用，不能补造事实或术语。
```

项目可提供 `docs/thesis-writing-profile.md`，或在 `AGENTS.md` 中指定配置位置。详见 [项目接入](references/project-profile.md)。缺少配置不影响已经明确的局部任务。

## 来源与许可证

基于 [doctoral-dissertation-skills](https://github.com/syc9336-rgb/doctoral-dissertation-skills) 和 [dissertation-polisher-zh](https://github.com/ChipsAhoyM/dissertation-polisher-zh) 改写整合。

本项目采用 Apache-2.0，保留上游 Apache-2.0 与 MIT 通知。参见 [NOTICE](NOTICE.md) 和 [改写记录](references/upstream-adaptation.md)。

## 验证与限制

`evals/` 提供合成案例和验收要求。结构校验只能检查技能文件是否有效；案例审阅不能证明所有学科、长篇论文或所有模型下的表现。规则用于辅助判断，不承诺检测全部事实错误、保证论文质量或替代作者与导师审阅。
