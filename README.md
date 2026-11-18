# CyberFrank · 赛博弗兰克

个人站点 — FDE（Forward Deployed Engineer / 前向部署工程师）定位作品集。

- 十年企业级系统集成 × AI 原生产品
- 技术栈：纯静态 HTML/CSS/JS（零依赖、零图片、秒级加载）
- 部署：Vercel 生产环境；自定义域名 `cyberfrank.is-a.dev`（is-a.dev CNAME 到 `cname.vercel-dns.com`）
- 配色：CAMP 坎普 K9「变色蓝」灵感（深蓝 → 青蓝 → 深紫）

## 本地预览
直接用浏览器打开 `index.html` 即可。

## 更新技能与在研项目
站点内容的可变部分写在 `data/projects.json`。修改 JSON 后运行：

```bash
python3 scripts/render-site.py
```

脚本会把数据填进 `index.html` 里 `BEGIN:GENERATED:*` 标记之间的区块，站点仍然是单文件静态页，不需要在浏览器里再请求 JSON。

**不要在 JSON 或页面上放价格、购买按钮或收款信息。** `cyberfrank.is-a.dev` 受 [is-a.dev 服务条款](https://github.com/is-a-dev/register/blob/main/TERMS_OF_SERVICE.md) 约束，禁止商业 / 营利用途。本页只做作品展示；售卖走 WorkBuddy、闲鱼等独立渠道。如果以后有公开的技能详情 / 安装 URL，把它写到对应条目的 `install.url`。

## 部署到 Vercel
```bash
vercel --prod
```
或把变更推送到 GitHub 后由已绑定的 Vercel 项目自动发布。本仓库的补丁默认只停在本地分支，不自动 push。

## 目录
- `index.html` — 站点主页面（单文件）
- `data/projects.json` — 技能与在研项目的数据源
- `scripts/render-site.py` — 把 JSON 渲染进 HTML
- `CNAME` / `vercel.json` — 域名与 Vercel 配置
