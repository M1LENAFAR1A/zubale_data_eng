import pandas as pd

products = pd.read_csv('data/products.csv')
orders = pd.read_csv('data/orders.csv')

merge_df = pd.merge(products, orders,left_on='id', right_on='product_id', suffixes=('_product', '_order'))

merge_df['total_price'] = merge_df['price'] * merge_df['quantity']

final_df = merge_df[[
    'created_date',
    'id_order',
    'name',
    'quantity',
    'total_price'
]].rename(columns={
    'created_date': 'order_created_date',
    'id_order': 'order_id',
    'name': 'product_name'
})

final_df.to_csv('results/order_full_information.csv', index=False)

print("File 'order_full_information.csv' created successfully!")