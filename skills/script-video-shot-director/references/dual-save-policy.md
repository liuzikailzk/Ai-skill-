# GitHub保存与PR发布规则

现行修订：THREE-SKILL-INTEGRATION-20261017-01。本文件名保留以兼容已有引用；旧双端规则已被用户2026-10-17指令撤销。
1. 只读写 liuzikailzk/Ai-skill-；main为唯一可信源。不读取、不写入、不修复、不重建任何旧云端技能包。
2. 开始工作先读取根 pending-review/channel-policy.json、本包规则及影视包唯一主账。查询前登记GitHub配额并回读，失败停查询。
3. 修改前固定main提交并创建backup分支或完整可恢复快照，核验涉及文件路径和Git blob SHA。历史日志、原认可和原失败不改写。
4. 暂存、审计、案例更新经PR检查后可自行合并；任何核心版本升版PR须用户明确批准该PR后再合并。自动合并权不等于方法入库票。
5. 保存必须核对PR、预期head和合并结果，重新读取main逐文件比对。审阅分支保存成功只算待发布，不声称main生效；并发时重读合并，不强推。
6. 每日实际产出保存在 pending-review/YYYY-MM-DD/，包含审计、真实候选、human-brief及迁移矩阵。无审计/暂停日不造报告，不重跑历史检索。
7. 周六同次任务在GitHub固定快照并保留独立本地恢复备份，不再做云端自检；原05:00及暂停状态不因此改变，不新增任务。
8. 发布失败保留草稿、具体工具/分支/报错与回读结果；不能将本地commit或Everything up-to-date称为成功。
详情见[cross-skill-policy.md](cross-skill-policy.md)，实际授权以main通道规则为准。
