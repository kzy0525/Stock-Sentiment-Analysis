from flask import Flask, render_template, request, jsonify
import os
import pandas as pd
from dotenv import load_dotenv
from sentiment import RedditSentimentAnalyzer
from yahoo_data import StockDataFetcher
from plots import SentimentPlotter
import uuid  


# Load environment variables
load_dotenv()

ticker_df = pd.read_csv(os.path.join('datasets', 'tickers.csv'))
ticker_df.dropna(subset=['Symbol', 'Name'], inplace=True)

# Explicitly set the templates folder
app = Flask(__name__, template_folder='templates')

# Initialize analyzers
sentiment_analyzer = RedditSentimentAnalyzer()
stock_fetcher = StockDataFetcher()
plotter = SentimentPlotter()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        stock_symbol = request.form.get('stock_symbol', '').upper()
        print(f"📈 Received symbol: {stock_symbol}")

        sentiment_data = sentiment_analyzer.analyze_sentiment(stock_symbol)
        print(f"✅ Sentiment data received: {sentiment_data.keys()}")

        stock_data = stock_fetcher.get_stock_data(stock_symbol)
        print(f"✅ Stock data keys: {stock_data.keys()}")

        sentiment_plot_path = f"static/plots/{uuid.uuid4().hex}_sentiment.png"
        stock_plot_path = f"static/plots/{uuid.uuid4().hex}_stock.png"

        sentiment_fig = plotter.plot_sentiment_distribution(sentiment_data.get("sentiment_scores", []))
        plotter.save_plot(sentiment_fig, sentiment_plot_path)

        stock_fig = plotter.plot_stock_price(stock_data.get("data", pd.DataFrame()))
        plotter.save_plot(stock_fig, stock_plot_path)

        return jsonify({
            'stock_symbol': stock_symbol,
            'sentiment': sentiment_data,
            'stock_data': stock_data,
            'sentiment_plot': sentiment_plot_path,
            'stock_plot': stock_plot_path
        })
    except Exception as e:
        print(f"❌ Error: {e}")
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
