# 仓库维护入口

修订：MODULAR-RETRIEVAL-20261024-01。先确认本次是索引、版本、归档、记账还是完整性检查，只读对应规则和数据。用户持续授权同类维护PR；本批首步检索与读取分流已经明确获准，完成备份、PR差异审查、合并及main逐文件回读，不再重复确认。授权不替代技术/复现/人类票，不授权付费生成。

固定使用V1.次.修三段非负整数，主版本1保持不变；第三段不限一位，1.0.9→1.0.10，不自动进位。日常目录/索引/读取/规则治理、提示词或描述优化、案例及问题整理，若改变现行执行内容，只升修订号；纯记录且不改执行内容不空升版。只有新增经过实际验证的制作能力，满足既有三票并经周五汇总和用户明确确认后才升次版本，修订归零；不因每周考核、治理规模或文件数量升次版本。保留所有已发布版本和原始历史，不倒改编号。

所有新提交、PR与合并标题带V主.次.修；实际执行规则变化按版本政策处理，纯记录不空升版。先固定main并核验备份，不强推、不删历史、不覆盖并发变更。索引不新增积分，不改变评价、open问题或候选状态。GitHub main唯一可信；不读写旧云端。

维护不启动每日检索或创作。根入口第0层，只读取选中的第1层文件，不自动展开所有链接。源文件变更时同步更新索引摘要/标签/哈希，执行检索验证；不复制原文到索引。

用户触发版本检查并刷新当前制作时，按[强制刷新规则](skill-refresh.md)和任务涉及Skill入口处理；不要把该请求降为只报版本，也不要因命令措辞自动递增仓库版本。

## 按事项选择

- [版本、提交标题和发布](../registry/version-policy.json)
- [备份、PR、合并和回读](shared/dual-save-policy.md)
- [月底或手动暂存清理](../pending-review/cleanup-policy.json)
- [仅记账时读取奖惩](../skills/script-video-shot-director/references/credit-policy.md)
- [仅认可归档时读取](shared/case-ingestion-policy.md)
- [案例记录字段](shared/case-record-template.md)
- [引用深度与历史缺口](../registry/runtime-policy.json)
- [唯一来源与通道事实](../pending-review/channel-policy.json)

发布前运行 tools/verify_backup.py、tools/verify_versions.py、tools/query_knowledge.py --validate 及变更对应测试；引用变动再运行 tools/check_references.py。保留45条历史归档缺口，不找回或造占位。验收报告只描述真实完成，不把入口减小当实际Token或生成效果提升。
