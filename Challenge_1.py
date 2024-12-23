import pandas as pd 

products_df = pd.read_csv('data/products.csv')
orders_df = pd.read_csv('data/orders.csv')

merged_df = pd.merge(
    orders_df,         
    products_df,      
    left_on='product_id',  
    right_on='id'         
)

merged_df['total_price'] = merged_df['quantity'] * merged_df['price']

final_df = merged_df[[
    'created_date',   
    'id_x',           
    'name',           
    'quantity',       
    'total_price'     
]]

final_df.columns = [
    'order_created_date',
    'order_id',
    'product_name',
    'quantity',
    'total_price'
]

final_df.to_csv('results/order_full_information.csv', index=False)

print("File 'order_full_information.csv' created successfully!")

