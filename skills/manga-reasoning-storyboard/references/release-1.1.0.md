# 漫画分镜 V1.1.0 发布摘要

发布日期：2026-10-23。修订：SEMVER-20261023-01。旧版本标识保留在version.json历史字段；本次主版本仍为1。

## 本次整合

先还原格序、对白归属、人物身份与原作因果，再制作视频；分镜默认指视频规划，读取不自动画漫画。

- [cross-skill-adaptation.md](cross-skill-adaptation.md)：将观看重点、空间与动作检查适配至漫画；不把影视局部验证当漫画复现票。 状态：`adapt_pending_validation`。
- [direction-and-action.md](direction-and-action.md)：保留原作能力、胜负与因果，动态调度不新编剧情。 状态：`existing_director_guidance`。
- [2026-10-16.md](improvements/2026-10-16.md)：四项检查继续保留待验证状态。 状态：`open`。

整合现有[前期沟通与对标](style-preproduction-policy.md)、[逐项交付底线](creative-delivery-policy.md)、[人物与空间优先验收](cross-skill-policy.md)、[联合可视复现](joint-visual-reproduction-policy.md)及[暂存隔离](pending-review-policy.md)。
正式视频制作前继续执行[当前模型与时长核验](model-capability-gate.md)，版本/入口切换重新查询；本次版本维护不触发制作。

## 验证与回滚边界

本次核验版本与发布规则、引用、文件完整性和已有审计门禁；未运行新的生图/视频，也不宣称生成效果提高。原active/candidate状态、四项open问题、原评分与信用事件不变。

按本包入口执行V主.次.修、带版本的commit/PR标题及README大版本日志。完整来源、三套迁移与回滚目标见[统一发布记录](../../../registry/releases/V1.1.0.json)。
