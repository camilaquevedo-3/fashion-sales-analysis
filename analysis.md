# Fashion Sales Analysis

## Dataset Overview
- Source: `fashion_sales.csv`
- Records analyzed: 240 (no missing values)
- Period: January 2024 - December 2025 (24 months)
- Channels: Online, Store
- Categories: Accessories, Denim, Dresses, Footwear, Outerwear

## 1. Overall Performance

- **Total revenue:** $13,220,481.53
- **Total units sold:** 202,500
- **Average return rate:** 17.3%

## 2. Best-Selling Product Categories

| Category | Units Sold | Revenue (USD) |
|----------|------------|---------------|
| Outerwear | 31,905 | $4,045,991.60 |
| Dresses | 47,760 | $2,995,076.08 |
| Footwear | 33,765 | $2,794,483.04 |
| Denim | 39,984 | $2,078,649.65 |
| Accessories | 49,086 | $1,306,281.16 |

Top category by revenue: **Outerwear** ($4,045,991.60)
Top category by units: **Accessories** (49,086 units)

## 3. Online vs Store Sales

| Channel | Revenue (USD) | Units Sold | Avg Rating | Ad Spend (USD) |
|---------|---------------|------------|------------|----------------|
| Online | $6,966,152.40 | 105,687 | 4.15 | $1,340,200.00 |
| Store | $6,254,329.13 | 96,813 | 4.29 | $997,330.00 |

- Online share of revenue: 52.7%
- Store share of revenue: 47.3%
- Online revenue per ad dollar: **$5.20** vs Store **$6.27**
- Store has higher average customer rating (4.29 vs 4.15)

## 4. Monthly Revenue Trends

- Peak month: **2025-12** ($754,942.56)
- Lowest month: **2024-06** ($453,369.26)
- Revenue shows clear **seasonal peaks in November–December** (holiday season)
- Q4 consistently outperforms other quarters; summer months (June–August) show variability
- 2025 generally outperformed 2024 in most months

## 5. Discounts vs Sales

- Correlation (discount % vs units sold): **0.513** (moderate positive)
- Correlation (discount % vs revenue): **0.202** (weak positive)
- Higher discount percentages are associated with higher units sold, suggesting promotions drive volume
- However, discount impact on total revenue is weak — deep discounts may erode margin without proportional revenue gains

## 6. Advertising Spend vs Revenue

- Correlation (ad spend vs revenue): **0.208** (weak positive)
- Advertising spend shows a weak-to-moderate positive relationship with revenue
- The correlation is not strong, indicating other factors (seasonality, product mix, discounts) also drive revenue significantly

## Key Findings

1. **Outerwear drives the most revenue** ($4.05M) despite selling fewer units (31,905) — highest revenue per unit ($126.81). **Accessories leads in unit volume** (49,086) but generates the least revenue ($1.31M) due to low price point ($26.61/unit).

2. **Channels are nearly even in revenue** (Online 52.7% vs Store 47.3%), but **Store is more ad-efficient** ($6.27 revenue per ad dollar vs Online's $5.20) and has higher customer ratings (4.29 vs 4.15).

3. **Revenue is strongly seasonal** with clear Q4 holiday peaks (November–December consistently 30–60% above average). The lowest month was June 2024, not January.

4. **Discounts moderately increase unit volume** (r=0.51) but weakly affect revenue (r=0.20), suggesting volume gains may not offset margin erosion from deep discounts.

5. **Advertising spend has only a weak correlation with revenue** (r=0.21), indicating spend alone doesn't strongly predict outcomes; channel allocation, timing, and creative quality likely matter more.

## Business Recommendations

1. **Test reallocating a portion of Online ad budget to Store.** Store generates $1.07 more revenue per ad dollar and has higher customer satisfaction. Incrementally shifting spend toward Store (while monitoring Online volume impact) could improve overall return on ad spend.

2. **Build inventory and marketing plans around the Q4 holiday peak.** Ensure Outerwear and Dresses (top revenue categories) are well-stocked and promoted for November–December. Use the June–August lull for clearance of seasonal inventory rather than year-round deep discounting.

3. **Apply targeted discount strategies by category.** Since Accessories drives high volume at low price, use bundle/BOGO promotions rather than steep % discounts to protect margin. Reserve aggressive discounts for Denim (moderate margin, strong volume response) and protect full-price positioning for high-margin Outerwear.

## Charts
All charts are saved in the `charts/` folder:
- `charts/01_overall_kpis.png` — Total revenue & units sold
- `charts/02_revenue_by_category.png` — Revenue by category (horizontal bar)
- `charts/03_units_by_category.png` — Units sold by category
- `charts/04_channel_revenue.png` — Online vs Store revenue comparison
- `charts/05_monthly_revenue_trend.png` — Monthly revenue line chart (Jan 2024–Dec 2025)
- `charts/06_discount_vs_units.png` — Scatter: discount % vs units sold
- `charts/07_ad_spend_vs_revenue.png` — Scatter: ad spend vs revenue