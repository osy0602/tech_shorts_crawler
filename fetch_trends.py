"""
Tech Trends Crawler
매일 최신 테크 뉴스 헤드라인을 긁어서 텍스트 파일로 저장
"""

import feedparser
import datetime
import os

# ── RSS 피드 목록 ──────────────────────────────────────────
FEEDS = [
    ("Hacker News",     "https://news.ycombinator.com/rss"),
    ("TechCrunch",      "https://techcrunch.com/feed/"),
    ("The Verge",       "https://www.theverge.com/rss/index.xml"),
    ("Ars Technica",    "https://feeds.arstechnica.com/arstechnica/technology-lab"),
    ("MIT Tech Review", "https://www.technologyreview.com/feed/"),
]

MAX_ITEMS_PER_FEED = 5


def fetch_headlines() -> list[dict]:
    """RSS 피드에서 헤드라인 수집"""
    headlines = []
    for source, url in FEEDS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:MAX_ITEMS_PER_FEED]:
                headlines.append({
                    "source": source,
                    "title": entry.get("title", "").strip(),
                    "summary": entry.get("summary", "")[:300].strip(),
                    "link": entry.get("link", ""),
                })
            print(f"✅ {source}: {min(MAX_ITEMS_PER_FEED, len(feed.entries))}개 수집")
        except Exception as e:
            print(f"❌ {source} 실패: {e}")
    return headlines


def save_output(headlines: list[dict]):
    """결과를 날짜별 파일로 저장"""
    today = datetime.date.today().strftime("%Y-%m-%d")
    os.makedirs("output", exist_ok=True)
    filepath = f"output/{today}_headlines.txt"

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"📰 테크 뉴스 헤드라인 — {today}\n")
        f.write("=" * 50 + "\n\n")
        for h in headlines:
            f.write(f"[{h['source']}]\n")
            f.write(f"제목: {h['title']}\n")
            f.write(f"요약: {h['summary']}\n")
            f.write(f"링크: {h['link']}\n")
            f.write("-" * 40 + "\n")
        f.write(f"\n총 {len(headlines)}개 수집\n")

    print(f"\n💾 저장 완료: {filepath}")
    return filepath


def main():
    print(f"🔍 테크 뉴스 수집 시작 — {datetime.date.today()}\n")

    headlines = fetch_headlines()
    if not headlines:
        print("헤드라인을 가져오지 못했어. 네트워크 확인해봐.")
        return

    print(f"\n총 {len(headlines)}개 헤드라인 수집 완료")
    filepath = save_output(headlines)

    print("\n" + "=" * 50)
    for h in headlines:
        print(f"[{h['source']}] {h['title']}")
        print(f"  {h['link']}\n")


if __name__ == "__main__":
    main()
