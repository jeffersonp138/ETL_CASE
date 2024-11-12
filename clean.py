import pandas as pd


df = pd.read_csv('steam_sales.csv', delimiter=';')

# Limpeza do campo "Nome"
df['Nome'] = df['Nome'].str.strip()  
df['Nome'] = df['Nome'].str.replace(r'[^\w\s]', '', regex=True)
df['Nome'] = df['Nome'].str.lower() 


df.to_csv('steam_sales_clean.csv', index=False)
