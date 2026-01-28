import urllib.request
from html.parser import HTMLParser
import re

class SimpleHTMLTextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = []

    def handle_data(self, d):
        self.text.append(d)

    def get_text(self):
        return "".join(self.text)

def fetch_text_from_url(url: str) -> str:
    """
    Fetches text content from a URL using standard library.
    Basic implementation to satisfy 'URL input' requirement without external deps.
    """
    try:
        # User agent to avoid some basic blocks
        headers = {'User-Agent': 'Mozilla/5.0'}
        req = urllib.request.Request(url, headers=headers)

        with urllib.request.urlopen(req) as response:
            html_content = response.read().decode('utf-8')

        parser = SimpleHTMLTextExtractor()
        parser.feed(html_content)
        text = parser.get_text()

        # Clean up whitespace
        clean_text = re.sub(r'\s+', ' ', text).strip()
        return clean_text

    except Exception as e:
        print(f"Error fetching URL {url}: {e}")
        return ""
