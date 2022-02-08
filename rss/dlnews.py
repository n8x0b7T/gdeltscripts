from rss_parser import Parser
from requests import get
import json


rss_urls = open("rss.txt").read().split("\n")

stories = []

for i in rss_urls:

    xml = get(i, verify=False)
    print(i+":")
    # Limit feed output to 5 items
    # To disable limit simply do not provide the argument or use None
    parser = Parser(xml=xml.content, limit=5)
    feed = parser.parse()

    # Iteratively print feed items
    for item in feed.feed:
        towrite = {}
        towrite["title"] = item.title
        towrite["description"] = item.description
        stories.append(towrite)

print(json.dumps(stories))

with open("result.json", "a+") as f:
    f.write(json.dumps(stories))
