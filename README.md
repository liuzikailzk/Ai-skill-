# AI Skill 双端备份

保存资产、影视剧本分镜、漫画分镜三套Skill的完整文件，来源为已保存的GPT技能云端。

| Skill | 文件 |
|---|---|
| 资产 | [script-visual-assets](skills/script-visual-assets/SKILL.md) |
| 影视分镜 | [script-video-shot-director](skills/script-video-shot-director/SKILL.md) |
| 漫画分镜 | [manga-reasoning-storyboard](skills/manga-reasoning-storyboard/SKILL.md) |

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
