# Power BI — Connecting to Azure SQL Warehouse

## Prerequisites

- Power BI Desktop installed ([download](https://powerbi.microsoft.com/desktop/))
- Azure SQL Warehouse deployed with tables populated by the Databricks notebooks

## Steps

### 1. Open Power BI Desktop
Launch the application and click **Get Data** → **Azure** → **Azure SQL Database**.

### 2. Enter Connection Details
| Field | Value |
|---|---|
| Server | `<your-server>.database.windows.net` |
| Database | `<your-database-name>` |
| Authentication | SQL Server or Azure AD |

### 3. Select Tables
Choose the following tables:
- `RestaurantPerformance`
- `ReviewsSentiment`
- `OrdersFact` (optional, for drill-down)

### 4. Suggested Dashboards

| Dashboard | Visualization | Data Source |
|---|---|---|
| Top Restaurants | Star rating cards | `RestaurantPerformance` |
| Avg Prep Delay | Bar chart by restaurant | `RestaurantPerformance` |
| Review Sentiment | Pie chart (Positive/Negative) | `ReviewsSentiment` |
| Delivery Bottlenecks | Stacked bar (prep vs driver wait) | `RestaurantPerformance` |
| Revenue Leaderboard | Table sorted by TotalRevenue | `RestaurantPerformance` |

### 5. Publish
Click **Publish** → select your Power BI workspace to share dashboards with your team.
