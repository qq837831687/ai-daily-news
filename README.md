# AI 每日简报

> 自动抓取 AI 新闻并生成中文摘要的每日简报网站

[![Build Daily AI News](https://github.com/yourusername/ai-daily-news/actions/workflows/daily_build.yml/badge.svg)](https://github.com/yourusername/ai-daily-news/actions/workflows/daily_build.yml)

## 功能特性

- 🤖 **自动抓取** - 从 The Verge、TechCrunch 等权威源抓取最新 AI 新闻
- 📝 **AI 总结** - 使用 OpenAI GPT-3.5 自动生成中文摘要
- 🌐 **静态网站** - 生成纯 HTML，部署到 GitHub Pages
- ⏰ **每日更新** - GitHub Actions 每天 UTC 0:00 自动运行（北京时间早上8点）
- 📱 **响应式设计** - 完美适配手机、平板、电脑

## 在线预览

访问：`https://yourusername.github.io/ai-daily-news/`

## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/yourusername/ai-daily-news.git
cd ai-daily-news
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，添加你的 OpenAI API Key
# OPENAI_API_KEY=sk-your-key-here
```

**获取 OpenAI API Key：**
1. 访问 [OpenAI Platform](https://platform.openai.com/)
2. 注册/登录账号
3. 进入 API Keys 页面创建新密钥

### 4. 本地运行

```bash
# Windows (CMD)
set OPENAI_API_KEY=sk-your-key-here
python main.py

# Windows (PowerShell)
$env:OPENAI_API_KEY="sk-your-key-here"
python main.py

# Linux/Mac
export OPENAI_API_KEY="sk-your-key-here"
python main.py
```

生成后的 HTML 文件位于 `public/index.html`，用浏览器打开即可查看。

## 部署到 GitHub Pages

### 1. 创建 GitHub 仓库

将项目推送到你的 GitHub 仓库。

### 2. 配置 GitHub Secrets

在仓库设置中添加 OpenAI API Key：

1. 进入仓库 **Settings** → **Secrets and variables** → **Actions**
2. 点击 **New repository secret**
3. Name: `OPENAI_API_KEY`
4. Secret: `sk-your-actual-key-here`

### 3. 启用 GitHub Pages

1. 进入 **Settings** → **Pages**
2. Source 选择 **GitHub Actions**

### 4. 启用 Actions

1. 进入 **Actions** 标签页
2. 启用 workflows（如果提示禁用）
3. 点击 **Run workflow** 手动测试第一次运行

### 5. 访问你的网站

等待几分钟后，访问：`https://yourusername.github.io/ai-daily-news/`

## 自定义配置

### 添加更多新闻源

编辑 `main.py` 中的 `RSS_URLS` 列表：

```python
RSS_URLS = [
    "https://www.theverge.com/rss/ai/index.xml",
    "https://techcrunch.com/category/artificial-intelligence/feed/",
    "https://arstechnica.com/tag/ai/feed/",  # 添加新源
]
```

推荐的 AI 新闻 RSS 源：
- MIT Technology Review: `https://www.technologyreview.com/feed/`
- Ars Technica AI: `https://arstechnica.com/tag/ai/feed/`
- VentureBeat AI: `https://venturebeat.com/ai/feed/`

### 修改新闻数量

编辑 `main.py` 中的 `MAX_ITEMS` 变量：

```python
MAX_ITEMS = 10  # 每天显示10条新闻
```

### 修改更新时间

编辑 `.github/workflows/daily_build.yml` 中的 cron 表达式：

```yaml
schedule:
  - cron: '0 2 * * *'  # UTC 时间 2:00 (北京时间上午10点)
```

Cron 格式：`分钟 小时 日期 月份 星期`
- `0 0 * * *` - 每天 00:00
- `0 12 * * *` - 每天 12:00
- `0 */6 * * *` - 每6小时

### 优化 AI 提示词

编辑 `main.py` 中的 `prompt` 变量：

```python
prompt = f"""请用3个要点总结这篇 AI 新闻，每个要点不超过20字：
标题: {item['title']}
内容: {item['summary']}
"""
```

## 文件结构

```
ai-daily-news/
├── .github/
│   └── workflows/
│       └── daily_build.yml       # GitHub Actions 配置
├── templates/
│   └── index.html                # HTML 模板
├── public/
│   └── index.html                # 生成的静态网站
├── main.py                       # 核心脚本
├── requirements.txt              # Python 依赖
├── .env.example                  # 环境变量示例
└── README.md                     # 使用说明
```

## 常见问题

### Q: GitHub Actions 运行失败？

**A:** 检查以下几点：
1. OpenAI API Key 是否正确配置在 Secrets 中
2. API Key 是否有足够的余额
3. 查看 Actions 日志获取详细错误信息

### Q: 本地运行正常，但部署后无法访问？

**A:**
1. 确认 GitHub Pages 已启用并选择了正确的分支
2. 检查 Actions 是否成功运行
3. 等待几分钟让 CDN 刷新

### Q: 如何控制 API 成本？

**A:**
1. 使用 GPT-3.5 而不是 GPT-4（代码中已默认使用）
2. 减少 `MAX_ITEMS` 数量
3. 缩短 `max_tokens` 参数
4. 使用更简洁的提示词

### Q: 可以换成其他 AI 服务吗？

**A:** 可以！修改 `main.py` 中的 `summarize_with_ai()` 函数：

```python
# 使用 Anthropic Claude
import anthropic
client = anthropic.Anthropic(api_key=api_key)
response = client.messages.create(
    model="claude-3-haiku-20240307",
    max_tokens=100,
    messages=[{"role": "user", "content": prompt}]
)
item["ai_summary"] = response.content[0].text
```

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

## 相关链接

- [OpenAI API 文档](https://platform.openai.com/docs/)
- [GitHub Pages 文档](https://docs.github.com/pages)
- [Feedparser 文档](https://feedparser.readthedocs.io/)
- [Jinja2 文档](https://jinja.palletsprojects.com/)
