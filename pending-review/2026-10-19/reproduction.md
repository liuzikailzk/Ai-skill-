# 静态联合试验 AUDIT-20261019-01

环境：内置image_gen，一次生成；后端型号/版本/seed/采样参数未暴露，不能写为Seedance。原始无参考图，原创走廊与保安。图片storyboard.png，1672×941，SHA-256 fa6758a1ab871daa693efaac8c7cc83fd018b3528b7487196006cc33fadf8c6b。

## 实际完整输入

Use case: illustration-story. Create ONE storyboard contact sheet with THREE stacked widescreen panels, clean cinematic realistic charcoal-and-muted-color concept art. Original test, not based on any copyrighted story. No text or labels. Fixed scene: a narrow gray hallway, a single closed dark red door on the RIGHT wall, brushed silver horizontal lever. One adult male security worker, short black hair, olive work jacket, no hat. Cold overhead lighting. Panel 1: wide establishing view, worker at LEFT facing screen-right toward the red door at RIGHT, both visible, standing motionless. Panel 2: close-up of same worker's face and olive collar, face in left half looking screen-right into empty gray negative space; the door is completely OUTSIDE this crop. He is motionless, alert, lips closed. Panel 3: extreme close-up of the same red door's silver horizontal lever and door surface only, lever still horizontal; worker is outside crop. No hand, no monster, no extra people or doors. Static camera in each panel; no motion blur. Maintain worker identity, door material and lighting. This is one static first-frame sequence testing offscreen spatial continuity, not a depiction of completed movement.

## 逐镜首帧与试验时间轴

时间为拟剪辑计划，不是已生成视频：
1. 00:00–00:02，全景，固定机位；男子静立左侧朝右看，灰走廊右侧红门与银把手同时入画。
2. 00:02–00:04，脸部特写，固定机位；同一男子静止警觉朝画右看，脸在左半部，门在画外，右侧灰墙留空。
3. 00:04–00:06，把手大特写，固定机位；红门银色水平把手静止，人物在画外。
声音本要素不适用，原因是仅静态试验；漫画原作/气泡本要素不适用，原因是无原漫画输入。主体动作均为静止状态，无动态效果声称。

## 预期/真实输出/失败

预期同人同门，局部取景不带入画外对象，每格16:9。
实际：人物短发、橄榄夹克、朝画右方向基本一致；第二格门未入画，第三格人物未入画。失败：每格约5.3:1，并非16:9；第一格门左缘可见铰链，第三格门右缘出现铰链，侧别不一致。空间/资产一致性不通过，人物仅可见部分初检，身体背面未测；没有视频/声音/动作接触，整体复现票不通过。
这是一次失败样张，未进行修图或第二次生成，不隐藏原始结果，不声称失败已修复。
最小下一次方案：先锁定门正视资产与铰链左侧；分开生成三张16:9，逐张引用同一资产；再在真实视频入口做同材料对照，记录型号版本参数、输入和成片。此为计划，未运行；今日不再搜索。