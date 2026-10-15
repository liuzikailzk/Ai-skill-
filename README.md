# AI Skill 双端备份

保存资产、影视剧本分镜、漫画分镜三套Skill的完整文件，来源为已保存的GPT技能云端。

| Skill | 文件 |
|---|---|
| 资产 | [script-visual-assets](skills/script-visual-assets/SKILL.md) |
| 影视分镜 | [script-video-shot-director](skills/script-video-shot-director/SKILL.md) |
| 漫画分镜 | [manga-reasoning-storyboard](skills/manga-reasoning-storyboard/SKILL.md) |

## 时间安排

- 每天北京时间05:00执行学习审计，包括周末。
- 周五先巩固并提交待审更新，等用户明确确认。
- 每周六北京时间05:00，在同次任务中先做GPT技能云端自检与GitHub完整备份，再做每日三次审计。未获确认的新方法不发布；无获批变化仍核验最近已确认版本，不伪造升版。
- 备份沿用完整目录、历史、版本/修订、逐文件校验清单、旧提交备份及实际核验回执格式。

## 每周更新规则

周五先完成巩固、去重、证据审计和回测，提交明确变更，等用户确认本批没问题后再更新。两个位置是GPT自己的技能云端与本GitHub仓库，仍是三套Skill。未获确认，两端正式方法与版本保持不变。

每次先备份，依次保存GPT云端和GitHub；两端实际回读、文件与版本核验都通过，才报告“已经保存完好”。失败主动诊断、修复并重新验证，不等用户追问，也不虚报成功。完整规则见[双端保存约定](skills/script-video-shot-director/references/dual-save-policy.md)。

## 清单与历史

- [完整文件清单](registry/latest.json)：源提交、版本、修订、逐文件SHA-256与Git blob SHA。
- [重建前备份](registry/rebuild-backup.json)：原main提交及备份分支；旧文件保存在`backup/pre-rebuild-20261013-2104`和Git历史，main当前内容已按用户要求重建。
- 各Skill的`history/`保留修改前原件，`references/learning-log.md`记录修订。
- V1.0.0是历史基线；candidate、observing、active以审计记录为准。把文件备份到仓库不等于技巧转正。
- 本次同步不证明其他聊天或制作会话已加载这些文件。不要恢复旧仓库的GitHub Actions定时监控。

## 文件自检

在完整仓库副本运行：`python3 tools/verify_backup.py`。该命令逐文件检查完整性、清单和校验值；它不替代两端真实回读，也不证明技巧效果。



## 当前新增学习与资讯规则｜SCOPE-NEWS-20261014-01

每天北京时间05:00必检最新AI资讯与市场新技术、新工具、新功能、新技能/工作流，并输出简明报告。AI提示词、分镜提示词、构图/镜头/调色美学、角色情绪神态描写等开放选题，其他学习方向不设严格轮换或配额。原3次技巧审计保留，另设每日1次资讯查询单独记账。周五用户确认和周六05:00自检备份保留；资讯不自动转正。完整新增规则见[每日资讯规则](skills/script-video-shot-director/references/ai-news-policy.md)，从2026-10-15 05:00的同一任务完整执行。

本次只公开新增规则，不上传完整私有Skill正文和每日审计原始快照；GPT云端已保存的新增规则与这三份规则逐文件核验，原公开文件不删。


## 当前报告模板与最终奖惩｜REPORT-CREDIT-20261014-01

每日审计必须交付完整八模块，含证据矩阵、反证与复现、七问逐答、时效、三票状态、版本与原始查询留痕。缺模块打回重审；基础技巧检索3次不因奖惩改变，独立资讯扫描保留，绝不处罚无合格入库。

新奖励：完整审计空手+3；S一手+1；明确反证避免误入库+2；主动发现active过期/错误+3；观察30天后实验有效+2；复现且用户采纳转正+2。轻度扣1补齐重审；中度冻结3天扣3并说明偏差；重度冻结7天、抽检3个Skill包、信用余额清零。一次真实评分差>10即复盘校准、暂停新增入库3天。兑换10点额外验证、15点优先迭代、20点申请全库专项排查。

细则：[固定报告模板](skills/script-video-shot-director/references/daily-report-template.md)、[最终奖惩](skills/script-video-shot-director/references/credit-policy.md)。最新控制文件优先于旧正文中冲突分值；不删除旧历史、不追溯制造积分。云端与GitHub本次核验范围是新增控制规则，不称全包实时镜像。


## 当前暂存与正式库规则｜PENDING-REVIEW-20261015-01

[pending-review/](pending-review/README.md)保存每日候选、完整八模块报告、证据矩阵和human-brief.txt，包括证据不足不入库的日期，并同步GitHub以便恢复。暂存及archive/不供创作直接使用。指定候选获用户人类票后才合并skills/、升版、同步并归档；rejected同样注明原因永久归档。本条覆盖旧批次不上传每日审计的范围限制。恢复入口为未合并日期目录、三套版本与审计索引，以及[共用积分台账](skills/script-video-shot-director/references/audit/global-state.json)。本次只建立规则和目录，不补造10-13至10-15的审计记录；云端同步结果单独见[回执](registry/receipts/PENDING-REVIEW-20261015-01.json)。
