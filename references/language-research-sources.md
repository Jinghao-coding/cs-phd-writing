# 语言修订的研究与工具来源

核对日期：2026-10-05。本文记录方法参考与本技能的采用方式，配套[版本清单](language-source-manifest.json)保存18个仓库README的固定提交和摘要；旧上游改写记录及许可证继续保留。以下流程和中文教学案例独立编写，不捆绑第三方模型、代码或语料。来源资料用于分析，不构成运行本技能所必需的依赖。

## 写作技能：采用具体判断，保留任务自由度

| 来源与本轮阅读范围 | 内化到本技能的做法 | 取舍 |
| --- | --- | --- |
| [Research-Paper-Writing-Skills](https://github.com/Master-cai/Research-Paper-Writing-Skills)，本地安装入口及反向提纲规则 | 由段落判断、证据及作用还原论证，见[衔接与转写](cohesion-and-translation.md) | 不要求每次润色交付提纲或固定段落模板 |
| [Orchestra systems-paper-writing](https://github.com/Orchestra-Research/AI-research-SKILLs/blob/main/20-ml-paper-writing/systems-paper-writing/SKILL.md)，入口的读者理解、机制与评估组织 | 检查概念前提，连接观察、决策和实验，见[修订流程](revision-workflow.md) | 不移植会议论文页数、固定摘要句数或首屏图要求 |
| [Orchestra ml-paper-writing](https://github.com/Orchestra-Research/AI-research-SKILLs/blob/main/20-ml-paper-writing/ml-paper-writing/SKILL.md)，信息位置与表达原则 | 英中转写时重组信息、恢复主体，保留命题 | 不把英文语序经验设为中文硬约束 |
| [ieee-acm-paper-writing](https://github.com/huguryildiz/ieee-acm-paper-writing)，证据、humanize与审阅规则 | 逐项核对数字、基线、条件和情态强度 | 允许按任务查证补充材料，不要求所有技术词逐字出现在输入中 |
| [K-Dense scientific-writing](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/scientific-writing/SKILL.md)，证据定位与一致性规则 | 重要论断关联位置，核对摘要、正文和图表中的数字 | 沿用项目记录，不为单句创建大型证据台账 |
| [PaperJury](https://github.com/u7079256/paperjury-codex)，问题与关闭条件 | 位置、具体影响、修复完成条件 | 不默认多代理裁决 |
| [PaperSpine](https://github.com/WUBING2023/PaperSpine)，本地安装的贡献与证据组织 | 检查段落是否支持本章研究问题 | 不移植全套阶段、固定文件或确认流程 |
| [PaperOrchestra](https://github.com/Ar9av/PaperOrchestra)，本地refinement与autorater入口、公开README | 修订前后成对比较，质量与含义分别评价 | 文献选择F1、LLM分数不能替代真实性、论断支持和人工判断 |
| [Humanizer](https://github.com/blader/humanizer)，公开说明 | 将空泛、重复、自评转换为可定位问题 | 不检测作者身份，不以口语化或人格化作为学术写作目标 |

本地安装的研究技能快照与远程最新README版本可能不同。所用本地快照包括 Research-Paper-Writing-Skills `77e7c2c1ba06f7d71844873147665437a03aac1b`、ieee-acm-paper-writing `ff1b1ed91ff4e0bb0225834b2c3b2f50598fbf67`、PaperJury `6383d0ca3c1b6cec3e9c8d7fda75092d67857768`、PaperSpine `1fe46f0e76aab800db381b0a0c392cebe14d86bf`、PaperOrchestra `798f03a14ce582607ba2742d025691f226470641`。本地个人系统写作技能仅用于比较需求，通用包不收录私人材料或本机路径。

## 修订研究：用错误类型、修改意图和真实修订设计评估

| 研究 | 核对材料与范围 | 采用方式 |
| --- | --- | --- |
| [NaSGEC，Findings ACL 2023](https://aclanthology.org/2023.findings-acl.630/) | 摘要、仓库说明；中文母语者多领域，含科学写作，多参考答案 | 区分领域、母语写作与学习者错误；优先建立系统领域案例，避免将通用模型效果视为领域效果 |
| [MuCGEC，NAACL 2022](https://arxiv.org/abs/2204.10994) | 摘要及[仓库](https://github.com/HillZhang1999/MuCGEC)说明；学习者语料与ChERRANT | 多参考答案与编辑级评价，保留合理异写；不要求字面一致 |
| [FCGEC，Findings EMNLP 2022](https://aclanthology.org/2022.findings-emnlp.137/) | 摘要及[仓库](https://github.com/xlxwalex/FCGEC)说明；细粒度检测、识别、纠正 | 先定位再分类，区分语病、歧义、论证缺口和风格 |
| [IteraTeR，ACL 2022](https://aclanthology.org/2022.acl-long.250/) | 摘要、仓库与dataset/README的真实修订示例 | 明确修订意图，区分表达优化与含义改变；真实示例见[案例分析](../evals/real-revision-analysis.md) |
| [ARIES，ACL 2024](https://aclanthology.org/2024.acl-long.377/) | 摘要、仓库数据格式、对齐与许可说明 | 将意见与实际改动对应，评价问题是否解决；作者接受的改动仍需核对科学证据 |

这里采用评估设计，未将整个数据集打包。需扩展真实样本时，在项目允许的外部数据目录保存数据、版本、记录ID、领域、许可和划分；评估正文不要进入通用技能。IteraTeR Plus/v2的数据获取有单独条件，遵循其dataset说明；ARIES代码与数据分别按Apache-2.0和ODC-BY 1.0处理。GitHub API中的NOASSERTION或unspecified不等于可随意转载；以具体内容的许可为准。

## 原始写作参考与工具

- [Gopen科学写作资料](https://georgegopen.com/scientific-writing-articles/)：从读者预期分析信息位置，转化为主题承接检查。
- [Gernot Heiser技术写作指南](https://cgi.cse.unsw.edu.au/~gernot/style-guide.html)：参考技术论述的清晰性与读者理解；不将单篇会议写作经验转换为学校规范。
- textlint、中文技术规则集、Vale、pycorrector和LanguageTool的采用范围、配置与人工核对入口集中在[语言工具](language-tools.md)。它们可提供候选诊断；本技能的语义核对与证据来源保持独立。

维护时记录新增规则解决的实际问题和案例，不因参考项目升级就整包覆盖。公开真实材料只作必要短引或带定位的转述；原文权利归其权利人，许可证分别适用。

## systems-paper-writing 的进一步核对

2026-10-05读取该项目入口v1.1.0及`references/section-blueprints.md`，并回查[Irene Zhang原文](https://irenezhang.net/blog/2021/06/05/hints.html)和[Levin与Redell原文](https://www.usenix.org/conferences/author-resources/how-and-how-not-write-good-systems-paper)。将主张范围、问题—设计—证据对应、关键替代方案、总体与机制评价及可迁移认识落实到[系统上下文表达](systems-context-expression.md)。

原文的重复结论建议改为正文与图注的信息分工；固定页数、摘要句数、贡献数和必须首屏配图不作为通用规则。新意可能来自问题、环境、机制或经验认识，不要求统一写成性能优越性。Levin与Redell列出的Focus也纳入检查。该上游所列样本年份、获奖、会议页数与期限不转录为已核验事实；投稿时直接查当届官方要求。问题—设计的对应可用于审阅，不强制改写成一一对应清单。
