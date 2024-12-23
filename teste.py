import pandas as pd
import requests

# ✅ Parte 1: Conversão de Moeda

# 1. Carregar o arquivo consolidado
try:
    df = pd.read_csv('order_full_information.csv')
    print("✅ Arquivo 'order_full_information.csv' carregado com sucesso!")
except FileNotFoundError:
    print("❌ Erro: Arquivo 'order_full_information.csv' não encontrado.")
    exit()
except Exception as e:
    print(f"❌ Erro ao carregar arquivo: {e}")
    exit()

# 2. Obter a taxa de câmbio BRL -> USD
API_KEY = 'fca_live_774wB3jww9G4qUNjculDYDbf8CCR77onRNI2mmCQ'  # Substitua pela sua chave válida
API_URL = f'https://api.freecurrencyapi.com/v1/latest?apikey={API_KEY}&currencies=USD&base_currency=BRL'

try:
    response = requests.get(API_URL)
    response.raise_for_status()
    data = response.json()
    
    if 'data' in data and 'USD' in data['data']:
        exchange_rate = float(data['data']['USD'])
        print(f"✅ Taxa de câmbio BRL → USD: {exchange_rate}")
    else:
        print("❌ Erro: A resposta da API não contém a taxa de câmbio esperada.")
        exit()
except requests.exceptions.HTTPError as http_err:
    print(f"❌ Erro HTTP: {http_err}")
    exit()
except requests.exceptions.RequestException as err:
    print(f"❌ Erro ao conectar com a API: {err}")
    exit()

# 3. Adicionar colunas para total_price_br e total_price_us
try:
    df['total_price_br'] = df['total_price']
    df['total_price_us'] = df['total_price'] * exchange_rate
    print("✅ Colunas 'total_price_br' e 'total_price_us' adicionadas com sucesso!")
except KeyError:
    print("❌ Erro: Coluna 'total_price' não encontrada no arquivo.")
    exit()
except Exception as e:
    print(f"❌ Erro ao adicionar colunas: {e}")
    exit()

# 4. Salvar os resultados em um novo arquivo
try:
    df.to_csv('fixed_order_full_information.csv', index=False)
    print("✅ Arquivo 'fixed_order_full_information.csv' criado com sucesso!")
except Exception as e:
    print(f"❌ Erro ao salvar arquivo: {e}")
    exit()

# ✅ Parte 2: Cálculo de KPIs

# 1. Data com maior número de pedidos
try:
    max_orders_date = df['order_created_date'].value_counts().idxmax()
except KeyError:
    print("❌ Erro: Coluna 'order_created_date' não encontrada.")
    max_orders_date = 'N/A'

# 2. Produto mais demandado e total vendido
try:
    most_demanded_product = df.groupby('product_name')['quantity'].sum().idxmax()
    most_demanded_product_total = df.groupby('product_name')['total_price_br'].sum().loc[most_demanded_product]
except KeyError:
    print("❌ Erro: Coluna 'product_name' ou 'quantity' não encontrada.")
    most_demanded_product = 'N/A'
    most_demanded_product_total = 0.0

# 3. Top 3 categorias mais demandadas
try:
    if 'category' in df.columns:
        top_categories = df.groupby('category')['quantity'].sum().nlargest(3)
        top_categories_list = ', '.join(top_categories.index)
    else:
        top_categories_list = 'Categoria não disponível'
except Exception as e:
    print(f"❌ Erro ao calcular categorias: {e}")
    top_categories_list = 'Erro ao calcular categorias'

# 4. Salvar KPIs em um arquivo CSV
kpi_data = {
    'kpi_name': [
        'Max Orders Date', 
        'Most Demanded Product', 
        'Most Demanded Product Total Sales (BRL)', 
        'Top 3 Categories'
    ],
    'kpi_value': [
        max_orders_date, 
        most_demanded_product, 
        most_demanded_product_total, 
        top_categories_list
    ]
}

try:
    kpi_df = pd.DataFrame(kpi_data)
    kpi_df.to_csv('kpi_product_orders.csv', index=False)
    print("✅ Arquivo 'kpi_product_orders.csv' criado com sucesso!")
except Exception as e:
    print(f"❌ Erro ao salvar KPIs: {e}")
    exit()
