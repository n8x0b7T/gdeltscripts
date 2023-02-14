import feedparser

feeds = open("feeds.txt").read().split("\n")
# print(feeds)
def get_articles_urls(URL):
    d = feedparser.parse(URL)

    urls = []
    for i in d.entries:
        urls.append(i.link)
    return urls

urls = []

for i in feeds:
    current = get_articles_urls(f"https://{i}")
    print(current)
    urls += current

string = ""

for i in urls:
    string += f"{i}\n"

open("articles.txt", "a").write(string)