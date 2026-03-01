import sys
import os
import sqlite3
import streamlit as st
import pandas as pd

# ======================================================
# PATH HANDLING (SAFE FOR LOCAL + CLOUD)
# ======================================================

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
LOCAL_DB_PATH = os.path.join(BASE_DIR, "data", "waste_telemetry.db")
CLOUD_DB_PATH = "waste_telemetry.db"


def get_db_path():
    if os.path.exists(LOCAL_DB_PATH):
        return LOCAL_DB_PATH
    return CLOUD_DB_PATH


# ======================================================
# DATABASE INITIALIZATION (SAFE)
# ======================================================

def initialize_empty_db(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS detection_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            item_label TEXT,
            is_correct BOOLEAN,
            confidence REAL,
            purity_score REAL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS carbon_savings_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_label TEXT,
            carbon_value REAL,
            cumulative_total REAL,
            timestamp TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS low_confidence_detections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            frame_id INTEGER,
            label TEXT,
            confidence REAL,
            lighting_metric REAL,
            dynamic_threshold REAL,
            timestamp TEXT
        )
    """)

    conn.commit()
    conn.close()


# ======================================================
# LOAD DATA (DEFINED BEFORE CALL — NO ERROR)
# ======================================================

def load_data():
    db_path = get_db_path()

    if not os.path.exists(db_path):
        initialize_empty_db(db_path)

    conn = sqlite3.connect(db_path)

    try:
        detections = pd.read_sql_query("SELECT * FROM detection_results", conn)
    except:
        detections = pd.DataFrame()

    try:
        carbon = pd.read_sql_query("SELECT * FROM carbon_savings_log", conn)
    except:
        carbon = pd.DataFrame()

    try:
        low_conf = pd.read_sql_query("SELECT * FROM low_confidence_detections", conn)
    except:
        low_conf = pd.DataFrame()

    conn.close()

    return detections, carbon, low_conf


# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(
    page_title="♻️ RecycloVision Dashboard",
    layout="wide"
)

st.title("♻️ RecycloVision - Sustainability Intelligence Dashboard")


# ======================================================
# LOAD DATABASE
# ======================================================

detections_df, carbon_df, low_conf_df = load_data()


# ======================================================
# FILTER ONLY YOUR CUSTOM WASTE CLASSES
# ======================================================

VALID_CLASSES = ["PLASTIC", "METAL", "PAPER", "CARDBOARD", "GLASS", "TRASH"]

if not detections_df.empty and "item_label" in detections_df.columns:
    detections_df = detections_df[
        detections_df["item_label"].str.upper().isin(VALID_CLASSES)
    ]


# ======================================================
# KEY METRICS
# ======================================================

st.subheader("📊 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

total_detections = len(detections_df)

avg_confidence = (
    detections_df["confidence"].mean()
    if not detections_df.empty and "confidence" in detections_df.columns
    else 0
)

purity = (
    detections_df["purity_score"].mean()
    if not detections_df.empty and "purity_score" in detections_df.columns
    else 0
)

total_carbon = (
    carbon_df["cumulative_total"].max()
    if not carbon_df.empty and "cumulative_total" in carbon_df.columns
    else 0
)

col1.metric("Total Detections", total_detections)
col2.metric("Avg Confidence", f"{avg_confidence:.2f}")
col3.metric("Avg Purity", f"{purity:.2f}%")
col4.metric("Total CO₂ Saved (kg)", f"{total_carbon:.2f}")


# ======================================================
# WASTE BREAKDOWN
# ======================================================

st.subheader("🗂 Waste Category Breakdown")

if not detections_df.empty:
    item_counts = detections_df["item_label"].value_counts()
    st.bar_chart(item_counts)
else:
    st.info("No waste detection data available yet.")


# ======================================================
# PURITY TREND
# ======================================================

st.subheader("📈 Purity Trend Over Time")

if not detections_df.empty and "timestamp" in detections_df.columns:
    detections_df["timestamp"] = pd.to_datetime(
        detections_df["timestamp"],
        errors="coerce"
    )

    purity_trend = detections_df.groupby(
        detections_df["timestamp"].dt.date
    )["purity_score"].mean()

    st.line_chart(purity_trend)
else:
    st.info("No purity data available yet.")


# ======================================================
# LOW CONFIDENCE
# ======================================================

st.subheader("⚠️ Low Confidence Detections")

st.metric("Low Confidence Events", len(low_conf_df))

if not low_conf_df.empty:
    st.dataframe(low_conf_df.tail(10))
else:
    st.info("No low-confidence detections logged.")


# ======================================================
# AI INSIGHTS
# ======================================================

st.subheader("🔍 AI Insights")

if not detections_df.empty:

    most_common_item = detections_df["item_label"].value_counts().idxmax()
    st.write(f"• Most recycled item: **{most_common_item}**")

    if purity > 85:
        st.success("Segregation performance is excellent 🚀")
    elif purity > 70:
        st.warning("Segregation performance is moderate.")
    else:
        st.error("Segregation performance needs improvement.")

else:
    st.info("Not enough waste data for insights.")


st.markdown("---")
st.caption("Dashboard auto-updates when refreshed.")