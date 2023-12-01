import pandas as pd

df = pd.read_csv('input.csv')

df['ID'] = 'gid://shopify/Product/' + df['ID'].astype(str)
df['Display Name'] = df['Title'].str.split(' - ').str.get(0)

grouped = df.groupby('Display Name')['ID'].apply(lambda x: '["' + '","'.join(x) + '"]').reset_index()
grouped['Handle'] = grouped['Display Name'].str.lower().str.replace(' ', '-')
grouped['Command'] = 'MERGE'
grouped['Status'] = 'Active'
grouped['Definition: Handle'] = 'coupled_product'
grouped['Definition: Name'] = 'Coupled Product'

# Duplicate each row and keep other values the same
grouped = grouped.loc[grouped.index.repeat(2)].reset_index(drop=True)

# Assign different values to the 'Field' column for even and odd rows
grouped.loc[grouped.index % 2 == 0, 'Field'] = 'title'
grouped.loc[grouped.index % 2 != 0, 'Field'] = 'products'
grouped.loc[grouped.index % 2 == 0, 'Value'] = grouped['Display Name']
grouped.loc[grouped.index % 2 != 0, 'Value'] = grouped['ID']

grouped.to_csv('output.csv', index=False)