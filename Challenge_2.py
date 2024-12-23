import pandas as pd
import requests
import json

# =========================
# PARTE 1: Conversão de Moeda
# =========================

# 1. Carregar os dados dos arquivos CSV
products = pd.read_csv('data/products.csv')
orders = pd.read_csv('data/orders.csv')

# 2. Mesclar os dados
merged_df = pd.merge(
    orders,
    products,
    left_on='product_id',
    right_on='id',
    suffixes=('_order', '_product')
)

# 3. Calcular o preço total em BRL
merged_df['total_price_br'] = merged_df['quantity'] * merged_df['price']

# 4. Obter API Key do arquivo config.json
with open('config.json') as config_file:
    config = json.load(config_file)
    API_KEY = config.get('api_key')

# 5. Obter taxa de câmbio da API
response = requests.get(f'https://api.freecurrencyapi.com/v1/latest?apikey={API_KEY}&currencies=USD')
exchange_rate = response.json()['data']['USD']

# 6. Calcular o preço total em USD
merged_df['total_price_us'] = merged_df['total_price_br'] / exchange_rate

# 7. Selecionar colunas específicas
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

# 8. Salvar o resultado
final_df.to_csv('results/fixed_order_full_information.csv', index=False)
print("✅ Arquivo 'fixed_order_full_information.csv' salvo com sucesso!")

# =========================
# PARTE 2: Análise de Dados
# =========================

# 9. Data com o maior número de pedidos
max_orders_date = orders['created_date'].value_counts().idxmax()

# 10. Produto mais demandado e receita total
product_demand = merged_df.groupby('product_id').agg({
    'quantity': 'sum',
    'total_price_br': 'sum'
}).reset_index()

most_demanded_product_id = product_demand.sort_values('quantity', ascending=False).iloc[0]['product_id']
most_demanded_product_name = products.loc[products['id'] == most_demanded_product_id, 'name'].iloc[0]
most_demanded_product_total_sell = product_demand.sort_values('quantity', ascending=False).iloc[0]['total_price_br']

# 11. Top 3 categorias mais demandadas
top_categories = merged_df.groupby('category')['quantity'].sum().sort_values(ascending=False).head(3)

# 12. Salvar KPI em um arquivo CSV
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

print("✅ Arquivo 'kpi_product_orders.csv' salvo com sucesso!")
