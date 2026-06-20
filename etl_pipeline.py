import pandas as pd

# =========================
# EXTRACT
# =========================
df = pd.read_csv("telecom_billing.csv")

print("\nRAW DATA:")
print(df)

# =========================
# TRANSFORM
# =========================

# Check missing values
df = df.dropna()

# Create new column: total usage score
df["total_usage"] = df["data_usage_gb"] + df["calls_minutes"]/60 + df["sms_count"]/10

# Create bill category
def categorize_bill(amount):
    if amount >= 1200:
        return "High"
    elif amount >= 700:
        return "Medium"
    else:
        return "Low"

df["bill_category"] = df["bill_amount"].apply(categorize_bill)

# =========================
# LOAD (OUTPUT)
# =========================

print("\nCLEANED DATA:")
print(df)

# Save cleaned file
df.to_csv("cleaned_billing_data.csv", index=False)

# =========================
# ANALYSIS
# =========================

print("\nTOTAL REVENUE:")
print(df["bill_amount"].sum())

print("\nAVERAGE BILL:")
print(df["bill_amount"].mean())

print("\nCUSTOMER SUMMARY:")
print(df[["customer_id", "name", "bill_amount", "bill_category"]])
