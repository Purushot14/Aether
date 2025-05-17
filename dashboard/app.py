"""
File: app
Author: prakash
Created: 17/05/25.
"""

__author__ = "prakash"
__date__ = "17/05/25"

import streamlit as st
import pandas as pd
import json

st.set_page_config(page_title="Aether Cost Optimization", layout="wide")

st.title("🌩️ Aether – AI-Powered Cloud Cost Optimization")
st.markdown("This dashboard displays cost optimization recommendations based on historical usage patterns.")

# Simulated data for now
sample_data = [
    {
        "tenant": "Customer_A",
        "resource_id": "analytics-pod",
        "current_cpu": "1000m",
        "recommended_cpu": "500m",
        "current_memory": "2Gi",
        "recommended_memory": "1Gi",
        "confidence": 0.93,
        "reason": "Low utilization with stable trends"
    },
    {
        "tenant": "Customer_B",
        "resource_id": "api-service-pod",
        "current_cpu": "500m",
        "recommended_cpu": "300m",
        "current_memory": "1Gi",
        "recommended_memory": "750Mi",
        "confidence": 0.89,
        "reason": "Periodic spikes, lower average usage"
    },
    {
        "tenant": "Customer_C",
        "resource_id": "web-frontend-pod",
        "current_cpu": "800m",
        "recommended_cpu": "400m",
        "current_memory": "1.5Gi",
        "recommended_memory": "1Gi",
        "confidence": 0.92,
        "reason": "Consistently under CPU quota"
    },
    {
        "tenant": "Customer_D",
        "resource_id": "report-generator-pod",
        "current_cpu": "1200m",
        "recommended_cpu": "750m",
        "current_memory": "3Gi",
        "recommended_memory": "2Gi",
        "confidence": 0.88,
        "reason": "High peaks, underutilized baseline"
    },
    {
        "tenant": "Customer_E",
        "resource_id": "batch-processor-pod",
        "current_cpu": "1500m",
        "recommended_cpu": "900m",
        "current_memory": "4Gi",
        "recommended_memory": "2.5Gi",
        "confidence": 0.95,
        "reason": "Predictable batch windows, average usage lower"
    },
    {
        "tenant": "Customer_F",
        "resource_id": "ml-model-pod",
        "current_cpu": "2000m",
        "recommended_cpu": "1800m",
        "current_memory": "6Gi",
        "recommended_memory": "5.5Gi",
        "confidence": 0.80,
        "reason": "Spiky memory usage, borderline optimization"
    }
]

df = pd.DataFrame(sample_data)

st.subheader("📊 Optimization Recommendations")
st.dataframe(df)

# Optional: select a tenant to view detailed breakdown
selected_tenant = st.selectbox("Select a Tenant for Details", df['tenant'].unique())
tenant_data = df[df['tenant'] == selected_tenant].iloc[0]

st.markdown(f"### 🔍 Details for `{selected_tenant}`")
st.json(tenant_data.to_dict())