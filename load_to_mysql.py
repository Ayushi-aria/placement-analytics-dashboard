import pandas as pd
from sqlalchemy import create_engine

# apna MySQL password yahan daalo
engine = create_engine("mysql+pymysql://USER:PASSWORD@localhost:3306/placement_db")

folder = "placement_data/"

# order important hai (foreign keys ki wajah se)
for table in ["students", "companies", "applications", "offers"]:
    df = pd.read_csv(folder + f"{table}_clean.csv")
    df.to_sql(table, engine, if_exists="append", index=False)
    print(f"{table}: {len(df)} rows loaded")