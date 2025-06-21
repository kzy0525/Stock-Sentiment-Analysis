import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for Flask
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os

class SentimentPlotter:
    def __init__(self):
        plt.style.use('seaborn-v0_8-darkgrid')
        self.figsize = (12, 8)

    def plot_stock_price(self, stock_data, title="Stock Price Chart"):
        fig, ax = plt.subplots(figsize=self.figsize)

        if stock_data is None or stock_data.empty or 'Close' not in stock_data.columns:
            ax.text(0.5, 0.5, 'No stock data available',
                    ha='center', va='center', color='white', fontsize=14)
        else:
            ax.plot(stock_data.index, stock_data["Close"], color="#498659", linewidth=4)
            ax.fill_between(stock_data.index, stock_data["Close"], 
                        color="#498659", alpha=0.1, zorder=1)
            
            mean_price = stock_data["Close"].mean()
            price_range = stock_data["Close"].max() - stock_data["Close"].min()
            padding = price_range * 0.6
            ax.set_ylim(mean_price - padding, mean_price + padding)


        # Styling
        ax.set_facecolor("#1F1F1F")
        fig.patch.set_facecolor("#1F1F1F")
        ax.tick_params(axis='both', colors='white', labelsize=5)
        ax.spines[['top', 'right']].set_visible(False)
        ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.2, color='white')
        ax.set_title("", color='white')

        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.set_title("")
        ax.set_xlabel("")
        ax.set_ylabel("")

        return fig

    def plot_sentiment_distribution(self, sentiment_scores, title="Sentiment Distribution"):
        fig, ax = plt.subplots(figsize=self.figsize)

        ax.set_facecolor("#1F1F1F")
        fig.patch.set_facecolor("#1F1F1F")

        if sentiment_scores:
            sns.histplot(sentiment_scores, kde=True, ax=ax, color="#7abaff")
        else:
            ax.text(0.5, 0.5, 'No sentiment data available',
                    ha='center', va='center', color='white', fontsize=14)

        ax.set_title(title, color='white')
        ax.set_xlabel('Sentiment Score', color='white')
        ax.set_ylabel('Frequency', color='white')
        ax.tick_params(axis='both', colors='white')

        return fig

    def save_plot(self, fig, relative_path):
        # Save plots relative to the src/ directory where this file lives
        base_dir = os.path.dirname(os.path.abspath(__file__))  # points to src/
        full_path = os.path.join(base_dir, '..', relative_path)

        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        fig.savefig(full_path, bbox_inches='tight')
        print(f"✅ Plot saved to {full_path}")
        plt.close(fig)
