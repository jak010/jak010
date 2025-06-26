import feedparser
from datetime import datetime

RSS_URL = "https://jakpentest.tistory.com/rss"
README_PATH = "./README.md"
MAX_ITEMS = 5

start_marker = "<!-- RECENTE ARTICLES START -->"
end_marker = "<!-- RECENTE ARTICLES END -->"


def fetch_blog_entries():
    feed = feedparser.parse(RSS_URL)
    entries = feed.entries[:MAX_ITEMS]
    result = []
    for entry in entries:
        date = datetime(*entry.published_parsed[:6]).strftime("%Y-%m-%d")
        result.append(f"- [{entry.title}]({entry.link}) ({date})")
    return "\n".join(result)


def update_readme(content):
    with open(README_PATH, "r", encoding="utf-8") as f:
        readme = f.read()

    start = readme.find(start_marker)
    end = readme.find(end_marker)
    if start == -1 or end == -1:
        raise Exception("Markers not found in README.md")

    new_readme = (
            readme[:start + len(start_marker)] +
            "\n" + content + "\n" +
            readme[end:]
    )

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_readme)


if __name__ == "__main__":
    blog_md = fetch_blog_entries()
    update_readme(blog_md)
