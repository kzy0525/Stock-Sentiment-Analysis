import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for Flask
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os
from matplotlib.ticker import FuncFormatter
import matplotlib.lines as mlines


class SentimentPlotter:
    def __init__(self):
        plt.style.use('seaborn-v0_8-darkgrid')
        self.figsize = (14, 14)

    # plots the stock price chart for the given stock data
    def plot_stock_price(self, stock_data, title="Stock Price Chart"):
        fig, ax = plt.subplots(figsize=self.figsize)

        if stock_data is None or stock_data.empty or 'Close' not in stock_data.columns:
            ax.text(0.5, 0.5, 'No stock data available',
                    ha='center', va='center', color='white', fontsize=14)
        else:
            start_price = stock_data["Close"].iloc[0]
            end_price = stock_data["Close"].iloc[-1]
            color = "#498659" if end_price >= start_price else "#dc3545"
            ax.plot(stock_data.index, stock_data["Close"], color=color, linewidth=4)
            ax.fill_between(stock_data.index, stock_data["Close"], color=color, alpha=0.1, zorder=1)
            
            mean_price = stock_data["Close"].mean()
            price_range = stock_data["Close"].max() - stock_data["Close"].min()
            padding = price_range * 0.6
            ax.set_ylim(mean_price - padding, mean_price + padding)

        ax.set_facecolor("#1F1F1F")
        fig.patch.set_facecolor("#1F1F1F")
        ax.tick_params(axis='both', colors='white', labelsize=20)
        ax.spines[['top', 'right']].set_visible(False)
        ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.2, color='white')
        ax.set_title("", color='white')

        ax.set_xticklabels([])
        ax.tick_params(axis='y', pad=12) 
        ax.set_title("1 Year Pricing Data", color='white', pad=20, fontsize=40, fontweight='bold')
        # ax.set_xlabel('1 Year Data', color='white', fontsize=14, labelpad=40)
        # ax.set_ylabel('Price (USD)', color='white', fontsize=14, labelpad=40)
        fig.tight_layout(pad=2)  
        fig.subplots_adjust(top=0.80)  

        ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'${x:,.0f}'))

        return fig

    #plots the sentiment distribution of the posts
    def plot_sentiment_distribution(self, sentiment_scores, average_sentiment=0, title="Sentiment Distribution"):
        print("📊 Sentiment scores received:", sentiment_scores)
        fig, ax = plt.subplots(figsize=self.figsize)

        ax.set_facecolor("#1F1F1F")
        fig.patch.set_facecolor("#1F1F1F")

        if sentiment_scores:
            color = "#498659" if average_sentiment >= 0 else "#dc3545"
            sns.histplot(sentiment_scores, kde=True, ax=ax, color=color)
            for line in ax.lines:
                if isinstance(line, mlines.Line2D):
                    line.set_linewidth(4)
        else:
            ax.text(0.5, 0.5, 'No sentiment data available',
                    ha='center', va='center', color='white', fontsize=14)

        ax.set_yticklabels([])
        ax.tick_params(axis='x', pad=12)
        ax.tick_params(axis='both', colors='white', labelsize=20)
        ax.spines[['top', 'right']].set_visible(False)
        ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.2, color='white')

        ax.set_title("Sentiment Scores and Score Frequency", color='white', pad=20, fontsize=40, fontweight='bold')
        # ax.set_xlabel('Sentiment Score', color='white', fontsize=14, labelpad=40)
        # ax.set_ylabel('Score Frequency', color='white', fontsize=14, labelpad=40)

        fig.tight_layout(pad=2)  
        fig.subplots_adjust(top=0.80) 
        return fig

    # saves the plots to static/plots folder to acess in the flask app
    def save_plot(self, fig, relative_path):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(base_dir, '..', relative_path)

        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        fig.savefig(full_path, bbox_inches='tight')
        print(f"Plot saved to {full_path}")
        plt.close(fig)
