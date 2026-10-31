# 证据矩阵与独立性

候选：ASSET-REFERENCE-SCOPE-20261031-S。证据核对日期2026-10-31。S表示身份核验的一手文档，不表示效果已验证。

| 核心主张 | 支持证据 | 反对/边界 | 置信度与缺口 |
|---|---|---|---|
| Gen-4 Image References可使用上传图像作为对象等特征的输入，并用文字指定变化 | [S1：Runway官方References说明](https://help.runwayml.com/hc/en-us/articles/40042718905875-Creating-with-Gen-4-Image-References) | 支持入口功能，不保证任意道具的细部不变 | 功能事实高；本次茶壶保真效果未知 |
| 复杂变化应逐项试验，避免同时增加多个变量 | [S1：官方迭代说明](https://help.runwayml.com/hc/en-us/articles/40042718905875-Creating-with-Gen-4-Image-References) | 文档承认增加变量会增加结果变化；不是无漂移保证 | 文档建议高；提示词改善幅度未知 |
| Gen-4 Image的Vary动作会产生结构或构图不同的变体 | [S2：Runway官方Image说明](https://help.runwayml.com/hc/en-us/articles/37053594806419-Creating-with-Gen-4-Image) | 该判断仅适用此文档中的Vary动作，不扩张为所有模型同名功能 | 功能定义高；不能由此推算References成功率 |
| 只知道模型名仍不足以照抄引用语法和入口 | [S1](https://help.runwayml.com/hc/en-us/articles/40042718905875-Creating-with-Gen-4-Image-References)与[S3：Scenario自身接入说明](https://help.scenario.com/articles/6803483730-runway-gen-4-references) | Scenario写明API渠道与image_1等标签；不代表Runway网页或豆包语法 | 渠道差异高；用户账号未实测 |
| 这组完整词能提高同一道具换背景的保真度 | 尚无合格直接证据 | 无目标图像输出，第三次反证查询失败 | 低；不通过证据票和复现票 |

来源链接、发布/更新日期及短快照见 sources.json。

S1和S2同属Runway，不能充当两家独立证据。S3由Scenario发布，对其自家API入口是第一方；大量功能介绍与Runway相似，不能当独立效果对照。搜索返回的Replicate发布页及Runway官方宣传仍非独立实测。媒体教程未核实独立实验条件；论文镜像仅检索摘录、未取得原作者全文，不用于核心判断。没有达到“1个S/A＋1个独立A/B”的候选效果证据门槛。

反证查询返回 isError=true 且无内容，不能写“未发现反例”。现有官方功能边界来自前两次检索及已知链接直读，不能冒充第三次查询成功。
