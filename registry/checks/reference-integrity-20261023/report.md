# 三套 Skill 引用完整性检测报告

日期：2026-10-23（Asia/Shanghai）。扫描基线：`76089ae5a06b34720082222628a76404d6133c21`。本次路径修订：三套均为 **V1.1.1**。

**结论：现行规则加载路径已修复；存在循环引用与历史资源缺口，整体待审，不能标记全库通过。** 未添加绿色 `[引用完整性校验: 通过]` 徽章。循环仅检测并报告，未擅自拆解，也未伪造缺失素材、回执或历史快照。

## 范围和计数口径

- 全部162个Skill文件中的77份Markdown都已扫描：包含三个入口、所有references子目录、案例、日志和候选说明。没有遗漏现存Markdown。
- 提取Markdown链接、引用式链接、代码跨度内文件路径和正文文件名引用，按出现次数计数；同一目标多次引用分别计数，链接标签不重复算一个引用。
- Markdown链接严格按来源文件目录解析；正文路径允许明确的本包根目录、仓库根目录、指定共用包及唯一文件名解析，完整记录解析模式。不用模糊搜索掩盖写错的Markdown链接。
- 补充跟踪1份被直接引用的暂存证据Markdown；该文件的历史主记录和未公开私有素材单独列为辅助范围缺口，不并入三套的引用数量。
- 外部网址联网可用性、Markdown标题锚点不属于本次“文件是否存在”检查；正文里的参数化输出位置单列，不创建虚假的实例文件。

| Skill | 文件总数 | Markdown数 | 引用出现次数 | 可定位现存文件 | 参数/输出模板 | 历史缺失或歧义 |
|---|---:|---:|---:|---:|---:|---:|
| 影视分镜 | 64 | 29 | 253 | 181 | 27 | 45 |
| 漫画分镜 | 52 | 27 | 177 | 153 | 24 | 0 |
| 视觉资产 | 46 | 21 | 158 | 134 | 24 | 0 |
| 合计 | 162 | 77 | 588 | 468 | 75 | 45 |

共588处内部引用条目，其中468处能定位现存文件，去重后涉及139个文件；75处为参数/输出模板；45处为历史资源缺口。不能把588处全部称为“有效文件链接”。全部明确的Markdown链接177处已通过目标文件存在性检查。

## 死链与定位修复

1. 修复27处Markdown死链：影视10处、漫画11处、资产6处。共同原因是制作正文被移动至引用目录后，链接仍多带一层前缀。
2. 修复3处旧自动化配置简写：指向真实存在的影视包对应日期原件，不创建替身。
3. 修正三套审计命令的工作目录为仓库根目录，并写出共享脚本/主账路径。其中漫画、资产原命令共有4处实际无法在本包定位的目标；影视原目标存在，仅统一执行位置说明。
4. 共34处失效或不完整的当前路径已解决，对应33处编辑（命令一处可包含两个目标；影视命令另作一致性说明）。复查无当前加载路径缺失、无当前路径歧义、无未审查示例。

| 来源 | 原行号 | 原引用/命令 | 修复后 | 类型 |
|---|---:|---|---|---|
| `skills/script-video-shot-director/references/production-baseline.md` | 21 | `references/dual-save-policy.md` | `dual-save-policy.md` | markdown_link |
| `skills/script-video-shot-director/references/production-baseline.md` | 23 | `references/dual-save-policy.md` | `dual-save-policy.md` | markdown_link |
| `skills/script-video-shot-director/references/production-baseline.md` | 27 | `references/audit/registry.json` | `audit/registry.json` | markdown_link |
| `skills/script-video-shot-director/references/production-baseline.md` | 29 | `references/learning-policy.md` | `learning-policy.md` | markdown_link |
| `skills/script-video-shot-director/references/production-baseline.md` | 29 | `references/learning-log.md` | `learning-log.md` | markdown_link |
| `skills/script-video-shot-director/references/production-baseline.md` | 29 | `references/audit/registry.json` | `audit/registry.json` | markdown_link |
| `skills/script-video-shot-director/references/production-baseline.md` | 33 | `references/test-20261013-01.md` | `test-20261013-01.md` | markdown_link |
| `skills/script-video-shot-director/references/production-baseline.md` | 217 | `references/direction-and-action.md` | `direction-and-action.md` | markdown_link |
| `skills/script-video-shot-director/references/production-baseline.md` | 247 | `references/direction-and-action.md` | `direction-and-action.md` | markdown_link |
| `skills/script-video-shot-director/references/production-baseline.md` | 249 | `references/input-and-style.md` | `input-and-style.md` | markdown_link |
| `skills/script-video-shot-director/references/audit/governance-migration.md` | 15 | `history/automation-before.json` | `../../history/AUDIT-GOV-20261013-01/automation-before.json` | bare_to_markdown_link |
| `skills/script-video-shot-director/references/audit/record-format.md` | 27 | `python scripts/audit_gate.py <record.json> --ledger references/audit/global-state.json --date YYYY-MM-DD` | `python skills/script-video-shot-director/scripts/audit_gate.py <record.json> --ledger skills/script-video-shot-director/references/audit/global-state.json --date YYYY-MM-DD` | shared_command |
| `skills/manga-reasoning-storyboard/references/production-baseline.md` | 21 | `references/dual-save-policy.md` | `dual-save-policy.md` | markdown_link |
| `skills/manga-reasoning-storyboard/references/production-baseline.md` | 23 | `references/dual-save-policy.md` | `dual-save-policy.md` | markdown_link |
| `skills/manga-reasoning-storyboard/references/production-baseline.md` | 27 | `references/audit/registry.json` | `audit/registry.json` | markdown_link |
| `skills/manga-reasoning-storyboard/references/production-baseline.md` | 29 | `references/learning-policy.md` | `learning-policy.md` | markdown_link |
| `skills/manga-reasoning-storyboard/references/production-baseline.md` | 29 | `references/learning-log.md` | `learning-log.md` | markdown_link |
| `skills/manga-reasoning-storyboard/references/production-baseline.md` | 29 | `references/audit/registry.json` | `audit/registry.json` | markdown_link |
| `skills/manga-reasoning-storyboard/references/production-baseline.md` | 58 | `references/project-memory.md` | `project-memory.md` | markdown_link |
| `skills/manga-reasoning-storyboard/references/production-baseline.md` | 79 | `references/panel-reasoning.md` | `panel-reasoning.md` | markdown_link |
| `skills/manga-reasoning-storyboard/references/production-baseline.md` | 168 | `references/direction-and-action.md` | `direction-and-action.md` | markdown_link |
| `skills/manga-reasoning-storyboard/references/production-baseline.md` | 176 | `references/input-and-style.md` | `input-and-style.md` | markdown_link |
| `skills/manga-reasoning-storyboard/references/production-baseline.md` | 178 | `references/output-format.md` | `output-format.md` | markdown_link |
| `skills/manga-reasoning-storyboard/references/audit/governance-migration.md` | 15 | `history/automation-before.json` | `../../../script-video-shot-director/history/AUDIT-GOV-20261013-01/automation-before.json` | bare_to_markdown_link |
| `skills/manga-reasoning-storyboard/references/audit/record-format.md` | 27 | `python scripts/audit_gate.py <record.json> --ledger references/audit/global-state.json --date YYYY-MM-DD` | `python skills/script-video-shot-director/scripts/audit_gate.py <record.json> --ledger skills/script-video-shot-director/references/audit/global-state.json --date YYYY-MM-DD` | shared_command |
| `skills/script-visual-assets/references/production-baseline.md` | 21 | `references/dual-save-policy.md` | `dual-save-policy.md` | markdown_link |
| `skills/script-visual-assets/references/production-baseline.md` | 23 | `references/dual-save-policy.md` | `dual-save-policy.md` | markdown_link |
| `skills/script-visual-assets/references/production-baseline.md` | 27 | `references/audit/registry.json` | `audit/registry.json` | markdown_link |
| `skills/script-visual-assets/references/production-baseline.md` | 29 | `references/learning-policy.md` | `learning-policy.md` | markdown_link |
| `skills/script-visual-assets/references/production-baseline.md` | 29 | `references/learning-log.md` | `learning-log.md` | markdown_link |
| `skills/script-visual-assets/references/production-baseline.md` | 29 | `references/audit/registry.json` | `audit/registry.json` | markdown_link |
| `skills/script-visual-assets/references/audit/governance-migration.md` | 15 | `history/automation-before.json` | `../../../script-video-shot-director/history/AUDIT-GOV-20261013-01/automation-before.json` | bare_to_markdown_link |
| `skills/script-visual-assets/references/audit/record-format.md` | 27 | `python scripts/audit_gate.py <record.json> --ledger references/audit/global-state.json --date YYYY-MM-DD` | `python skills/script-video-shot-director/scripts/audit_gate.py <record.json> --ledger skills/script-video-shot-director/references/audit/global-state.json --date YYYY-MM-DD` | shared_command |

## 循环引用：待用户决定拆解

对所有已解析的Markdown目标建立有向图，以强连通分量检测循环。共229条去重Markdown图边，发现5个循环组：3组多文件互引，另有2个案例文件自指；共51份文件处于循环组中，15对直接双向引用，9个文件存在自指边（其中7个已包含于多文件组）。强连通分量覆盖所有循环边；下面不把一个循环组冒充只有一条环。

静态互引不等于已证明AI运行时无限循环，但会使无已读集合/递归边界的加载器重复加载。历史日志、索引回看与“先读”控制指令的风险不同；本次均保留并标出，不自行删除。

| 循环组 | 范围 | 文件数 | 组内去重边 | 直接互引对 |
|---|---|---:|---:|---:|
| CYCLE-01 | 漫画分镜 | 16 | 48 | 4 |
| CYCLE-02 | 影视分镜 | 18 | 58 | 7 |
| CYCLE-03 | 影视分镜：案例自指 | 1 | 1 | 0 |
| CYCLE-04 | 影视分镜：案例自指 | 1 | 1 | 0 |
| CYCLE-05 | 视觉资产 | 15 | 46 | 4 |

### CYCLE-01

已确认的一条环：

`skills/manga-reasoning-storyboard/SKILL.md` → `skills/manga-reasoning-storyboard/references/case-ingestion-policy.md` → `skills/manga-reasoning-storyboard/references/cross-skill-adaptation.md` → `skills/manga-reasoning-storyboard/references/production-baseline.md` → `skills/manga-reasoning-storyboard/SKILL.md`

成员：

- `skills/manga-reasoning-storyboard/SKILL.md`
- `skills/manga-reasoning-storyboard/references/ai-news-policy.md`
- `skills/manga-reasoning-storyboard/references/case-ingestion-policy.md`
- `skills/manga-reasoning-storyboard/references/creative-delivery-policy.md`
- `skills/manga-reasoning-storyboard/references/credit-policy.md`
- `skills/manga-reasoning-storyboard/references/cross-skill-adaptation.md`
- `skills/manga-reasoning-storyboard/references/cross-skill-policy.md`
- `skills/manga-reasoning-storyboard/references/daily-report-template.md`
- `skills/manga-reasoning-storyboard/references/dual-save-policy.md`
- `skills/manga-reasoning-storyboard/references/improvements/2026-10-16.md`
- `skills/manga-reasoning-storyboard/references/input-and-style.md`
- `skills/manga-reasoning-storyboard/references/learning-log.md`
- `skills/manga-reasoning-storyboard/references/learning-policy.md`
- `skills/manga-reasoning-storyboard/references/pending-review-policy.md`
- `skills/manga-reasoning-storyboard/references/production-baseline.md`
- `skills/manga-reasoning-storyboard/references/release-1.1.0.md`

全部直接互引对（行号按修复后扫描）：

- `skills/manga-reasoning-storyboard/SKILL.md` 第[71]行 ↔ `skills/manga-reasoning-storyboard/references/creative-delivery-policy.md` 第[8, 28]行。
- `skills/manga-reasoning-storyboard/SKILL.md` 第[89]行 ↔ `skills/manga-reasoning-storyboard/references/production-baseline.md` 第[13]行。
- `skills/manga-reasoning-storyboard/references/cross-skill-adaptation.md` 第[20]行 ↔ `skills/manga-reasoning-storyboard/references/improvements/2026-10-16.md` 第[29]行。
- `skills/manga-reasoning-storyboard/references/learning-log.md` 第[22, 52, 71, 82, 112, 133]行 ↔ `skills/manga-reasoning-storyboard/references/learning-policy.md` 第[125]行。

### CYCLE-02

已确认的一条环：

`skills/script-video-shot-director/SKILL.md` → `skills/script-video-shot-director/references/ai-news-policy.md` → `skills/script-video-shot-director/references/daily-report-template.md` → `skills/script-video-shot-director/references/cross-skill-policy.md` → `skills/script-video-shot-director/references/cross-skill-adaptation.md` → `skills/script-video-shot-director/SKILL.md`

成员：

- `skills/script-video-shot-director/SKILL.md`
- `skills/script-video-shot-director/references/ai-news-policy.md`
- `skills/script-video-shot-director/references/audit/governance-migration.md`
- `skills/script-video-shot-director/references/audit/governance-regression.md`
- `skills/script-video-shot-director/references/case-ingestion-policy.md`
- `skills/script-video-shot-director/references/creative-delivery-policy.md`
- `skills/script-video-shot-director/references/credit-policy.md`
- `skills/script-video-shot-director/references/cross-skill-adaptation.md`
- `skills/script-video-shot-director/references/cross-skill-policy.md`
- `skills/script-video-shot-director/references/daily-report-template.md`
- `skills/script-video-shot-director/references/dual-save-policy.md`
- `skills/script-video-shot-director/references/improvements/2026-10-16.md`
- `skills/script-video-shot-director/references/input-and-style.md`
- `skills/script-video-shot-director/references/learning-log.md`
- `skills/script-video-shot-director/references/learning-policy.md`
- `skills/script-video-shot-director/references/pending-review-policy.md`
- `skills/script-video-shot-director/references/release-1.1.0.md`
- `skills/script-video-shot-director/references/verified-practices/2026-10-16-returned-watch.md`

全部直接互引对（行号按修复后扫描）：

- `skills/script-video-shot-director/SKILL.md` 第[50]行 ↔ `skills/script-video-shot-director/references/creative-delivery-policy.md` 第[8]行。
- `skills/script-video-shot-director/SKILL.md` 第[42]行 ↔ `skills/script-video-shot-director/references/cross-skill-adaptation.md` 第[3]行。
- `skills/script-video-shot-director/SKILL.md` 第[91]行 ↔ `skills/script-video-shot-director/references/learning-log.md` 第[43, 70, 91, 122, 132, 321, 331, 351]行。
- `skills/script-video-shot-director/SKILL.md` 第[91]行 ↔ `skills/script-video-shot-director/references/learning-policy.md` 第[124]行。
- `skills/script-video-shot-director/references/audit/governance-migration.md` 第[13]行 ↔ `skills/script-video-shot-director/references/audit/governance-regression.md` 第[31]行。
- `skills/script-video-shot-director/references/cross-skill-adaptation.md` 第[9]行 ↔ `skills/script-video-shot-director/references/improvements/2026-10-16.md` 第[29]行。
- `skills/script-video-shot-director/references/learning-log.md` 第[21, 51, 70, 81, 111, 132, 314]行 ↔ `skills/script-video-shot-director/references/learning-policy.md` 第[125]行。

### CYCLE-03

已确认的一条环：

`skills/script-video-shot-director/references/cases/2026-10-17-stepback-final.md` → `skills/script-video-shot-director/references/cases/2026-10-17-stepback-final.md`

成员：

- `skills/script-video-shot-director/references/cases/2026-10-17-stepback-final.md`

### CYCLE-04

已确认的一条环：

`skills/script-video-shot-director/references/cases/2026-10-18-stepback-continuous.md` → `skills/script-video-shot-director/references/cases/2026-10-18-stepback-continuous.md`

成员：

- `skills/script-video-shot-director/references/cases/2026-10-18-stepback-continuous.md`

### CYCLE-05

已确认的一条环：

`skills/script-visual-assets/SKILL.md` → `skills/script-visual-assets/references/case-ingestion-policy.md` → `skills/script-visual-assets/references/cross-skill-adaptation.md` → `skills/script-visual-assets/references/production-baseline.md` → `skills/script-visual-assets/SKILL.md`

成员：

- `skills/script-visual-assets/SKILL.md`
- `skills/script-visual-assets/references/ai-news-policy.md`
- `skills/script-visual-assets/references/case-ingestion-policy.md`
- `skills/script-visual-assets/references/creative-delivery-policy.md`
- `skills/script-visual-assets/references/credit-policy.md`
- `skills/script-visual-assets/references/cross-skill-adaptation.md`
- `skills/script-visual-assets/references/cross-skill-policy.md`
- `skills/script-visual-assets/references/daily-report-template.md`
- `skills/script-visual-assets/references/dual-save-policy.md`
- `skills/script-visual-assets/references/improvements/2026-10-16.md`
- `skills/script-visual-assets/references/learning-log.md`
- `skills/script-visual-assets/references/learning-policy.md`
- `skills/script-visual-assets/references/pending-review-policy.md`
- `skills/script-visual-assets/references/production-baseline.md`
- `skills/script-visual-assets/references/release-1.1.0.md`

全部直接互引对（行号按修复后扫描）：

- `skills/script-visual-assets/SKILL.md` 第[47]行 ↔ `skills/script-visual-assets/references/creative-delivery-policy.md` 第[8]行。
- `skills/script-visual-assets/SKILL.md` 第[65]行 ↔ `skills/script-visual-assets/references/production-baseline.md` 第[13]行。
- `skills/script-visual-assets/references/cross-skill-adaptation.md` 第[20]行 ↔ `skills/script-visual-assets/references/improvements/2026-10-16.md` 第[29]行。
- `skills/script-visual-assets/references/learning-log.md` 第[22, 52, 71, 82, 112, 133]行 ↔ `skills/script-visual-assets/references/learning-policy.md` 第[125]行。

可供用户决定的拆解方向：先将实际“先读”依赖改成入口到叶子规则的单向关系；叶子文件的返回索引可保留为说明性回链，并给加载器加已读集合。历史日志和案例自指可单列文档导航图，不作为递归加载指令。这里只提出方案，本次没有实施这些改变。

## 历史资源缺口：没有冒充通过

三套范围内45处均在影视历史日志/案例/测试记录中：25处文件不在当前仓库，20处只写通用文件名，存在多个可能对象，无法据此确定唯一目标。原上下文明确这些是旧云端快照、历史回执或原会话生成图片；当前Git历史未检出所核查的两份旧回执和原会话图片，不能补写替代“原件”。这些是可追溯性缺口，不是已验证存在的文件；保留原历史事实，后续有原件才可恢复。

| 来源 | 行号 | 历史标识 | 状态 |
|---|---:|---|---|
| `skills/script-video-shot-director/references/cases/2026-10-18-stepback-continuous.md` | 115 | `before.json` | historical_ambiguous |
| `skills/script-video-shot-director/references/learning-log.md` | 141 | `history/AUDIT-20261014-01-reserve1/before.json` | historical_artifact_unavailable |
| `skills/script-video-shot-director/references/learning-log.md` | 141 | `manifest.json` | historical_ambiguous |
| `skills/script-video-shot-director/references/learning-log.md` | 148 | `history/AUDIT-20261014-01-reserve2/before.json` | historical_artifact_unavailable |
| `skills/script-video-shot-director/references/learning-log.md` | 148 | `manifest.json` | historical_ambiguous |
| `skills/script-video-shot-director/references/learning-log.md` | 155 | `history/AUDIT-20261014-01-reserve3/before.json` | historical_artifact_unavailable |
| `skills/script-video-shot-director/references/learning-log.md` | 155 | `manifest.json` | historical_ambiguous |
| `skills/script-video-shot-director/references/learning-log.md` | 162 | `history/AUDIT-20261014-01-complete/before.json` | historical_artifact_unavailable |
| `skills/script-video-shot-director/references/learning-log.md` | 162 | `manifest.json` | historical_ambiguous |
| `skills/script-video-shot-director/references/learning-log.md` | 169 | `history/AUDIT-20261014-01-receipt/before.json` | historical_artifact_unavailable |
| `skills/script-video-shot-director/references/learning-log.md` | 169 | `manifest.json` | historical_ambiguous |
| `skills/script-video-shot-director/references/learning-log.md` | 178 | `history/SCOPE-NEWS-20261014-01/before.json` | historical_artifact_unavailable |
| `skills/script-video-shot-director/references/learning-log.md` | 178 | `manifest.json` | historical_ambiguous |
| `skills/script-video-shot-director/references/learning-log.md` | 187 | `history/REPORT-CREDIT-20261014-01/before.json` | historical_artifact_unavailable |
| `skills/script-video-shot-director/references/learning-log.md` | 187 | `manifest.json` | historical_ambiguous |
| `skills/script-video-shot-director/references/learning-log.md` | 195 | `references/audit/governance/REPORT-CREDIT-20261014-01-save-receipt.json` | historical_artifact_unavailable |
| `skills/script-video-shot-director/references/learning-log.md` | 214 | `references/audit/governance/REPORT-CREDIT-20261014-01-dual-save-receipt.json` | historical_artifact_unavailable |
| `skills/script-video-shot-director/references/learning-log.md` | 222 | `history/STYLE-PREPROD-20261014-01/before.json` | historical_artifact_unavailable |
| `skills/script-video-shot-director/references/learning-log.md` | 222 | `manifest.json` | historical_ambiguous |
| `skills/script-video-shot-director/references/learning-log.md` | 230 | `history/STYLE-PREPROD-20261014-01-RECEIPT/before.json` | historical_artifact_unavailable |
| `skills/script-video-shot-director/references/learning-log.md` | 230 | `manifest.json` | historical_ambiguous |
| `skills/script-video-shot-director/references/learning-log.md` | 238 | `history/INLINE-AUDIT-20261014-01/before.json` | historical_artifact_unavailable |
| `skills/script-video-shot-director/references/learning-log.md` | 238 | `manifest.json` | historical_ambiguous |
| `skills/script-video-shot-director/references/learning-log.md` | 257 | `history/AUDIT-20261015-01-news-reserve/before.json` | historical_artifact_unavailable |
| `skills/script-video-shot-director/references/learning-log.md` | 257 | `manifest.json` | historical_ambiguous |
| `skills/script-video-shot-director/references/learning-log.md` | 264 | `history/AUDIT-20261015-01-reserve1/before.json` | historical_artifact_unavailable |
| `skills/script-video-shot-director/references/learning-log.md` | 264 | `manifest.json` | historical_ambiguous |
| `skills/script-video-shot-director/references/learning-log.md` | 271 | `history/AUDIT-20261015-01-reserve2/before.json` | historical_artifact_unavailable |
| `skills/script-video-shot-director/references/learning-log.md` | 271 | `manifest.json` | historical_ambiguous |
| `skills/script-video-shot-director/references/learning-log.md` | 278 | `history/AUDIT-20261015-01-reserve3/before.json` | historical_artifact_unavailable |
| `skills/script-video-shot-director/references/learning-log.md` | 278 | `manifest.json` | historical_ambiguous |
| `skills/script-video-shot-director/references/learning-log.md` | 285 | `history/AUDIT-20261015-01-complete/before.json` | historical_artifact_unavailable |
| `skills/script-video-shot-director/references/learning-log.md` | 285 | `manifest.json` | historical_ambiguous |
| `skills/script-video-shot-director/references/learning-log.md` | 292 | `history/AUDIT-20261015-01-receipt/before.json` | historical_artifact_unavailable |
| `skills/script-video-shot-director/references/learning-log.md` | 292 | `manifest.json` | historical_ambiguous |
| `skills/script-video-shot-director/references/learning-log.md` | 302 | `history/AUDIT-20261015-01-USER-VERDICT-01/before.json` | historical_artifact_unavailable |
| `skills/script-video-shot-director/references/learning-log.md` | 302 | `manifest.json` | historical_ambiguous |
| `skills/script-video-shot-director/references/learning-log.md` | 309 | `history/HUMAN-BRIEF-20261016-01/before.json` | historical_artifact_unavailable |
| `skills/script-video-shot-director/references/learning-log.md` | 309 | `manifest.json` | historical_ambiguous |
| `skills/script-video-shot-director/references/learning-log.md` | 324 | `history/CREATIVE-DELIVERY-CASES-20261015-01/before.json` | historical_artifact_unavailable |
| `skills/script-video-shot-director/references/learning-log.md` | 324 | `manifest.json` | historical_ambiguous |
| `skills/script-video-shot-director/references/learning-log.md` | 333 | `history/VERSION-20261016-01/before.json` | historical_artifact_unavailable |
| `skills/script-video-shot-director/references/test-20261013-01.md` | 12 | `exec-05a857c0-29ce-4ecf-a019-67e8c457ace6.png` | historical_artifact_unavailable |
| `skills/script-video-shot-director/references/test-20261013-01.md` | 13 | `exec-005af2e8-2a6a-44bd-bd6c-ab4d01f244f5.png` | historical_artifact_unavailable |
| `skills/script-video-shot-director/references/test-20261013-01.md` | 14 | `exec-be5e5f43-0bd9-4beb-ae30-603b4d9c484e.png` | historical_artifact_unavailable |

辅助跟踪的暂存证据记录还含1处不可定位的旧案例主记录及2处明确未公开的私有素材入口；未将这些缺口统计进588处三套引用，也未上传私有原件或伪造占位文件。逐条记录见机器清单。

## 检测工具和验证

- 新增可重复运行的检测器及20项测试，覆盖失效相对路径、跨包共享路径、大小写、百分号编码、引用式链接、中文文件名/连接词、模板、间接环、自指和无环共用依赖。
- 版本一致性及11项版本规则场景通过；162个Skill文件完整性通过；既有审计门禁14项测试通过。仅修路径和说明，未新增生成测试、候选票、技巧入库或积分。
- 检测器返回2表示“循环/历史缺口待审”，不宣称退出码0全通过。本次普通文件加载检查零缺失，但总体保留待审状态。
- 三套按已批准规则从V1.1.0递增到V1.1.1；README Changelog不添加修订号条目；commit/PR标题包含V1.1.1。
- 修改前的完整备份：`backup/pre-link-audit-20261023`，固定源提交如上；本地完整Git bundle已核验。

复现命令：

```bash
python3 tools/check_references.py --follow-outside --json /tmp/skill-references.json
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools/tests
python3 tools/verify_backup.py
```

完整机器记录见[引用与全部循环边](references.json)、[修复前未决项](before-issues.json)、[汇总和修复映射](summary.json)。每条引用均记录来源、行号、原目标、解析方式与状态；这里的静态验证不证明生成模型效果或其他会话已加载。
