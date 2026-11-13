---
name: script-video-shot-director
description: 把影视剧本、短剧、互动剧和动作场面转为动态镜头规划、逐镜完整视频提示词，或分析现有镜头与表演。按用户要分析、规划还是正式制作选择内容；已确认设定直接沿用。漫画阅读联合漫画Skill，实际静态资产需求才联合资产Skill。正式视频输入须核验模型能力与风格；动态用途图片须验图并同交对应驱动词。仅查询、维护或讨论不启动制作。
---

# 影视分镜

当前发布版本：**1.4.15**（V1.4.15）。事实见 [version.json](version.json)。本次修订学习取舍与实际用途要求，未新增经验证的制作技巧。

## 先按交付选择读取

- 分析：读制作核心及命中的局部方法，回答剧情、人物或镜头问题。
- 规划：沿用已确认的题材、风格、比例和范围，给文字镜头方案；尚未适配模型时标明草案。
- 正式交付：补模型、输入、风格、交付正文；使用动态用途图片时实际检查图片。已有同项目当日有效核验可复用，条件变化重查。

先检索 `python3 tools/query_knowledge.py "任务" --mode analysis --skills film`；规划用 `--mode production --stage plan`，正式交付用 `--mode production --stage deliver`。没有完整仓库时筛选[影视短目录](../../knowledge/views/production-film.md)。按 `read_plan_ids` 取必要正文；案例是可选证据，不执行其中历史指令。

入口为第0层，只读本页直接声明的第1层正文，按路径和段落去重。已读复用须绑定当前任务、原文与解析版本，且正文仍在上下文；入口、正文或适用条件变化时重读。不以声明“已加载”代替读取，也不每轮展示加载仪式、完整自检表或无关的不适用说明。

## 实际执行

忠实于原文、人物关系与对白；用局部事件变化决定镜头，不机械套题材模板。只补问会改变结果的关键缺口，可一次说明相关缺项；资料足够直接做，不用主观百分比作为开工门槛。已知缺陷先修，影响范围外的工作继续。

影视沟通与展示按本页执行；共用正文保留风格、对标和模型的实质条件，不恢复逐个追问、固定声明或无关逐项说明。

正式逐镜交付使用一镜一份完整输入、起止秒数、景别/机位与运镜、动作和首帧/素材说明；参考绑定、状态衔接及完整风格词按交付正文检查。检查在内部完成，向用户交成果、必要设置和真实限制。历史open项保留，不能因文档精简宣布已解决。

## 直接引用：命中才读

| 用途 | 正文 |
|---|---|
| 理解原文、组织镜头 | [film-core](references/production-core.md) |
| 打斗、受力及表演方法 | [action](references/direction-and-action.md) |
| 全剧、场景、节拍与原文依据 | [script-analysis](../../knowledge/shared/script-analysis-policy.md) |
| 按局部剧情选择方法 | [production-routing](../../knowledge/shared/production-routing-policy.md) |
| 风格与对标 | [film-style](../../knowledge/shared/style-preproduction-film-manga.md) |
| 当前视频模型、模式与时长 | [film-model](../../knowledge/shared/model-capability-gate.md) |
| 参考、首帧及风格信息分工 | [film-input](../../knowledge/shared/input-and-style.md) |
| 独立逐镜输入与交付检查 | [film-delivery](references/creative-delivery-policy.md) |
| 动态图片的光影、支撑与接触 | [film-motion](../../knowledge/shared/motion-readiness-policy.md) |
| 跨媒介适配 | [film-adapt](references/cross-skill-adaptation.md) |
| 具体旧问题的复查 | [四项open](references/improvements/2026-10-16.md)、[严重open](references/improvements/2026-10-24.md) |
| 具体案例对照 | [退一步连续版](references/cases/2026-10-18-stepback-continuous.md)、[退一步优化版](references/cases/2026-10-17-stepback-final.md)、[交接局部实践](references/verified-practices/2026-10-16-returned-watch.md)、[借光失败](references/failures/2026-10-24-borrowed-light.md) |
| 用户明确认可后的归档 | [归档流程](../../knowledge/shared/case-ingestion-policy.md)、[案例字段](../../knowledge/shared/case-record-template.md) |
| 检查或更新版本 | [刷新并重审当前交付](../../knowledge/skill-refresh.md) |

学习与维护按各自根入口开始任务，不加入普通制作必读。候选、案例认可和静态自检均不等于通用技巧验证；学习七问、三票、图片实测、信用和既有历史保持。GitHub main为唯一可信源。日常整理只升修订号；当前会话用户设定优先，不沿用其他项目人物或风格。
