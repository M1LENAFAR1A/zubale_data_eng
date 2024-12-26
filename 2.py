import pandas as pd
import freecurrencyapi
import requests
import json

base = pd.read_csv('results/order_full_information.csv')
base.rename(columns={"total_price": "total_price_br"})
print(base.head())
# try:
#     with open('config.json') as config_file:
#         config = json.load(config_file)
#         API_KEY = config.get('api_key')
# except FileNotFoundError:
#     print("Error: config.json not found.")
#     API_KEY = None

# if API_KEY:
#     try:
#         client = freecurrencyapi.Client(API_KEY)
        
#         # Fazer a solicitação para obter as moedas BRL e CAD
#         result = client.currencies(currencies=['BRL', 'CAD'])
#         print("Currency Data:", result)
    
#     except freecurrencyapi.exceptions.FreecurrencyAPIException as e:
#         print(f"API Error: {e}")
#         exchange_rate = 1  
#     except Exception as e:
#         print(f"Unexpected Error: {e}")
#         exchange_rate = 1  
# else:
#     print("Error: API_KEY not available. Please check your config.json.")
#     exchange_rate = 1 

# base['total_price_us'] = base['total_price_br'] / exchange_rate

# base.to_csv('results/fixed_order_full_information22.csv', index=False)




