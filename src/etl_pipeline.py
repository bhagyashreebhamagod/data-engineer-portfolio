import pandas as pd
import sqlite3
import os

print("🚀 ETL + DATABASE PIPELINE STARTED")

# =========================
# LOAD DATA
# =========================
df = pd.read_csv("data/telecom_billing.csv")

print("\n📊 RAW DATA")
print(df)

# =========================
# CLEAN DATA
# =========================
df = df.dropna()

# =========================
# TRANSFORM DATA
# =========================
df["total_usage"] = (
    df["data_usage_gb"] +
    df["calls_minutes"] / 60 +
    df["sms_count"] / 10
)

df["bill_category"] = df["bill_amount"].apply(
    lambda x: "High" if x >= 1200 else "Medium" if x >= 700 else "Low"
)

print("\n📊 TRANSFORMED DATA")
print(df)

# =========================
# LOAD INTO SQLITE DATABASE
# =========================

# create folder if not exists
os.makedirs("database", exist_ok=True)

db_path = "database/billing.db"

conn = sqlite3.connect(db_path)

# write data into table
df.to_sql("billing_data", conn, if_exists="replace", index=False)

print("\n✅ DATA LOADED INTO DATABASE SUCCESSFULLY")

# =========================
# RUN SQL QUERIES
# =========================

cursor = conn.cursor()

print("\n💰 TOTAL REVENUE:")
cursor.execute("SELECT SUM(bill_amount) FROM billing_data")
print(cursor.fetchone()[0])

print("\n📈 AVERAGE BILL:")
cursor.execute("SELECT AVG(bill_amount) FROM billing_data")
print(cursor.fetchone()[0])

print("\n🏆 HIGH VALUE CUSTOMERS:")
cursor.execute("""
SELECT name, bill_amount 
FROM billing_data 
WHERE bill_category = 'High'
""")

for row in cursor.fetchall():
    print(row)

conn.close()

print("\n🎯 PIPELINE COMPLETED SUCCESSFULLY")
print("📁 DATABASE CREATED: database/billing.db")