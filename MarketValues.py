from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def GetRSI(driver, ticker):
    try:
        # Navigate to TradingView Technicals page
        driver.get(f"https://www.tradingview.com/symbols/NSE-{ticker}/technicals/")

        # Waiting until the RSI value element is present
        rsi_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Relative Strength Index')]/ancestor::td/following-sibling::td[1]"))
        )
        return float(rsi_element.text)
    except Exception as e:
        print(f"Error retrieving RSI for {ticker}: {e}")
        return None

def MMI(driver):
    try:
        # Navigate to Tickertape Market Mood Index page
        driver.get("https://www.tickertape.in/market-mood-index")

        # Extract MMI zone and value
        MMIZone = driver.find_element(By.XPATH, "//p[contains(text(), 'MMI is in')]//span").text
        MMIValue = driver.find_element(By.XPATH, "//div[contains(@class, 'mmi-value')]//span[contains(@class, 'number')]").text
        return MMIZone, MMIValue
    except Exception as e:
        print(f"Error retrieving MMI: {e}")
        return "Unknown", "N/A"
