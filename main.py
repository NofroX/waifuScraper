from html.parser import HTMLParser
from urllib.request import Request, urlopen
import time, random


class WaifuHTMLParser(HTMLParser):
    name_state = None
    name = None
    s_link = None
    w_link = None
    characters = None

    def __init__(self):
        super().__init__()
        self.characters = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for i in attrs:
                if not i[1] is None:
                    if i[0] == 'href':
                        if i[1][0:7] == '/waifu/':
                            self.w_link = i[1]
                            self.name_state = True
                        if i[1][0:8] == '/series/':
                            self.s_link = i[1]

    def handle_data(self, data):
        if self.name_state:
            self.name = data
            self.name_state = False
        elif self.s_link is not None:
            self.characters.append(tuple([self.name, data, self.w_link, self.s_link]))
            self.s_link = None

    def get_characters(self):
        return self.characters


hdr = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8'}


def scrape_page(page, f):
    site = f"https://mywaifulist.moe/husbandos?page={page}"

    req = Request(site, headers=hdr)
    page = urlopen(req)
    data = page.read()
    page.close()
    parser = WaifuHTMLParser()
    parser.feed(data.decode("utf8"))
    return parser.get_characters()


with open("husbandos.db", "a") as f:
    for i in range(1, 10):
        list = scrape_page(i, f)
        s = ""
        for e in list:
            s += f'"{e[0]}", "{e[1]}", "{e[2]}", "{e[3]}"\n'
        f.write(s)
        print(f"{i}/10")
        time.sleep(4+random.uniform(0, 12))
