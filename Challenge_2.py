import pandas as pd
import json
import freecurrencyapi

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

    merged_df['total_price_us'] = (merged_df['total_price_br'] / exchange_rate).round(2)
    
else:
    print("Error: Invalid exchange rate.")


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
print("File 'fixed_order_full_information.csv' saved successfully!")

max_orders_date = orders['created_date'].value_counts().idxmax()

product_demand = merged_df.groupby('product_id').agg({
    'quantity': 'sum',
    'total_price_us': 'sum'
}).reset_index()

most_demanded_product_id = product_demand.sort_values('quantity', ascending=False).iloc[0]['product_id']
most_demanded_product_name = products.loc[products['id'] == most_demanded_product_id, 'name'].iloc[0]
most_demanded_product_total_sell = product_demand.sort_values('quantity', ascending=False).iloc[0]['total_price_us']

top_categories = merged_df.groupby('category')['quantity'].sum().sort_values(ascending=False).head(3)

kpi_data = {
    'metric': [
        'max_orders_date',
        'most_demanded_product',
        'most_demanded_product_total_sell',
        'top_3_categories'
    ],
    'value': [
        max_orders_date,
        most_demanded_product_name,
        f"${most_demanded_product_total_sell:.2f} USD", 
        ', '.join([f"{i+1}. {category}" for i, category in enumerate(top_categories.index)]) 
        if 'top_categories' in locals() else 'N/A'
    ]
}

kpi_df = pd.DataFrame(kpi_data)

kpi_df.to_csv('results/kpi_product_orders.csv', index=False)

print("Results saved in 'kpi_product_orders.csv'")
