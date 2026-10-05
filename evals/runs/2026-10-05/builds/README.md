# 实际构建证据

当前分发包已按用户要求移除example，本记录保留当时实际构建结果，产物链接指向历史提交。

环境：macOS arm64；XeTeX/TeX Live 2026；本机已有ctex及平台中文字体。使用-no-shell-escape。所有构建由维护者执行，与不编译的Agent任务分开。

| 入口/产物 | 实际结果 | 日志 |
| --- | --- | --- |
| examples/paper-to-chapter/project/main.tex | 两遍成功，4页；逐页查看渲染，公式/引用/表格可读 | [最终日志](example-final.txt) |
| evals/integration/project/main.tex | 两遍成功，3页 | [日志](fixture-main.txt) |
| evals/integration/project/main-full.tex | 两遍成功，4页 | [日志](fixture-main-full.txt) |
| I1-current实际改动在最终字体入口上的确定性重放 | collect --build两遍成功，输入/技能哈希未变，无文件级越界；无新模型调用 | [checks](I1-replay-checks.json)、[日志](I1-replay-build.txt) |

[源文件SHA256](source-sha256.json)对应最终构建输入及示例PDF。重放通过复制原I1-current的三个实际改动文件到新prepare的I1工程，保留最终fixture平台默认字体入口，再执行collect --build。它检查运行器实际构建能力，不冒充新的Agent运行或原Fandol配置构建。

[首次失败](example-first-failure.txt)为Fandol字体缺失。最终工程移除强制fontset=fandol，由ctex选择平台默认已安装字体；没有全局安装或配置修改。最终三份入口日志无未定义引用和Overfull/Underfull提示。PDF见[历史示例产物](https://github.com/Jinghao-coding/cs-phd-writing/blob/6d2b2161928ebd3e01517b5c1a3870df1b0df4bf/examples/paper-to-chapter/output/example.pdf)。
