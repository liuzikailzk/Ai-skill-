# 知识图书馆导航

正文只有一份权威来源。分类与短目录是可重建视图；全库可见不等于全库可执行。

## 按任务检索

- [production-film](views/production-film.md)
- [production-assets](views/production-assets.md)
- [production-manga](views/production-manga.md)
- [analysis-film](views/analysis-film.md)
- [analysis-assets](views/analysis-assets.md)
- [analysis-manga](views/analysis-manga.md)
- [learning](views/learning.md)
- [maintenance](views/maintenance.md)
- [lookup](views/lookup.md)

## 内容所在位置

- skills：三套入口与媒介专用正文。
- knowledge/shared：公共规则。
- knowledge/catalog.json：带状态和精确定位的运行目录。
- pending-review：候选、来源与审计证据，按状态使用。
- history 与各级 archive：历史追溯，不执行旧指令。
- registry：版本、恢复与清单。
- tools：确定性检索、读取与检查工具。

完整路径清单见 [library-inventory.json](../registry/library-inventory.json)。新增正文后更新元数据，再运行 tools/build_knowledge_views.py；不要手工维护第二份知识。
