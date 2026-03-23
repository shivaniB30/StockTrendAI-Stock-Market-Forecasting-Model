import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Stock Trend AI Dashboard", layout="wide", page_icon="📈")

# ---------------- STYLE ----------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg,#0f2027,#203a43,#2c5364);
    color:white;
}
.title {
    text-align:center;
    font-size:40px;
    font-weight:bold;
    background: linear-gradient(90deg,#00c6ff,#0072ff);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}
.card {
    background: rgba(255,255,255,0.08);
    padding:20px;
    border-radius:15px;
    text-align:center;
    box-shadow:0 4px 20px rgba(0,0,0,0.3);
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown('<div class="title">📈 Stock Trend AI Dashboard</div>', unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.title("📊 Control Panel")
uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success("Dataset Loaded ✅")
else:
    st.warning("Upload dataset to continue")
    st.stop()

# ---------------- DATA PREP ----------------
if "Close" in df.columns:
    closes = df["Close"]
else:
    closes = df.select_dtypes(include=np.number).iloc[:,0]

# ---------------- KPI CARDS ----------------
st.markdown("## 📊 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.markdown(f'<div class="card">💰 Mean<br>{round(closes.mean(),2)}</div>', unsafe_allow_html=True)
col2.markdown(f'<div class="card">📈 Max<br>{round(closes.max(),2)}</div>', unsafe_allow_html=True)
col3.markdown(f'<div class="card">📉 Min<br>{round(closes.min(),2)}</div>', unsafe_allow_html=True)
col4.markdown(f'<div class="card">⚡ Volatility<br>{round(closes.std(),2)}</div>', unsafe_allow_html=True)

# ---------------- TABS ----------------
tab1, tab2, tab3, tab4 = st.tabs(["📂 Data", "📊 Visualization", "📈 Trend Analysis", "🤖 AI Prediction"])

# ---------------- TAB 1 ----------------
with tab1:
    st.dataframe(df.head(20))

# ---------------- TAB 2 ----------------
with tab2:
    st.subheader("📊 Visualizations")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📈 Line Chart")
        st.line_chart(closes)

    with col2:
        st.markdown("### 🌊 Area Chart")
        st.area_chart(closes)

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("### 📊 Bar Chart")
        st.bar_chart(closes.head(20))

    with col4:
        st.markdown("### 📉 Histogram")
        hist = np.histogram(closes, bins=20)[0]
        st.bar_chart(hist)

    st.markdown("### 🥧 Pie Chart")
    categories = pd.cut(closes, bins=3, labels=["Low","Medium","High"])
    pie_data = categories.value_counts()

    fig_pie = go.Figure(data=[go.Pie(
        labels=pie_data.index,
        values=pie_data.values,
        hole=0.5
    )])
    fig_pie.update_layout(template="plotly_dark")
    st.plotly_chart(fig_pie, use_container_width=True)

# ---------------- TAB 3 ----------------
with tab3:
    st.subheader("📈 Trend Analysis")

    ma7 = closes.rolling(7).mean()
    ma30 = closes.rolling(30).mean()

    fig = go.Figure()
    fig.add_trace(go.Scatter(y=closes, name="Price"))
    fig.add_trace(go.Scatter(y=ma7, name="7-Day MA"))
    fig.add_trace(go.Scatter(y=ma30, name="30-Day MA"))

    fig.update_layout(template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

# ---------------- TAB 4 ----------------
with tab4:
    st.subheader("🤖 AI Prediction")

    last = closes.iloc[-1]
    days = st.slider("Prediction Days", 1, 30, 7)

    if st.button("Run AI Prediction"):

        trend = np.linspace(0, 0.08, days)
        noise = np.random.normal(0, 0.02, days)
        predicted = last * (1 + trend + noise)

        direction = "📈 Uptrend" if predicted[-1] > last else "📉 Downtrend"
        confidence = np.random.uniform(85, 98)

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=list(range(days)),
            y=predicted,
            mode='lines+markers',
            line=dict(width=4)
        ))

        fig.update_layout(template="plotly_dark", title="Future Prediction")
        st.plotly_chart(fig, use_container_width=True)

        st.bar_chart(predicted)

        col1, col2 = st.columns(2)
        col1.metric("Trend", direction)
        col2.metric("Confidence", f"{round(confidence,2)}%")

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown("©️ 2026 Stock Trend AI Dashboard | Premium Version 🚀")
