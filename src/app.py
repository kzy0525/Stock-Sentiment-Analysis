from flask import Flask, render_template, request, jsonify
import os
import pandas as pd
from dotenv import load_dotenv
from sentiment import RedditSentimentAnalyzer
from yahoo_data import StockDataFetcher
from plots import SentimentPlotter
import uuid  
import re
import glob



# Load environment variables
load_dotenv()

ticker_df = pd.read_csv(os.path.join('datasets', 'tickers.csv'))
ticker_df.dropna(subset=['Symbol', 'Name'], inplace=True)

# Explicitly set the templates folder
app = Flask(__name__, template_folder='templates', static_folder='../static')

# Initialize analyzers
sentiment_analyzer = RedditSentimentAnalyzer()
stock_fetcher = StockDataFetcher()
plotter = SentimentPlotter()

def remove_links(text):
    if not text:
        return ""
    # Remove Markdown-style links: [text](url)
    text = re.sub(r'\[([^\]]+)\]\((https?://[^\)]+)\)', r'\1', text)
    # Remove raw URLs
    text = re.sub(r'https?://\S+', '', text)
    return text.strip()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        plot_folder = os.path.join('static', 'plots')
        for file in glob.glob(os.path.join(plot_folder, '*.png')):
            os.remove(file)

        stock_symbol = request.form.get('stock_symbol', '').upper()
        print(f"Received symbol: {stock_symbol}")

        sentiment_data = sentiment_analyzer.analyze_sentiment(stock_symbol)
        print(f"Sentiment data received: {sentiment_data.keys()}")

        for post in sentiment_data.get("top_posts", []):
            post["body"] = remove_links(post.get("body", ""))

            
        stock_data = stock_fetcher.get_stock_data(stock_symbol)
        print(f"Stock data keys: {stock_data.keys()}")

        # Step 1: Generate plot figures
        sentiment_scores = sentiment_data.get("sentiment_scores", [])
        average_sentiment = sentiment_data.get("average_sentiment", 0)

        sentiment_fig = plotter.plot_sentiment_distribution(sentiment_scores, average_sentiment)

        stock_df = stock_fetcher.get_stock_dataframe(stock_symbol, period="1y", interval="1d")
        stock_fig = plotter.plot_stock_price(stock_df)

        # Step 2: Build both absolute and relative paths for saving
        relative_sentiment_path = f"static/plots/{uuid.uuid4().hex}_sentiment.png"
        absolute_sentiment_path = os.path.join(os.getcwd(), relative_sentiment_path)
        plotter.save_plot(sentiment_fig, absolute_sentiment_path)

        relative_stock_path = f"static/plots/{uuid.uuid4().hex}_stock.png"
        absolute_stock_path = os.path.join(os.getcwd(), relative_stock_path)
        plotter.save_plot(stock_fig, absolute_stock_path)

        # Step 3: Return with proper browser-accessible paths
        return jsonify({
            'stock_symbol': stock_symbol,
            'sentiment': sentiment_data,
            'stock_data': stock_data,
            'sentiment_plot': '/' + relative_sentiment_path,
            'stock_plot': '/' + relative_stock_path
        })
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/tickers')
def get_tickers():
    query = request.args.get('q', '').lower()
    matches = ticker_df[
        ticker_df['Symbol'].str.lower().str.contains(query) |
        ticker_df['Name'].str.lower().str.contains(query)
    ]
    results = matches.head(10).to_dict(orient='records')
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
