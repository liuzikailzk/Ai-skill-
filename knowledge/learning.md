# 学习任务入口

修订：MODULAR-RETRIEVAL-20261024-01。用户已授权首批检索与读取分流；本入口只用于学习审计，不适用于普通制作。

先确定当天实际任务与已完成情况。按元数据检索相关知识、旧案例与未决项，学习主题开放，不固定只练一种问题；每个新候选说明与已有知识的补充、冲突、替代或新增关系。找不到相关项就说明检索缺口，不强建关联。候选仍隔离，索引收录不授票。

基础3次顺序技巧查询、另1次资讯、预留后回读、失败计次、当日去重、八模块正文、三票和周五人类确认保持。可视候选沿用既有联合复现规则；动态效果须视频证据，不因这次整理宣称静态图能验证动作。原有明确暂停/付费边界保持。

只选择本次适用Skill，不为三套迁移矩阵通读三套相同规则；公共规则以下面影视副本为读取代表，文件副本本批不删除。媒介差异按选中Skill的适配文件补读。规则入口第0层，下列直接文件第1层；不继续执行其中的递归读取指令。索引筛选可扩展主题，不扩展引用深度。

## 按课表选择方向

本课表覆盖旧学习规则中“不设严格轮换、固定顺序”的选题安排；独立AI资讯扫描仍保持原有广度。

用户已批准课表，2026-10-27起在现有任务执行。先读取[课表与科目范围](curriculum.json)，用根脚本 `python3 tools/plan_learning.py --date YYYY-MM-DD` 确定当天课程；按北京时间自然日，A/B周交替。周一提示词、周二风格为核心，其他方向轮换；每日只选一个具体问题，不能把近期举例长期变成主线。今天已完成的记录不重跑。

题目可来自工作缺口、知识补充或探索，说明用途与证据边界；源于项目的插课记录理由，下一次回课表，不补跑欠课。首两周到2026-11-09同任务复盘，未经调整继续轮换。先给课程/问题、用途、真实收获与未测项，再完成原八模块；查询3+1、三票、周五审查、周六备份与付费/暂停边界不变。

归档时同步未决清单与知识索引元数据；索引只帮助查找，不授票、不注入普通制作。运行根脚本 `python3 tools/plan_learning.py --check-index` 和既有索引哈希校验，遗漏不得称已规整。验证媒介随主张选择，不为了每天有图强造候选；现有可视候选复现与模型门禁继续执行。

## 本次任务直接依据

- [媒介适配（film）](../skills/script-video-shot-director/references/cross-skill-adaptation.md)：按实际环节读取。
- [媒介适配（assets）](../skills/script-visual-assets/references/cross-skill-adaptation.md)：按实际环节读取。
- [媒介适配（manga）](../skills/manga-reasoning-storyboard/references/cross-skill-adaptation.md)：按实际环节读取。
- [学习审计](../skills/script-video-shot-director/references/learning-policy.md)：按实际环节读取。
- [AI资讯](../skills/script-video-shot-director/references/ai-news-policy.md)：按实际环节读取。
- [每日完整报告](../skills/script-video-shot-director/references/daily-report-template.md)：按实际环节读取。
- [信用奖惩](../skills/script-video-shot-director/references/credit-policy.md)：按实际环节读取。
- [GitHub保存与回读](../skills/script-video-shot-director/references/dual-save-policy.md)：按实际环节读取。
- [候选与正式库隔离](../skills/script-video-shot-director/references/pending-review-policy.md)：按实际环节读取。
- [可视候选复现](../skills/script-video-shot-director/references/joint-visual-reproduction-policy.md)：按实际环节读取。
- [唯一共用账本：仅当日预算/积分事实，不另建主账](../skills/script-video-shot-director/references/audit/global-state.json)
- [学习审计字段契约](../skills/script-video-shot-director/references/audit/process-contract.json)
- [未决元数据索引：旧未决不自动展开](../pending-review/active-index.json)
- [现行完整运行指令](../registry/automation-prompt-current.txt)

当日运行登记、配额和证据属于任务数据，按当日路径定向读取；近7天限制只适用于日常暂存扫描，不过滤正式案例。生成阶段才另选已明确需要的制作入口，记录根集合；不从依赖文件递归跳转。
