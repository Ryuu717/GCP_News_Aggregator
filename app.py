from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

NEWS_API_KEY = os.getenv('NEWS_API_KEY')

def get_top_headlines():
    url = (
        'https://newsapi.org/v2/top-headlines?'
        'sources=bbc-news&'
        f'apiKey={NEWS_API_KEY}'
    )
    response = requests.get(url)
    return response.json()

def search_news_articles(query):
    url = (
        'https://newsapi.org/v2/everything?'
        f'q={query}&'
        f'apiKey={NEWS_API_KEY}'
    )
    response = requests.get(url)
    return response.json()

def filter_removed_content(articles):
    # Filter out articles with "Removed" in the title or description
    return [
        article for article in articles
        if "Removed" not in article.get('title', '') and
           "Removed" not in article.get('description', '')
    ]

@app.route('/', methods=['GET', 'POST'])
def index():
    articles = []
    if request.method == 'POST':
        query = request.form.get('query')
        search_results = search_news_articles(query)
        articles = search_results.get('articles', [])
    else:
        top_headlines = get_top_headlines()
        articles = top_headlines.get('articles', [])
    
    # Filter out any "Removed" content
    articles = filter_removed_content(articles)
    
    return render_template('index.html', articles=articles)

if __name__ == '__main__':
    app.run(debug=True)
