# v0.7.0 发布核验

日期：2026-10-05。版本0.7.0，使用Python标准库工具；本地环境为macOS arm64、Python 3.14.8。

## 本轮实际检查

- 升级SKILL与双语README的当前版本声明，整理正式变更记录；历史版本及运行快照保留原值。
- 将版本冲突回归改为读取当前声明后注入冲突，不再写死0.6.0。
- 执行 `python3 -m unittest discover -s evals -p 'test_*.py'`：36项通过。
- 独立example已移除，当前包保留真实多文件任务、验收依据与六次实际运行证据。

此前实现验证见[2026-10-05记录](validation-2026-10-05.md)，其中工具边界、六次独立任务、分项判断和构建日志均有实际产物。行为执行使用当时保存的未发布技能快照；发布时只同步版本与说明，未将这些运行重新命名为新模型测试。

## 安装包与使用

发布附件包括cs-phd-writing-v0.7.0.zip、file-manifest.json和SHA256SUMS.txt。ZIP使用单层cs-phd-writing目录，内容取自发布提交；manifest记录提交和逐文件摘要。解压后可运行：

```bash
python3 cs-phd-writing/scripts/validate_repo.py
```

维护者在发布前从ZIP重新解压，核对manifest并执行上述完整校验。安装使用解压后的cs-phd-writing目录，或按README中的skills CLI命令更新。已有项目配置按需合并使用位置字段；修订检查保留protected_changes、number_changes和terminology_candidates，新位置及候选字段采用schema_version=2。
