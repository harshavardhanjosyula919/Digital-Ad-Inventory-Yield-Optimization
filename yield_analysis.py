import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Load data
print("Loading data...")
df = pd.read_csv('data/ad_inventory_data.csv')
df['Date'] = pd.to_datetime(df['Date'])

# Create figure
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Digital Ad Inventory Yield Optimization Dashboard\nQ4 2024 Analysis', 
             fontsize=18, fontweight='bold', y=0.98)

# Chart 1: Revenue Loss by Vertical
vertical_loss = df.groupby('Vertical')['Revenue_Loss'].sum().sort_values(ascending=True)
colors = ['#e74c3c' if x > vertical_loss.mean() else '#3498db' for x in vertical_loss]
axes[0,0].barh(vertical_loss.index, vertical_loss.values/1e6, color=colors)
axes[0,0].set_xlabel('Revenue Loss ($ Millions)', fontweight='bold')
axes[0,0].set_title('Yield Opportunity by Business Vertical', fontweight='bold', pad=15)
axes[0,0].grid(axis='x', alpha=0.3)
for i, v in enumerate(vertical_loss.values):
    axes[0,0].text(v/1e6 + 0.02, i, f'${v/1e6:.2f}M', va='center', fontweight='bold')

# Chart 2: Pacing Distribution
pacing_bins = [0, 60, 70, 80, 85, 90, 100]
pacing_labels = ['<60%', '60-70%', '70-80%', '80-85%', '85-90%', '90-100%']
df['Pacing_Bucket'] = pd.cut(df['Pacing_Rate'], bins=pacing_bins, labels=pacing_labels, include_lowest=True)
pacing_dist = df['Pacing_Bucket'].value_counts().sort_index()
colors2 = ['#e74c3c' if i < 3 else '#27ae60' for i in range(len(pacing_dist))]
axes[0,1].bar(range(len(pacing_dist)), pacing_dist.values/1000, color=colors2, alpha=0.8)
axes[0,1].set_xticks(range(len(pacing_dist)))
axes[0,1].set_xticklabels(pacing_labels, rotation=45)
axes[0,1].set_ylabel('Inventory Units (Thousands)', fontweight='bold')
axes[0,1].set_title('Inventory Health: Pacing Distribution', fontweight='bold', pad=15)
axes[0,1].axvline(x=3.5, color='darkred', linestyle='--', linewidth=2, alpha=0.7)
axes[0,1].text(3.6, max(pacing_dist.values/1000)*0.9, 'Target\n(85%)', fontsize=9, color='darkred', fontweight='bold')

# Chart 3: Weekly Trend
weekly = df.resample('W', on='Date').agg({
    'Actual_Revenue': 'sum',
    'Potential_Revenue': 'sum'
})
weekly['Yield_Rate'] = (weekly['Actual_Revenue'] / weekly['Potential_Revenue'] * 100)
axes[1,0].plot(weekly.index, weekly['Yield_Rate'], marker='o', linewidth=3, markersize=8, color='#2980b9', label='Actual Yield')
axes[1,0].axhline(y=85, color='#c0392b', linestyle='--', linewidth=2, alpha=0.7, label='Target (85%)')
axes[1,0].fill_between(weekly.index, weekly['Yield_Rate'], 85, where=(weekly['Yield_Rate'] < 85), alpha=0.3, color='#e74c3c')
axes[1,0].set_ylabel('Yield Rate (%)', fontweight='bold')
axes[1,0].set_title('Weekly Yield Performance Trend', fontweight='bold', pad=15)
axes[1,0].legend()
axes[1,0].grid(True, alpha=0.3)

# Chart 4: Audience Performance
audience_perf = df.groupby('Audience_Segment').apply(
    lambda x: (x['Actual_Revenue'].sum()/x['Potential_Revenue'].sum())*100
).sort_values()
colors4 = ['#27ae60' if x > 85 else '#f39c12' if x > 75 else '#e74c3c' for x in audience_perf]
axes[1,1].barh(audience_perf.index, audience_perf.values, color=colors4, alpha=0.8)
axes[1,1].set_xlabel('Yield Rate (%)', fontweight='bold')
axes[1,1].set_title('Yield Rate by Audience Segment', fontweight='bold', pad=15)
axes[1,1].axvline(x=85, color='#c0392b', linestyle='--', linewidth=2, alpha=0.7)
for i, v in enumerate(audience_perf.values):
    axes[1,1].text(v + 1, i, f'{v:.1f}%', va='center', fontweight='bold', fontsize=9)

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig('assets/yield_dashboard.png', dpi=300, bbox_inches='tight', facecolor='white')
print("✓ Dashboard saved: assets/yield_dashboard.png")

# Generate insights
total_loss = df['Revenue_Loss'].sum()
recoverable = df[df['Pacing_Rate'] < 85]['Revenue_Loss'].sum()
under_pacing_pct = df['Is_Under_Pacing'].mean() * 100
top_vertical = vertical_loss.idxmax()

print(f"\n{'='*50}")
print("KEY INSIGHTS")
print(f"{'='*50}")
print(f"Total Revenue Loss: ${total_loss:,.2f}")
print(f"Recoverable Revenue: ${recoverable:,.2f}")
print(f"Under-Pacing Rate: {under_pacing_pct:.1f}%")
print(f"Highest Risk Vertical: {top_vertical} (${vertical_loss[top_vertical]:,.2f})")
