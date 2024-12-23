# Desafio 1: Consolidação de arquivos CSV

# 1. Importando as bibliotecas necessárias
import pandas as pd  # Para manipulação de dados em tabelas

# 2. Carregando os arquivos CSV
# Lendo o arquivo de produtos
products_df = pd.read_csv('products.csv')
# Lendo o arquivo de pedidos
orders_df = pd.read_csv('orders.csv')

# 3. Realizando o Merge entre as tabelas
# Unimos os dados usando a coluna 'product_id' de orders e 'id' de products
merged_df = pd.merge(
    orders_df,         # DataFrame de pedidos
    products_df,       # DataFrame de produtos
    left_on='product_id',  # Coluna de referência em orders
    right_on='id'         # Coluna de referência em products
)

# 4. Calculando o preço total
# Criamos uma nova coluna chamada 'total_price'
merged_df['total_price'] = merged_df['quantity'] * merged_df['price']

# 5. Selecionando e renomeando as colunas necessárias
# Escolhemos apenas as colunas importantes para o arquivo final
final_df = merged_df[[
    'created_date',   # Data do pedido
    'id_x',           # ID do pedido (de orders)
    'name',           # Nome do produto (de products)
    'quantity',       # Quantidade do pedido
    'total_price'     # Preço total calculado
]]

# Renomeamos as colunas para o formato desejado
final_df.columns = [
    'order_created_date',
    'order_id',
    'product_name',
    'quantity',
    'total_price'
]

# 6. Salvando o resultado em um novo arquivo CSV
final_df.to_csv('order_full_information.csv', index=False)

print("Arquivo 'order_full_information.csv' criado com sucesso!")
