import os
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px
import time

st.set_page_config(page_title="AutoShield Cyber War Room", layout="wide", page_icon="🛡️")
st.markdown("""
    <style>
    /* רקע כללי של האפליקציה */
    .stApp {
        background-color: #0e1117; /* שחור-כחול עמוק */
        background-image: radial-gradient(circle at 50% 50%, #1a2a4a 0%, #0e1117 100%);
    }

    /* עיצוב המטריקות למעלה */
    [data-testid="stMetricValue"] {
        color: #00d4ff; /* תכלת זוהר למספרים */
    }

    /* עיצוב ה-Sidebar */
    [data-testid="stSidebar"] {
        background-color: #112244;
    }
    </style>
    """, unsafe_allow_html=True)

load_dotenv()

def connect_to_db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

def fetch_data(query):
    conn = connect_to_db()
    df = pd.read_sql(query, conn)
    conn.close()
    return df

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/6831/6831103.png", width=100)
    st.title("🛡️ Admin Panel")
    st.write("System Status: **ACTIVE** 🟢")
    st.divider()

    st.subheader("📊 Reporting")
    if st.button("Generate CSV Report"):
        full_log = fetch_data("SELECT * FROM Blacklist")
        st.download_button("Download Full Log", full_log.to_csv(), "security_report.csv", "text/csv")

    st.divider()
    st.info("The system is currently running in **Autonomous Mode**. Mitigation engine is active.")

st.title("🛡️ AutoShield - Autonomous Cyber War Room")
st.markdown("### Real-Time Threat Detection & Automated Mitigation")
st.divider()

placeholder = st.empty()

while True:
    with placeholder.container():
        total_count_df = fetch_data("SELECT COUNT(*) as total FROM Network_Traffic")
        total_packets = total_count_df['total'][0]

        df_traffic = fetch_data("SELECT * FROM Network_Traffic ORDER BY id DESC LIMIT 1000")
        df_blacklist = fetch_data("SELECT * FROM Blacklist ORDER BY block_time DESC")  # היסטוריה מלאה!
        df_assets = fetch_data("SELECT * FROM assets")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Traffic", f"{total_packets} pkts")
        col2.metric("Total Blocked", f"{len(df_blacklist)} IPs", delta="Security Active")

        active_threats = df_traffic[df_traffic['is_anomaly'] == 1]['source_ip'].nunique()
        col3.metric("Current Threats", f"{active_threats} 🚨")
        col4.metric("Assets Protected", "4/4 🛡️")

        st.divider()

        left_col, right_col = st.columns([1, 1.5])

        with left_col:
            df_threat_counts = fetch_data("SELECT reason, COUNT(*) as count FROM Blacklist GROUP BY reason")

            if not df_threat_counts.empty:
                fig = px.pie(df_threat_counts,
                             values='count',
                             names='reason',
                             hole=0.4,
                             # 1. החזרת צבעי ה"אש" - אדומים וכתומים
                             color_discrete_map={
                                 'Brute Force Attack (SSH)': '#B22222',  # אדום אש (Firebrick)
                                 'DDoS Attack (High Volume)': '#FF0000',  # אדום דם (DDoS)
                                 'Port Scanning Activity': '#FF8C00'  # כתום כהה (סריקה)
                             })

                fig.update_layout(
                    title={
                        'text': "🔥 Threat Distribution (Total History)",
                        'y': 0.95,
                        'x': 0.5,
                        'xanchor': 'center',
                        'yanchor': 'top',
                        'font': {'size': 24, 'color': 'white', 'family': 'Arial Black'}
                    },
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    showlegend=True,

                    legend=dict(
                        orientation="v",
                        yanchor="middle",
                        y=0.5,  # מרכז הגובה
                        xanchor="left",
                        x=1.05,  # צמוד לעוגה מימין
                        font=dict(size=20, color="white"),  # טקסט גדול (20)
                        bgcolor='rgba(0,0,0,0)'
                    ),
                    margin=dict(t=80, b=20, l=10, r=180)
                )

                fig.update_traces(textinfo='percent', textfont_size=18, textfont_color="white")

                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Waiting for security logs...")

        with right_col:
            st.subheader("📜 Global Blacklist History")

            search_query = st.selectbox("Filter by Threat Type",
                                        ["All", "DDoS Attack (High Volume)", "Brute Force Attack (SSH)",
                                         "Port Scanning Activity"])

            if search_query != "All":
                display_df = df_blacklist[df_blacklist['reason'] == search_query]
            else:
                display_df = df_blacklist

            st.dataframe(
                display_df[['blocked_ip', 'reason', 'block_time']],
                use_container_width=True,
                height=350,
                column_config={
                    "blocked_ip": "Source IP",
                    "reason": "Detection Logic",
                    "block_time": "Timestamp"
                }
            )

        st.subheader("🖥️ Network Infrastructure Status")

        df_asset_attacks = fetch_data("""
                                      SELECT dest_asset_id, COUNT(*) as attacks
                                      FROM Network_Traffic
                                      WHERE is_anomaly = 1
                                      GROUP BY dest_asset_id
                                      """)

        if not df_asset_attacks.empty:
            df_status = df_assets.merge(df_asset_attacks, left_on='id', right_on='dest_asset_id', how='left').fillna(0)
            fig_assets = px.bar(df_status, x='asset_name', y='attacks', color='importance_score',
                                color_continuous_scale="Reds",
                                labels={'attacks': 'Detected Attacks', 'asset_name': 'Server Name'})
            st.plotly_chart(fig_assets, use_container_width=True)
        else:
            st.info("Scanning infrastructure for threats...")

        time.sleep(3)
        st.rerun()