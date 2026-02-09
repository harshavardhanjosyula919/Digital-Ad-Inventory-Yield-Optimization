-- Disney Addressable Inventory Analytics
-- SQL Analysis Queries

-- 1. Revenue Loss by Vertical
SELECT 
    Vertical,
    COUNT(*) as Total_Units,
    SUM(Is_Under_Pacing) as Under_Pacing_Count,
    ROUND(AVG(Pacing_Rate), 2) as Avg_Pacing,
    ROUND(SUM(Revenue_Loss), 2) as Total_Revenue_Loss
FROM ad_inventory 
GROUP BY Vertical
ORDER BY Total_Revenue_Loss DESC;

-- 2. High-Value Under-Pacing Inventory
SELECT 
    Inventory_ID,
    Vertical,
    CPM,
    Pacing_Rate,
    Revenue_Loss,
    CASE 
        WHEN Pacing_Rate < 70 THEN 'CRITICAL'
        WHEN Pacing_Rate < 85 THEN 'AT RISK'
        ELSE 'ON TARGET'
    END as Priority_Level
FROM ad_inventory 
WHERE Pacing_Rate < 85 
    AND CPM > (SELECT AVG(CPM) * 1.2 FROM ad_inventory)
ORDER BY Revenue_Loss DESC
LIMIT 100;

-- 3. Weekly Yield Performance
SELECT 
    DATE_TRUNC('week', Date) as Week,
    COUNT(*) as Units,
    ROUND(AVG(Pacing_Rate), 2) as Avg_Pacing,
    ROUND(SUM(Actual_Revenue), 2) as Weekly_Revenue,
    ROUND((SUM(Actual_Revenue) / SUM(Potential_Revenue) * 100), 2) as Yield_Rate
FROM ad_inventory 
GROUP BY DATE_TRUNC('week', Date)
ORDER BY Week ASC;

-- 4. Audience Segment Analysis
SELECT 
    Audience_Segment,
    COUNT(*) as Impression_Count,
    ROUND(AVG(CPM), 2) as Avg_CPM,
    ROUND((SUM(Actual_Revenue) / SUM(Potential_Revenue) * 100), 2) as Yield_Rate
FROM ad_inventory 
GROUP BY Audience_Segment
ORDER BY Yield_Rate ASC;

-- 5. Device Performance
SELECT 
    Device_Type,
    SUM(CASE WHEN Pacing_Rate < 85 THEN Revenue_Loss ELSE 0 END) as Recoverable_Revenue,
    ROUND(AVG(Fill_Rate), 2) as Avg_Fill_Rate
FROM ad_inventory 
GROUP BY Device_Type
ORDER BY Recoverable_Revenue DESC;
