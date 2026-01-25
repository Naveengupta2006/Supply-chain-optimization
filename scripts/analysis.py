import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('../data/supply_chain_data.csv')
df

# Data Cleaning & Preparation
df.info()
df.describe()
df.isnull().sum()

# Removed duplicates SKU-date records
df = df.drop_duplicates(subset=['SKU'])

df.columns.str.lower().str.strip()

# filled missing revenue generated with business accepted averges.
avg_revenue = df['Revenue generated'].mean()
df['Revenue generated'] = df['Revenue generated'].fillna(avg_revenue)

# Standardized product and location names.
def standardized_product(df):
    cols = ['Product type','Revenue generated']
    for col in cols:
        if col in df.columns:
            df[col] = df[col].str.strip().str.upper()

    print('Standardization complete.') 
    return df           

# Ensured numeric fields (sales, revenue, stock) were consistent
def ensure_numeric_field(df):
    cols = ['Price', 'Revenue generated','Shipping costs','Manufacturing costs','defeat rates','Costs']
    for col in cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
ensure_numeric_field(df)

df['Lead_time'] = pd.to_datetime(df['Lead time'], errors= 'coerce')
df['Manufacturing lead time'] = pd.to_datetime(df['Manufacturing lead time'], errors= 'coerce')

# Demand Trend Analysis
# Compared sales volume across SKUs
sku_demand = df.groupby('SKU')['Revenue generated'].sum().sort_values(ascending= False).head(50)
print(sku_demand)


plt.Figure(figsize=(12,6))
sns.histplot(x= sku_demand.index, y= sku_demand.values)
plt.title("Top 7 Product Groups Driving Consistent Revenue Decline")
plt.xlabel("SKU", fontsize= 12)
plt.ylabel('Total Revenue', fontsize= 12)
plt.xticks(rotation= 45)
plt.show()

# identify high-demand vs low-demand products.
threshold = sku_demand.mean()

high_demand_sku = sku_demand[sku_demand >= threshold]
low_demand_sku = sku_demand[sku_demand < threshold]

print("High Demand SKU:",high_demand_sku.index.to_list())
print("Low Demand SKU:", low_demand_sku.index.to_list())

# define colour using if-else function
colors = ['green' if x >= threshold else 'red' for x in sku_demand]

# create bar plot
plt.figure(figsize=(12,6))

# use seaborn for the bar chart
sns.barplot(x= sku_demand.index, y= sku_demand.values, palette= colors)

# add a dashed line to show the average threshold
plt.axhline(threshold, color='black', linestyle='--', linewidth=2, label= f'Average Threshold: {threshold:.0f}')

plt.title('Critical Performance Split: 50% of SKUs Falling Below Revenue Targets', fontsize= 16)
plt.xlabel('SKU Names', fontsize= 12)
plt.ylabel('Total Revenue', fontsize= 12)
plt.legend()
plt.xticks(rotation= 45)
plt.tight_layout()
plt.show()

# analyzed sales trend by location
location_revenue = df.groupby('Location')['Revenue generated'].sum().sort_values(ascending= False)
print(location_revenue)

plt.Figure(figsize=(10,6))
sns.barplot(x= location_revenue.index, y= location_revenue.values, palette='magma')
plt.title('Mumbai and Kolkata Lead Revenue Growth, While 50% of SKUs Face Stagnation', fontsize= 12)
plt.xlabel('Location', fontsize= 12)
plt.ylabel('Revenue Genarated', fontsize= 12)
plt.xticks(rotation= 45)
plt.tight_layout()
plt.show()

#check consistency for demand over time
time_trend = df.groupby('Lead_time')['Revenue generated'].sum().reset_index()
print(time_trend)

plt.figure(figsize=(12,6))
sns.lineplot(data= time_trend, x='Lead_time', y= 'Revenue generated', marker='o', color= 'purple', linewidth= 2.5)

plt.title('Operational Volatility and Regional Gaps Threaten Consistent Revenue Growth', fontsize= 12)
plt.xlabel('Lead Time (Days)', fontsize= 12)
plt.ylabel('Total Revenue', fontsize= 12)
plt.grid(True, linestyle='--', alpha=0.6)

plt.tight_layout()
plt.show()

# calculated the customer demographics and revenue generated
cust_demo = df.groupby('Customer demographics')['Revenue generated'].sum().reset_index()
print(cust_demo)

# convert the proper dataframe using reset_index()
cust_demo_df = cust_demo.reset_index()

# create the chart
plt.figure(figsize=(10,6))

sns.barplot(data= cust_demo_df, x= 'Customer demographics', y= 'Revenue generated', palette='viridis')

# add label and title
plt.title('Performance Gap: Nearly Half of SKU portfolio to Meet Average Revenue Benchmark', fontsize= 16)
plt.xlabel('Demographic Group', fontsize=12)
plt.ylabel('Total Rvenue Generated', fontsize= 12)
plt.ticklabel_format(style='plain', axis='y')
plt.tight_layout()
plt.show()

demo_sku = df.groupby(['Customer demographics','SKU'])['Revenue generated'].sum().reset_index().head(10)
print(demo_sku)

# create the chart
plt.Figure(figsize=(12,6))

# X = demographics
# y = revenue
# hue = sku
sns.barplot(data= demo_sku, x= 'Customer demographics', y= 'Revenue generated', hue='SKU',palette='viridis')

# add label and title
plt.title('SKU 29 and SKU 36 Are the Clear "Best Sellers" for Female Customers', fontsize= 16)
plt.xlabel('Customer Demographics', fontsize= 12)
plt.ylabel('Total Revenue', fontsize= 12)
plt.legend(title='Product (SKU)', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.ticklabel_format(style='plain', axis='y')
plt.show()

location_demo = (df.groupby(['Location','Customer demographics'])['Revenue generated'].sum().reset_index())
print(location_demo)

# create a graph 
plt.figure(figsize=(12,6))

# x = location
# y = revenue
# hue = Demographics
sns.barplot(data= location_demo, x='Location', y='Revenue generated', hue= 'Customer demographics', palette='rocket')

# add labels and title
plt.title('Unknown Users Dominate in Chennai & Kolkata, While Female Shoppers Lead in Delhi', fontsize= 16)
plt.xlabel('Location', fontsize= 12)
plt.ylabel('Total Revenue', fontsize= 12)
plt.legend(title= 'Demographic Group', bbox_to_anchor=(1.05, 1), loc= 'upper left')
plt.ticklabel_format(style='plain', axis='y')
plt.tight_layout()
plt.show()

# Forecast Gap identification
# Actual sales vs avaiable stock
df['forecast_gap'] = df['Revenue generated'] - df['Stock levels']

gap_summary = df.groupby('SKU')['forecast_gap'].mean().reset_index().head(10)

print(gap_summary)

# sort the data
gap_sorted = gap_summary.sort_values('forecast_gap')

# create simple color rule
# red = negative gap (overstock)
# green = positive gap(high demand/stock-out risk)
my_colors = ['red'if x < 0 else'green' for x in gap_sorted['forecast_gap']]

# create the graph
plt.figure(figsize=(12, 6))
sns.barplot(data=gap_sorted, x='SKU', y='forecast_gap', palette=my_colors)

# Add a black line at 0 to separate the two sides
plt.axhline(0, color='black', linewidth=1)

plt.title('Missed Revenue Alert: 10 Key Products Facing Critical Inventory Shortages', fontsize=14)
plt.ylabel('Gap Amount')
plt.xlabel('SKU Name')
plt.show()

# identify under forecasted skus
under_forecasted = gap_summary[gap_summary['forecast_gap'] > 0].sort_values('forecast_gap',ascending= False)
under_forecasted

# 1. Setup the plot
plt.figure(figsize=(10, 6))

# 2. Create a simple bar chart
sns.barplot(data=under_forecasted, x='SKU', y='forecast_gap', color='#2ecc71')

# 3. Add Labels
plt.title('Critical Supply Chain Alert: SKU0 and SKU14 Lead Major Inventory Shortages', fontsize=14)
plt.xlabel('SKU Name')
plt.ylabel('Shortage Gap Amount')
plt.xticks(rotation=45) # Rotate labels so they are easy to read

plt.tight_layout()
plt.show()

# identify over forecasted skus
over_forcasted = gap_summary[gap_summary['forecast_gap'] < 0].sort_values('forecast_gap')
print(over_forcasted)