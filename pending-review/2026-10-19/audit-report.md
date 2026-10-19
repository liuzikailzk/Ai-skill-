# 2026-10-19联合审计｜AUDIT-20261019-01

已加载script-video-shot-director Skill。本次适用底线规则：禁止未验证方法直接写入正式规则。
已加载manga-reasoning-storyboard Skill。本次适用底线规则：共享证据不等于共享验证结论。
已加载script-visual-assets Skill。本次适用底线规则：作品认可不自动视为合并人类票。

## 1.结论
技巧3/3、资讯1/1完成，额外查询0。证据不足，今日不入库。静态样张有几何失败，不能证明视频效果。首次两个查询精确取钟未持久化，保留约10:04–10:05，不补造秒数。

## 2.候选信息与时效
OFFSCREEN-CONTINUITY-20261019-S：先定位，再用视线与局部细节交代画外空间。影视现有悬疑/空间连续性迭代；漫画需原作适配，资产需先锁几何。目标AI视频版本未核实；实跑为内置image_gen，不冒称Seedance。
S1 Zack Eritz《Eyeline Match》2021-07-16；S2 Tseng/van Leeuwen/Djonov《The fragmentation and plasticity of space in film》2025-04-15；均S级原来源，链接/短快照见sources.json。
核对日期2026-10-19，最后整体验证通过日期null。理论无固定到期；平台复审2026-11-18，方法候选复审2027-04-19，不是active有效期。
四维配对：步骤0.5、场景1、结果1、约束1，等权87.5%，旧位置及理由见cross-skill-transfer.json，归已有Skill迭代，不新建。

## 3.证据矩阵与独立性
|主张|来源|反证/缺口|置信度|
|---|---|---|---|
|视线镜头接对象细节有助交代画外关系|S1原教学；S2原论文|不是目标AI模型实测|理论中高；模型迁移低|
|叙事可连贯而几何仍不一致|S2；本次样张|不可用有意电影剪辑为意外资产漂移免责|中高|
|单次明确局部取景可隐藏画外对象|本次三格静态样张|第二格未出现门，第三格未出现人物；仅一次|低，不能外推成功率|
|该提示词能稳定保持资产和空间|无合格支持|门铰链侧别疑似反转；格幅不符|低，当前不通过|

独立性：S1和S2不同作者/机构/方法，无所读范围内互抄迹象，属独立理论材料；并非两份独立目标AI实验。S2-C与S2同源不计新票。S2-C披露作者为期刊顾问编委、未参与本稿评审，不是结果更正。未找到合格独立A/B目标生成实测，证据票未过。

## 4.反证与复现
第三查询未检出目标Seedance直接失败实验；不等于没有。S2表明叙事连贯可掩盖空间变化，不能为意外资产错误免责。
实际内置image_gen一次生成三格；后端型号/版本/seed/采样参数不提供；原创走廊、保安、红门，无外部参考图。完整实际输入见reproduction.md；图片storyboard.png。
预期每格16:9且门几何固定。实得1672×941整图，各格约5.3:1；全景左缘铰链、特写右缘铰链，侧别不一致，未通过。人物可见部分和局部取景初检基本符合；背面、视频/声音/接触因果未测。失败原图保留，无修复/第二次生成。
拟剪辑时间轴（非已生成视频）：00:00–00:02全景，男子左、红门右；00:02–00:04脸部特写朝右，门在画外；00:04–00:06门把手大特写，人物在画外。三镜均固定机位，主体静止。
声音本要素不适用，原因是静态试验；漫画原作/气泡本要素不适用，原因是无漫画输入。
最小下一试验：先锁定门正视与左铰链，再分别生成三张16:9，用同素材在实际视频入口做对照。仅计划，未运行。

## 5.七问逐答
1. 最可能错处：把传统剪辑理论外推成AI空间稳定性；门铰链漂移说明风险。
2. 过时或替代：理论无固定期限；S2已核2026-02-23利益披露更正，未检出目标规则弃用但版本未知。
3. 来源互抄：S1与S2不同团队和方法；S2更正不独立计票；缺独立A/B目标实测。
4. 版本、付费、地区：内置图像入口可用，后端版本和seed未暴露，Seedance入口条件未测。
5. 更简单替代：固定门资产后独立取景或裁切；是否更优未做对照，不当结论。
6. 复现失败点：门铰链侧别与格幅；视频身份、视线错接和动作时序仍未测。
7. 是否凑数：只保留1个迭代候选，不发布；理论与既有规则重合高，不宣称稳定增益。
今日非周五，不编总分；真实缺口是独立目标模型实验和视频/资产一致性。

## 6.六状态与三票
candidate；证据票未通过（缺独立A/B目标生成验证）；复现票未通过（静态失败、无视频）；人类票未收到。未进入observing/active。暂无未解释的来源直接冲突，不强标conflicted；未发布，故非deprecated/rolled_back。单次实现失败不代表理论证伪。三套分别记录结果，不共享通过票。

## 7.版本、保存与信用
三套V1.01不变，无方法发布；只写pending-review与唯一主账实际日志/待核事件。余额8，到账0；拟完整空手+3、一手来源+1，共4待周五确认，credit_delta=0、不可用。不申请反证额外+2，不把实现失败当充分因果反证。
新verified案例0；既有认可案例未满30天且无新复用证据，不重复奖励。
备份backup/audit-20261019-01；新增backup/audit-20261019-results固定16ec9d6de8d7edd110cfc89a2ebf75aa131e7282并回读。PR23并发启动检查未动配额/主账，本批保留原文；不重跑已完成查询。本地只保留本次生成图，不声称全仓本地备份、双端或镜像。
结果走audit/20261019-results维护PR；本文写成时待合并及独立main回读，最终回执另列，未提前宣称保存成功。

## 8.检索与留痕
预留PR22已合并并独立回读后检索；同一run_id及slot，无新增额度。
- news/1：AI model tools release October 18 19 2026 official announcements；2026-10-19 10:04–10:05 Asia/Shanghai；前一执行段工具结果确认已完成，精确取钟未持久化，不补造；system1 recency=2; broad AI news; since 2026-10-18 12:40 Asia/Shanghai；成功；主窗口未检出可确认重要新发布；10月17日DeepSeek更新仅作7日回顾。
- technique/1：offscreen space eyeline close up suspense film spatial continuity；2026-10-19 10:04–10:05 Asia/Shanghai；前一执行段工具结果确认已完成，精确取钟未持久化，不补造；system2 no date filter; one candidate: local framing and offscreen threat continuity；成功；筛选局部取景与画外空间一个候选。
- technique/2：off screen space eyeline match film viewer spatial continuity research；2026-10-19T10:05:31.162+08:00；system1 no date filter; independent primary evidence for same candidate；成功；原作者教学与独立论文可核；缺目标AI环境独立实测。
- technique/3："offscreen space" "film" (limitations OR failure OR confusion OR alternative)；2026-10-19T10:05:40.583+08:00；system2 no date filter; counterevidence for same candidate；成功；未检出目标Seedance直接反例；论文限定视线连贯不保证空间几何，静态实跑亦有铰链侧别漂移。
已知页面必要直读不加查询。sources.json逐条含原URL、作者日期、范围、短片段、快照时间与SHA-256，不冒称整页存档。
文件：query-ledger.json、candidate-offscreen.json、audit-report.md、evidence-matrix.md、cross-skill-transfer.json、sources.json、reproduction.md、storyboard.png、news-report.md、human-brief.txt。
图片SHA-256 fa6758a1ab871daa693efaac8c7cc83fd018b3528b7487196006cc33fadf8c6b。简报五部分7行。其他环境启动失败不等于本run未执行，保留原历史并由本日志澄清。
