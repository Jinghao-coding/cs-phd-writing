# 历史导航（2026-10-04）

先前摘要使用80 KiB。旧记录称“读者退出时无需更新引用计数”。作者随后已在研究章手工更正这句话；继续任务时应读取当前文件，不恢复旧句。

| 依据 | 来源 | 使用位置 | 状态 |
| --- | --- | --- | --- |
| R1 峰值空间 | tables/results.tex，教学合成值 | abstract.tex；chapters/reclaim.tex 结果节 | 2026-10-05 已逐处核验：摘要同步为轨迹W的72 KiB，相对基线100 KiB降低28%；研究章原有72 KiB及28%正确，保留。结论限定于W，未推广至轨迹V。 |
| A1 回收条件 | algorithms/reclaim.tex | chapters/reclaim.tex 方法段 | 2026-10-05 已核验：释放条件更正为对象已退役且引用计数为零，与算法及作者补充一致；保留读者退出临界区后递减引用计数的作者补充。 |
| 符号 $r_i$ | shared/notation.tex；algorithms/reclaim.tex | chapters/reclaim.tex 方法段 | 2026-10-05 已核验：将等待时长更正为对象 $i$ 当前的读者引用计数，与符号约定及算法输入一致。 |
