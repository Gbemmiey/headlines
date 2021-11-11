from flask import Flask, render_template, request
import feedparser

app = Flask(__name__)

RSS_FEEDS = {
    'bbc':'http://feeds.bbci.co.uk/news/world/africa/rss.xml',
    'cnn': 'http://rss.cnn.com/rss/edition_africa.rss',
    'punch': 'https://rss.punchng.com/v1/category/latest_news'
    }

@app.route('/')
def getNews():
    query = request.args.get("publication")
    # ?publication=punch
    if not query or query.lower() not in RSS_FEEDS:
        publication = "bbc"
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    # first_article = feed['entries'][0]
    return render_template("home.html", articles=feed['entries'], publisher=publication.upper())

if __name__ == '__main__':
    app.run(port=5000, debug=True)