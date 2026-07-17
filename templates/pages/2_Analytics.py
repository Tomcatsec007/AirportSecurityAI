import streamlit as st
import pandas as pd
import plotly.express as px

# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Analytics | Airport Security AI",
    page_icon="📊",
    layout="wide"
)

# ==================================================
# LOAD GLOBAL CSS
# ==================================================

with open("style.css", encoding="utf-8") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )


# ==================================================
# ANALYTICS HERO
# ==================================================

st.markdown(
    """
    <div class="analytics-hero">
        <div class="analytics-badge">
            PERFORMANCE INTELLIGENCE
        </div>

        <h1>📊 Model Analytics</h1>

        <p>
            Explore and compare the detection performance of the
            YOLO models evaluated for X-ray contraband detection.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# ==================================================
# BENCHMARK DATA
# ==================================================

data = {
    "Model": [
        "YOLOv8n",
        "YOLOv10n",
        "YOLO11n",
        "YOLO11s"
    ],

    "Precision": [
        0.9330,
        0.9163,
        0.9374,
        0.9524
    ],

    "Recall": [
        0.8630,
        0.8615,
        0.8702,
        0.8893
    ],

    "mAP@50": [
        0.9130,
        0.9086,
        0.9197,
        0.9356
    ],

    "Inference (ms)": [
        2.2,
        2.4,
        2.4,
        4.6
    ]
}

df = pd.DataFrame(data)


# ==================================================
# SUMMARY CARDS
# ==================================================

st.markdown(
    '<div class="section-label">OVERVIEW</div>',
    unsafe_allow_html=True
)

st.subheader("Performance at a Glance")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(
        """
        <div class="analytics-stat-card">
            <div class="stat-icon">🤖</div>
            <div class="stat-value">4</div>
            <div class="stat-title">Models Evaluated</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c2:
    st.markdown(
        """
        <div class="analytics-stat-card">
            <div class="stat-icon">🎯</div>
            <div class="stat-value">95.24%</div>
            <div class="stat-title">Best Precision</div>
            <div class="stat-model">YOLO11s</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c3:
    st.markdown(
        """
        <div class="analytics-stat-card">
            <div class="stat-icon">🏆</div>
            <div class="stat-value">93.56%</div>
            <div class="stat-title">Best mAP@50</div>
            <div class="stat-model">YOLO11s</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c4:
    st.markdown(
        """
        <div class="analytics-stat-card">
            <div class="stat-icon">⚡</div>
            <div class="stat-value">2.2 ms</div>
            <div class="stat-title">Fastest Inference</div>
            <div class="stat-model">YOLOv8n</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ==================================================
# BENCHMARK TABLE
# ==================================================

st.markdown("<br>", unsafe_allow_html=True)

st.markdown(
    '<div class="section-label">BENCHMARK</div>',
    unsafe_allow_html=True
)

st.subheader("🏆 Model Comparison")

st.caption(
    "Side-by-side comparison of the reported benchmark metrics "
    "for the evaluated detection models."
)

display_df = df.copy()

display_df["Precision"] = (
    display_df["Precision"] * 100
).round(2)

display_df["Recall"] = (
    display_df["Recall"] * 100
).round(2)

display_df["mAP@50"] = (
    display_df["mAP@50"] * 100
).round(2)

display_df = display_df.rename(
    columns={
        "Precision": "Precision (%)",
        "Recall": "Recall (%)",
        "mAP@50": "mAP@50 (%)"
    }
)

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)


# ==================================================
# CHART SETTINGS
# ==================================================

chart_layout = {
    "template": "plotly_dark",
    "height": 420,
    "margin": dict(
        l=30,
        r=30,
        t=70,
        b=30
    ),
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(0,0,0,0)"
}


# ==================================================
# PERFORMANCE CHARTS
# ==================================================

st.markdown("<br>", unsafe_allow_html=True)

st.markdown(
    '<div class="section-label">PERFORMANCE METRICS</div>',
    unsafe_allow_html=True
)

st.subheader("🎯 Detection Performance")

left, right = st.columns(2)


# ---------------- Precision ----------------

with left:

    fig_precision = px.bar(
        df,
        x="Model",
        y="Precision",
        text_auto=".3f",
        title="Precision Comparison"
    )

    fig_precision.update_layout(
        **chart_layout,
        yaxis_range=[0.80, 1.0],
        showlegend=False
    )

    fig_precision.update_traces(
        textposition="outside"
    )

    st.plotly_chart(
        fig_precision,
        use_container_width=True
    )


# ---------------- Recall ----------------

with right:

    fig_recall = px.bar(
        df,
        x="Model",
        y="Recall",
        text_auto=".3f",
        title="Recall Comparison"
    )

    fig_recall.update_layout(
        **chart_layout,
        yaxis_range=[0.80, 1.0],
        showlegend=False
    )

    fig_recall.update_traces(
        textposition="outside"
    )

    st.plotly_chart(
        fig_recall,
        use_container_width=True
    )


# ==================================================
# mAP AND INFERENCE
# ==================================================

left, right = st.columns(2)


# ---------------- mAP@50 ----------------

with left:

    fig_map = px.bar(
        df,
        x="Model",
        y="mAP@50",
        text_auto=".3f",
        title="mAP@50 Comparison"
    )

    fig_map.update_layout(
        **chart_layout,
        yaxis_range=[0.80, 1.0],
        showlegend=False
    )

    fig_map.update_traces(
        textposition="outside"
    )

    st.plotly_chart(
        fig_map,
        use_container_width=True
    )


# ---------------- Inference ----------------

with right:

    fig_inference = px.bar(
        df,
        x="Model",
        y="Inference (ms)",
        text_auto=".1f",
        title="Inference Time Comparison"
    )

    fig_inference.update_layout(
        **chart_layout,
        showlegend=False
    )

    fig_inference.update_traces(
        textposition="outside"
    )

    st.plotly_chart(
        fig_inference,
        use_container_width=True
    )


# ==================================================
# OVERALL PERFORMANCE
# ==================================================

st.markdown("<br>", unsafe_allow_html=True)

st.markdown(
    '<div class="section-label">COMPARATIVE ANALYSIS</div>',
    unsafe_allow_html=True
)

st.subheader("📈 Overall Performance")

performance_df = df.melt(
    id_vars="Model",
    value_vars=[
        "Precision",
        "Recall",
        "mAP@50"
    ],
    var_name="Metric",
    value_name="Score"
)

fig_overall = px.line(
    performance_df,
    x="Model",
    y="Score",
    color="Metric",
    markers=True
)

fig_overall.update_layout(
    template="plotly_dark",
    height=480,
    yaxis_range=[0.80, 1.0],
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(
        l=30,
        r=30,
        t=40,
        b=30
    )
)

fig_overall.update_traces(
    line=dict(width=3),
    marker=dict(size=10)
)

st.plotly_chart(
    fig_overall,
    use_container_width=True
)


# ==================================================
# ANALYTICAL SUMMARY
# ==================================================

st.markdown("<br>", unsafe_allow_html=True)

st.markdown(
    '<div class="section-label">INSIGHTS</div>',
    unsafe_allow_html=True
)

st.subheader("🔬 Performance Summary")

col1, col2 = st.columns(2)

with col1:

    st.markdown(
        """
        <div class="insight-card">
            <div class="insight-icon">🏆</div>

            <h3>Highest Detection Performance</h3>

            <p>
                Based on the benchmark values displayed on this page,
                YOLO11s has the highest Precision, Recall, and mAP@50
                among the four evaluated models.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:

    st.markdown(
        """
        <div class="insight-card">
            <div class="insight-icon">⚡</div>

            <h3>Fastest Reported Inference</h3>

            <p>
                Based on the displayed inference values, YOLOv8n has
                the lowest reported inference time at 2.2 ms.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


# ==================================================
# FOOTER
# ==================================================

st.markdown(
    """
    <div class="analytics-footer">
        Airport Security AI • Model Performance Analytics
    </div>
    """,
    unsafe_allow_html=True
)