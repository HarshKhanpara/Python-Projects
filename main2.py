import requests
import matplotlib.pyplot as plt
from textblob import TextBlob

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_API_KEY = "36MR4SB4CXMQDEDH"
NEWS_API_KEY = "28bd74a6f5de402d9dc86b5f8f459ff5"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

def get_stock_data(start_date, end_date):
    stock_parameters = {
        "function": "TIME_SERIES_DAILY_ADJUSTED",
        "symbol": STOCK_NAME,
        "apikey": STOCK_API_KEY
    }
    response = requests.get(STOCK_ENDPOINT, params=stock_parameters)
    response.raise_for_status()
    data = response.json()["Time Series (Daily)"]
    dates = list(data.keys())
    dates.reverse()  # Reverse to get latest dates first
    closing_prices = [float(data[date]["4. close"]) for date in dates if start_date <= date <= end_date]
    return closing_prices

def plot_stock_prices(closing_prices):
    plt.plot(closing_prices)
    plt.title(f"Stock Prices for {COMPANY_NAME}")
    plt.xlabel("Days")
    plt.ylabel("Closing Price (USD)")
    plt.show()

def analyze_sentiment(news_data):
    sentiments = []
    for article in news_data:
        text = article["title"] + ". " + article["description"]
        blob = TextBlob(text)
        sentiment = blob.sentiment.polarity
        sentiments.append(sentiment)
    average_sentiment = sum(sentiments) / len(sentiments)
    return average_sentiment

def get_news():
    news_parameters = {
        "qInTitle": COMPANY_NAME,
        "apiKey": NEWS_API_KEY
    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_parameters)
    news_response.raise_for_status()
    news_data = news_response.json()["articles"]
    return news_data

def main():
    try:
        start_date = input("Enter start date (YYYY-MM-DD): ")
        end_date = input("Enter end date (YYYY-MM-DD): ")
        stock_prices = get_stock_data(start_date, end_date)
        plot_stock_prices(stock_prices)
        
        if len(stock_prices) >= 2:
            yesterday_price = stock_prices[0]
            day_before_yesterday_price = stock_prices[1]
            difference_percentage = abs(yesterday_price - day_before_yesterday_price) / yesterday_price * 100
            
            if difference_percentage > 1:
                news_data = get_news()
                average_sentiment = analyze_sentiment(news_data)
                print("Average Sentiment for News:", average_sentiment)
                for article in news_data[:3]:
                    print("Headline:", article["title"])
                    print("Description:", article["description"])
                    print()
            else:
                print("No significant change in stock price.")
        else:
            print("Insufficient data to analyze.")
            
    except Exception as e:
        print("An error occurred:", str(e))

if __name__ == "__main__":
    main()


