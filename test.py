
# import the modules
import pandas as pd 
from sqlalchemy import create_engine
  
# SQLAlchemy connectable
cnx = create_engine('sqlite:///database.db').connect()
  
# table named 'contacts' will be returned as a dataframe.
df = pd.read_sql_table('user', cnx)
print(df)