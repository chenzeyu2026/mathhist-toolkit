# 用 Zenodo 为 mathhist-toolkit 获取 DOI

Zenodo 的 GitHub 集成只能用仓库所有者的 GitHub 账号在网页上授权，命令行无法代办。以下步骤由仓库所有者本人完成；完成后把 DOI 回填到仓库即可。

## 前置条件

- GitHub 仓库已公开：<https://github.com/chenzeyu2026/mathhist-toolkit>
- 已创建 Release：`v0.2.0`（Zenodo 在 Release 发布后才会归档并分配 DOI）

## 操作步骤

1. 打开 <https://zenodo.org>，点 **Sign in with GitHub**，用 `chenzeyu2026` 账号登录并授权。
2. 点右上角头像 → **Settings** → 左侧 **GitHub**。
3. 在仓库列表中找到 `chenzeyu2026/mathhist-toolkit`，把右侧开关拨到 **On**。首次开启时 Zenodo 会请求读取公开仓库的权限，确认授权。
4. 回到 GitHub 仓库，确认 **Releases** 中已有 `v0.2.0`。若还没有，以该 tag 创建 Release；Zenodo 只归档已发布的 Release，不归档草稿或普通 commit。
5. 回到 Zenodo 的 **Settings → GitHub** 页面，等待几秒到几分钟。该 Release 旁边会出现一个 DOI，形如 `10.5281/zenodo.XXXXXXX`。
6. 复制 DOI，回填到以下位置：
   - `CITATION.cff`：取消 `# doi:` 的注释并填入，例如 `doi: "10.5281/zenodo.XXXXXXX"`
   - `README.md` 与 `README.en.md` 顶部的首发信息
   - `PRIORITY.md`
7. 提交并推送回填改动。

## 说明

- **版本 DOI** 对应单个 Release（如 v0.2.0）；**Concept DOI** 始终指向该项目的最新版本。引用具体版本时用版本 DOI，引用项目整体时可用 Concept DOI。
- 以后发布新 Release 会得到新的版本 DOI；旧 DOI 仍然有效，指向旧版本。
- 如果仓库列表里看不到目标仓库，先确认 Zenodo 的 GitHub 授权是否包含该仓库，再刷新页面。
