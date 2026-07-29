import numpy as np, pandas as pd

def get_portfolio_pacing():
    """Generates portfolio-level budget pacing and TripleWhale MER metrics."""
    return pd.DataFrame([
        {"Client": "Brand A (Apparel)", "Target_Spend": 45000, "Current_Spend": 41500, "Revenue": 207500, "Target_ROAS": 4.5, "Actual_ROAS": 5.0, "MER": 0.18, "Target_POAS": 1.5, "Actual_POAS": 1.85, "Retention": "Stable"},
        {"Client": "Brand B (Home Goods)", "Target_Spend": 120000, "Current_Spend": 118000, "Revenue": 448400, "Target_ROAS": 3.5, "Actual_ROAS": 3.8, "MER": 0.22, "Target_POAS": 1.2, "Actual_POAS": 1.40, "Retention": "Stable"},
        {"Client": "Brand C (Supplements)", "Target_Spend": 25000, "Current_Spend": 26200, "Revenue": 83840, "Target_ROAS": 3.0, "Actual_ROAS": 3.2, "MER": 0.28, "Target_POAS": 1.1, "Actual_POAS": 1.15, "Retention": "At Risk (Overspend)"},
        {"Client": "Brand D (Tech Acc)", "Target_Spend": 65000, "Current_Spend": 62000, "Revenue": 266600, "Target_ROAS": 4.0, "Actual_ROAS": 4.3, "MER": 0.20, "Target_POAS": 1.4, "Actual_POAS": 1.65, "Retention": "Stable"},
    ])

def get_campaign_performance():
    """Generates campaign-level analytics across Google & Microsoft Ads."""
    return pd.DataFrame([
        {"Campaign_Name": "UK_PMax_BestSellers", "Platform": "Google Ads", "Type": "Performance Max", "Spend": 18500, "CPA": 22.50, "ROAS": 4.8, "POAS": 1.9, "Status": "Active"},
        {"Campaign_Name": "US_Search_Brand", "Platform": "Google Ads", "Type": "Search", "Spend": 4200, "CPA": 8.10, "ROAS": 8.5, "POAS": 3.2, "Status": "Active"},
        {"Campaign_Name": "UK_Shopping_MidTier", "Platform": "Microsoft Ads", "Type": "Shopping", "Spend": 3800, "CPA": 18.90, "ROAS": 3.9, "POAS": 1.4, "Status": "Active"},
        {"Campaign_Name": "Global_DemandGen_Lookalike", "Platform": "Google Ads", "Type": "Demand Gen", "Spend": 6500, "CPA": 35.00, "ROAS": 2.1, "POAS": 0.8, "Status": "Flagged (Underperforming)"},
        {"Campaign_Name": "UK_Search_Competitor", "Platform": "Microsoft Ads", "Type": "Search", "Spend": 2100, "CPA": 42.00, "ROAS": 1.8, "POAS": 0.6, "Status": "Paused (Testing)"}
    ])

def get_sprint_tasks():
    """Generates ClickUp-style structured testing and sprint data."""
    return pd.DataFrame([
        {"Task": "A/B Test Demand Gen Creative Assets", "Client": "Brand D", "Due_Date": "2026-08-02", "Status": "In Progress", "Forecasted_Hours": 2.5},
        {"Task": "PMax Asset Group Segmentation (AI Text vs Manual)", "Client": "Brand A", "Due_Date": "2026-08-04", "Status": "To Do", "Forecasted_Hours": 3.0},
        {"Task": "TripleWhale MER vs GA4 Discrepancy Audit", "Client": "Brand B", "Due_Date": "2026-08-01", "Status": "Completed", "Forecasted_Hours": 1.5},
        {"Task": "Microsoft Ads Shopping Feed Optimization", "Client": "Brand C", "Due_Date": "2026-08-05", "Status": "To Do", "Forecasted_Hours": 2.0}
    ])
