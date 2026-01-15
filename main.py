import os
import requests
import feedparser
import datetime
from jinja2 import Environment, FileSystemLoader
from openai import OpenAI

# 配置部分
RSS_URLS = [
    "https://www.theverge.com/rss/ai/index.xml",  # The Verge AI
    "https://techcrunch.com/category/artificial-intelligence/feed/",  # TechCrunch AI
    # 你可以添加更多 RSS 源
]
MAX_ITEMS = 5  # 每天选几条新闻
OUTPUT_DIR = "public"


def fetch_news():
    """从 RSS 源抓取新闻"""
    news_items = []
    print("正在抓取新闻...")

    for url in RSS_URLS:
        try:
            feed = feedparser.parse(url)
            print(f"  [OK] From {url} fetched {len(feed.entries)} items")

            for entry in feed.entries[:3]:  # 每个源取前3条
                news_items.append({
                    "title": entry.title,
                    "link": entry.link,
                    "published": entry.get("published", str(datetime.date.today())),
                    "summary": entry.get("summary", entry.get("description", ""))[:200] + "..."
                })
        except Exception as e:
            print(f"  [FAIL] Failed to fetch {url}: {e}")

    # 按发布时间排序（如果有）
    news_items = news_items[:MAX_ITEMS]
    print(f"\n总共获取 {len(news_items)} 条新闻\n")
    return news_items


def summarize_with_ai(news_items):
    """使用 OpenAI API 生成中文摘要"""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("警告: 未找到 OPENAI_API_KEY，跳过 AI 摘要生成。")
        for item in news_items:
            item["ai_summary"] = "（未配置 API Key，无法生成摘要）"
        return news_items

    client = OpenAI(api_key=api_key)
    print("正在调用 AI 生成摘要...")

    for i, item in enumerate(news_items, 1):
        try:
            prompt = f"""请用中文简要总结这篇 AI 新闻，一句话（不超过30字）概括核心价值：

标题: {item['title']}
内容片段: {item['summary']}

请直接输出摘要，不要加任何前缀或解释。"""

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100,
                temperature=0.7
            )

            item["ai_summary"] = response.choices[0].message.content.strip()
            print(f"  [{i}/{len(news_items)}] [DONE] {item['ai_summary'][:30]}...")

        except Exception as e:
            print(f"  [{i}/{len(news_items)}] [ERROR] AI processing failed: {e}")
            item["ai_summary"] = "AI 暂时无法生成摘要。"

    print()
    return news_items


def generate_html(news_items, date):
    """使用 Jinja2 生成 HTML 页面"""
    print("正在生成 HTML 页面...")

    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("index.html")
    html = template.render(news_items=news_items, date=date)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = f"{OUTPUT_DIR}/index.html"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"[DONE] HTML generated: {output_path}")


def main():
    """主函数"""
    print("=" * 50)
    print("AI 每日新闻生成器")
    print("=" * 50)
    print()

    # 1. 抓取新闻
    news = fetch_news()

    if not news:
        print("错误: 未能获取任何新闻，请检查 RSS 源。")
        return

    # 2. AI 生成摘要
    news_with_summary = summarize_with_ai(news)

    # 3. 生成 HTML
    today = datetime.date.today().strftime("%Y年%m月%d日")
    generate_html(news_with_summary, today)

    print("=" * 50)
    print("[DONE] Completed!")
    print("=" * 50)


if __name__ == "__main__":
    main()
