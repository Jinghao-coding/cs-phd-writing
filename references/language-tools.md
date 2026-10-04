# 可选语言检查工具

工具用于发现可定位的候选问题。优先使用项目已有环境；没有工具时按指南完成编辑。安装、下载模型和向远程服务传输正文不属于普通润色的默认步骤。

## 轻量本地检查

本技能提供标准库脚本，只读源文件，比较公式、引用/标签/交叉引用及数字，并根据项目词表查找候选异名：

```bash
python3 <skill-dir>/scripts/check_revision.py before.tex after.tex
python3 <skill-dir>/scripts/check_revision.py before.tex after.tex --glossary glossary.json
```

输入可以是纯文本、Markdown或LaTeX。脚本按原始文本比较常见数学定界符、equation/align/gather/multline环境及标准引用宏；项目自定义宏、注释中的文字和数值对应关系由编辑器diff与语义核对补查。程序输出JSON；`protected_changes`是需核对的公式/引用/代码差异，`number_changes`是数字差异，`terminology_candidates`是词表候选。合法的技术更正或等价数值换算也可能产生差异。输出没有“语义通过”或“质量总分”；变更位置可用编辑器diff查看。命令退出0表示分析完成，退出2表示输入或配置错误。

项目词表示例：

```json
{"terms": [{"preferred": "吞吐率", "variants": ["吞吐量"], "reason": "本项目按单位时间完成任务数定义"}], "allow": ["历史接口吞吐量"]}
```

这只是项目定义示例；吞吐量在其他上下文可以成立。`allow`仅排除命中的完整短语，不全局禁用该词。词表存放在当前项目，不写入通用技能的默认禁词库。标点、单位和引文显示服从当前学校及文献后端要求。

## 外部工具如何接入

| 工具 | 适用输入与配置 | 如何消费结果 |
| --- | --- | --- |
| [textlint](https://github.com/textlint/textlint) | 项目已有的Markdown/文本检查；显式选规则 | 将规则ID、位置、建议作为候选，按校规筛选；不默认执行自动修复 |
| [中文技术规则集](https://github.com/darkyzhou/textlint-rule-preset-zh-technical-writing) | 借鉴成对标点、混排等规则组织；仓库已归档 | 逐项审查单位和空格规则，不能整体套到LaTeX科学写作 |
| [Vale](https://github.com/vale-cli/vale) | 现有样式包与项目术语词表 | 适合名称和约定一致性；保留认可译名、代码与引用中的例外 |
| [pycorrector](https://github.com/shibing624/pycorrector) | 可选本地中文错字/纠错候选；沿用明确模型版本 | 先标出专名、公式和缩写；采纳前读上下文，记录误报 |
| [LanguageTool](https://github.com/languagetool-org/languagetool) | 可选英文摘要语法检查；明确本地或远程运行 | 核对技术词、比较对象和情态含义，不自动改全文 |

已有项目配置时，可使用其既有textlint命令或`vale <text-file>`检查范围内的文本；参数和解析器随已安装版本确认。不要把原始TeX直接交给不理解TeX的纠错器再覆盖源文件。

为外部工具准备临时文本时，应建立段落/行号映射，保护数学、命令、代码、URL、引用键与专名。工具只生成建议，由编辑流程逐条应用回原文件；抽取破坏上下文时回到原段核查。临时文本留在项目允许的临时目录，完成后清理。

## 有效性判断

在当前领域的错误样本与正确样本上分别检查：修复了哪些问题，误报了哪些术语，是否损坏格式。误报高的规则禁用或缩小作用域。模型下载大小、性能或支持语言以实际版本为准；不把安装成功当作写作效果。评估方法见[修订评估](../evals/revision-evaluation.md)。
