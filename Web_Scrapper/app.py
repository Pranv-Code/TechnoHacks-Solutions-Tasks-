from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

app = Flask(__name__)

def scrape_news(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    news = []
    seen = set()

    for a in soup.find_all("a"):
        if len(news) == 10:
            break

        title = a.get_text(strip=True)
        href = a.get("href")

        if not title or not href:
            continue
        if len(title) < 20:
            continue

        link = urljoin(url, href)

        if link in seen:
            continue

        seen.add(link)
        news.append({"title": title, "link": link})

    return news



@app.route("/", methods=["GET", "POST"])
def index():
    news = []
    if request.method == "POST":
        url = request.form["url"]
        news = scrape_news(url)
    return render_template("index.html", news=news)


if __name__ == "__main__":
    app.run(debug=True)

