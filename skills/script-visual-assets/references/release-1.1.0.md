# 资产 V1.1.0 发布摘要

发布日期：2026-10-23。修订：SEMVER-20261023-01。旧版本标识保留在version.json历史字段；本次主版本仍为1。

## 本次整合

分开基础人物/场景/道具与剧情参考帧；锁外形、空间和单一静态状态，静态资产不承担运镜或动作时序。

- [cross-skill-adaptation.md](cross-skill-adaptation.md)：关注构图可读性、材质区分和多视图空间；无新增本套实测。 状态：`adapt_pending_validation`。
- [production-baseline.md](production-baseline.md)：静态提示词写展示视角、静止状态与无运镜；保留原资产制作边界。 状态：`existing_asset_scope`。
- [2026-10-16.md](improvements/2026-10-16.md)：四项的静态对应检查不等于动态问题已解决。 状态：`open`。

整合现有[前期沟通与对标](style-preproduction-policy.md)、[逐项交付底线](creative-delivery-policy.md)、[人物与空间优先验收](cross-skill-policy.md)、[联合可视复现](joint-visual-reproduction-policy.md)及[暂存隔离](pending-review-policy.md)。

## 验证与回滚边界

本次核验版本与发布规则、引用、文件完整性和已有审计门禁；未运行新的生图/视频，也不宣称生成效果提高。原active/candidate状态、四项open问题、原评分与信用事件不变。

按本包入口执行V主.次.修、带版本的commit/PR标题及README大版本日志。完整来源、三套迁移与回滚目标见[统一发布记录](../../../registry/releases/V1.1.0.json)。
