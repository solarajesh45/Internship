import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

sns.set_theme(style="whitegrid")
os.makedirs("outputs", exist_ok=True)
df = pd.read_csv("amazon_Sales.csv")
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_").str.replace("-", "_")
df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
df['date'] = pd.to_datetime(df['date'], errors='coerce', infer_datetime_format=True)
df.dropna(subset=['date', 'amount'], inplace=True)
df['month'] = df['date'].dt.to_period("M")
print("Data loaded:", df.shape, "rows")
print("Date range:", df['date'].min(), "to", df['date'].max())
print("Total Sales:", df['amount'].sum())
def safe_plot(data, kind, title, xlabel="", ylabel="", filename="", color=None, rotation=45, pie=False):
    if data.empty:
        print(f"⚠️ Skipped plot: {title} (no data)")
        return
    if pie:
        data.plot(kind="pie", autopct='%1.1f%%')
        plt.ylabel("")
    else:
        data.plot(kind=kind, color=color, figsize=(12, 6))
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.xticks(rotation=rotation)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(f"outputs/{filename}")
    plt.close()
    print(f"Saved: outputs/{filename}")

monthly_sales = df.groupby('month')['amount'].sum()
safe_plot(monthly_sales, kind="bar", title="Monthly Sales",
          xlabel="Month", ylabel="Total Sales", filename="monthly_sales.png", color="skyblue")

top_categories = df.groupby('category')['amount'].sum().sort_values(ascending=False).head(10)
safe_plot(top_categories, kind="bar", title="Top Categories",
          ylabel="Sales", filename="top_categories.png", color="orange")

most_sizes = df['size'].value_counts().head(10)
safe_plot(most_sizes, kind="bar", title="Most Sold Sizes",
          ylabel="Units Sold", filename="most_sold_sizes.png", color="green")

fba_mfn = df.groupby('fulfilment')['amount'].sum()
safe_plot(fba_mfn, kind="pie", title="FBA vs MFN Sales Share",
          filename="fba_vs_mfn.png", pie=True)

top_states = df.groupby('ship_state')['amount'].sum().sort_values(ascending=False).head(10)
safe_plot(top_states, kind="bar", title="Top 10 States by Sales",
          ylabel="Revenue", filename="top_states.png", color="purple")

top_cities = df.groupby('ship_city')['amount'].sum().sort_values(ascending=False).head(10)
safe_plot(top_cities, kind="bar", title="Top 10 Cities by Sales",
          ylabel="Revenue", filename="top_cities.png", color="teal")

city_segmentation = df.groupby('ship_city').agg({
    'order_id': 'count',
    'amount': 'sum'
}).reset_index()

city_segmentation.columns = ['city', 'total_orders', 'total_revenue']
city_segmentation = city_segmentation.sort_values(by='total_revenue', ascending=False)

print("\nTop 10 Cities by Revenue:\n", city_segmentation.head(10))
city_segmentation.to_csv("outputs/city_segmentation.csv", index=False)
#print("Saved: outputs/city_segmentation.csv")
#print("\n Analysis complete! All results are saved in the 'outputs/' folder.")
