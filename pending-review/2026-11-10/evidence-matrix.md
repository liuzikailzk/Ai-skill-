# 证据矩阵与独立性

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
