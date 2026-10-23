# 审计记录字段

与record-template.json一起使用。缺项用null／空列表并记录理由；本文件中的结构说明不是实际证据。每个候选单独JSON，引用输出文件或快照而非仅写“已通过”。

| 字段 | 填写要求 |
|---|---|
| id、skill、status、origin | 唯一条目、所属包、六状态之一、来源是新候选或历史待审 |
| searches | 3个有序对象：slot=1/2/3、query、time（含时区）、scope、summary、result_status=completed/failed；引用共用日台账查询ID，不重新执行 |
| sources | 每来源：id、title、author、published_at、updated_at、url、tier、first_party、identity_verified、retrieved_at；snapshot含excerpt、captured_at、read_scope、sha256、path；未知日期说明缺口 |
| independence | first、second为来源ID；verdict=independent/partially_independent/not_independent；reason写作者团队、发布时间、互引和同源分析 |
| evidence_matrix | 每项：claim、supports（来源ID）、opposes、confidence、reason；不能把支持无关主张的链接凑到核心主张上 |
| reproduction | environment（模型、版本、平台入口、账户/地区条件）、输入材料定位及SHA-256、steps、parameters（完整提示词与设置）、seed_availability、expected、actual（artifact定位与校验值、观察结果）、failure_conditions、passed；结果不完整不得passed |
| human_vote | approved、revoked、version、user_quote、time、review_id；必须能定位用户对该条目该版本的真实确认；不自动填true |
| currency | kind=volatile/generation/theory；last_verified、expires_on、期限选择理由；theory需current_version_applicable |
| overlap | dimensions四项：维度名、对照位置、comparisons逐项理由、points为0/0.5/1数组、denominator为两边原子项较大数；percent据规则计算 |
| adversarial_review | 对应七问的七条真实回答与证据定位 |
| scores | 原量规五项分、自评、用户终评、差异、至少两项真实不确定点；未覆盖组合写待裁定，不捏造总分 |
| proposal_action、existing_skill | iteration或new_skill；≥70%必须iteration并定位已有Skill，无增量不凑修订 |
| regression | fixed_task、环境、固定输入及参数、old_run、new_run、comparison、passed、rollback_target；记录真实输出及时间 |
| version_comparison | 维度、旧版、新版、依据、预期、回退；proposed_version仅是提案不改已发布号 |
| release | verified及verification_evidence须来自真实保存后回读；不能在保存前写已核验 |
| rejected、unresolved_conflict、fatal_counterevidence、compliance_block | 按事实填写并附理由；不能仅为让门禁通过而清空 |

预算／积分：只在影视分镜包的global-state.json维护。每次搜索先登记run_id、日期、slot、query、scope和状态reserved；调用后记真实结果。每条信用事件或兑换记录唯一ID、条目、来源／证据、时间、分值、余额及理由；冻结起止日期明确。并发或保存不确定时先停新查询、恢复账本一致性，不能双重消费。

门禁脚本位于影视分镜Skill scripts/audit_gate.py，用法（在仓库根目录执行，record.json替换为实际记录路径）：
`python skills/script-video-shot-director/scripts/audit_gate.py <record.json> --ledger skills/script-video-shot-director/references/audit/global-state.json --date YYYY-MM-DD`

脚本只读并检查所填字段之间的最低逻辑，不会检索、投人类票、证明来源真实、证明输出有效或自动发布；需审计员逐项看原始证据。测试样例仅在tests/中，使用example.invalid及fixture标签，禁止进入真实证据库、信用账本或发布清单。
