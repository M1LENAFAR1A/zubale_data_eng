import pandas as pd
import freecurrencyapi
import requests
import json

base = pd.read_csv('results/order_full_information.csv')
base = base.rename(columns={"total_price": "total_price_br"})

try:
    with open('config.json') as config_file:
        config = json.load(config_file)
        API_KEY = config.get('api_key')
except FileNotFoundError:
    print("Error: config.json not found.")
    API_KEY = None

if API_KEY:
    try:
        client = freecurrencyapi.Client(API_KEY)

        result = client.latest(currencies=['BRL', 'USD'])
        print("Currency Data:", result)
 
        exchange_rate = result['data']['BRL']
        print(f"Exchange Rate (BRL -> USD): {exchange_rate}")
    
    except Exception as e:  
        print(f"API Error: {e}")
        exchange_rate = 1  
else:
    print("Error: API_KEY not available. Please check your config.json.")
    exchange_rate = 1 

if exchange_rate and isinstance(exchange_rate, (int, float)):

    base['total_price_us'] = base['total_price_br'] / exchange_rate
    print(base.head())
else:
    print("Error: Invalid exchange rate.")

# Salvar os resultados
base.to_csv('results/fixed_order_full_information.csv', index=False)
