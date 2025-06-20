import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg') 
import seaborn as sns
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import os

class SentimentPlotter:
    def __init__(self):
        plt.style.use('seaborn-v0_8-darkgrid')
        self.figsize = (12, 8)
    
    def plot_stock_price(self, stock_data, title="Stock Price Chart"):
        if stock_data is None or stock_data.empty or 'Close' not in stock_data.columns:
            fig, ax = plt.subplots(figsize=self.figsize)
            ax.text(0.5, 0.5, 'No stock data available',
                    horizontalalignment='center', verticalalignment='center', color='white')
            ax.set_facecolor("#121212")
            fig.patch.set_facecolor("#121212")
            return fig

        fig, ax = plt.subplots(figsize=self.figsize)
        
        # Clean dark theme
        ax.set_facecolor("#121212")
        fig.patch.set_facecolor("#121212")
        ax.plot(stock_data.index, stock_data["Close"], color="#00ffae", linewidth=2)

        # Remove spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        # Customize grid
        ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.2, color='white')

        # Remove y-axis ticks & lighten x-axis
        ax.tick_params(axis='y', colors='white')
        ax.tick_params(axis='x', colors='white')

        # Optional: remove axis labels or title for cleaner look
        ax.set_title("", color='white')
        ax.set_xlabel("")
        ax.set_ylabel("")

        return fig


    
    # def plot_sentiment_trend(self, sentiment_data, stock_data=None, title="Sentiment Analysis"):
    #     """Plot sentiment trend with optional stock price overlay"""
    #     if sentiment_data.empty:
    #         # Create an empty plot if no data
    #         fig, ax = plt.subplots(figsize=self.figsize)
    #         ax.text(0.5, 0.5, 'No sentiment data available', 
    #                horizontalalignment='center', verticalalignment='center')
    #         plt.title(title)
    #         return fig
            
    #     fig, ax1 = plt.subplots(figsize=self.figsize)
        
    #     # Plot sentiment
    #     color = 'tab:blue'
    #     ax1.set_xlabel('Date')
    #     ax1.set_ylabel('Sentiment Score', color=color)
    #     ax1.plot(sentiment_data.index, sentiment_data.values, color=color, label='Sentiment')
    #     ax1.tick_params(axis='y', labelcolor=color)
        
    #     # Add stock price if provided
    #     if stock_data is not None and not stock_data.empty:
    #         ax2 = ax1.twinx()
    #         color = 'tab:red'
    #         ax2.set_ylabel('Stock Price', color=color)
    #         ax2.plot(stock_data.index, stock_data['Close'], color=color, label='Stock Price')
    #         ax2.tick_params(axis='y', labelcolor=color)
        
    #     plt.title(title)
    #     fig.tight_layout()
    #     return fig
    
    def plot_sentiment_distribution(self, sentiment_scores, title="Sentiment Distribution"):
        """Plot distribution of sentiment scores"""
        plt.figure(figsize=self.figsize)
        if len(sentiment_scores) > 0:
            sns.histplot(sentiment_scores, kde=True)
        else:
            plt.text(0.5, 0.5, 'No sentiment data available',
                    horizontalalignment='center', verticalalignment='center')
        plt.title(title)
        plt.xlabel('Sentiment Score')
        plt.ylabel('Frequency')
        return plt.gcf()
    
    # def plot_quality_scores(self, posts_df, title="Post Quality Distribution"):
    #     """Plot distribution of post quality scores"""
    #     plt.figure(figsize=self.figsize)
    #     if 'quality_score' in posts_df.columns and len(posts_df) > 0:
    #         sns.histplot(posts_df['quality_score'], kde=True)
    #     else:
    #         plt.text(0.5, 0.5, 'No quality score data available',
    #                 horizontalalignment='center', verticalalignment='center')
    #     plt.title(title)
    #     plt.xlabel('Quality Score')
    #     plt.ylabel('Frequency')
    #     return plt.gcf()
    
    def save_plot(self, fig, filename):
        """Save plot to file"""
        try:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            fig.savefig(filename)
        except Exception as e:
            print(f"Error saving plot: {str(e)}")
        finally:
            plt.close(fig) 