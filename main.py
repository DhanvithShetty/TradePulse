from Browser import BrowserInitialization
from MarketValues import GetRSI, MMI
from Message import SendTelegramMessage
from datetime import datetime
import os
import json
from dotenv import load_dotenv

# Utility Functions
def LoadEnvironmentVariables():
    load_dotenv("credentials.env")
    Bot_Token = os.getenv("TELEGRAM_BOT_TOKEN")
    Chat_ID = os.getenv("TELEGRAM_CHAT_ID")

    if not Bot_Token or not Chat_ID:
        raise ValueError("Missing Telegram credentials!")

    return Bot_Token, Chat_ID

def LoadTickerSymbols():
    try:
        with open('tickers.json', 'r') as f:
            data = json.load(f)
            return data.get('tickers', [])
    except Exception as e:
        print(f"Error reading tickers file: {e}")
        return []

def ComposeMessage(driver, current_date, MMIZone, MMIValue, tickers):
    message = (f"Hey there,\n\n"
               f"Here is market data for {current_date}:\n\n"
               f"Market Mood Index Value is {MMIValue}.\n"
               f"The market is in {MMIZone}\n\n")

    buy_opportunities = []

    for ticker in tickers:
        RSIIndicatorValue = GetRSI(driver, ticker)
        if RSIIndicatorValue is not None and RSIIndicatorValue <= 37.5:
            buy_opportunities.append(f"{ticker} --> RSI Value: {RSIIndicatorValue}")

    if buy_opportunities:
        message += "Buy Opportunities:\n\n" + "\n".join(buy_opportunities)
    else:
        message += "No Buy Opportunities today. Sorry :)"

    return message

def main():
    try:
        # Load environment variables
        Bot_Token, Chat_ID = LoadEnvironmentVariables()

        # Load tickers from the JSON file
        tickers = LoadTickerSymbols()

        # Initialize the browser driver
        driver = BrowserInitialization()

        try:
            MMIZone, MMIValue = MMI(driver)

            CurrentDate = datetime.now().strftime("%B %d, %Y")

            # Composing the message with market data and buying opportunities based on RSI
            ComposedMessage = ComposeMessage(driver, CurrentDate, MMIZone, MMIValue, tickers)

            SendTelegramMessage(Bot_Token, Chat_ID, ComposedMessage)
        finally:
            driver.quit()

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
