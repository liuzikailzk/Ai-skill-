# 学习任务入口

修订：MODULAR-RETRIEVAL-20261024-01。用户已授权首批检索与读取分流；本入口只用于学习审计，不适用于普通制作。

先确定当天实际任务与已完成情况。按元数据检索相关知识、旧案例与未决项，学习主题开放，不固定只练一种问题；每个新候选说明与已有知识的补充、冲突、替代或新增关系。找不到相关项就说明检索缺口，不强建关联。候选仍隔离，索引收录不授票。

基础3次顺序技巧查询、另1次资讯、预留后回读、失败计次、当日去重、八模块正文、三票和周五人类确认保持。可视候选沿用既有联合复现规则；动态效果须视频证据，不因这次整理宣称静态图能验证动作。原有明确暂停/付费边界保持。

只选择本次适用Skill，不为三套迁移矩阵通读三套相同规则；公共规则直接读取下面的共享正文，并按规范化路径去重。媒介差异按选中Skill的适配文件补读。规则入口第0层，下列直接文件第1层；不继续执行其中的递归读取指令。索引筛选可扩展主题，不扩展引用深度。

## 本周课表与共同成果

用户2026-10-26批准新课标，本周（10月26日—11月1日）先试行；今天已完成不重跑，10月27日起执行。读取[课表与共同交付标准](curriculum.json)，用根脚本 `python3 tools/plan_learning.py --date YYYY-MM-DD` 选课。周一提示词、周二风格为核心，其余课程保留原A/B轮换；本次周日总结后结束，未经用户安排不自动延长。原每日任务已由用户删除，按此次明确指令重建一个学习任务；月底清理保持原任务。

所有科目共同落到生成输入：专业知识→具体表达/参考输入调整→完整提示词与配套风格词→真实结果与边界。用户可以描述想要的感觉，由AI负责构图、布光、动作和导演判断，不让用户自己拼专业术语。聊天给完整可复制整合版及独立风格部分，同份备份；必要素材明确角色/顺序，动态用途同交驱动词。不能只交理论摘要或“建议加某词”。

允许删词、改参考或调整输入路线；尚未形成可用改善时明确“仅知识备查/未形成可用版”及原因，不强造新词或冒称有效。正式视频词/试写先核验模型与入口，静态预检不替视频；不新增研究、生成或付费额度。先展示上述可用成果与未测项，再按原八模块和资讯完整交付；报告完整不等于制作方法通过。

课题每天一个，跨类别与风格拓展，案例按相关性引用；用户明确项目插课记录理由，不补跑欠课。课表覆盖旧无固定顺序条款，AI资讯仍保持广度。归档同步未决清单与知识索引元数据，运行根脚本 `python3 tools/plan_learning.py --check-index` 及目录哈希校验，缺项不得称规整完成。

## 本次任务直接依据

- [媒介适配（film）](../skills/script-video-shot-director/references/cross-skill-adaptation.md)：按实际环节读取。
- [媒介适配（assets）](../skills/script-visual-assets/references/cross-skill-adaptation.md)：按实际环节读取。
- [媒介适配（manga）](../skills/manga-reasoning-storyboard/references/cross-skill-adaptation.md)：按实际环节读取。
- [学习审计](shared/learning-policy.md)：按实际环节读取。
- [AI资讯](shared/ai-news-policy.md)：按实际环节读取。
- [每日完整报告](shared/daily-report-template.md)：按实际环节读取。
- [信用奖惩](../skills/script-video-shot-director/references/credit-policy.md)：按实际环节读取。
- [GitHub保存与回读](shared/dual-save-policy.md)：按实际环节读取。
- [候选与正式库隔离](shared/pending-review-policy.md)：按实际环节读取。
- [可视候选复现](shared/joint-visual-reproduction-policy.md)：按实际环节读取。
- [唯一共用账本：仅当日预算/积分事实，不另建主账](../skills/script-video-shot-director/references/audit/global-state.json)
- [学习审计字段契约](../skills/script-video-shot-director/references/audit/process-contract.json)
- [未决元数据索引：旧未决不自动展开](../pending-review/active-index.json)
- [现行完整运行指令](../registry/automation-prompt-current.txt)

当日运行登记、配额和证据属于任务数据，按当日路径定向读取；近7天限制只适用于日常暂存扫描，不过滤正式案例。生成阶段才另选已明确需要的制作入口，记录根集合；不从依赖文件递归跳转。
