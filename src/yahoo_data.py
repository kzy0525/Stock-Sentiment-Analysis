import yfinance as yf
import time

class StockDataFetcher:
    def get_stock_data(self, stock_symbol, max_retries=3, retry_delay=5):
        for attempt in range(max_retries):
            try:
                if attempt > 0:
                    time.sleep(retry_delay)

                stock = yf.Ticker(stock_symbol)
                hist = stock.history(period='1d')

                if hist.empty:
                    raise ValueError(f"No historical data found for {stock_symbol}")

                current_price = hist['Close'].iloc[-1]
                fast_info = stock.fast_info  # Still okay for non-critical extras

                return {
                    'success': True,
                    'data': {
                        'name': stock_symbol,
                        'current_price': current_price,
                        'currency': fast_info.get('currency', 'USD'),
                        'fifty_two_week_high': fast_info.get('year_high'),
                        'fifty_two_week_low': fast_info.get('year_low'),
                        'volume': fast_info.get('last_volume'),
                        'market_cap': fast_info.get('market_cap', 'N/A')  # fallback if .info fails
                    }
                }

            except Exception as e:
                print(f"Error fetching stock data (attempt {attempt + 1}): {str(e)}")
                if attempt == max_retries - 1:
                    return {
                        'success': False,
                        'error': f"Failed to fetch stock data for {stock_symbol} after {max_retries} attempts: {str(e)}"
                    }
