# 历史证据矩阵原记录

从原候选记录补录；不重查、不改票据。

```json
{
  "matrix": [
    {
      "claim": "输入中的运动模糊/动态姿态等可能与静止主体指令冲突；可作为诊断线索。",
      "supports": [
        "S1"
      ],
      "opposes": [],
      "confidence": "中",
      "reason": "官方当前文档给出相关机制与单例描述；欠独立A/B与本次实跑，不能断言普遍因果或成功率。"
    },
    {
      "claim": "去除不需要的视觉运动线索能在目标输入中改善主体静止结果。",
      "supports": [
        "S1"
      ],
      "opposes": [],
      "confidence": "低",
      "reason": "仅官方示例的文字解释；未观看样片、没有本地同参数A/B、第三查询无相关结果。"
    },
    {
      "claim": "该改法不保证锁定相机，也没有Seedance或漫画原格通用效果证据。",
      "supports": [
        "S1"
      ],
      "opposes": [],
      "confidence": "高",
      "reason": "官方停车示例本身要求相机绕行；同页相机静止FAQ仍限定为尝试。跨模型/媒介效果未查得，保持未验证。"
    }
  ],
  "independence": [
    {
      "first": "S1",
      "second": "S2",
      "verdict": "not_independent",
      "reason": "相同Runway团队；均为厂商帮助文档，非两个独立实验。S1/S2发布日期均未知，不根据时间假定独立。"
    },
    {
      "first": "S1",
      "second": "C1",
      "verdict": "partially_independent",
      "reason": "用户原帖叙述自己的失败，没有在所读段落转抄官方文本；但匿名身份、关联和材料来源不全，无法确认完全独立。任务与版本不同，相关评论赞数不足，不能作独立A/B。"
    },
    {
      "first": "S1",
      "second": "C2",
      "verdict": "partially_independent",
      "reason": "不同署名与组织，2025-12-22文中把自做测试和官方样片分开。自做测试段有原创步骤，但文章也引官方指南；没有与候选对应的图生对照，不能用文生物理测试补该票。"
    },
    {
      "first": "S2",
      "second": "C3",
      "verdict": "not_independent",
      "reason": "2026-05-17文章、2026-06-18更新明确链接S2，声明按厂商文档查核，未给独立对照素材；措辞相近符合转述，时间不用于证明抄袭。"
    }
  ]
}
```
