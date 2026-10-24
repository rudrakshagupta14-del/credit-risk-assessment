
import requests
import streamlit as st
import pandas as pd
import plotly.express as px
from css import apply_css
API_URL = "http://127.0.0.1:8000"
st.set_page_config(
    page_title="Credit Risk Assessment",
    page_icon="📊",
    layout="wide")
apply_css()
st.title("📊 Credit Risk Assessment")
st.caption("XGBoost-powered credit default prediction")
dashboard, assessment, history = st.tabs(
    ["Dashboard", "Customer Assessment", "Prediction History"])
with dashboard:
    st.subheader("Overview")
    try:
        response = requests.get(
            f"{API_URL}/predictions",
            timeout=10)
        response.raise_for_status()
        records = response.json()
        total = len(records)
        defaults = sum(row["prediction"] == 1 for row in records)
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Predictions", total)
        col2.metric("Defaults Predicted", defaults)
        col3.metric("No Default Predicted",total - defaults)
        if records:
            st.markdown("---")
            st.subheader("Prediction Analytics")
            # Prepare prediction data
            df = pd.DataFrame(records)
            col1, col2 = st.columns(2)
            # 1. Donut Chart: Default vs Non-Default
            with col1:
                st.markdown("#### Prediction Distribution")
                df["Outcome"] = df["prediction"].map({
                    0: "Non-Default",
                    1: "Default"
                })
                counts = (
                    df["Outcome"]
                    .value_counts()
                    .reindex(["Default", "Non-Default"], fill_value=0)
                    .reset_index())
                counts.columns = ["Outcome", "Count"]
                fig_donut = px.pie(
                    counts,
                    names="Outcome",
                    values="Count",
                    hole=0.60,
                    color="Outcome",
                    color_discrete_map={
                        "Default": "#FF922B",
                        "Non-Default": "#626B75"})
                fig_donut.update_traces(
                    textinfo="percent+label",
                    textfont_color="white")
                fig_donut.update_layout(
                    template="plotly_dark",
                    paper_bgcolor="#111315",
                    plot_bgcolor="#111315",
                    showlegend=False,
                    margin=dict(t=20, b=20, l=10, r=10))
                st.plotly_chart(
                    fig_donut,
                    use_container_width=True)
            # 2. Line Chart: Predictions Over Time
            with col2:
                st.markdown("#### Prediction Activity Over Time")
                df["created_at"] = pd.to_datetime(
                    df["created_at"],
                    errors="coerce")
                timeline = (
                    df.dropna(subset=["created_at"])
                    .assign(Date=lambda x: x["created_at"].dt.date)
                    .groupby("Date")
                    .size()
                    .reset_index(name="Predictions")
                    .sort_values("Date"))
                if not timeline.empty:
                    fig_line = px.line(
                        timeline,
                        x="Date",
                        y="Predictions",
                        markers=True,
                        color_discrete_sequence=["#FF922B"])
                    fig_line.update_traces(
                        line=dict(width=3),
                        marker=dict(size=7))
                    fig_line.update_layout(
                        template="plotly_dark",
                        paper_bgcolor="#111315",
                        plot_bgcolor="#111315",
                        xaxis_title="Date",
                        yaxis_title="Number of Predictions",
                        margin=dict(t=20, b=20, l=10, r=10))
                    st.plotly_chart(
                        fig_line,
                        use_container_width=True)
                else:
                    st.info(
                        "No valid prediction timestamps available yet.")
    except requests.RequestException:
        st.warning("Cannot reach the API. Start FastAPI and refresh.")
with assessment:
    st.subheader("Assess a Customer")
    with st.form("customer_form"):
        st.write("Customer details")
        col1, col2, col3 = st.columns(3)
        limit_bal = col1.number_input("Credit Limit", min_value=0, value=50000)
        sex = col2.selectbox("Sex", [1, 2])
        education = col3.selectbox("Education", [1, 2, 3, 4, 5, 6])
        marriage = col1.selectbox("Marriage", [1, 2, 3])
        age = col2.number_input("Age", min_value=18, max_value=100, value=30)
        st.write("Repayment status")
        pay = {}
        for col, name in zip(
            st.columns(3), ["PAY_0", "PAY_2", "PAY_3"]):
            pay[name] = col.selectbox(name, [-2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8])
        for col, name in zip(st.columns(3), ["PAY_4", "PAY_5", "PAY_6"]):
            pay[name] = col.selectbox(name, [-2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8])
        st.write("Bill statement amounts")
        bills = {}
        for col, name in zip(st.columns(3),["BILL_AMT1", "BILL_AMT2", "BILL_AMT3"]):
            bills[name] = col.number_input(name, min_value=0, value=10000)
        for col, name in zip(st.columns(3),["BILL_AMT4", "BILL_AMT5", "BILL_AMT6"]):
            bills[name] = col.number_input(name, min_value=0, value=5000)
        st.write("Payment amounts")
        payments = {}
        for col, name in zip(st.columns(3),["PAY_AMT1", "PAY_AMT2", "PAY_AMT3"]):
            payments[name] = col.number_input(name, min_value=0, value=1000)
        for col, name in zip(st.columns(3),["PAY_AMT4", "PAY_AMT5", "PAY_AMT6"]):
            payments[name] = col.number_input(name, min_value=0, value=1000)
        submitted = st.form_submit_button("Predict Default Risk",type="primary")
    if submitted:
        features = {
            "LIMIT_BAL": limit_bal,
            "SEX": sex,
            "EDUCATION": education,
            "MARRIAGE": marriage,
            "AGE": age,
            **pay,
            **bills,
            **payments}
        try:
            response = requests.post(
                f"{API_URL}/predict",
                json={"features": features},
                timeout=30)
            response.raise_for_status()
            result = response.json()
            st.subheader("Prediction Result")
            if result["prediction"] == 1:
                st.error("Default predicted")
            else:
                st.success("No default predicted")
            st.metric("Estimated Default Probability",f'{result["default_probability"]:.2%}')
            st.caption(
                "Model estimate based on historical data; "
                "not a guarantee of future repayment.")
        except requests.RequestException as error:
            st.error(f"Prediction request failed: {error}")
with history:
    st.subheader("Prediction History")
    if st.button("Refresh History"):
        st.rerun()
    try:
        response = requests.get(f"{API_URL}/predictions",timeout=10)
        response.raise_for_status()
        records = response.json()
        if records:
            for record in records:
                with st.expander(f"Prediction ID: {record['id']}"):
                    st.write("Prediction:", record["prediction"])
                    st.write("Risk label:", record["risk_label"])
                    st.write("Default probability:",f"{float(record['default_probability']):.2%}")
                    st.write("Created at:", record["created_at"])
        else:
            st.info("No predictions saved yet.")
    except requests.RequestException:
        st.warning("Cannot load history. Check that FastAPI is running.")
