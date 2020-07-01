import bs4, requests, datetime, urllib.parse
from config import token, chat_id


rq = "https://telegg.ru/orig/bot"
def get_news_from_billiardsu(starting_url):
    links = []
    now = datetime.datetime.now()
    r1 = requests.get(starting_url)
    coverpage = r1.content
    soup1 = bs4.BeautifulSoup(coverpage, 'lxml')
    coverpage_news = soup1.find_all("tr")
    for row in coverpage_news:
        t = row.find("time")
        if t is not None:
            date = t.get_text()
            if int(date[0]+date[1]) == now.day and int(date[3]+date[4]) == now.month:
                kek = row.find("a")
                links.append("billiard.su/"+kek['href']+ row.get_text())
    return links


def post(text):
    t = urllib.parse.quote_plus(text)
    requests.get(rq+token+"/sendMessage?chat_id="+chat_id+"&text="+t)


urls = [
    "http://billiard.su/news_list.asp"
]

get_news_from_billiardsu(urls[0])
bsu_news = get_news_from_billiardsu(urls[0])

f = open('webLinks.txt', 'r')
cache_links = f.read()
f.close()
f = open('webLinks.txt', 'a')
for url in bsu_news:
    if url[:url.find('\n')] not in cache_links:
        post(url)
        f.write(url[:url.find('\n')]+'\n')
f.close()