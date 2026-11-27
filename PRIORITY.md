# 优先权与引用说明 / Priority and Citation

本文件只记录可公开核对的事实，不主张“首创”“首次提出”一类无法验证的排他性优先权。

## 公开记录

- **首次公开日期**：2026-11-23
- **公开仓库**：<https://github.com/chenzeyu2026/mathhist-toolkit>
- **首发 commit**：`eaae8c823e093f9d92023e7be01f423352bb500d`
- **版本**：v0.2.0
- **DOI（v0.2.0）**：`10.5281/zenodo.24455228`
- **Concept DOI**：`10.5281/zenodo.24455227`

## v0.2.0 的公开内容

- **16 类节点**：概念、方法、定理、问题、理论、失败路线、记号、文本、见证、人物、事件、机构、期刊、分支、教学点、主张（以 `spec/object-model.md` 为准）。
- **36 类边**：每类边的端点定义域/值域、方向、属性、条件必填、等级上限与释义，集中保存在 `spec/framework/edge-signatures.yaml`。
- **两个试点**：`pilots/group-theory/`（51 节点 / 80 边）与 `pilots/calculus/`（58 节点 / 102 边）。
- **边签名单源**：`graph.schema.json` 的边枚举与 `spec/object-model.md` §5.2 / §5.6 的表格均由 `edge-signatures.yaml` 生成。
- **`graphlint`**：提供 `check`、`check-all`、`generate [--check]`；校验端点类型与方向、条件必填、证据等级上限、环、权重和、互斥关系、孤立节点与 `claims` 引用。

## 如需引用

优先使用仓库根目录的 `CITATION.cff`。v0.2.0 的版本 DOI 为 <https://doi.org/10.5281/zenodo.24455228>，Concept DOI 为 <https://doi.org/10.5281/zenodo.24455227>。也可引用：

> Chen Zeyu. *mathhist-toolkit: evidence tags and a graph ontology for the history of mathematics*. v0.2.0, 2026-11-23. <https://doi.org/10.5281/zenodo.24455228>.

DOI 获取步骤见 [`docs/zenodo-doi.md`](docs/zenodo-doi.md)。
