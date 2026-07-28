import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Olist E-Commerce Insights",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# DESIGN SYSTEM
# =========================================================
INK = "#1C2541"
GREY_LIGHT = "#E5E9F0"
AMBER = "#E8871E"
BG = "#FAFBFC"

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700&family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"], .stMarkdown, p, div, span {{ font-family: 'Inter', sans-serif; }}
    h1, h2, h3, h4 {{ font-family: 'Fraunces', serif !important; color: {INK} !important; font-weight: 600 !important; }}
    h4 {{ font-size: 1.15rem !important; margin-bottom: 0.3rem !important; }}
    .stApp {{ background-color: {BG}; }}

    /* KPI cards */
    [data-testid="stMetric"] {{
        background: #FFFFFF; border: 1px solid {GREY_LIGHT}; border-top: 3px solid {AMBER};
        border-radius: 8px; padding: 16px 18px 12px 18px;
    }}
    [data-testid="stMetricLabel"] {{
        font-family: 'Inter', sans-serif; color: #6B7280; font-size: 0.78rem;
        text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600;
    }}
    [data-testid="stMetricValue"] {{ font-family: 'Fraunces', serif; color: {INK}; font-size: 1.9rem; }}

    /* Sidebar */
    section[data-testid="stSidebar"] {{ background-color: #FFFFFF; border-right: 1px solid {GREY_LIGHT}; }}
    section[data-testid="stSidebar"] h2 {{ font-size: 1.1rem !important; }}

    /* ---- Chart cards (bordered containers) ---- */
    [data-testid="stVerticalBlockBorderWrapper"] {{
        background: #FFFFFF;
        border: 1px solid {GREY_LIGHT} !important;
        border-radius: 12px !important;
        box-shadow: 0 1px 3px rgba(28, 37, 65, 0.05);
        padding: 6px 8px;
        margin-bottom: 22px;
    }}

    /* ---- Tabs, styled to look like real tabs ---- */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 6px;
        background: #FFFFFF;
        border: 1px solid {GREY_LIGHT};
        border-radius: 12px;
        padding: 6px;
        display: inline-flex;
        margin-bottom: 8px;
    }}
    .stTabs [data-baseweb="tab"] {{
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        color: #6B7280;
        font-size: 0.92rem;
        border-radius: 8px;
        padding: 8px 20px;
        background: transparent;
        transition: all 0.15s ease;
    }}
    .stTabs [data-baseweb="tab"]:hover {{
        background: {BG};
        color: {INK};
    }}
    .stTabs [aria-selected="true"] {{
        background: {AMBER} !important;
        color: #FFFFFF !important;
    }}
    .stTabs [data-baseweb="tab-highlight"] {{ display: none; }}
    .stTabs [data-baseweb="tab-border"] {{ display: none; }}

    .chart-note {{ color: #6B7280; font-size: 0.86rem; margin-top: 4px; padding: 0 6px 6px 6px; }}
    .hero-eyebrow {{
        color: {AMBER}; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase;
        font-size: 0.8rem; margin-bottom: -6px;
    }}
    hr {{ border-color: {GREY_LIGHT}; }}
    </style>
    """,
    unsafe_allow_html=True,
)


def shorten_label(text, max_len=22):
    """Truncate long category names for axis ticks / titles, e.g.
    'small_appliances_home_oven_and_coffee' -> 'small appliances ho…'"""
    text = str(text).replace("_", " ")
    if len(text) <= max_len:
        return text
    return text[: max_len - 1].rstrip() + "…"


def chart_card(title, fig, note=None, height=None, left_margin=None, legend_title=""):
    """Render a chart inside a real bordered card, with the title as wrapping HTML
    (not a Plotly title, which clips instead of wrapping)."""
    fig.update_layout(
        title_text="",  # empty string, NOT None — a missing title.text key renders as
                        # the literal word "undefined" in Streamlit's chart header
        legend_title_text=legend_title,  # defaults to "" to avoid Plotly auto-combining
                                          # "Category, group" etc.; pass legend_title="X" to set one
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="white",
        font=dict(family="Inter, sans-serif", size=12, color=INK),
    )
    fig.update_xaxes(automargin=True)
    if left_margin is not None:
        # deterministic fixed margin instead of automargin, which was over-reserving
        # space (e.g. for an axis title) and leaving a large blank gap on the left
        fig.update_yaxes(automargin=False)
        fig.update_layout(margin=dict(l=left_margin, r=10, t=16, b=10))
    else:
        fig.update_yaxes(automargin=True)
        fig.update_layout(margin=dict(l=10, r=10, t=16, b=10))
    if height:
        fig.update_layout(height=height)

    with st.container(border=True):
        st.markdown(f"#### {title}")
        st.plotly_chart(fig, use_container_width=True)
        if note:
            st.markdown(f'<p class="chart-note">{note}</p>', unsafe_allow_html=True)


# =========================================================
# DATA LOADING (mirrors notebook cells 1, 12, 13, 14)
# =========================================================
@st.cache_data
def load_data():
    orders = pd.read_csv("data/olist_orders_dataset.csv")
    customers = pd.read_csv("data/olist_customers_dataset.csv")
    order_items = pd.read_csv("data/olist_order_items_dataset.csv")
    payments = pd.read_csv("data/olist_order_payments_dataset.csv")
    reviews = pd.read_csv("data/olist_order_reviews_dataset.csv")
    products = pd.read_csv("data/olist_products_dataset.csv")
    sellers = pd.read_csv("data/olist_sellers_dataset.csv")
    category_translation = pd.read_csv("data/product_category_name_translation.csv")

    df = orders.merge(customers, on="customer_id", how="left")
    df = df.merge(order_items, on="order_id", how="left")
    df = df.merge(products, on="product_id", how="left")
    df = df.merge(sellers, on="seller_id", how="left")
    df = df.merge(payments, on="order_id", how="left")
    df = df.merge(category_translation, on="product_category_name", how="left")

    date_cols = [
        "order_purchase_timestamp", "order_approved_at",
        "order_delivered_carrier_date", "order_delivered_customer_date",
        "order_estimated_delivery_date", "shipping_limit_date",
    ]
    for col in date_cols:
        df[col] = pd.to_datetime(df[col], errors="coerce")

    df["delivery_delay_days"] = (df["order_delivered_customer_date"] - df["order_estimated_delivery_date"]).dt.days
    df["product_category_name_english"] = df["product_category_name_english"].fillna(df["product_category_name"])
    df["purchase_day_of_week"] = df["order_purchase_timestamp"].dt.day_name()
    df["cross_state"] = df["customer_state"] != df["seller_state"]

    return df, reviews


df_all, reviews = load_data()

# =========================================================
# SIDEBAR FILTERS
# =========================================================
st.sidebar.markdown("## Filters")

min_date = df_all["order_purchase_timestamp"].min().date()
max_date = df_all["order_purchase_timestamp"].max().date()
date_range = st.sidebar.date_input("Order date range", value=(min_date, max_date), min_value=min_date, max_value=max_date)
start_date, end_date = date_range if len(date_range) == 2 else (min_date, max_date)

all_states = sorted(df_all["customer_state"].dropna().unique().tolist())
selected_states = st.sidebar.multiselect("Customer state", all_states, default=[])

all_categories = sorted(df_all["product_category_name_english"].dropna().unique().tolist())
selected_categories = st.sidebar.multiselect("Product category", all_categories, default=[])

st.sidebar.markdown("---")
st.sidebar.caption(
    "Built on the Olist Brazilian E-Commerce dataset (2016–2018), mirroring the 10-question analysis "
    "from the project notebook. Category names are shown in English for readability."
)

mask = (df_all["order_purchase_timestamp"].dt.date >= start_date) & (df_all["order_purchase_timestamp"].dt.date <= end_date)
if selected_states:
    mask &= df_all["customer_state"].isin(selected_states)
if selected_categories:
    mask &= df_all["product_category_name_english"].isin(selected_categories)
df = df_all[mask].copy()


def thresh(default, floor=3):
    return max(floor, min(default, int(len(df) * 0.01)))


# =========================================================
# HEADER + KPIs
# =========================================================
st.markdown('<p class="hero-eyebrow">Olist Brazilian E-Commerce · 2016–2018</p>', unsafe_allow_html=True)
st.markdown("# E-Commerce Performance Dashboard")
st.markdown("How delivery speed, geography, payment behavior, and product category shape order outcomes.")
st.markdown("---")

if len(df) == 0:
    st.warning("No orders match the current filters. Try widening your selection.")
    st.stop()

review_lookup = df.merge(reviews[["order_id", "review_score"]], on="order_id", how="left")

k1, k2, k3, k4 = st.columns(4)
k1.metric("Orders", f"{df['order_id'].nunique():,}")
k2.metric("Avg. item price", f"R$ {df['price'].mean():,.2f}")
k3.metric("Avg. review score", f"{review_lookup['review_score'].mean():.2f} / 5")
k4.metric("Avg. delivery delay", f"{df['delivery_delay_days'].mean():,.1f} days")
st.markdown("<br>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🚚 Delivery & Logistics", "🏷️ Products & Reviews", "💳 Payments"])

# =========================================================
# TAB 1 — OVERVIEW  (Q3 + Q10)
# =========================================================
with tab1:
    # ---- Q3: order value trend, top vs bottom categories ----
    category_volume = df.groupby("product_category_name_english")["order_id"].nunique().sort_values(ascending=False)
    top3 = category_volume.head(3).index.tolist()
    bottom3 = category_volume[category_volume >= thresh(30)].tail(3).index.tolist()
    selected = top3 + bottom3

    if selected:
        trend_df = df[df["product_category_name_english"].isin(selected)].copy()
        trend_df["order_month"] = trend_df["order_purchase_timestamp"].dt.to_period("M").dt.to_timestamp()
        monthly = trend_df.groupby(["order_month", "product_category_name_english"]).agg(
            avg_order_value=("price", "mean")
        ).reset_index()
        monthly["group"] = monthly["product_category_name_english"].apply(
            lambda c: "Top-selling" if c in top3 else "Bottom-selling"
        )
        monthly["category_short"] = monthly["product_category_name_english"].apply(shorten_label)

        fig = px.line(
            monthly, x="order_month", y="avg_order_value", color="category_short", line_dash="group",
            labels={"order_month": "Month", "avg_order_value": "Average Order Value (R$)", "category_short": ""},
        )
        for trace in fig.data:
            trace.update(line=dict(width=1.8), opacity=0.85)
        fig.update_xaxes(gridcolor=GREY_LIGHT)
        fig.update_yaxes(gridcolor=GREY_LIGHT)
        fig.update_layout(
            legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.25,
                xanchor="center",
                x=0.5,
                font=dict(size=10),
                itemwidth=120
            ),
            margin=dict(b=90)
        )
        chart_card(
            "Top-selling categories keep stable prices; bottom-sellers swing more",
            fig,
            legend_title="Category",
            note="Solid vs. dashed lines mark top- vs. bottom-selling.",
        )
    else:
        st.info("Not enough categories in the current filter to show this trend.")

    # ---- Q10: order volume + delivery buffer by day of week ----
    q10_df = df.dropna(subset=["order_purchase_timestamp", "delivery_delay_days"]).copy()
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day_summary = q10_df.groupby("purchase_day_of_week").agg(
        order_count=("order_id", "nunique"), avg_delay=("delivery_delay_days", "mean")
    ).reindex(day_order).reset_index()
    day_summary["avg_delay_display"] = -day_summary["avg_delay"]

    bar_fig = px.bar(day_summary, x="purchase_day_of_week", y="order_count")
    bar_fig.update_traces(marker_color="#2E75B6", name="Order Volume", showlegend=True)
    line_fig = px.line(day_summary, x="purchase_day_of_week", y="avg_delay_display", markers=True)
    line_fig.update_traces(line=dict(color="#2A9D8F", width=2.5), marker=dict(size=8),
                            name="Avg Days Ahead of Estimate", showlegend=True)

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    for t in bar_fig.data:
        fig.add_trace(t, secondary_y=False)
    for t in line_fig.data:
        fig.add_trace(t, secondary_y=True)

    fig.update_xaxes(categoryorder="array", categoryarray=day_order, showgrid=False)
    fig.update_yaxes(title_text="Order Volume", color="#2E75B6", gridcolor=GREY_LIGHT, secondary_y=False)
    fig.update_yaxes(title_text="Avg Days Ahead of Estimate", color="#2A9D8F", secondary_y=True, showgrid=False)
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5))
    chart_card("Weekend orders are less frequent but arrive with more buffer time", fig)

# =========================================================
# TAB 2 — DELIVERY & LOGISTICS  (Q1, Q6, Q7, Q8)
# =========================================================
with tab2:
    # ---- Q1 ----
    delay_df = df.merge(reviews[["order_id", "review_score"]], on="order_id", how="left")
    delay_df = delay_df.dropna(subset=["delivery_delay_days"])
    state_summary = delay_df.groupby("customer_state").agg(
        avg_delay=("delivery_delay_days", "mean"), avg_review=("review_score", "mean"),
        order_count=("order_id", "nunique"),
    ).reset_index()
    state_summary = state_summary[state_summary["order_count"] >= thresh(30)]

    if len(state_summary) > 0:
        state_summary["size_display"] = np.sqrt(state_summary["order_count"])
        worst_state = state_summary.loc[state_summary["avg_review"].idxmin()]
        best_state = state_summary.loc[state_summary["avg_review"].idxmax()]

        fig = px.scatter(
            state_summary, x="avg_delay", y="avg_review", size="size_display", size_max=30,
            hover_data={"order_count": True, "size_display": False},
            labels={"avg_delay": "Average Delivery Delay (days, negative = early)", "avg_review": "Average Review Score"},
        )
        fig.update_traces(marker=dict(color="#4C72B0", line=dict(width=0.5, color="white")))
        for row, dy in [(worst_state, -30), (best_state, 30)]:
            fig.add_annotation(x=row["avg_delay"], y=row["avg_review"], text=f"<b>{row['customer_state']}</b>",
                                showarrow=True, arrowcolor="#333333", arrowhead=1, ax=0, ay=dy,
                                font=dict(size=12, color="#333333"))
        fig.update_xaxes(gridcolor=GREY_LIGHT)
        fig.update_yaxes(gridcolor=GREY_LIGHT)
        chart_card("States with less delivery buffer tend to score orders lower", fig)
    else:
        st.info("Not enough orders per state in the current filter to show this chart.")

    # ---- Q6 ----
    sfs = df.groupby("customer_state").agg(
        total_price=("price", "sum"), total_freight=("freight_value", "sum"), order_count=("order_id", "nunique")
    ).reset_index()
    sfs = sfs[(sfs["order_count"] >= thresh(30)) & (sfs["total_price"] > 0)]

    if len(sfs) > 0:
        sfs["freight_burden_pct"] = sfs["total_freight"] / sfs["total_price"] * 100
        top15 = sfs.sort_values("freight_burden_pct", ascending=False).head(15)

        fig = px.bar(
            top15.sort_values("freight_burden_pct"), x="freight_burden_pct", y="customer_state", orientation="h",
            color="freight_burden_pct", color_continuous_scale="Reds",
            labels={"freight_burden_pct": "Freight Cost as % of Product Price", "customer_state": "State"},
        )
        fig.update_traces(marker_line_width=0)
        fig.update_coloraxes(showscale=False)
        fig.update_xaxes(gridcolor=GREY_LIGHT)
        fig.update_yaxes(gridcolor=GREY_LIGHT, categoryorder="total ascending")
        chart_card("Remote states pay a much steeper shipping tax relative to product price", fig, height=480)
    else:
        st.info("Not enough orders per state in the current filter to show this chart.")

    # ---- Q7 ----
    wf = df.dropna(subset=["product_weight_g", "freight_value", "cross_state"]).copy()
    if len(wf) > 20:
        wf["distance_group"] = wf["cross_state"].map({True: "Cross-state", False: "In-state"})
        p99 = wf["product_weight_g"].quantile(0.99)
        wf = wf[wf["product_weight_g"] <= p99]
        wf["weight_bin"] = pd.cut(wf["product_weight_g"], bins=12)
        wf["weight_bin_mid"] = wf["weight_bin"].apply(lambda x: x.mid)
        binned = wf.groupby(["weight_bin_mid", "distance_group"], observed=True).agg(
            avg_freight=("freight_value", "mean"), order_count=("freight_value", "count")
        ).reset_index()
        binned = binned[binned["order_count"] >= thresh(30, floor=3)]

        if len(binned) > 0:
            fig = px.line(
                binned, x="weight_bin_mid", y="avg_freight", color="distance_group",
                color_discrete_map={"In-state": "#2E75B6", "Cross-state": "#E63946"}, markers=True,
                hover_data={"order_count": True},
                labels={"weight_bin_mid": "Product Weight (g)", "avg_freight": "Average Freight Cost (R$)", "distance_group": ""},
            )
            fig.update_traces(line=dict(width=2.5), marker=dict(size=7))
            fig.update_xaxes(gridcolor=GREY_LIGHT)
            fig.update_yaxes(gridcolor=GREY_LIGHT)
            fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5))
            chart_card("Cross-state shipments cost more at every weight", fig, note="Top 1% of products by weight excluded to avoid distortion from rare, very heavy items.")
        else:
            st.info("Not enough data in the current filter to show this chart.")
    else:
        st.info("Not enough data in the current filter to show this chart.")

    # ---- Q8 ----
    cs_df = df.dropna(subset=["delivery_delay_days", "freight_value", "cross_state",
                               "order_delivered_customer_date", "order_purchase_timestamp"]).copy()
    if len(cs_df) > 0:
        cs_df["distance_group"] = cs_df["cross_state"].map({True: "Cross-state", False: "In-state"})
        cs_df["delivery_days"] = (cs_df["order_delivered_customer_date"] - cs_df["order_purchase_timestamp"]).dt.days
        cs_summary = cs_df.groupby("distance_group").agg(
            avg_delivery_days=("delivery_days", "mean"), avg_freight=("freight_value", "mean")
        ).reset_index()

        if len(cs_summary) > 0:
            fig = go.Figure()
            fig.add_trace(go.Bar(x=cs_summary["distance_group"], y=cs_summary["avg_delivery_days"],
                                  name="Avg Delivery Time (days)", marker_color="#2E75B6", yaxis="y1", offsetgroup=0))
            fig.add_trace(go.Bar(x=cs_summary["distance_group"], y=cs_summary["avg_freight"],
                                  name="Avg Freight Cost (BRL)", marker_color="#E63946", yaxis="y2", offsetgroup=1))
            fig.update_traces(texttemplate="%{y:.1f}", textposition="outside")
            fig.update_layout(
                yaxis=dict(title=dict(text="Avg Delivery Time (days)", font=dict(color="#2E75B6")), gridcolor=GREY_LIGHT, tickfont=dict(color="#2E75B6")),
                yaxis2=dict(title=dict(text="Avg Freight Cost (BRL)", font=dict(color="#E63946")), overlaying="y", side="right", tickfont=dict(color="#E63946"), showgrid=False),
                barmode="group",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
            )
            chart_card("Cross-state orders take longer and cost more than in-state orders", fig)
    else:
        st.info("Not enough data in the current filter to show this chart.")

# =========================================================
# TAB 3 — PRODUCTS & REVIEWS  (Q2, Q5, Q9a, Q9b)
# =========================================================
with tab3:
    # ---- Q2 ----
    cat_summary = df.groupby("product_category_name_english").agg(
        total_revenue=("price", "sum"), total_freight=("freight_value", "sum"), item_count=("order_id", "nunique")
    ).reset_index()
    cat_summary = cat_summary[(cat_summary["item_count"] >= thresh(30)) & (cat_summary["total_freight"] > 0)]

    if len(cat_summary) > 0:
        cat_summary["revenue_per_freight"] = cat_summary["total_revenue"] / cat_summary["total_freight"]
        top15 = cat_summary.sort_values("revenue_per_freight", ascending=False).head(15)
        top15["category_short"] = top15["product_category_name_english"].apply(shorten_label)

        fig = px.bar(
            top15.sort_values("revenue_per_freight"), x="revenue_per_freight", y="category_short",
            orientation="h", color="revenue_per_freight", color_continuous_scale="Blues",
            hover_data={"product_category_name_english": True},
            labels={"revenue_per_freight": "Revenue per R$1 of Freight Cost", "category_short": "Category"},
        )
        fig.update_traces(marker_line_width=0)
        fig.update_coloraxes(showscale=False)
        fig.update_xaxes(gridcolor=GREY_LIGHT)
        fig.update_yaxes(gridcolor=GREY_LIGHT, categoryorder="total ascending")
        chart_card("These categories earn the most revenue per R$ of shipping cost", fig, height=500)
    else:
        st.info("Not enough categories in the current filter to show this chart.")

    # ---- Q5 ----
    rdf = df.merge(reviews[["order_id", "review_score"]], on="order_id", how="left")
    rdf = rdf.dropna(subset=["review_score", "delivery_delay_days"])
    if len(rdf) > 0:
        rdf["delay_group"] = rdf["delivery_delay_days"].apply(lambda x: "Early / On-time" if x <= 0 else "Late")
        top_cats = df.groupby("product_category_name_english")["order_id"].nunique().sort_values(ascending=False).head(10).index.tolist()
        rdf = rdf[rdf["product_category_name_english"].isin(top_cats)]

        if len(rdf) > 0:
            cds = rdf.groupby(["product_category_name_english", "delay_group"]).agg(
                avg_review=("review_score", "mean")
            ).reset_index()
            cds["category_short"] = cds["product_category_name_english"].apply(shorten_label)
            overall_order = (
                cds.groupby("category_short")["avg_review"].mean().sort_values(ascending=False).index.tolist()
            )

            fig = px.bar(
                cds, x="category_short", y="avg_review", color="delay_group", barmode="group",
                color_discrete_map={"Early / On-time": "#DDDDDD", "Late": "#6C9ECC"},
                category_orders={"category_short": overall_order},
                labels={"category_short": "Category", "avg_review": "Average Review Score", "delay_group": ""},
            )
            fig.update_xaxes(showgrid=False, tickangle=-30)
            fig.update_yaxes(gridcolor=GREY_LIGHT, range=[0, 5])
            fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5))
            chart_card("Late deliveries drag down review scores across nearly every category", fig, height=480)
        else:
            st.info("Not enough data in the current filter to show this chart.")
    else:
        st.info("Not enough data in the current filter to show this chart.")

    # ---- Q9a + Q9b ----
    review_df = df.merge(reviews[["order_id", "review_score"]], on="order_id", how="inner")
    review_df["is_negative"] = review_df["review_score"] <= 2
    cat_review = review_df.groupby("product_category_name_english").agg(
        total_reviews=("review_score", "count"), negative_rate=("is_negative", "mean")
    ).reset_index()
    cat_review = cat_review[cat_review["total_reviews"] >= thresh(50, floor=5)]
    top10_worst = cat_review.sort_values("negative_rate", ascending=False).head(10)

    if len(top10_worst) > 0:
        plot_df = top10_worst.sort_values("negative_rate").copy()
        plot_df["category_short"] = plot_df["product_category_name_english"].apply(shorten_label)
        worst = top10_worst.iloc[0]

        fig1 = px.bar(
            plot_df, x="negative_rate", y="category_short", orientation="h",
            color="negative_rate", color_continuous_scale="Reds",
            text=plot_df["negative_rate"].mul(100).round(1).astype(str) + "%",
            hover_data={"product_category_name_english": True},
            labels={"negative_rate": "Negative Review Rate", "category_short": "Category"},
        )
        fig1.update_traces(textposition="outside")
        fig1.update_coloraxes(showscale=False)
        fig1.update_xaxes(tickformat=".0%", gridcolor=GREY_LIGHT)
        fig1.update_yaxes(gridcolor=GREY_LIGHT)
        chart_card(
            f"{shorten_label(worst['product_category_name_english'], 30)} has the highest negative review rate ({worst['negative_rate']*100:.1f}%)",
            fig1, height=460,
        )

        # ---- heatmap uses Portuguese category names end-to-end, mirroring the notebook exactly ----
        cat_review_pt = review_df.groupby("product_category_name").agg(
            total_reviews=("review_score", "count"), negative_rate=("is_negative", "mean")
        ).reset_index()
        cat_review_pt = cat_review_pt[cat_review_pt["total_reviews"] >= thresh(50, floor=5)]
        top10_worst_pt = cat_review_pt.sort_values("negative_rate", ascending=False).head(10)

        worst_categories_pt = top10_worst_pt.sort_values("negative_rate", ascending=False).head(5)["product_category_name"].tolist()
        trend_df = review_df[review_df["product_category_name"].isin(worst_categories_pt)].copy()
        trend_df["order_quarter"] = trend_df["order_purchase_timestamp"].dt.to_period("Q").dt.to_timestamp()

        heat = trend_df.groupby(["product_category_name", "order_quarter"]).agg(
            negative_rate=("is_negative", "mean"), review_count=("review_score", "count")
        ).reset_index()
        heat.loc[heat["review_count"] < thresh(20, floor=3), "negative_rate"] = None

        if heat["order_quarter"].nunique() > 1 and len(worst_categories_pt) > 0:
            pivot = heat.pivot(index="product_category_name", columns="order_quarter", values="negative_rate")
            pivot = pivot.dropna(axis=1, how="all")  # drop quarters where every category was masked (too few reviews)
        else:
            pivot = pd.DataFrame()

        if pivot.shape[1] > 1:
            fig2 = px.imshow(
                pivot, color_continuous_scale="Reds", aspect="auto",
                labels=dict(x="Quarter", y="Product Category", color="Negative Review Rate"),
            )
            fig2.update_layout(plot_bgcolor="#FFF6F3")
            fig2.update_xaxes(tickformat="%b %Y", showgrid=False)
            fig2.update_yaxes(showgrid=False)
            fig2.update_coloraxes(colorbar_tickformat=".0%")
            chart_card(
                "No category shows a steady worsening or improving trend — spikes are isolated to single quarters",
                fig2, height=420, left_margin=210,
                note="Cells with fewer than a reliable number of reviews that quarter are left blank rather than shown as a misleading rate.",
            )
        else:
            st.info("Not enough time range in the current filter to show this trend.")
    else:
        st.info("Not enough reviews in the current filter to show these charts.")

# =========================================================
# TAB 4 — PAYMENTS  (Q4)
# =========================================================
with tab4:
    pay_df = df.dropna(subset=["payment_type", "payment_installments", "payment_value"]).copy()
    if len(pay_df) > 0:
        pay_df["payment_mode"] = pay_df["payment_installments"].apply(lambda x: "One-time" if x == 1 else "Installments")
        type_counts = pay_df["payment_type"].value_counts()
        common_types = type_counts[type_counts >= thresh(100, floor=5)].index.tolist()
        pay_df = pay_df[pay_df["payment_type"].isin(common_types)]

        if len(pay_df) > 0:
            p95 = pay_df["payment_value"].quantile(0.95)
            pay_cap = pay_df[pay_df["payment_value"] <= p95].copy()
            one_time_med = pay_cap.loc[pay_cap["payment_mode"] == "One-time", "payment_value"].median()
            inst_med = pay_cap.loc[pay_cap["payment_mode"] == "Installments", "payment_value"].median()

            fig = px.box(
                pay_cap, x="payment_type", y="payment_value", color="payment_mode",
                color_discrete_map={"Installments": "#2E75B6", "One-time": "#AAAAAA"},
                notched=True, points="outliers",
                labels={"payment_type": "Payment Type", "payment_value": "Order Value (R$)", "payment_mode": ""},
            )
            fig.update_xaxes(showgrid=False)
            fig.update_yaxes(gridcolor=GREY_LIGHT, title="Order Value (BRL)")
            fig.update_layout(boxmode="group", legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5))
            chart_card(
                f"Installment payments run higher for credit cards (median R${inst_med:.0f} vs. R${one_time_med:.0f} one-time)",
                fig, height=520,
                note=f"Top 5% of orders excluded above R${p95:.0f} to keep the box plot readable.",
            )
        else:
            st.info("Not enough payment types in the current filter to show this chart.")
    else:
        st.info("Not enough data in the current filter to show this chart.")

st.markdown("---")
st.caption("Data: Olist Brazilian E-Commerce Public Dataset (Kaggle). Built with Streamlit + Plotly.")
