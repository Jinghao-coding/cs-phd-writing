# CS PhD Writing

An agent skill for writing and reviewing computer science PhD dissertations in Chinese.

面向计算机学科的中文博士学位论文写作与审阅。以真实研究为依据组织章节，检查中文语义、事实、术语、论证和跨章一致性。

基于 [doctoral-dissertation-skills](https://github.com/syc9336-rgb/doctoral-dissertation-skills) 和 [dissertation-polisher-zh](https://github.com/ChipsAhoyM/dissertation-polisher-zh) 改写整合，保留上游署名与许可证。

## 能做什么

- 把多项研究组织成有明确问题和证据的学位论文。
- 逐句检查主谓宾搭配、指代、语序、因果与比较关系。
- 核对事实和术语依据，防止改写改变技术含义。
- 清理防御性、宣传性和写作过程表述，保留必要推导与研究条件。
- 接入当前论文的学校规范、范文分析及个人偏好。

学校、作者、题目、论文来源和篇幅目标保存在论文项目中。通用技能包不携带这些个人配置，也不默认指定学校或具体研究方向。

## 安装到 Codex

将仓库克隆到 Codex 的用户技能目录：

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
git clone https://github.com/Jinghao-coding/cs-phd-writing.git "${CODEX_HOME:-$HOME/.codex}/skills/cs-phd-writing"
```

也可以下载仓库，将完整目录命名为 `cs-phd-writing/` 后放入用户技能目录（通常为 `~/.codex/skills/`）。保留 `references/`、许可证和其他随包文件。

开启一个新会话以刷新技能发现。也可以在现有会话中提供 `SKILL.md` 路径，明确要求读取后使用。

## 使用示例

```text
使用 $cs-phd-writing，审阅第三章，只给修改建议。
重点检查中文主谓宾、指代、术语和实验结论，不改源码。
```

```text
使用 $cs-phd-writing，根据材料索引和已完成研究调整大纲。
说明每章解决的问题及证据，不按论文数量决定章数。
```

```text
使用 $cs-phd-writing，把这段英文方法说明改写成中文博士论文表述。
保留技术含义、公式和引用，不能补造事实或术语。
```

项目可提供 `docs/thesis-writing-profile.md`，或在 `AGENTS.md` 中指定配置位置。详见 [项目接入](references/project-profile.md)。缺少配置不影响已经明确的局部任务。

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

## 验证与限制

`evals/` 提供合成案例和验收要求。结构校验只能检查技能文件是否有效；案例审阅不能证明所有学科、长篇论文或所有模型下的表现。规则用于辅助判断，不承诺检测全部事实错误、保证论文质量或替代作者与导师审阅。
