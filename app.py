import streamlit as st
import pandas as pd
import altair as alt
from datetime import timedelta
from snowflake.snowpark.context import get_active_session

session = get_active_session()

st.set_page_config(page_title="Aurora Inventory Dashboard", layout="wide")
st.title("Aurora Inventory – Stock Health Dashboard")


# =====================================================
# 1. Load Data
# =====================================================
stock_df = session.table("AURORA_INVENTORY.MAIN.DAILY_STOCK").to_pandas()
health_df = session.table("AURORA_INVENTORY.MAIN.STOCK_HEALTH").to_pandas()
alerts_df = session.table("AURORA_INVENTORY.MAIN.STOCK_ALERTS").to_pandas()

stock_df["DATE"] = pd.to_datetime(stock_df["DATE"])
health_df["DATE"] = pd.to_datetime(health_df["DATE"])

current_date = health_df["DATE"].max()


# =====================================================
# 2. Filters
# =====================================================
st.sidebar.header("Filters")

locations = ["All"] + sorted(health_df["LOCATION_NAME"].unique())
items = ["All"] + sorted(health_df["ITEM_NAME"].unique())

selected_location = st.sidebar.selectbox("Location", locations)
selected_item = st.sidebar.selectbox("Item", items)

chart_type = st.sidebar.selectbox(
    "Chart Type",
    ["Heatmap", "Bar Chart (Days of Cover)", "Line Chart (Stock Trend)"]
)

filtered_df = health_df.copy()
filtered_stock_df = stock_df.copy()

if selected_location != "All":
    filtered_df = filtered_df[filtered_df["LOCATION_NAME"] == selected_location]
    filtered_stock_df = filtered_stock_df[filtered_stock_df["LOCATION_NAME"] == selected_location]

if selected_item != "All":
    filtered_df = filtered_df[filtered_df["ITEM_NAME"] == selected_item]
    filtered_stock_df = filtered_stock_df[filtered_stock_df["ITEM_NAME"] == selected_item]


# =====================================================
# 3. KPI Cards
# =====================================================
critical_count = sum(health_df["RISK_LEVEL"] == "CRITICAL")
warning_count = sum(health_df["RISK_LEVEL"] == "WARNING")
healthy_count = sum(health_df["RISK_LEVEL"] == "OK")
total_records = len(health_df)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Critical Items", critical_count)
col2.metric("Warning Items", warning_count)
col3.metric("Healthy Items", healthy_count)
col4.metric("Total Records", total_records)


# =====================================================
# 3B. Top 5 Risk Items & Top 5 Healthy Items
# =====================================================

st.subheader("Top Inventory Insights")

# Risk items sorted: CRITICAL first, then WARNING, lowest days left first
risk_items = (
    health_df[health_df["RISK_LEVEL"].isin(["CRITICAL", "WARNING"])]
    .sort_values(by=["RISK_LEVEL", "DAYS_OF_COVER"], ascending=[True, True])
    .head(5)
    [["ITEM_NAME", "LOCATION_NAME", "DAYS_OF_COVER", "RISK_LEVEL"]]
)

# Healthy items sorted by highest days of cover
healthy_top = (
    health_df[health_df["RISK_LEVEL"] == "OK"]
    .sort_values(by="DAYS_OF_COVER", ascending=False)
    .head(5)
    [["ITEM_NAME", "LOCATION_NAME", "DAYS_OF_COVER"]]
)

colA, colB = st.columns(2)

with colA:
    st.markdown("**Top 5 Highest-Risk Items**")
    if risk_items.empty:
        st.info("No high-risk items available.")
    else:
        st.dataframe(risk_items, use_container_width=True)

with colB:
    st.markdown("**Top 5 Healthiest Items**")
    if healthy_top.empty:
        st.info("No healthy items available.")
    else:
        st.dataframe(healthy_top, use_container_width=True)



# =====================================================
# 4. Forecasting Table
# =====================================================
st.subheader("Forecasted Stockout Analysis")

forecast_df = filtered_df.copy()

forecast_df["EST_STOCKOUT"] = forecast_df["DAYS_OF_COVER"].apply(
    lambda x: current_date + timedelta(days=float(x)) if pd.notnull(x) else None
)

def priority(days):
    if pd.isnull(days):
        return "Unknown"
    if days < 2:
        return "Critical"
    elif days <= 5:
        return "Warning"
    else:
        return "Healthy"

forecast_df["PRIORITY"] = forecast_df["DAYS_OF_COVER"].apply(priority)

st.dataframe(
    forecast_df[[
        "DATE",
        "LOCATION_NAME",
        "ITEM_NAME",
        "DAILY_CONSUMPTION",
        "DAYS_OF_COVER",
        "EST_STOCKOUT",
        "PRIORITY"
    ]],
    use_container_width=True
)


# =====================================================
# 5. High-Risk Alerts (Critical / Warning)
# =====================================================
st.subheader("High-Risk Alerts")

filtered_alerts = alerts_df.copy()

if selected_location != "All":
    filtered_alerts = filtered_alerts[filtered_alerts["LOCATION_NAME"] == selected_location]

if selected_item != "All":
    filtered_alerts = filtered_alerts[filtered_alerts["ITEM_NAME"] == selected_item]

if filtered_alerts.empty:
    st.info("No critical or warning items under current filters.")
else:
    st.dataframe(filtered_alerts, use_container_width=True)


# =====================================================
# 6. Healthy Inventory (Separate Section)
# =====================================================
st.subheader("Healthy Inventory Overview")

healthy_df = filtered_df[filtered_df["RISK_LEVEL"] == "OK"]

if healthy_df.empty:
    st.info("No healthy items found under the applied filters.")
else:
    st.dataframe(
        healthy_df[[
            "DATE",
            "LOCATION_NAME",
            "ITEM_NAME",
            "DAILY_CONSUMPTION",
            "DAYS_OF_COVER",
            "RISK_LEVEL"
        ]],
        use_container_width=True
    )


# =====================================================
# 7. Charts
# =====================================================
st.subheader("Stock Visualization")

if filtered_df.empty:
    st.info("No data available for selected filters.")

else:
    # ------------------------ Heatmap ------------------------
    if chart_type == "Heatmap":
        heatmap_data = filtered_df[["LOCATION_NAME", "ITEM_NAME", "DAYS_OF_COVER"]]

        chart = (
            alt.Chart(heatmap_data)
            .mark_rect()
            .encode(
                x="LOCATION_NAME:N",
                y="ITEM_NAME:N",
                color=alt.Color("DAYS_OF_COVER:Q", scale=alt.Scale(scheme="yelloworangebrown")),
                tooltip=["LOCATION_NAME", "ITEM_NAME", "DAYS_OF_COVER"]
            )
            .properties(height=300)
        )
        st.altair_chart(chart, use_container_width=True)

    # ------------------------ Bar Chart ------------------------
    elif chart_type == "Bar Chart (Days of Cover)":
        bar_data = filtered_df[["ITEM_NAME", "LOCATION_NAME", "DAYS_OF_COVER"]]

        chart = (
            alt.Chart(bar_data)
            .mark_bar()
            .encode(
                x="ITEM_NAME:N",
                y="DAYS_OF_COVER:Q",
                color="LOCATION_NAME:N",
                tooltip=["ITEM_NAME", "LOCATION_NAME", "DAYS_OF_COVER"]
            )
            .properties(height=300)
        )
        st.altair_chart(chart, use_container_width=True)

    # ------------------------ Line Chart ------------------------
    elif chart_type == "Line Chart (Stock Trend)":
        if filtered_stock_df.empty:
            st.info("Not enough data for trend visualization.")
        else:
            chart = (
                alt.Chart(filtered_stock_df)
                .mark_line(point=True)
                .encode(
                    x="DATE:T",
                    y="CLOSING_STOCK:Q",
                    color="ITEM_NAME:N",
                    tooltip=["DATE", "ITEM_NAME", "CLOSING_STOCK"]
                )
                .properties(height=300)
            )
            st.altair_chart(chart, use_container_width=True)


# =====================================================
# 8. AI Summary
# =====================================================
st.subheader("AI-Generated Stock Summary")

if st.button("Generate Summary"):
    ai_summary = None

    # Try AI SQL
    try:
        result = session.sql("""
            SELECT SNOWFLAKE.CORTEX.COMPLETE(
                'gpt-4o-mini',
                'Summarize the inventory including critical, warning, and healthy items. ' ||
                (SELECT LISTAGG(CONCAT(
                    ITEM_NAME, ' at ', LOCATION_NAME, 
                    ' (Risk: ', RISK_LEVEL, ', Days left: ', DAYS_OF_COVER, ')'), '; ')
                FROM AURORA_INVENTORY.MAIN.STOCK_HEALTH)
            ) AS SUMMARY
        """).collect()

        if result and "SUMMARY" in result[0]:
            ai_summary = result[0]["SUMMARY"]

    except Exception:
        ai_summary = None


    # Fallback AI Summary
    if ai_summary is None:
        critical = health_df[health_df["RISK_LEVEL"] == "CRITICAL"][["ITEM_NAME", "LOCATION_NAME"]].drop_duplicates()
        warning = health_df[health_df["RISK_LEVEL"] == "WARNING"][["ITEM_NAME", "LOCATION_NAME"]].drop_duplicates()
        healthy = health_df[health_df["RISK_LEVEL"] == "OK"][["ITEM_NAME", "LOCATION_NAME"]].drop_duplicates()

        summary = f"""
Inventory Summary
Critical items: {len(critical)}
Warning items: {len(warning)}
Healthy items: {len(healthy)}

Critical Risks:
"""

        for _, row in critical.iterrows():
            summary += f"- {row['ITEM_NAME']} at {row['LOCATION_NAME']} (CRITICAL)\n"

        summary += "\nWarning Risks:\n"
        for _, row in warning.iterrows():
            summary += f"- {row['ITEM_NAME']} at {row['LOCATION_NAME']} (WARNING)\n"

        summary += "\nHealthy Inventory:\n"
        for _, row in healthy.iterrows():
            summary += f"- {row['ITEM_NAME']} at {row['LOCATION_NAME']} (HEALTHY)\n"

        summary += """
Recommended Actions:
- Reorder critical items immediately.
- Reorder warning items within 2–3 days.
- Maintain healthy items and monitor fast-moving stock.
"""

        st.warning(summary)

    else:
        st.success(ai_summary)
