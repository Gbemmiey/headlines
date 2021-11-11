from flask import Flask, render_template
import feedparser

app = Flask(__name__)

RSS_FEEDS = {
    'bbc':'http://feeds.bbci.co.uk/news/world/africa/rss.xml',
    'cnn': 'http://rss.cnn.com/rss/edition_africa.rss',
    'punch': 'https://rss.punchng.com/v1/category/latest_news'
    }

@app.route('/')
def getNews():
    current_feed = RSS_FEEDS['bbc']
    feed = feedparser.parse(current_feed)
    # first_article = feed['entries'][0]
    return render_template("home.html", articles=feed['entries'])

if __name__ == '__main__':
    app.run(port=5000, debug=True)