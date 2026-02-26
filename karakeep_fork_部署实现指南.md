# Karakeep 项目调研：Fork、实现原理与部署指南

目标仓库：`https://github.com/karakeep-app/karakeep`

## 1. 项目定位
Karakeep（原 Hoarder）是一个可自托管的「万物收藏」应用，支持链接、笔记、图片、PDF 的保存，并带有抓取、检索和 AI 自动标注能力。

核心特性：
- 网页收藏与自动元信息抓取（标题、描述、缩略图）
- 列表协作、全文搜索
- AI 自动摘要/打标签（可接 OpenAI 或本地 Ollama）
- OCR、RSS 自动归档、视频归档等扩展能力

## 2. 技术栈与实现方式（How it works）
根据官方文档与目录结构，系统为 Monorepo，核心实现可分为以下部分：

### 2.1 Monorepo 结构
- `apps/web`：主 Web 应用（Next.js）
- `apps/workers`：后台异步任务 Worker
- `apps/mobile`：移动端（React Native / Expo）
- `apps/browser-extension`：浏览器扩展
- `packages/db`：数据库 schema 与迁移
- `packages/trpc`：核心业务逻辑（tRPC 路由）
- `packages/shared`：共享配置、日志、公共模块

### 2.2 运行架构
在官方文档中，典型运行由三个关键服务组成：
1. **Web 服务**：对外提供 UI 与 API
2. **Worker 服务**：消费后台任务（抓取、AI 推理、索引等）
3. **Meilisearch**：全文检索引擎

另有一个独立的 Headless Chrome 容器用于页面抓取（crawler）。

### 2.3 任务流（典型）
1. 用户提交一个链接/资源
2. Worker 触发抓取任务，使用 Headless Chrome 拉取内容
3. 提取文本、元数据、封面图等
4. 可选调用 AI（OpenAI/Ollama）生成标签与摘要
5. 把可检索内容写入 Meilisearch
6. 前端通过检索与过滤展示结果

## 3. 如何 Fork 这个项目

> 我在当前环境完成了仓库拉取与分析；但由于没有你的 GitHub 账号授权，无法代你在 GitHub 网页上真正创建 fork。下面给你可直接执行的两种方式。

### 3.1 网页方式（最简单）
1. 打开：`https://github.com/karakeep-app/karakeep`
2. 点击右上角 **Fork**
3. 选择你的账号/组织，创建 fork
4. 在你的 fork 页面复制仓库地址

### 3.2 命令行方式（GitHub CLI）
先登录：
```bash
gh auth login
```
执行 fork 并本地克隆：
```bash
gh repo fork karakeep-app/karakeep --clone
```
如果你已经先 clone 了 upstream，也可以追加你的 fork 远端：
```bash
git remote rename origin upstream
git remote add origin git@github.com:<your_name>/karakeep.git
git push -u origin main
```

## 4. 最快部署方案：Docker Compose
这是官方推荐的入门部署方式。

### 4.1 准备目录与 compose
```bash
mkdir karakeep-app
cd karakeep-app
wget https://raw.githubusercontent.com/karakeep-app/karakeep/main/docker/docker-compose.yml
```

### 4.2 创建 `.env`
最小可运行配置：
```env
KARAKEEP_VERSION=release
NEXTAUTH_SECRET=替换成随机字符串
MEILI_MASTER_KEY=替换成随机字符串
NEXTAUTH_URL=http://localhost:3000
```
建议生成随机字符串：
```bash
openssl rand -base64 36
```

### 4.3 启动
```bash
docker compose up -d
```
访问：`http://localhost:3000`

### 4.4 可选：启用 AI
在 `.env` 增加：
```env
OPENAI_API_KEY=<你的key>
```
或改走 Ollama（本地模型），参考官方 AI Provider 配置文档。

## 5. 生产部署建议（简版）

### 5.1 必做项
- 用反向代理（Nginx/Caddy/Traefik）接入 HTTPS
- `NEXTAUTH_URL` 设为公网域名（如 `https://keep.example.com`）
- 强随机 `NEXTAUTH_SECRET` 与 `MEILI_MASTER_KEY`
- 做数据卷备份（`/data` 与 meilisearch 数据）

### 5.2 建议项
- 设置 `LOG_LEVEL=warning`（生产环境减少噪音）
- 给 Worker 和 Meilisearch 设资源限制
- 对象存储/外部存储按需启用（大规模场景）

## 6. 本地二次开发（实现级）

### 6.1 一键开发启动
在仓库根目录：
```bash
./start-dev.sh
```
该脚本会自动拉起 Meilisearch、Headless Chrome、安装依赖并并行启动 web+workers。

### 6.2 手动开发（更可控）
```bash
# 安装 Node 24、启用 corepack
pnpm install
cp .env.sample .env
pnpm run db:migrate
pnpm web
pnpm workers
```

## 7. 你可以直接照抄的上线流程（推荐）
1. 在 GitHub Fork 到你自己的账号
2. 在你的服务器 clone 你的 fork
3. 使用官方 `docker/docker-compose.yml` + `.env` 启动
4. 配置反向代理 + HTTPS
5. 配置备份与监控
6. 后续升级通过修改 `KARAKEEP_VERSION` 或 `docker compose up --pull always -d`

---
如果你愿意，我下一步可以给你一份**按你服务器环境定制**的版本（例如：Ubuntu + Docker + Nginx + Cloudflare），包含可直接复制执行的命令清单和配置文件模板。
