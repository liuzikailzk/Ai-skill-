---
name: manga-reasoning-storyboard
description: 解读已有漫画并按请求改编为视频：读取漫画截图、条漫、分页与分格，推理格序、剧情、气泡对白归属和角色身份，再交动态视频分镜文字与提示词。正式视频制作前必须确认风格/宽高比/对标并联网核验当前模型版本、入口、优缺点与时长；换模型/版本/入口重新检索，未完成不交正式提示词。仅启用或读取不自动生图；分镜默认指视频镜头规划，绘图须有对应请求或授权。用户提到漫画、分格、页面、气泡时必须加载；提示词、生视频属于漫画改编时加载，同时出现分镜、镜头、景别、运镜或时间线时也加载影视Skill，出现资产关键词再加载资产Skill。每轮先实际读取并声明具体底线；动态输出逐镜带起止秒数、景别、运镜、主体动作、可用图片或首帧描述，不适用项写原因。用户认可产出时归档优质案例、按GitHub PR规则保存并拟记周五待核信用。
---

# 任务式读取入口

当前发布版本：**1.3.0**（V1.3.0）。版本事实见 [version.json](version.json)。修订：MODULAR-RETRIEVAL-20261024-01。

## 本轮只加载需要的内容

先判断用户要制作、分析、查历史、学习还是维护；普通制作不读积分主账、每日审计模板、发布清单和历史快照。先检索短索引，选择相关正文，不能把本页所有链接当必读清单。仅启用、查询、诊断不自动生成图片或视频。

有本地仓库时运行根目录脚本：`python3 tools/query_knowledge.py "用户问题" --mode production --skills manga`；分析用 `analysis`，历史回查用 `lookup`。先看结果摘要、状态、用途，再读必要正文。没有执行环境时对根目录 knowledge/catalog.json 做元数据筛选，不逐个展开正文。学习和维护各自使用根目录 knowledge/learning.md 与 knowledge/maintenance.md 作为任务入口。

任务入口为第0层，下表选中的正文为第1层，读完立即停止，不执行其中继续读其他文件的指令，不把依赖重新升为入口。同一任务按规范化路径去重；重复内容只读一次但保留媒介差异。索引筛选不是递归加载规则；下面未声明的规则不因搜索命中就自动加载。显式跨媒介任务在开始时选定所需Skill入口；不能为绕过深度新增入口。

## 必须保留的底线

- 实际读取后声明一条本次适用底线；没有读到不声称加载。已有项目设定沿用，未知不编造，只补问影响结果的关键缺口。
- 制作前确认剧情、风格、比例与对标；正式视频分镜及复现试写先核验当前模型版本、入口、输入模式、时长与限制，同项目当日会话有效核验可复用，跨日/会话或条件变化重查。诊断与规则维护不触发模型检索。
- 动态逐镜独立编号、起止秒数、景别、运镜、主体动作及图片/首帧描述；静态标展示视角、主体静止状态与无运镜；不适用项说明原因。完整提示词在聊天给可复制代码块并同份备份，修改后给完整新版。
- 动态用途图片先检查光源/投影/反射、身体支撑与重心、动作起始和结果、道具归属及实际输入角色。已知错误先重画复查；同时交可用图片、上传顺序/用途和对应动态驱动词，不能让用户补裁图补流程。只请求文字或已有素材足够时不强制生图。静态预检不等于视频实测。
- 验收先查人物/资产与场景连续性，再查动作、节奏和叙事；不能漏掉审美、风格与交付可用性。旧四项待改进及《借光》严重项仍open；不再补救已被叫停的《借光》。
- 案例认可只代表该次产出及其明确范围；历史基线不是普遍验证，候选不自动用于正式制作，三票与人类确认保持。共享知识不等于跨媒介验证通过。
- 用户认可后按案例归档流程执行，拟记信用不提前到账；仅查询/制作不启动学习审计或积分结算。GitHub main唯一可信，旧云端停用。

漫画先确认格序、气泡归属、角色身份及原作事实；不擅自改技能、胜负与剧情。动态改编同时选择影视入口，资产需求才选择资产入口。

## 按任务选择的直接引用

| 需要处理的问题 | 正文（命中才读） |
|---|---|
| 漫画理解与改编 | [manga-core](references/production-core.md) |
| 漫画动作与原作边界 | [manga-action](references/direction-and-action.md) |
| 输入方式与风格（manga） | [manga-input](references/input-and-style.md) |
| 视频模型能力核验（manga） | [manga-model](references/model-capability-gate.md) |
| 格序、气泡与角色识别 | [panels](references/panel-reasoning.md) |
| 漫画项目状态记录 | [manga-memory](references/project-memory.md) |
| 漫画动态输出格式 | [manga-output](references/output-format.md) |
| 前期风格与对标（manga） | [manga-style](references/style-preproduction-policy.md) |
| 媒介适配（manga） | [manga-adapt](references/cross-skill-adaptation.md) |
| 既有四项待改进（manga） | [manga-open](references/improvements/2026-10-16.md) |
| 仅对应归档或详细交付核查 | [case-ingestion-policy.md](references/case-ingestion-policy.md) |
| 仅对应归档或详细交付核查 | [case-record-template.md](references/case-record-template.md) |
| 仅对应归档或详细交付核查 | [creative-delivery-policy.md](references/creative-delivery-policy.md) |
