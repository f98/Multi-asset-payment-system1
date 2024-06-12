import requests

API_KEY = 'ZCO7J6HNOW5SGNAY'

class Assets:
    def __init__(self):
        self.exchange_rate = self.get_exchange_rate('EUR', 'USD')
        self.goldman_sachs_price = self.get_stock_price('GS')
        self.american_express_price = self.get_stock_price('AXP')
        self.chevron_price = self.get_stock_price('CVX')

    def get_exchange_rate(self, from_currency, to_currency):
        try:
            url = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={from_currency}&to_currency={to_currency}&apikey={API_KEY}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            exchange_rate = data['Realtime Currency Exchange Rate']['5. Exchange Rate']
            return float(exchange_rate)
        except (requests.RequestException, KeyError) as e:
            print(f"Error fetching exchange rate: {e}")
            return None

    def get_stock_price(self, symbol):
        try:
            url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=1min&apikey={API_KEY}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            last_refreshed = data['Meta Data']['3. Last Refreshed']
            stock_price = data['Time Series (1min)'][last_refreshed]['4. close']
            return float(stock_price)
        except (requests.RequestException, KeyError) as e:
            print(f"Error fetching stock price for {symbol}: {e}")
            return None

    def print_current_prices(self):
        print(f"Exchange rate from EUR to USD: {self.exchange_rate}")
        print(f"Goldman Sachs current price: {self.goldman_sachs_price}")
        print(f"American Express current price: {self.american_express_price}")
        print(f"Chevron current price: {self.chevron_price}")

    def simulate_price_change(self, percentage_increase=0.001):
        self.exchange_rate *= (1 + percentage_increase)
        self.goldman_sachs_price *= (1 + percentage_increase)
        self.american_express_price *= (1 + percentage_increase)
        self.chevron_price *= (1 + percentage_increase)

if __name__ == "__main__":
    assets = Assets()
    assets.print_current_prices()
