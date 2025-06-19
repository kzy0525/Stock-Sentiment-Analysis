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
        sentiment_data = sentiment_analyzer.analyze_sentiment(stock_symbol)
        stock_df = stock_fetcher.get_stock_dataframe(stock_symbol)  # Ensure this returns a DataFrame with 'Close'

        # Plot sentiment distribution
        sentiment_scores = pd.Series([p['sentiment'] for p in sentiment_data['posts']])
        sentiment_fig = plotter.plot_sentiment_distribution(sentiment_scores)
        sentiment_filename = f"static/plots/sentiment_{uuid.uuid4().hex}.png"
        plotter.save_plot(sentiment_fig, sentiment_filename)

        # Plot stock price chart
        stock_fig = plotter.plot_stock_price(stock_df)
        stock_filename = f"static/plots/stock_{uuid.uuid4().hex}.png"
        plotter.save_plot(stock_fig, stock_filename)

        return jsonify({
            'stock_symbol': stock_symbol,
            'sentiment_plot': sentiment_filename,
            'stock_plot': stock_filename
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
