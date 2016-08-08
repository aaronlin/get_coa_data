import pandas as pd
import json
import sqlalchemy


with open('aggregated_price_data.txt') as f:
    data = [json.loads(x) for x in f]
    df = pd.DataFrame(data)
    df.columns = ['upper_price', 'lower_price', 'middle_price', 'date',
                  'amount', 'id', 'name', 'market_id', 'market_name',
                  'mean_price']

engine = sqlalchemy.create_engine('sqlite:///price.db')
df.to_sql('Price', con=engine)
