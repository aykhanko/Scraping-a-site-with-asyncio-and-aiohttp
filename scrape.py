import requests
from bs4 import BeautifulSoup
import time
import json
import asyncio
import aiohttp

start = time.time()

async def news_links():
    async with aiohttp.ClientSession() as session:
        links_list = []
        url = "https://globalnews.ca/"
        response = await session.get(url)
        soup = BeautifulSoup(await response.text(), "html.parser")
        links = soup.find_all("a", class_ = "c-posts__inner")
        for i in links:
            href = i["href"]
            if href.startswith("https://globalnews.ca/news/"):
                links_list.append(href)
        return links_list


async def news(url):
    async with aiohttp.ClientSession() as session:
        response = await session.get(url)
        soup = BeautifulSoup(await response.text(), "html.parser")
        title = soup.find("h1", class_ = "l-article__title")
        datetime = soup.find("div", class_ = "c-byline__date c-byline__date--pubDate")
        text = soup.find("article", class_ = "l-article__text js-story-text")
        return {
            "Title": title.text if title else "None",
            "Date": datetime.text.strip() if title else "None",
            "Text": text.text.replace("\n", "") if title else "None" 
        }

async def main():
    links = await news_links()
    tasks = []
    for count, link in enumerate(links, start=1):
        print(f"{count} news saved ...")
        tasks.append(news(link))

    results = await asyncio.gather(*tasks)
    with open ("globalnews.json", "w", encoding="utf8") as f:
        f.write(json.dumps(results, indent=4, ensure_ascii=False))

asyncio.run(main())

end = time.time()
print(end -start)