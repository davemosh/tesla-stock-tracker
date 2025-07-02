import requests
import smtplib

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
#stockapikey
API_KEY = "C4OE9RU7YWAYVNEC"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API = "75c917e7c9c74e4a93cc5e893e9b6431"

my_email = "davidmoshe110@gmail.com"
my_password = "D@vidM0She@_27"

    ## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

stock_parameter = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": API_KEY,
}

news_parameters ={ 
    "apiKey": NEWS_API,
    "q": COMPANY_NAME,
    "language": "en",
    "sources": "bloomberg"
}

#fetching STOCK API for tesla and its daily price, it may change since it is real-time tracker
response = requests.get(STOCK_ENDPOINT, params=stock_parameter)
s_data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in s_data.items()]
yesterday_data = data_list[0]
yes_clo_pri = yesterday_data["4. close"]
print(yes_clo_pri)

day_b4_yesterday_data = data_list[1]
day_b4_yesterday_closing_price = day_b4_yesterday_data["4. close"]
print(day_b4_yesterday_closing_price)

# Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp
difference = abs(float(yes_clo_pri) - float(day_b4_yesterday_closing_price))
print(difference)

# Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
percentage_diff = (difference / float(yes_clo_pri)) * 100
print(f"The percentage difference: {percentage_diff}%")

# If TODO4 percentage is greater than 5 then print("Get News").
if percentage_diff > 5:
    ## STEP 2: https://newsapi.org/ 
    news_response = requests.get(NEWS_ENDPOINT, params=news_parameters)
    # Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.
    n_articles = news_response.json()["articles"]
    print(n_articles)

# Use Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation
t_articles = n_articles[:3]
print(t_articles)

    ## STEP 3: Use smtp email with python 
    #to send a separate emails with each article's title and description to your email. 

# Create a new list of the first 3 article's headline and description using list comprehension.
formated_articles = [f"Headlines: {article['title']}. \n Brief: {article['description']}" for article in t_articles]
# Send each article as a separate message via Twilio. 
with smtplib.SMTP("smtp.gmail.com") as connection:
    connection.starttls()
    connection.login(user=my_email, password=my_password)
    connection.sendmail(
        from_address = my_email, to_address="moshedavid27@yahoo.com",
        msg=formated_articles
        )


#Optional TODO: Format the message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

