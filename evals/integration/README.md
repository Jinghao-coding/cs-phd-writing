# 可复现的多文件任务

project是独立构造的共享对象回收教学工程；表中合成值不是真实系统实测。含两个章节、两个编译入口、符号、伪代码、结果表、旧版材料及当前项目说明。整个reclamation-teaching项目属开发集；不与相邻段落拆分为保留样本。

| 任务输入 | 范围 | 执行目标 |
| --- | --- | --- |
| [I1](tasks/I1.md) | 研究章为主，允许必要摘要/记录同步 | 实际修订 |
| [I2](tasks/I2.md) | 所有文件只读 | 当前启用内容审阅 |
| [I3](tasks/I3.md) | 所有文件只读 | 入口、版本与阅读范围 |
| [I4](tasks/I4.md) | 仅研究章方法部分 | 从旧记录恢复并保护作者新稿 |

任务输入不揭示全部问题。评价者使用[独立验收依据](expected/rubric.md)与[范围配置](expected/scope.json)；执行者不读这些文件。

从技能根目录运行：

```bash
python3 scripts/run_integration.py prepare /tmp/cs-phd-I1-current --task I1 --variant current
# 给Agent的输入仅为上述目录的 task.md、project/、skill/。
# 在project中执行任务，把最终回复原样保存到run根目录的response.md。
python3 scripts/run_integration.py collect /tmp/cs-phd-I1-current --model '实际模型ID' --method '实际宿主及调用方式' --build
```

prepare拒绝覆盖已存在的运行目录。`--variant none`不放技能并去除请求中的技能调用语句；`--variant /path/to/previous-skill`从固定旧版本目录复制。三种条件都排除技能中的evals及成稿示例，避免答案泄露；技能引用这些路径时按缺失处理，不回到安装目录找答案。其余任务、工具和模型保持一致。没有模型调用内置于脚本；可用宿主Agent或已授权CLI执行，不能将prepare标为Agent运行完成。

collect输出manifest/checks、实际output.patch及candidates.json；可选XeLaTeX两遍构建使用-no-shell-escape且产物位于run/build。收集失败会返回非零；它不评价中文含义，不因候选存在判错。I2/I3禁止构建时不传--build。`response.md`和评价者另写的[运行记录](run-record-template.md)须一并保存。公开运行包前检查内容许可和私人路径；输入和技能清单的SHA256支持复查，运行宿主/模型自述单独登记。

作者修改保护的静态样例检验旧记录与当前稿件冲突；它不模拟两个进程同时写文件。真实并发保护另需宿主支持，不能从此样例通过推断并发安全。
