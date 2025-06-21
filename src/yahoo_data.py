import yfinance as yf
import time
import pandas as pd



def format_large_number(value):
    if value is None:
        return None
    elif value >= 1_000_000_000_000:
        return f"{value / 1_000_000_000_000:.2f}T"
    elif value >= 1_000_000_000:
        return f"{value / 1_000_000_000:.2f}B"
    elif value >= 1_000_000:
        return f"{value / 1_000_000:.2f}M"
    else:
        return f"{value:,}"  # e.g., 45,000

class StockDataFetcher:
    def get_stock_data(self, stock_symbol, max_retries=3, retry_delay=5):
        for attempt in range(max_retries):
            try:
                if attempt > 0:
                    time.sleep(retry_delay)

                stock = yf.Ticker(stock_symbol)

                # 1-day price for current
                hist_1d = stock.history(period='1d')
                if hist_1d.empty:
                    raise ValueError(f"No recent price data for {stock_symbol}")
                current_price = hist_1d['Close'].iloc[-1]

                # 1-year history for high/low/volume
                hist_1y = stock.history(period='1y')
                year_high = hist_1y['High'].max() if not hist_1y.empty else None
                year_low = hist_1y['Low'].min() if not hist_1y.empty else None
                last_volume = hist_1y['Volume'].iloc[-1] if not hist_1y.empty else None

                # Try market cap from info
                try:
                    info = stock.info
                    market_cap = info.get('marketCap')
                    pe_ratio = info.get('trailingPE')
                    dividend_yield = info.get('dividendYield')
                except:
                    market_cap = None
                    pe_ratio = None
                    dividend_yield = None


                return {
                    'success': True,
                    'data': {
                        'name': stock_symbol,
                        'current_price': round(float(current_price), 2),
                        'currency': 'USD',
                        'fifty_two_week_high': round(float(year_high), 2) if year_high else None,
                        'fifty_two_week_low': round(float(year_low), 2) if year_low else None,
                        'volume': format_large_number(last_volume),
                        'market_cap': format_large_number(market_cap),
                        'pe_ratio': f"{pe_ratio:.2f}" if pe_ratio else "N/A",
                        'dividend_yield': f"{dividend_yield:.2f}%" if dividend_yield else "N/A%"

                    }
                }

            except Exception as e:
                print(f"Error fetching stock data (attempt {attempt + 1}): {str(e)}")
                if attempt == max_retries - 1:
                    return {
                        'success': False,
                        'error': f"Failed to fetch stock data for {stock_symbol} after {max_retries} attempts: {str(e)}"
                    }
                
    
    def get_stock_dataframe(self, stock_symbol, period="6mo", interval="1d"):
        """Fetch historical stock data as a DataFrame for plotting"""
        ticker = yf.Ticker(stock_symbol)
        hist = ticker.history(period=period, interval=interval)
        if hist.empty:
            raise ValueError(f"No stock data found for {stock_symbol}")
        return hist


