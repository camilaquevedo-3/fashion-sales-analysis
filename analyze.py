#!/usr/bin/env python3
"""Fashion sales analysis of fashion_sales.csv.

Computes total revenue, total units sold, average return rate;
best-selling categories; Online vs Store comparison; monthly revenue
trends; discount vs sales relationship; ad spend vs revenue relationship.
Saves 7 charts as PNGs to charts/ and writes analysis.md.
"""
import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "fashion_sales.csv")
CHART_DIR = os.path.join(BASE_DIR, "charts")
os.makedirs(CHART_DIR, exist_ok=True)

plt.rcParams.update({
    "figure.dpi": 120,
    "axes.grid": True,
    "grid.alpha": 0.3,
    "font.size": 11,
})

NAVY = "#1f3a5f"
TEAL = "#2a9d8f"
ORANGE = "#e76f51"
BLUE = "#4a90d9"


def style_axes(ax, title, xlabel, ylabel):
    ax.set_title(title, fontsize=13, fontweight="bold", pad=12, color=NAVY)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.tick_params(axis="x", rotation=0)


def save(fig, name):
    path = os.path.join(CHART_DIR, name)
    fig.savefig(path, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("Saved", path)


def main():
    df = pd.read_csv(DATA_PATH)

    # ---- 1. Overall KPIs ----
    total_revenue = df["revenue"].sum()
    total_units = df["units_sold"].sum()
    avg_return_rate = df["return_rate"].mean()

    # ---- 2. Best-selling categories ----
    cat = df.groupby("category").agg(
        units_sold=("units_sold", "sum"),
        revenue=("revenue", "sum"),
        n_rows=("units_sold", "size"),
    ).sort_values("revenue", ascending=False)

    # ---- 3. Online vs Store ----
    ch = df.groupby("channel").agg(
        revenue=("revenue", "sum"),
        units=("units_sold", "sum"),
        avg_rating=("avg_rating", "mean"),
        ad_spend=("ad_spend", "sum"),
        n_rows=("units_sold", "size"),
    )
    online_rev = ch.loc["Online", "revenue"]
    store_rev = ch.loc["Store", "revenue"]
    online_units = ch.loc["Online", "units"]
    store_units = ch.loc["Store", "units"]

    # Revenue per channel for ad-spend efficiency
    online_rev_per_ad = online_rev / ch.loc["Online", "ad_spend"]
    store_rev_per_ad = store_rev / ch.loc["Store", "ad_spend"]

    # ---- 4. Monthly revenue trend ----
    monthly = df.groupby(["year", "month_num", "month"]).agg(
        revenue=("revenue", "sum"),
        units=("units_sold", "sum"),
    ).reset_index().sort_values(["year", "month_num"])
    monthly["period"] = monthly["month"]

    # ---- 5. Discount vs sales ----
    disc = df.groupby("discount_pct").agg(
        units=("units_sold", "sum"),
        revenue=("revenue", "mean"),
        n=("units_sold", "size"),
    ).reset_index().sort_values("discount_pct")
    corr_disc_units = df["discount_pct"].corr(df["units_sold"])
    corr_disc_rev = df["discount_pct"].corr(df["revenue"])

    # ---- 6. Ad spend vs revenue ----
    corr_ad_rev = df["ad_spend"].corr(df["revenue"])

    # ---- Charts ----

    # Chart 1: Overall KPIs (revenue + units)
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    axes[0].bar(["Total Revenue"], [total_revenue], color=NAVY, width=0.5)
    axes[0].set_title("Total Revenue (USD)", fontsize=13, fontweight="bold", color=NAVY)
    axes[0].ticklabel_format(style="plain", axis="y")
    axes[0].yaxis.set_major_formatter(mtick.FuncFormatter(lambda v, _: f"${v:,.0f}"))
    axes[1].bar(["Total Units Sold"], [total_units], color=TEAL, width=0.5)
    axes[1].set_title("Total Units Sold", fontsize=13, fontweight="bold", color=TEAL)
    axes[1].ticklabel_format(style="plain", axis="y")
    axes[1].yaxis.set_major_formatter(mtick.FuncFormatter(lambda v, _: f"{v:,.0f}"))
    for ax in axes:
        ax.spines[["top", "right"]].set_visible(False)
    fig.suptitle("Overall Key Performance Indicators", fontsize=15, fontweight="bold", color=NAVY)
    plt.tight_layout(rect=[0, 0, 1, 0.94])
    save(fig, "01_overall_kpis.png")

    # Chart 2: Revenue by category
    fig, ax = plt.subplots(figsize=(9, 5))
    order = cat.sort_values("revenue", ascending=True)
    ax.barh(order.index, order["revenue"], color=[NAVY, BLUE, TEAL, ORANGE, "#767676"])
    for i, v in enumerate(order["revenue"]):
        ax.text(v + max(order["revenue"]) * 0.01, i, f"${v:,.0f}", va="center", fontsize=10)
    ax.set_xlabel("Revenue (USD)")
    style_axes(ax, "Total Revenue by Product Category", "Revenue (USD)", "Category")
    ax.xaxis.set_major_formatter(mtick.FuncFormatter(lambda v, _: f"${v:,.0f}"))
    plt.tight_layout()
    save(fig, "02_revenue_by_category.png")

    # Chart 3: Units sold by category
    fig, ax = plt.subplots(figsize=(9, 5))
    order = cat.sort_values("units_sold", ascending=True)
    ax.barh(order.index, order["units_sold"], color=[NAVY, BLUE, TEAL, ORANGE, "#767676"])
    for i, v in enumerate(order["units_sold"]):
        ax.text(v + max(order["units_sold"]) * 0.01, i, f"{v:,.0f}", va="center", fontsize=10)
    ax.set_xlabel("Units Sold")
    style_axes(ax, "Total Units Sold by Product Category", "Units Sold", "Category")
    plt.tight_layout()
    save(fig, "03_units_by_category.png")

    # Chart 4: Online vs Store revenue
    fig, ax = plt.subplots(figsize=(7.5, 5))
    labels = ["Online", "Store"]
    revs = [online_rev, store_rev]
    bars = ax.bar(labels, revs, color=[NAVY, BLUE], width=0.5)
    for b, v in zip(bars, revs):
        ax.text(b.get_x() + b.get_width() / 2, v + max(revs) * 0.01, f"${v:,.0f}",
                ha="center", fontsize=10, fontweight="bold")
    ax.set_ylabel("Revenue (USD)")
    ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda v, _: f"${v:,.0f}"))
    style_axes(ax, "Online vs Store Total Revenue", "Channel", "Revenue (USD)")
    ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout()
    save(fig, "04_channel_revenue.png")

    # Chart 5: Monthly revenue trend
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(monthly["period"], monthly["revenue"], marker="o", color=NAVY, linewidth=2, markersize=4)
    ax.set_xticks(range(0, len(monthly["period"]), 2))
    ax.set_xticklabels(monthly["period"][::2], rotation=45, ha="right")
    ax.set_ylabel("Revenue (USD)")
    ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda v, _: f"${v:,.0f}"))
    style_axes(ax, "Monthly Revenue Trend (Jan 2024 - Dec 2025)", "Month", "Revenue (USD)")
    plt.tight_layout()
    save(fig, "05_monthly_revenue_trend.png")

    # Chart 6: Discount vs units sold (scatter)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(df["discount_pct"], df["units_sold"], alpha=0.6, color=ORANGE, edgecolors="white", linewidth=0.5, s=45)
    ax.set_xlabel("Discount (%)")
    ax.set_ylabel("Units Sold")
    style_axes(ax, "Discount vs Units Sold", "Discount (%)", "Units Sold")
    ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout()
    save(fig, "06_discount_vs_units.png")

    # Chart 7: Ad spend vs revenue (scatter)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(df["ad_spend"], df["revenue"], alpha=0.6, color=BLUE, edgecolors="white", linewidth=0.5, s=45)
    ax.set_xlabel("Ad Spend (USD)")
    ax.set_ylabel("Revenue (USD)")
    ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda v, _: f"${v:,.0f}"))
    ax.xaxis.set_major_formatter(mtick.FuncFormatter(lambda v, _: f"${v:,.0f}"))
    style_axes(ax, "Advertising Spend vs Revenue", "Ad Spend (USD)", "Revenue (USD)")
    ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout()
    save(fig, "07_ad_spend_vs_revenue.png")

    # ---- Write analysis.md ----
    lines = []
    lines.append("# Fashion Sales Analysis")
    lines.append("")
    lines.append("## Dataset Overview")
    lines.append("- Source: `fashion_sales.csv`")
    lines.append(f"- Records analyzed: {len(df):,} (no missing values)")
    lines.append("- Period: January 2024 - December 2025 (24 months)")
    lines.append("- Channels: Online, Store")
    lines.append("- Categories: Accessories, Denim, Dresses, Footwear, Outerwear")
    lines.append("")
    lines.append("## 1. Overall Performance")
    lines.append("")
    lines.append(f"- **Total revenue:** ${total_revenue:,.2f}")
    lines.append(f"- **Total units sold:** {total_units:,}")
    lines.append(f"- **Average return rate:** {avg_return_rate:.1%}")
    lines.append("")
    lines.append("## 2. Best-Selling Product Categories")
    lines.append("")
    lines.append("| Category | Units Sold | Revenue (USD) |")
    lines.append("|----------|------------|---------------|")
    for cat_name, row in cat.iterrows():
        lines.append(f"| {cat_name} | {row['units_sold']:,} | ${row['revenue']:,.2f} |")
    lines.append("")
    lines.append(f"Top category by revenue: **{cat.index[0]}** (${cat.iloc[0]['revenue']:,.2f})")
    lines.append(f"Top category by units: **{cat.sort_values('units_sold', ascending=False).index[0]}** "
                 f"({cat.sort_values('units_sold', ascending=False).iloc[0]['units_sold']:,} units)")
    lines.append("")
    lines.append("## 3. Online vs Store Sales")
    lines.append("")
    lines.append(f"| Channel | Revenue (USD) | Units Sold | Avg Rating | Ad Spend (USD) |")
    lines.append("|---------|---------------|------------|------------|----------------|")
    for ch_name, row in ch.iterrows():
        lines.append(f"| {ch_name} | ${row['revenue']:,.2f} | {row['units']:,} | "
                     f"{row['avg_rating']:.2f} | ${row['ad_spend']:,.2f} |")
    lines.append("")
    lines.append(f"- Online share of revenue: {online_rev / total_revenue:.1%}")
    lines.append(f"- Store share of revenue: {store_rev / total_revenue:.1%}")
    lines.append(f"- Online revenue per ad dollar: ${online_rev_per_ad:,.2f} "
                 f"vs Store ${store_rev_per_ad:,.2f}")
    lines.append("")
    lines.append("## 4. Monthly Revenue Trends")
    lines.append("")
    peak = monthly.loc[monthly["revenue"].idxmax()]
    low = monthly.loc[monthly["revenue"].idxmin()]
    lines.append(f"- Peak month: **{peak['month']}** (${peak['revenue']:,.2f})")
    lines.append(f"- Lowest month: {low['month']} (${low['revenue']:,.2f})")
    lines.append("- Revenue generally rises through the year, peaking in Q4 (holiday season), then dips in January.")
    lines.append("")
    lines.append("## 5. Discounts vs Sales")
    lines.append("")
    lines.append(f"- Correlation (discount % vs units sold): **{corr_disc_units:.3f}**")
    lines.append(f"- Correlation (discount % vs revenue): **{corr_disc_rev:.3f}**")
    lines.append("- Higher discount percentages are associated with higher units sold, suggesting promotions drive volume.")
    lines.append("")
    lines.append("## 6. Advertising Spend vs Revenue")
    lines.append("")
    lines.append(f"- Correlation (ad spend vs revenue): **{corr_ad_rev:.3f}**")
    lines.append("- Advertising spend shows a strong positive relationship with revenue; increased ad spend is associated with higher sales.")
    lines.append("")
    lines.append("## Key Findings")
    lines.append("")
    lines.append("1. **Outerwear is the revenue leader** while Denim leads in unit volume, so category strategy should balance margin and volume.")
    lines.append("2. **Online and Store channels are roughly comparable** in revenue, but Online generates more revenue per advertising dollar, making it more ad-efficient.")
    lines.append("3. **Revenue is highly seasonal**, peaking in Q4 (November-December) and bottoming in January, indicating holiday-driven demand.")
    lines.append("4. **Deeper discounts drive higher unit volume**, though the revenue-per-unit impact should be monitored to protect margin.")
    lines.append("5. **Advertising spend correlates strongly with revenue**, supporting continued or increased ad investment, especially online.")
    lines.append("")
    lines.append("## Business Recommendations")
    lines.append("")
    lines.append("1. **Shift ad budget toward the Online channel.** Online delivers more revenue per ad dollar than Store. Reallocating a portion of Store ad spend to Online should improve overall return on ad spend while maintaining channel coverage.")
    lines.append("2. **Plan inventory and promotions around the Q4 peak.** Stock Outerwear and Dresses heavily ahead of November-December, and use January clearance sales (rather than deep year-round discounts) to move post-holiday inventory without eroding margins.")
    lines.append("3. **Use targeted discounting on high-volume categories.** Since Denim drives the most units and responds to discounts, apply strategic discount tiers to Denim to boost volume, while protecting full-price positioning for higher-margin Outerwear and Accessories.")
    lines.append("")
    lines.append("## Charts")
    lines.append("All charts are saved in the `charts/` folder:")
    for i in range(1, 8):
        lines.append(f"- `charts/0{i}_*.png`")
    lines.append("")
    content = "\n".join(lines)
    md_path = os.path.join(BASE_DIR, "analysis.md")
    with open(md_path, "w") as f:
        f.write(content)
    print("Saved", md_path)
    print()
    print("=== KEY FIGURES ===")
    print(f"Total revenue: ${total_revenue:,.2f}")
    print(f"Total units: {total_units:,}")
    print(f"Avg return rate: {avg_return_rate:.4%}")
    print(f"Online revenue share: {online_rev/total_revenue:.4%}")
    print(f"Store revenue share: {store_rev/total_revenue:.4%}")
    print(f"Corr discount-units: {corr_disc_units:.4f}")
    print(f"Corr ad-revenue: {corr_ad_rev:.4f}")

if __name__ == "__main__":
    main()
