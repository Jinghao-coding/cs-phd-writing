# 可选语言检查工具

工具用于发现可定位的候选问题。优先使用项目已有环境；没有工具时按指南完成编辑。安装、下载模型和向远程服务传输正文不属于普通润色的默认步骤。

## 轻量本地检查

本技能提供标准库脚本，只读源文件，比较公式、引用/标签/交叉引用及数字，并根据项目词表查找候选异名：

```bash
python3 <skill-dir>/scripts/check_revision.py before.tex after.tex
python3 <skill-dir>/scripts/check_revision.py before.tex after.tex --glossary glossary.json
```

输入可以是UTF-8纯文本、Markdown或LaTeX。退出0表示分析完成，退出2表示文件、编码或配置错误；不表示论文语义正确。文件只读，不自动修复。

### 输出与兼容性

原有 `protected_changes`、`number_changes`、`terminology_candidates` 字段保持可用；schema_version=2新增 `objects`、`local_candidates`、`diff_hunks` 和 `coverage_warnings`。旧消费者可继续读取原字段，新消费者应忽略未知字段。全局数字统计沿用旧口径（包括代码/公式等原始文本中的数字），局部数字只抽取代码、公式和引用以外的区域；这些区域由完整受保护对象覆盖。代码围栏与正文术语排除共享同一识别器。

输入：

```text
before: A为18 ms，B为24 ms
 after: A为24 ms，B为18 ms
```

实际输出的首项摘录（完整输出还含两个对象列表和diff区间）：

```json
{
  "number_changes": {"removed": [], "added": []},
  "local_candidates": [{
    "candidate_type": "local_replacement",
    "object_type": "number",
    "before": {"text": "18 ms", "start": 2, "end": 7, "line": 1, "column": 3, "context": "A为18 ms"},
    "after": {"text": "24 ms", "start": 2, "end": 7, "line": 1, "column": 3, "context": "A为24 ms"},
    "match_basis": "unique_clause_slot"
  }]
}
```

以上为字段摘录，不是完整schema。每个对象含类型、原始文本、起止位置、结束行列、局部子句及所在段落；偏移以Unicode码点从0计、区间左闭右开，行列从1计，制表符计一个字符。CLI用Python文本读取将CRLF/CR规范为LF，偏移对应规范化后的字符串，不是文件字节偏移。位置会因前文编辑移动，不能单靠偏移判断对象搬移。

| 候选类型 | 含义与处理 |
| --- | --- |
| local_replacement | 同类型对象在唯一子句词法槽中替换；核对归属和合法更正 |
| unit_or_marker_changed | 数值相同，支持的单位或百分比标记变化，如12 ms→12 s、25\%→25 |
| context_or_position_changed | 唯一同文本对象的邻近子句发生变化；可能是正常润色或引用支撑语句变化 |
| unmatched_old / unmatched_new | 无可靠一对一匹配；可能是增删、搬移、拆合或修改，保留单侧位置与不确定性 |

匹配先保留文本和子句一致的对象，再尝试唯一子句槽，最后匹配唯一同文本对象。重复对象无法唯一配对时不强行指定归属。完整子句/段落移动可不产生对象候选，位置变化仍见objects和diff_hunks；检查器不能断言移动后科学含义保持。普通表述修改不产生受保护对象的增删，但可能产生中性的上下文候选；不能把它称为对象损坏。等价换算24 ms→18 ms与降低25%仍会报告词法差异。

### 支持范围与人工入口

支持0–3空格缩进的反引号/波浪线围栏、较长闭合围栏和未闭合至文件尾的代码区；正文术语扫描默认跳过这些区域，局部allow短语只屏蔽自身。四空格代码块、列表嵌套围栏、行内代码、LaTeX verbatim/listings/minted未作为代码区域解析，命中需人工区分。

识别常见数学定界符 `$`、`$$`、`\(`、`\[`及equation/align/gather/multline（含星号）环境；识别常见cite系列、label/ref/eqref/autoref/cref/Cref/pageref宏及平衡参数。支持数字的符号、小数/逗号、指数与常见SI/存储单位（具体集合见脚本UNIT）。未支持的单位、自定义宏、TeX注释、条件编译、宏展开、嵌套数学环境以及复杂转义须在编辑器中核对，脚本不是完整LaTeX解析器；未闭合宏参数会给coverage_warnings，空警告不代表结构已全面覆盖。

先在编辑器diff定位候选，再读对象所在段落、相邻定义和来源。确认是合法修改、需更正还是无法判断；保留合法重排与等价表达。词法匹配不能恢复科学归属，语义核对仍按[修订流程](revision-workflow.md)。

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
