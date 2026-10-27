from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# 1. Set up project paths
BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "Online Retail.xlsx"
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# 2. Load the dataset
print("Loading dataset...")
df = pd.read_excel(DATA_FILE)

print("\nOriginal dataset shape:", df.shape)
print("\nColumn names:")
print(df.columns.tolist())

# 3. Clean column names and data
df.columns = df.columns.str.strip()

required_columns = [
    "InvoiceNo", "Quantity", "InvoiceDate",
    "UnitPrice", "CustomerID"
]

missing_columns = set(required_columns) - set(df.columns)
if missing_columns:
    raise ValueError(f"Missing required columns: {missing_columns}")

df["InvoiceDate"] = pd.to_datetime(
    df["InvoiceDate"], errors="coerce"
)
df["Quantity"] = pd.to_numeric(
    df["Quantity"], errors="coerce"
)
df["UnitPrice"] = pd.to_numeric(
    df["UnitPrice"], errors="coerce"
)

# Remove rows without essential information
df = df.dropna(subset=required_columns)

# Remove cancelled invoices
df["InvoiceNo"] = df["InvoiceNo"].astype(str).str.strip()
df = df[~df["InvoiceNo"].str.startswith("C", na=False)]

# Keep valid purchases
df = df[
    (df["Quantity"] > 0) &
    (df["UnitPrice"] > 0)
].copy()

# Customer IDs should be consistent
df["CustomerID"] = df["CustomerID"].astype(str).str.replace(
    r"\.0$", "", regex=True
)

# Calculate transaction value
df["TotalPrice"] = df["Quantity"] * df["UnitPrice"]

print("\nCleaned dataset shape:", df.shape)
print("Unique customers:", df["CustomerID"].nunique())

# 4. Calculate RFM values
snapshot_date = df["InvoiceDate"].max() + pd.Timedelta(days=1)

rfm = df.groupby("CustomerID").agg(
    Recency=("InvoiceDate", lambda x:
             (snapshot_date - x.max()).days),
    Frequency=("InvoiceNo", "nunique"),
    Monetary=("TotalPrice", "sum")
).reset_index()

# 5. Create RFM scores
# Recency: lower number of days is better
# Frequency and Monetary: higher values are better

rfm["R_Score"] = pd.qcut(
    rfm["Recency"].rank(method="first"),
    5,
    labels=[5, 4, 3, 2, 1]
).astype(int)

rfm["F_Score"] = pd.qcut(
    rfm["Frequency"].rank(method="first"),
    5,
    labels=[1, 2, 3, 4, 5]
).astype(int)

rfm["M_Score"] = pd.qcut(
    rfm["Monetary"].rank(method="first"),
    5,
    labels=[1, 2, 3, 4, 5]
).astype(int)

rfm["RFM_Score"] = (
    rfm["R_Score"].astype(str) +
    rfm["F_Score"].astype(str) +
    rfm["M_Score"].astype(str)
)

# 6. Assign customer segments
def assign_segment(row):
    r = row["R_Score"]
    f = row["F_Score"]
    m = row["M_Score"]

    if r >= 4 and f >= 4 and m >= 4:
        return "Champions"
    elif r >= 3 and f >= 4:
        return "Loyal Customers"
    elif r >= 4 and f >= 2:
        return "Potential Loyalists"
    elif r <= 2 and f >= 3:
        return "At Risk"
    elif r <= 2 and f <= 2:
        return "Need Attention"
    else:
        return "Regular Customers"

rfm["Segment"] = rfm.apply(assign_segment, axis=1)

# 7. Create segment summary
summary = rfm.groupby("Segment").agg(
    Customer_Count=("CustomerID", "count"),
    Total_Revenue=("Monetary", "sum"),
    Average_Spending=("Monetary", "mean")
).reset_index()

summary["Customer_Percentage"] = (
    summary["Customer_Count"] / len(rfm) * 100
).round(2)

summary = summary.sort_values(
    "Customer_Count", ascending=False
)

# 8. Export results
rfm.to_csv(
    OUTPUT_DIR / "customer_rfm_segments.csv",
    index=False
)

summary.to_csv(
    OUTPUT_DIR / "segment_summary.csv",
    index=False
)

# 9. Chart: Number of customers by segment
plt.figure(figsize=(10, 6))
plt.bar(summary["Segment"], summary["Customer_Count"])
plt.title("Customer Count by Segment")
plt.xlabel("Customer Segment")
plt.ylabel("Number of Customers")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.savefig(
    OUTPUT_DIR / "customer_segments.png",
    dpi=150
)
plt.close()

# 10. Chart: Revenue by segment
plt.figure(figsize=(10, 6))
plt.bar(summary["Segment"], summary["Total_Revenue"])
plt.title("Total Revenue by Customer Segment")
plt.xlabel("Customer Segment")
plt.ylabel("Revenue")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.savefig(
    OUTPUT_DIR / "revenue_by_segment.png",
    dpi=150
)
plt.close()

# 11. Display final results
print("\nCUSTOMER SEGMENT SUMMARY")
print(summary.round(2).to_string(index=False))

print("\nTOP 10 CUSTOMERS BY SPENDING")
print(
    rfm.sort_values("Monetary", ascending=False)
    .head(10)
    [["CustomerID", "Recency", "Frequency",
      "Monetary", "Segment"]]
    .round(2)
    .to_string(index=False)
)

print("\nProject completed successfully!")
print("Check the output folder for CSV files and charts.")