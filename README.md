# learngit

一个用于学习 Git 基础流程与 Python 小工具开发的示例仓库。

## 项目包含什么

- `git.md`：日常 Git 使用规范与命令速查。
- `get_shortURL.py`：调用微博短链 API，将长链接转换为短链接的命令行工具。
- `requirements.txt`：Python 依赖列表。

## 这个项目的作用

1. **Git 学习**：帮助新手建立“status → diff → add → commit → push”的固定工作流。
2. **API 调用示例**：展示如何在 Python 中通过 `requests` 调用第三方 HTTP API。
3. **CLI 实践**：通过参数化输入（`--url`）实现可复用的小工具。

## 核心实现思路

`get_shortURL.py` 的流程如下：

1. 解析命令行参数（必须传入 `--url`）。
2. 组装请求：
   - API: `https://api.weibo.com/2/short_url/shorten.json`
   - Query 参数：`source` 与 `url_long`
3. 校验响应状态码与响应结构。
4. 从 JSON 的 `urls[0].url_short` 提取短链并输出。

## 本地运行

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python get_shortURL.py --url https://example.com
```

> 提示：`source` 参数依赖微博开放平台应用配置，不同应用需要替换为自己的 `source` 值。

## “Fork 到你自己的项目”怎么做

如果你希望把本仓库 fork 到你自己的 GitHub 账号：

1. 在 GitHub 页面点击 **Fork**。
2. 将你 fork 后的仓库克隆到本地：

```bash
git clone <你的fork仓库地址>
cd <仓库目录>
```

3. 设置上游仓库（方便同步原仓库更新）：

```bash
git remote add upstream <原仓库地址>
git fetch upstream
```

4. 后续同步：

```bash
git checkout main
git merge upstream/main
git push origin main
```

## 如何部署

这个项目是**脚本型工具**，没有 Web 服务，部署通常有三种方式：

1. **个人机器直接运行**（最简单）：用 venv 安装依赖后直接调用脚本。
2. **CI/CD 任务执行**：在 GitHub Actions/Jenkins 中按命令运行，用于批量生成短链。
3. **容器化运行**：写 Dockerfile 打包成镜像，适合团队统一环境。

一个最小 Dockerfile 示例：

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt get_shortURL.py ./
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "get_shortURL.py"]
```

构建与运行：

```bash
docker build -t shorturl-tool .
docker run --rm shorturl-tool --url https://example.com
```
