# 压缩方法（独立构造的英文教学材料）

The reclaimer releases a retired object only when its reference count reaches zero. Removal from the index prevents new references. Retirement and the last reader release both invoke the reclamation check under the same lock. This event-driven check avoids waiting for the next periodic scan. In synthetic trace W, the peak retained space is 72 KiB, compared with 100 KiB for periodic scanning; in trace V, the values are 110 and 100 KiB. These values include bookkeeping space.

本段是修改前材料，不代表已发表论文。详细假设、状态、伪代码与合成数据分别保存在同目录文件中；研究章可补足这些已提供而压缩段落省略的信息。
