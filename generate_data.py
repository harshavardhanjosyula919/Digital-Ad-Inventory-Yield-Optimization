import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Generate Disney-like ad inventory data
np.random.seed(42)
random.seed(42)

n = 550000
start_date = datetime(2024, 10, 1)
verticals = ['Entertainment', 'Sports', 'News', 'Lifestyle', 'Kids']
devices = ['Desktop', 'Mobile', 'Tablet', 'CTV', 'Streaming']
audiences = ['Gen Z', 'Millennials', 'Gen X', 'Parents', 'Sports Fans', 'Movie Buffs']
formats = ['Video', 'Display', 'Native', 'Interactive']

data = []
for i in range(n):
    date = start_date + timedelta(days=random.randint(0, 90))
    vertical = random.choice(verticals)
    device = random.choice(devices)
    audience = random.choice(audiences)
    ad_format = random.choice(formats)
    
    total = np.random.poisson(1500) + 100
    delivered = int(total * np.random.beta(2, 1.5))
    pacing = (delivered / total) * 100
    
    base_cpm = {'Video': 25, 'Display': 5, 'Native': 12, 'Interactive': 18}[ad_format]
    vert_mult = {'Entertainment': 1.3, 'Sports': 1.5, 'News': 0.9, 'Lifestyle': 1.1, 'Kids': 0.8}[vertical]
    cpm = base_cpm * vert_mult * np.random.normal(1, 0.15)
    
    pot_rev = (total / 1000) * cpm
    act_rev = (delivered / 1000) * cpm
    
    data.append({
        'Date': date.strftime('%Y-%m-%d'),
        'Inventory_ID': f"INV_{i:06d}",
        'Vertical': vertical,
        'Device_Type': device,
        'Audience_Segment': audience,
        'Ad_Format': ad_format,
        'Total_Impressions': total,
        'Delivered_Impressions': delivered,
        'Pacing_Rate': round(pacing, 2),
        'CPM': round(cpm, 2),
        'Potential_Revenue': round(pot_rev, 2),
        'Actual_Revenue': round(act_rev, 2),
        'Revenue_Loss': round(pot_rev - act_rev, 2),
        'Is_Under_Pacing': 1 if pacing < 85 else 0,
        'Fill_Rate': round(np.random.beta(3, 1.5) * 100, 2)
    })

df = pd.DataFrame(data)
df.to_csv('data/ad_inventory_data.csv', index=False)
print(f"✓ Generated {len(df):,} records")
print(f"✓ Total Revenue Opportunity: ${df['Revenue_Loss'].sum():,.2f}")
