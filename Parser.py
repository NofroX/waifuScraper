from html.parser import HTMLParser
from urllib.request import Request, urlopen


characters = []


def add_character(name, series):
    characters.append(tuple([name, series]))


class WaifuHTMLParser(HTMLParser):

    name_state = False
    name = None
    series_state = False

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for i in attrs:
                if not i[1] is None:
                    if i[0] == 'href':
                        if i[1][0:7] == '/waifu/':
                            self.name_state = True
                        if i[1][0:8] == '/series/':
                            self.series_state = True

    def handle_data(self, data):
        if self.name_state:
            self.name = data
            self.name_state = False
        elif self.series_state:
            add_character(self.name, data)
            self.series_state = False


site = "https://mywaifulist.moe/husbandos"
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8'}

req = Request(site, headers=hdr)
page = urlopen(req)
data = page.read()
page.close()

parser = WaifuHTMLParser()
print(data.decode('utf8'))
parser.feed(data.decode("utf8"))
print(characters)

