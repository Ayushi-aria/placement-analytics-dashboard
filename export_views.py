import os
import pandas as pd
from sqlalchemy import create_engine

# yahan wahi credentials daalo jo load_to_mysql.py mein use kiye the
engine = create_engine("mysql+pymysql://USER:PASSWORD@localhost:3306/placement_db")

os.makedirs("dashboard_data", exist_ok=True)

for view in ["v_branch_placement", "v_funnel", "v_company_performance", "v_offer_details"]:
    df = pd.read_sql(f"SELECT * FROM {view}", engine)
    df.to_csv(f"dashboard_data/{view}.csv", index=False)
    print(f"{view}: {len(df)} rows exported")