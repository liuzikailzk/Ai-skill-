# 历史证据矩阵原记录

从原候选记录补录；不重查、不改票据。

```json
{
  "matrix": [
    {
      "claim": "镜头角度、景别与主体相对关系应分开描述",
      "supports": [
        "S1",
        "S3"
      ],
      "opposes": [
        "S1/S3为同厂；未取得目标入口重复对照"
      ],
      "confidence": "中",
      "reason": "原作者文档明确相关描述；文档支持不是视频效果证明"
    },
    {
      "claim": "画面左右与物体自身左右是不同参照，不能混用",
      "supports": [
        "S2"
      ],
      "opposes": [
        "论文全文读取失败；只有索引摘要，研究对象为T2I而非本视频入口"
      ],
      "confidence": "中",
      "reason": "索引摘要直接讨论参照差异；不能核其全部模型与实验"
    },
    {
      "claim": "仅写过肩镜头并不能据此确认双设备取景和表面朝向",
      "supports": [
        "S3"
      ],
      "opposes": [
        "从术语定义推出的几何检查，不是模型失败实测"
      ],
      "confidence": "中",
      "reason": "定义是从肩后显示角色所看；不包含手机后摄与表盘的全部物理关系"
    },
    {
      "claim": "加入明确相对关系可提高本手表拍摄镜头成功率",
      "supports": [
        "S1"
      ],
      "opposes": [
        "缺同入口独立A/B与真实视频；S2摘要反而提示物体本征方向表述更困难；Q3未命中直接反例不代表无反证"
      ],
      "confidence": "低",
      "reason": "核心效果主张仍为待验证假设"
    }
  ],
  "independence": [
    {
      "first": "S1",
      "second": "S3",
      "verdict": "not_independent",
      "reason": "同属Runway；S1直接引用S3，不能按两票计。"
    },
    {
      "first": "S1",
      "second": "S2",
      "verdict": "partially_independent",
      "reason": "索引署名不同、T2I研究而非厂商教程；全文未读，未完整核查互引/素材，且非目标视频实测，不构成独立A/B票。"
    }
  ]
}
```
