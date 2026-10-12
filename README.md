# AI制作工作台

管理三套 Skill 的同步副本、历史、学习资料与制作素材。**规则维护来源始终是 ChatGPT 维护端已成功保存的文件**；GitHub 不独立修改制作规则。

三套 Skill：`script-visual-assets`、`script-video-shot-director`、`manga-reasoning-storyboard`。

## 当前可用情况

- 已提供独立导入、版本记录、SHA-256 校验、完整快照历史及制作交付包导出工具，仅需 Python 3.12，无第三方依赖。
- 真实 Skill 尚未收到。`registry/latest.json` 中版本、修订和更新时间均为空，不能用基线 1.0 冒充已导入文件。
- 维护端 → Codex：**手动导入，等待文件**。没有聊天文件读取或自动同步连接。
- Codex → GitHub：本次保存结果见 [验证记录](docs/verification.md)。每次后续导入仍需提交、推送并核对远端。
- GitHub → 两个制作会话：**未接通**。拟用附件手动导入；两端实际读取均**未验证**。
- 新增独立的 GitHub 仓库核验任务，计划每天北京时间 08:00 及入库变化后运行，详见 [云端核验](docs/cloud-monitoring.md)。ChatGPT 维护源仍未接通；既有工作日 09:00 学习、周五总结、周末休息安排保持不变。

## 无需写代码的使用流程

1. 在维护端完成学习、测试并成功保存 Skill 后，让它导出完整文件包及保存说明，格式见 [文件交接](docs/synchronization.md)。不从未保存的聊天草稿导出。
2. 把该包上传到 Codex，并说：“按仓库同步流程导入维护端已保存的文件；核对版本与修订、完整性和撤回记录，提交到 GitHub，并生成制作交付包。”首次交接需要全部三套；后续可以只交付变化的 Skill，但每套必须完整。
3. Codex 校验、保存历史并推送后，将最新版清单和制作交付包分别交给所需制作会话，粘贴 [接入指令](docs/production-access.md)。交付包由真实文件生成，当前尚无真实交付包。
4. 收到制作会话的实际读取回执后，再记录该会话采用的版本。接入文字、仓库测试、文件上传或单纯“已同步”回答均不能代替读取证据。

## 目录

| 路径 | 用途 |
| --- | --- |
| `registry/latest.json` | 轻量最新清单、每个文件的 SHA-256、版本/修订与历史索引 |
| `registry/snapshots/<Skill>/<标识>/payload/` | 按原样保存每次导入的完整文件，首次真实导入时建立 |
| `tools/skill_sync.py` | 手动导入、校验、状态和交付包导出 |
| `tests/test_skill_sync.py` | 仅使用临时合成材料的工具测试 |
| `docs/synchronization.md` | 来源、发布规则、导入格式及同步步骤 |
| `docs/production-access.md` | 两段可粘贴指令和读取回执要求 |
| `docs/project-isolation.md` | A、B 等独立制作项目的管理约定 |

## 工具检查（由 Codex 执行）

在仓库根目录运行：

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
python3 tools/skill_sync.py status
python3 tools/skill_sync.py verify
```

`status` 只读取清单；`verify` 完整校验已导入文件。首次真实导入前，`verified_snapshots: 0` 只表示没有可校验文件，**不表示三套 Skill 已验证**。
