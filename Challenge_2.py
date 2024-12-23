import pandas as pd
import requests
import json

products = pd.read_csv('data/products.csv')
orders = pd.read_csv('data/orders.csv')

merged_df = pd.merge(
    orders,
    products,
    left_on='product_id',
    right_on='id',
    suffixes=('_order', '_product')
)

merged_df['total_price_br'] = merged_df['quantity'] * merged_df['price']

try:
    with open('config.json') as config_file:
        config = json.load(config_file)
        API_KEY = config.get('api_key')
except FileNotFoundError:
    print("Error: config.json not found.")
    API_KEY = None

if API_KEY:
    try:
        response = requests.get(f'https://api.freecurrencyapi.com/v1/latest?apikey={API_KEY}&currencies=USD')
        if response.status_code == 200:
            exchange_rate = response.json()['data']['USD']
        else:
            print("Error: Failed to fetch exchange rate.")
            exchange_rate = 1  
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        exchange_rate = 1 
else:
    exchange_rate = 1  

merged_df['total_price_us'] = merged_df['total_price_br'] / exchange_rate

final_df = merged_df[[
    'created_date',
    'id_order',
    'name',
    'quantity',
    'total_price_br',
    'total_price_us'
]].rename(columns={
    'created_date': 'order_created_date',
    'id_order': 'order_id',
    'name': 'product_name'
})

final_df.to_csv('results/fixed_order_full_information.csv', index=False)
print("✅ File 'fixed_order_full_information.csv' saved successfully!")

max_orders_date = orders['created_date'].value_counts().idxmax()

product_demand = merged_df.groupby('product_id').agg({
    'quantity': 'sum',
    'total_price_br': 'sum'
}).reset_index()

most_demanded_product_id = product_demand.sort_values('quantity', ascending=False).iloc[0]['product_id']
most_demanded_product_name = products.loc[products['id'] == most_demanded_product_id, 'name'].iloc[0]
most_demanded_product_total_sell = product_demand.sort_values('quantity', ascending=False).iloc[0]['total_price_br']

top_categories = merged_df.groupby('category')['quantity'].sum().sort_values(ascending=False).head(3)

kpi_data = {
    'metric': ['max_orders_date', 'most_demanded_product', 'most_demanded_product_total_sell', 'top_3_categories'],
    'value': [
        max_orders_date,
        most_demanded_product_name,
        most_demanded_product_total_sell,
        ', '.join(top_categories.index)
    ]
}

kpi_df = pd.DataFrame(kpi_data)
kpi_df.to_csv('results/kpi_product_orders.csv', index=False)
print("File 'kpi_product_orders.csv' saved successfully!")
