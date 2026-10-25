---
name: script-video-shot-director
description: 将影视、短剧、互动剧和动作视频转为可制作的动态分镜提示词，并解析视频的镜头、动作与节奏。正式制作前必须确认风格/宽高比/对标并联网核验当前模型版本、入口、优缺点与时长；换模型/版本/入口重新检索，未完成不交正式提示词。用户提到分镜、镜头、景别、运镜、时间线时必须加载；提示词、生视频、解析视频属于动态制作时加载；漫画任务同时命中上述词时与漫画Skill共同加载。每轮先实际读取并声明一条具体底线，逐镜写起止秒数、景别、运镜、主体动作和可用图片或首帧描述，不适用项明确写原因。用户认可本技能产出时归档优质案例、按GitHub PR规则保存并拟记周五待核信用；不把案例认可当技巧转正。 动态用途图片交付前必须通过可动性测试，缺陷先重画，并同交可复制的对应多图动态驱动词。
---

# 任务式读取入口

当前发布版本：**1.4.0**（V1.4.0）。版本事实见 [version.json](version.json)。修订：MODULAR-RETRIEVAL-20261024-01。

## 本轮只加载需要的内容

先判断用户要制作、分析、查历史、学习还是维护；普通制作不读积分主账、每日审计模板、发布清单和历史快照。先检索短索引，选择相关正文，不能把本页所有链接当必读清单。仅启用、查询、诊断不自动生成图片或视频。

有本地仓库时运行根目录脚本：`python3 tools/query_knowledge.py "用户问题" --mode production --skills film`；分析用 `analysis`，历史回查用 `lookup`。先看结果摘要、状态、用途，再读必要正文。没有执行环境时对根目录 knowledge/catalog.json 做元数据筛选，不逐个展开正文。学习和维护各自使用根目录 knowledge/learning.md 与 knowledge/maintenance.md 作为任务入口。

任务入口为第0层，下表选中的正文为第1层，读完立即停止，不执行其中继续读其他文件的指令，不把依赖重新升为入口。同一任务按规范化路径去重；重复内容只读一次但保留媒介差异。索引筛选不是递归加载规则；下面未声明的规则不因搜索命中就自动加载。显式跨媒介任务在开始时选定所需Skill入口；不能为绕过深度新增入口。

## 必须保留的底线

- 实际读取后声明一条本次适用底线；没有读到不声称加载。已有项目设定沿用，未知不编造，只补问影响结果的关键缺口。
- 制作前确认剧情、风格、比例与对标；正式视频分镜及复现试写先核验当前模型版本、入口、输入模式、时长与限制，同项目当日会话有效核验可复用，跨日/会话或条件变化重查。诊断与规则维护不触发模型检索。
- 动态逐镜独立编号、起止秒数、景别、运镜、主体动作及图片/首帧描述；静态标展示视角、主体静止状态与无运镜；不适用项说明原因。完整提示词在聊天给可复制代码块并同份备份，修改后给完整新版。
- 动态用途图片先检查光源/投影/反射、身体支撑与重心、动作起始和结果、道具归属及实际输入角色。已知错误先重画复查；同时交可用图片、上传顺序/用途和对应动态驱动词，不能让用户补裁图补流程。只请求文字或已有素材足够时不强制生图。静态预检不等于视频实测。
- 验收先查人物/资产与场景连续性，再查动作、节奏和叙事；不能漏掉审美、风格与交付可用性。旧四项待改进及《借光》严重项仍open；不再补救已被叫停的《借光》。
- 案例认可只代表该次产出及其明确范围；历史基线不是普遍验证，候选不自动用于正式制作，三票与人类确认保持。共享知识不等于跨媒介验证通过。
- 用户认可后按案例归档流程执行，拟记信用不提前到账；仅查询/制作不启动学习审计或积分结算。GitHub main唯一可信，旧云端停用。

以剧本场次与当前项目为依据，不继承其他案例的角色、台词、画风或镜头形式。漫画理解由漫画入口处理，静态资产制作按资产入口处理。

## 按任务选择的直接引用

| 需要处理的问题 | 正文（命中才读） |
|---|---|
| 影视剧本与动态分镜 | [film-core](references/production-core.md) |
| 动作因果与摄影响应 | [action](references/direction-and-action.md) |
| 输入方式与风格（film） | [film-input](references/input-and-style.md) |
| 视频模型能力核验（film） | [film-model](references/model-capability-gate.md) |
| 前期风格与对标（film） | [film-style](references/style-preproduction-policy.md) |
| 媒介适配（film） | [film-adapt](references/cross-skill-adaptation.md) |
| 既有四项待改进（film） | [film-open](references/improvements/2026-10-16.md) |
| 动态用途图片可动性检查（film） | [film-motion](references/motion-readiness-policy.md) |
| 严重待改进（film） | [film-severe](references/improvements/2026-10-24.md) |
| 《退一步》连续攻防版（17日制作，18日认可） | [case-stepback-continuous](references/cases/2026-10-18-stepback-continuous.md) |
| 《退一步》17日晚优化版及第三方反馈 | [case-stepback-final](references/cases/2026-10-17-stepback-final.md) |
| 《还好没走远》交接动作局部实践 | [case-watch](references/verified-practices/2026-10-16-returned-watch.md) |
| 【严重失败】《借光》（film） | [failure-light-film](references/failures/2026-10-24-borrowed-light.md) |
| 仅对应归档或详细交付核查 | [case-ingestion-policy.md](references/case-ingestion-policy.md) |
| 仅对应归档或详细交付核查 | [case-record-template.md](references/case-record-template.md) |
| 仅对应归档或详细交付核查 | [creative-delivery-policy.md](references/creative-delivery-policy.md) |
