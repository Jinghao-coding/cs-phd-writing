# 从压缩方法到中文研究章

本目录全部为本项目独立构造的教学材料，按仓库 Apache-2.0 许可分发。数值是用于练习论证的合成值，不是真实系统实测。没有使用作者私人论文、学校材料或未公开结果。

先读 [压缩方法](inputs/paper.md)、[定义与假设](inputs/model.md)、[伪代码](inputs/algorithm.txt)、[合成结果](inputs/results.csv)和[结果口径](inputs/results-notes.md)，再看[前文定义](project/background.tex)与[实际成稿](output/chapter.tex)。[来源映射](source-map.md)逐项区分原有说明、可推导解释和待验证判断；[审阅记录](review.md)保存实际检查。

从 project 目录构建：

```bash
xelatex -no-shell-escape -interaction=nonstopmode -halt-on-error main.tex
xelatex -no-shell-escape -interaction=nonstopmode -halt-on-error main.tex
```

教学组织选择是场景→约束→贯穿示例→事件与状态→取舍→结果问题；其他研究章按其证据与贡献组织，无固定篇幅或图数。

已构建的[4页PDF](output/example.pdf)包含前文定义和研究章。
