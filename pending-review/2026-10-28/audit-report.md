# 2026-10-28 故事/分镜学习

本次可复制成果是给文字助手使用的叙事检查指令，不是图像/视频生成词。预期用途是发现提前剧透和无依据反应。本次改变信息出现顺序，未证明成片更好。配套生成风格词、上传顺序、首帧与动态驱动词不适用：没有进入媒体制作，没有实际图片和目标视频入口；沿用项目画风目标，不凭本次研究另造画风。生成输入改善仍为“仅知识备查/未形成可用版”。

## 可复制叙事检查指令
```text
请只做叙事信息检查，不生成图片，不写视频模型指令，不替我评定观众是否觉得有悬念。
测试剧情：夜里，独居的林岚听见厨房连续两次轻响。她停下脚步，望向半开的厨房门，门内暂时看不清。她走到门边，发现自家猫正在拨动地上的空碗。没有陌生人，没有超自然事件，没有对白。
现有草稿：第一段先展示猫拨空碗；第二段林岚听见声音，停步望向厨房；第三段她走到门口，看见猫。
本次目标：让观众先与林岚共同不知道声音来源，最后才揭示是猫；保留完整因果，不添加威胁或解释性旁白。
请逐段列出：观众已经知道什么、林岚知道什么、还不知道什么、判断依据来自哪一处文字。标出提前泄露答案或缺少必要线索的位置。
然后给一份完整改写的叙事段落，不给补丁，不添加新剧情。保留“轻响来自厨房、门内暂不可见、到门口才看清”三个条件。最后检查声音是否有来源、人物为何行动、结尾是否回答开头问题。把文字检查与观众测试分开，不给成功率或悬念评分。
```

## 本次文字走查结果
文字走查（本助手执行，非独立模型实验）：原第一段已告诉观众声源，破坏“共同未知”的指定目标；它并非普遍错误，在观众先知的喜剧目标下可以成立。
完整改写：
夜里，林岚听见厨房传来连续两次轻响。她停下脚步，望向半开的厨房门，从当前位置看不清门内。
她循着声响走向厨房，直到门边才看清地面。
自家的猫正用前爪拨动空碗，碗沿碰地的轻响与先前一致。林岚看向猫，原本绷紧的肩膀松下来。
自检：声源在结尾回收；走向厨房有声音动机；没有新增入侵者或超自然设定。这里只核对文本信息顺序，没有测观众理解或悬念。

## 1. 结论
AUDIT-20261028-01；A周周三。3次技巧顺序查询，独立资讯1次，额外0次。今日无合格制作技巧，证据不足今日不入库。26/27日不重跑；本周11月1日总结后结束，本次不改任务。

## 2. 候选与时效
REVEAL-CLUE-20261028-S：叙事已知/未知信息走查，归film；对漫画只研究叙事分析，原作理解未测；资产只涉及哪些信息可见，不改外观方法。与既有film适配文件“每镜信息任务”是补充检查表达，不宣称新理论。索引检索“信息 揭示 悬念”未命中，不代表全库没有。仅查近7日文件名和12条未决元数据。
证据核对2026-10-28，最后真实效果验证null；方法复审2027-04-28，理论无固定到期但应用需重核。无目标生成模型，不设虚构平台有效期。
S1 [The architecture of visual narrative comprehension](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2014.00680/full)；Neil Cohn；2014-07-01；S；正文Interfaces between narrative and layout及元数据
S2 [Reading Without Words: Eye Movements in the Comprehension of Comic Strips](https://repository.essex.ac.uk/16471/)；Tom Foulsham; Devon Wybrow; Neil Cohn；2016；S；机构仓库摘要；未读全文；年份精度，不以入库日当发表日
S3 [Being explicit about the implicit: inference generating techniques in visual narrative](https://www.cambridge.org/core/journals/language-and-cognition/article/being-explicit-about-the-implicit-inference-generating-techniques-in-visual-narrative/AEBDBD7A09A3892D860463AB57588112)；Neil Cohn；2019-04-30；S；摘要和3.2省略关键事件相关段落，非全文系统复核
S4 [Do Language Models Agree with Human Perceptions of Suspense in Stories?](https://arxiv.org/abs/2508.15794)；Glenn Matlin; Devin Zhang; Rodrigo Barroso Loza; Diana M. Popescu; Joni Isbell; Chandreyi Chakraborty; Mark Riedl；2025-08-13；S；摘要和元数据；未复现实验

## 3. 证据矩阵/独立性
|主张|证据|反证/限制|置信度|
|---|---|---|---|
|画面顺序影响理解|S1、S2|顺序研究不证明所有剧情都应延迟揭示|中|
|省略关键事件需要推理，可能增加理解负担|S3|删镜头不等于悬念更好|中|
|AI自评分能代表观众悬念感|S4提供反对证据|研究对象是其测试的语言模型和文本，不代表所有未来模型|不能作为验收依据|
|本次信息检查指令能改善成片|仅本次文字走查|无独立A/B实测、无成片|低|

S1和S3均为Neil Cohn；S2作者包含Cohn，属于部分独立，不能凑三票。S4为不同团队，但研究文本悬念评价，不是本检查指令的独立实测。证据票不通过。

## 4. 反证与真实复现
第三次命中S4：AI对悬念的判断不能直接等同于人类；S3指出省略关键事件存在理解成本。PMC补充页面出现验证码，未绕过；改读已知出版方来源。
真实执行只有本助手文字走查，完整输入与输出如上；不是独立模型A/B，也不是可视候选评估。模型精确后端参数、种子不可得，不编造。无外部素材、无图片或视频、无上传顺序；视频门禁未完成，因此未试写正式动态词。预期是找出信息提前泄露；实际发现草稿第一段提前给出猫，完成三段改写。未证明观众悬念提升。
最小后续验证计划：同一剧情制作原顺序/改顺序片段，在相同实际模型与素材条件下保留全部结果，让不了解答案的观看者分别复述声源与揭示点，并评价悬念。失败条件：看不懂行动动机、提前看见答案、因果改变或没有收益。计划未执行，不授权另跑付费生成，不恢复暂停视频。

## 5. 七问反方自检
1. 最可能错：把共同未知当成所有故事的目标；观众先知也可以成立。
2. 时效：2014—2019理论研究不是当下视频模型能力；本次无产品参数结论。
3. 同源：S1/S3同作者，S2有共同作者；S4团队不同但研究任务不同。
4. 入口限制：公司Seedance入口未核验，本次不输出视频词或虚构种子。
5. 更简单替代：先问每段观众多知道了什么；若原稿已清楚，不强行改顺序。
6. 失败点：隐藏声源同时删掉定位线索会造成困惑；文字无冲突也可能拍不清。
7. 凑数检查：只保留一个候选，不把文字练习冒充静态复现或人类认可。

## 6. 状态三票
candidate；证据票未通过（缺本项独立A/B实测），复现票未通过（仅文字走查），人类票未收到。未提交转正。主账余额7不变；本次不新增待核奖分，避免把研究文字进度当效果奖励；不改原待核事件。

## 7. 版本与保存范围
影视V1.4.4、资产V1.4.4、漫画V1.3.4，纯记录不升版。备份branch backup/pre-learning-20261028独立核对到ece56acaf1d3041079c9c058be45bd31aef4b576，本地day28-before.bundle已验证。预留PR70已合并回读；结果PR及main回执见最终交付。本次保存候选、输入、文字结果、来源、报告、资讯、唯一账本与索引；不改制作正文，不使用旧云端。validation.json记录索引/哈希校验，不代表效果验证。

## 8. 原始检索留痕
1. visual narrative suspense reveal information order reader comprehension comics research | 2026-10-27T19:57:56.692Z UTC | system2 | success
2. Neil Cohn visual narrative grammar inference deletion panels comprehension study | 2026-10-27T19:58:07.047Z UTC | system2 | success
3. visual narrative inference suspense reveal order limitations ambiguity comprehension study | 2026-10-27T19:58:11.058Z UTC | system2 | success
资讯：AI official announcements October 27 2026 models tools release | 2026-10-27T19:58:17.724Z UTC | system1 recency=2 | success。
搜索时间取调用前墙钟，UTC转北京时间加8小时。来源短原文、作者、日期、读取范围、快照时间和哈希在sources.json；原查询回执在query-ledger.json。候选证据目录pending-review/2026-10-28/，资讯在影视audit/news/2026-10-28。只打开已知链接，不额外搜索。
