# 2026-11-10 A周周二：风格锁定与视觉审美

**今天的具体改动：统一整体画风，但把棉布、釉瓷和黄铜的可见表面分别写清楚。** 用途是静态材质测试，不是某个项目的新资产设定。材料理论有依据；这组自然语言写法只有文本核对，**未形成经过出图验证的可用版**，不用于普通制作的默认流程。

完整整合试写（已包含风格词；无需自行拼接）：
```text
生成一张16:9横向静态材质测试图，无运镜，所有物体保持静止。
暖灰色哑光桌面上，从左到右依次放置：一块折叠整齐的灰蓝色棉布、一只直立的白色上釉瓷杯、一只盖子闭合的未涂漆黄铜圆盒。三个物体彼此留有间隔，不重叠、不接触。杯口、杯把与盒盖完整可见，物体底部自然贴住桌面。
中近景，略俯视的四分之三展示视角，三个物体完整入画并清晰可辨。背景为素净暖灰色，不添加其他物品、人物、文字、Logo或水印。
左前上方一盏大型中性白色柔光照明，三个物体接受同一光源，接触阴影与投影方向一致，亮部保留细节。
棉布：折边有厚度，表面保留细小而克制的棉纤维织纹，明暗过渡柔缓，不出现釉面式的连续亮斑。
瓷杯：表面平整细腻，白色釉层上保留沿杯身曲面延伸的清楚高光，与布料的纤维表面明显不同。
黄铜盒：呈黄铜本色，表面有细微拉丝与随曲面变化的环境明暗反射，仍能看清盒盖边缘；不表现成黄色涂漆、塑料或自行发光的物体。
整体风格：柔和的风格化3D静物画面，圆润简洁的造型，克制的细节密度，低饱和蓝、米白与少量黄铜色，干净清楚的轮廓，统一的建模与渲染语言；保留各物体本身的材质差异。
```

独立配套风格词（供单独调用，不能代替主体与材质说明）：
```text
柔和的风格化3D静物画面，圆润简洁的造型，克制的细节密度，低饱和蓝、米白与少量黄铜色，干净清楚的轮廓，统一的建模与渲染语言；保留各物体本身的材质差异。
```

必要参考输入：本组是纯文本静态测试，不需上传参考图；不存在上传顺序或视频片段对应。动态驱动词不适用。模型、入口、实际分辨率和种子尚未选择/运行，不能声称豆包或其他指定模型已经验证。完整实验基线也备份在prompts.json，基线是本次构造而非用户旧作。只将“三种材质都呈现柔和细腻的质感。”替换为三条材质分述，其余逐字相同；不把词更长算进步。真实结果：输入更明确且变量可对照，视觉效果未知。

## 1. 当日审计结论
北京时间2026-11-10，AUDIT-20261110-01。课表工具确定A周周二style，未补跑11月2–7日或重复昨日。三次顺序技巧查询3/3成功，独立资讯1/1成功，额外0次。**证据不足，今日不入库。** 缺独立输入效果证据及真实图像复现；人类票未收到。

## 2. 候选与时效
候选：STYLE-MATERIAL-SEPARATION-20261110-S，归资产，潜在迁移影视/漫画静态输入；核心价值是把已有材质差异检查落实到完整试写。不是新Skill，也不改变已确认项目风格。

来源标题、作者、链接与级别见下一表；S1年份2012，S2日期未知，S3为CVPR2024，S4为2024-07-26。今日核对的是原文相关章节，没有把检索抓取日期当发布日或阅读全文声明。
证据核对日2026-11-10；最后真实验证通过日=null。基础理论无固定到期；提示词推断保守按6个月于2027-05-10前重审，候选可在2026-11-13周五查看，均不是active有效期。平台信息未作为依赖，未来选入口时重新核验，默认30天复核。

现有位置：skills/script-visual-assets/references/cross-skill-adaptation.md“光影与材质”。四维各1项实质配对：
| 维度 | 旧约束与本次变化 | 配对分 |
|---|---|---|
| 步骤 | 已有材质差异检查 → 本次逐物体可见描述 | 0.5 |
| 场景 | 同为静态资产展示 | 1 |
| 结果 | 同为材料可分辨 | 1 |
| 限制 | 非保证性约束 → 加入生成模型形状漂移边界 | 0.5 |
等权重合度75%，仅为现有规则补充。它是治理比对近似，不是效果评分；保留原有中性展示与单一静态状态要求。

## 3. 证据矩阵与独立性
| 核心主张 | 支持来源 | 反对/质疑信息 | 置信度及缺口 |
|---|---|---|---|
| 在统一风格/光源下仍需区分材料表面响应 | S1, S2 | 两者讨论着色器而非提示词；Adobe部分同源。 | 高（限着色理论）；不能外推为文字输入必定奏效。 |
| 逐物体写可见表面表现，可能比统一“柔和细腻”更易辨材质 | S1, S2 | S3/S4显示材料与形状控制有边界；本写法无生成对照。 | 低（待测推断）；缺独立A/B来源及真实图像。 |
| 更详细材质词不能保证几何、反光和物理正确 | S3, S4 | Alchemist是2024专门编辑方法，不能证明2026任一模型必失败。 | 中（适用范围有限）；本次目标模型/入口未选定。 |

- S1（S）：Brent Burley, Walt Disney Animation Studios，2012，[Physically Based Shading at Disney](https://blog.selfshadow.com/publications/s2012-shading-course/burley/s2012_pbs_disney_brdf_notes_v3.pdf)。
- S2（S）：Adobe / Allegorithmic；读取页面未确认个人作者，发布日期未知，[The PBR Guide – Part 2; Part 1用于核对同源关系](https://www.adobe.com/learn/substance-3d-designer/web/the-pbr-guide-part-2)。
- S3（S）：Prafull Sharma, Varun Jampani, Yuanzhen Li, Xuhui Jia, Dmitry Lagun, Fredo Durand, Bill Freeman, Mark Matthews，2024，[Alchemist: Parametric Control of Material Properties with Diffusion Models](https://openaccess.thecvf.com/content/CVPR2024/papers/Sharma_Alchemist_Parametric_Control_of_Material_Properties_with_Diffusion_Models_CVPR_2024_paper.pdf)。
- S4（S）：Mark Matthews and Yuanzhen Li, Google Research，2024-07-26，[Smoothly editing material properties of objects with text-to-image models and synthetic data](https://research.google/blog/smoothly-editing-material-properties-of-objects-with-text-to-image-models-and-synthetic-data/)。

- S1 / S2：partially_independent；发布团队不同但Adobe Part1明确其着色模型基于Disney；不是两项独立提示词实测。
- S3 / S4：not_independent；同一Alchemist项目、作者重合，论文与作者博客只算一组。
- S1/S2 / S3/S4：independent_research_context_not_effect_validation；后者独立研究生成式材料控制的边界，但不是本次三物体中文试写的独立A/B测评。

缺少本提示词写法的独立A/B效果证据；不满足证据票。

## 4. 反证与真实复现
第三次查询命中Alchemist原论文的具体失败：粗糙度修改后仍有明显光泽、透明编辑中几何缺失。它是专门训练的2024编辑模型，不是对本中文输入的直接测试；用于否定“写上术语就保证正确”的外推。未检出本次写法的独立成功对照，不等于已证明它无效。

实际：阅读一手相关章节、编写基线和改写、核对风格与非材质段一致；图片0，视频0，无真实成功率、参数或种子。预期是材质辨识改善且风格/轮廓/布局不变；尚未验证。可用图片未提供，因为本阶段仅输入设计并未提交可视候选验收，不为每日任务强造图片，不申请或扩张生成/付费授权。
最小复现计划：确定并记录同一静态模型/入口后，使用prompts.json两版输入；有种子就配对，没有则记录随机性；完整保留输出并检查材质、形状、布局、光源和画风。材质仍糊成塑料、杯把/盒盖变形、布局变更或画风被写实细节替代均算失败。单组样本也不推导成功率。静态通过不能替动态与声音验证。

## 5. 七问反方自检
1. **最可能错在哪里？** 把着色理论当成文生图控制能力。S1/S2只支持材料原理；本次提示词改善效果未知。
2. **是否过时、弃用或已有替代？** 2012/2024资料作为原理与历史限制，不冒充2026模型评测；Alchemist是专门训练方案，不是复制几句词的等价替代。
3. **来源是否互抄／同源？** S1/S2部分同源，S3/S4同一项目；缺本写法的独立效果验证来源。
4. **是否仅特定版本、付费方案或地区有效？** 本次未选生成模型与入口，账户权限、价格与地区适用未知；没有新增付费或生成授权。
5. **有没有更简单、更优替代？** 先删掉把全部材质统一哑光/同光泽的总括约束，再只补出错物体的可见特征；已有合格图时可作为参考，但本次无图且未验证编辑入口。
6. **现在复现最可能失败在哪里？** 仍全部呈塑料感；为了呈现细节偏离画风；改材质同时改杯把/盒盖/布局；把反射写成自发光。
7. **是否为完成任务而强行写入？** 不申请正式入库，不声称新Skill。仅保存一次现有材质规则的补充试写和反证；不强造样张或评分。

## 6. 状态与三票
状态candidate。证据票未通过（缺独立效果证据）；复现票未通过（未实际生成）；人类票未收到。没有自评总分、用户评分或虚构样本。

| 套别 | 具体适用性 | 验证边界与本次处理 |
|---|---|---|
| 资产 | 静态材质分述试写 | 仅文本核对，候选保存 |
| 影视 | 将来可用于确认后的首帧材质说明 | 视频光影/动作/声音未测，未写入制作 |
| 漫画 | 仅适用于用户选择3D改编的情况 | 无原作验证，不改变2D默认画风 |

积分余额仍为7；本次只登记唯一待核“完整空审计”+3事件，实际入账0，须核验聊天完整交付并待周五人类确认；不为来源、反证或迁移重复计奖。

## 7. 版本与保存范围
影视V1.4.8、资产V1.4.8、漫画V1.3.8保持。仅保存候选、证据、提示词、资讯和运行账，并同步active-index、catalog、目录哈希；没有发布制作能力，不改README大版本Changelog或重建任务。
备份：backup/pre-audit-20261110（7f036bfa2402f2031eb3c7830a8f81d40dae0d63），及完成前backup/pre-audit-20261110-complete（235fb107189562d0a44fe0d930c1cf0556f40514）；两者均远端回读核实。本地隔离工作树保留恢复副本。查询预留PR[#90](https://github.com/liuzikailzk/Ai-skill-/pull/90)已合并且四文件回读后才检索。
本批正文的实际PR、diff检查、main逐文件回读与保存范围，记录在同目录save-receipt.json；本报告不是保存回执。检查结果及目录哈希在validation.json，缺失或失败时不能称规整完成。旧日期账、credit_events、余额、兑换与冻结记录保持。

## 8. 原始检索留痕
| slot | 用途 | 真实查询式 | 北京时间（2026-11-10） | 结果 |
|---|---|---|---|---|
| 1 | candidate | `Disney physically based shading roughness diffuse metals fabric principled` | 04:04:28.179 +08:00 | 成功：Disney材质模型参数及派生实现；同一框架允许材料差异。 |
| 2 | cross_validation | `Adobe PBR guide roughness metal dielectric lighting material appearance` | 04:04:34.114 +08:00 | 成功：Adobe教程解释粗糙度与金属；其底层明确基于Disney，不能算完全独立。 |
| 3 | counterevidence | `text to image material appearance roughness lighting disentanglement limitations failure` | 04:04:39.649 +08:00 | 成功：Alchemist原论文及作者说明：材质控制与形状可能纠缠，专门方法也有失败；非本次改写实测。 |
| 4 | 独立资讯 | `AI model tools release November 9 2026 official announcement` | 04:04:46.191 +08:00 | 成功：广泛扫描模型与工具新发布；追溯确认Anthropic 5.2与Seedream 5.5官方11月9日发布。 |

引擎均system1，每个调用1个查询式；技巧无recency限制（理论检索），资讯recency=2天。直接打开返回来源不计新查询，没有访问搜索页绕限。query-ledger.json保存预算投影，唯一主账仍是skills/script-video-shot-director/references/audit/global-state.json。
来源短快照含标题、作者、日期、范围、摘录与SHA-256；search-1至4.json保留真实输入/时间/命中元数据与原响应哈希。完整工具响应仅临时本地校核，不全文转载；不可将摘要称整页快照。候选与报告均在pending-review/2026-11-10/；资讯在skills/script-video-shot-director/references/audit/news/2026-11-10/。保存结果以main回读回执为准。

---

# 2026-11-10 独立AI资讯

run_id：NEWS-20261110-01。北京时间截止：2026-11-10T04:12:44.159788+08:00。默认观察窗：上一轮2026-11-09约04:03至本轮；本次唯一查询recency=2天，逐条核对实际发布日期，旧发布不重复计新增。查询1/1，未增加技巧查询。

## 最新AI资讯
- **Claude Fable 5.2 / Mythos 5.2，11月9日发布。** Anthropic公布新版本，官方称编码、推理与视觉能力有改进。Fable可从Claude Platform与所列云平台访问；Mythos仍需相应验证项目。对本工作流的潜在用途是复杂资料分析或程序维护，不是已验证的提示词改良；本轮未实测，也未切换工具或购买服务。[原始公告](https://www.anthropic.com/claude-fable-and-mythos-5-2)

## 市面上新技术、工具与能力
- **Seedream 5.5，11月9日发布。** 官方介绍原生RGBA透明资产和连续编辑，并展示100轮编辑示例。对资产/海报的潜在用途是输出可合成素材；对影视/漫画只涉及静态参考，不能据此宣称视频或原作还原通过。页面提供Dola与BytePlus Playground入口，但本账户功能、地区和费用未核实；Pro版是后续预告。100轮与画质改进均属官方展示，本轮没有生成、下载样例或观看演示视频。[原始公告](https://seed.bytedance.com/en/blog/more-realistic-images-more-stable-editing-across-100-rounds-introducing-seedream-5-5)

两项公告分属不同团队，均是一手发布证据；没有独立效果测评，不参与当天技巧候选证据票。其他搜索线索未在本轮追溯核实，不作为确定新闻。来源短快照与日期见sources/，查询见queries.json；保存核验回执指向当天唯一回执。
