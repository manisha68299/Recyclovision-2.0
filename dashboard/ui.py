import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import sqlite3
import pandas as pd
from database.db_manager import waste_db


# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="♻️ RecycloVision Dashboard",
    layout="wide"
)

st.title("♻️ RecycloVision - Sustainability Intelligence Dashboard")


# ===============================
# DATABASE CONNECTION
# ===============================
def load_data():
    conn = sqlite3.connect("data/waste_telemetry.db")

    detections = pd.read_sql_query(
        "SELECT * FROM detection_results",
        conn
    )

    carbon = pd.read_sql_query(
        "SELECT * FROM carbon_savings_log",
        conn
    )

    low_conf = pd.read_sql_query(
        "SELECT * FROM low_confidence_detections",
        conn
    )

    conn.close()

    return detections, carbon, low_conf


detections_df, carbon_df, low_conf_df = load_data()


# ===============================
# SUMMARY METRICS
# ===============================
st.subheader("📊 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

total_detections = len(detections_df)
avg_confidence = detections_df["confidence"].mean() if not detections_df.empty else 0
purity = detections_df["purity_score"].mean() if not detections_df.empty else 0
total_carbon = carbon_df["cumulative_total"].max() if not carbon_df.empty else 0

col1.metric("Total Detections", total_detections)
col2.metric("Avg Confidence", f"{avg_confidence:.2f}")
col3.metric("Avg Purity", f"{purity:.2f}%")
col4.metric("Total CO₂ Saved (kg)", f"{total_carbon:.2f}")


# ===============================
# ITEM BREAKDOWN
# ===============================
st.subheader("🗂 Waste Category Breakdown")

if not detections_df.empty:
    item_counts = detections_df["item_label"].value_counts()
    st.bar_chart(item_counts)
else:
    st.info("No detection data available yet.")


# ===============================
# PURITY TREND
# ===============================
st.subheader("📈 Purity Trend Over Time")

if not detections_df.empty:
    detections_df["timestamp"] = pd.to_datetime(detections_df["timestamp"])
    purity_trend = detections_df.groupby(
        detections_df["timestamp"].dt.date
    )["purity_score"].mean()

    st.line_chart(purity_trend)
else:
    st.info("No purity data available yet.")


# ===============================
# LOW CONFIDENCE ANALYSIS
# ===============================
st.subheader("⚠️ Low Confidence Detections")

low_conf_count = len(low_conf_df)

st.metric("Low Confidence Events", low_conf_count)

if not low_conf_df.empty:
    st.dataframe(low_conf_df.tail(10))
else:
    st.info("No low-confidence detections logged.")


# ===============================
# AI INSIGHTS SECTION
# ===============================
st.subheader("🔍 AI Insights")

if not detections_df.empty:

    most_common_item = detections_df["item_label"].value_counts().idxmax()

    st.write(f"• Most recycled item: **{most_common_item}**")

    if purity > 85:
        st.success("Campus segregation performance is excellent 🚀")
    elif purity > 70:
        st.warning("Segregation performance is moderate. Improvement possible.")
    else:
        st.error("Segregation performance needs improvement.")

else:
    st.info("Not enough data for insights.")


# ===============================
# AUTO REFRESH OPTION
# ===============================
st.markdown("---")
st.caption("Dashboard auto-updates when refreshed.")