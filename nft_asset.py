# Disclaimer: In order to be direct and honest and set the expectations level: 
# this Python file should by no means be taken as something to be used in real production. 
# What happened here is that I tried to 'simulate' how the non-fungible token (NFT) would be created 
# by trying to follow examples given on the Algorand ASA page. 
# With that being said, the logic I followed is as follows: 
# Create a supply of 1000 NFTs that takes the real prices from the Alpha Vantage API. 
# The NFTs are to be transferred using the package reached by Nash equilibrium, 
# and the rest of the supply will be burnt. 
# I highly encourage the visitors of this code to keep an eye on this repo 
# as the code will be changed as I get better, 
# and wherever there is a hypothetical key or something, put the text "if I understood correctly a key (or whatever depending on the context) should be put here."
# to get a clear idea on how it should work if everything goes according to the plan please visit the simulator:https://multi-asset-payment-system-ivvutnb3i243ds3n9kzf5c.streamlit.app/simulator
from algosdk.v2client import algod
from algosdk import account, mnemonic, transaction
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

# Hypothetical account credentials 
acct1_address = "if I understood correctly an address should be put here"
acct1_private_key = "if I understood correctly a key should be put here"

# Initialize an Algorand client
algod_token = "if I understood correctly a token should be put here"
algod_address = "http://localhost:4001"
algod_client = algod.AlgodClient(algod_token, algod_address)

def create_asset(asset_name, unit_name, total_units):
    sp = algod_client.suggested_params()
    txn = transaction.AssetConfigTxn(
        sender=acct1_address,
        sp=sp,
        default_frozen=False,
        unit_name=unit_name,
        asset_name=asset_name,
        manager=acct1_address,
        reserve=acct1_address,
        freeze=acct1_address,
        clawback=acct1_address,
        total=total_units,
        decimals=0,
    )
    stxn = txn.sign(acct1_private_key)
    txid = algod_client.send_transaction(stxn)
    print(f"Sent asset create transaction with txid: {txid}")
    results = transaction.wait_for_confirmation(algod_client, txid, 4)
    print(f"Result confirmed in round: {results['confirmed-round']}")
    created_asset = results["asset-index"]
    print(f"Asset ID created: {created_asset}")
    return created_asset

def create_nfts_for_assets():
    assets = Assets()
    created_assets = {}

    created_assets["goldman_sachs"] = create_asset(
        "Goldman Sachs", "GS", 1000
    )
    created_assets["american_express"] = create_asset(
        "American Express", "AXP", 1000
    )
    created_assets["chevron"] = create_asset(
        "Chevron", "CVX", 1000
    )
    created_assets["eur_usd"] = create_asset(
        "EUR/USD", "EURUSD", 1000
    )
    
    return created_assets

def transfer_asset(asset_id, sender, receiver, sender_private_key, amount):
    params = algod_client.suggested_params()
    txn = transaction.AssetTransferTxn(
        sender=sender,
        sp=params,
        receiver=receiver,
        amt=amount,
        index=asset_id
    )
    stxn = txn.sign(sender_private_key)
    txid = algod_client.send_transaction(stxn)
    print(f"Sent asset transfer transaction with txid: {txid}")
    results = transaction.wait_for_confirmation(algod_client, txid, 4)
    print(f"Transfer confirmed in round: {results['confirmed-round']}")

def burn_unused_supply(asset_id, manager, reserve, manager_private_key):
    params = algod_client.suggested_params()
    txn = transaction.AssetConfigTxn(
        sender=manager,
        sp=params,
        index=asset_id,
        strict_empty_address_check=False,
        reserve=reserve,
        total=0
    )
    stxn = txn.sign(manager_private_key)
    txid = algod_client.send_transaction(stxn)
    print(f"Sent asset burn transaction with txid: {txid}")
    results = transaction.wait_for_confirmation(algod_client, txid, 4)
    print(f"Burn confirmed in round: {results['confirmed-round']}")

if __name__ == "__main__":
    created_assets = create_nfts_for_assets()
