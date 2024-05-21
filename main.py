import scrapetube
import requests
from bs4 import BeautifulSoup

def extract_title(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, features="lxml")
    title_tag = soup.find("title")
    if title_tag:
        title = title_tag.text.strip()
        return title.replace(" - YouTube", "")
    return None

with open('channel_ids.txt', 'r') as file:
    channel_ids = file.readlines()

urls = []

base_url = "https://youtube.com/shorts/"

for channel_id in channel_ids:
    channel_id = channel_id.strip()
    videos = scrapetube.get_channel(channel_id, content_type="shorts", sort_by="newest", limit=6)

    if videos is None:
        print(f"No videos found for channel ID {channel_id}")
        continue

    channel_urls = []

    for video in videos:
        url = base_url + str(video['videoId'])
        channel_urls.append(url)

    channel_urls.reverse()
    urls.extend(channel_urls)

with open('generated_urls.txt', 'w') as file:
    for url in urls:
        file.write(url + '\n')

print("URLs extracted and saved to generated_urls.txt")

for url in urls:
    title = extract_title(url)
    if title:
        with open('titles.txt', 'a', encoding='utf-8') as outfile:
            outfile.write(title + '\n')

print("Titles extracted and saved to titles.txt")
