# 🛍️ Olist E-Commerce Performance Analysis

**Data Visualization Final Project · Summer 2026**

A 10-question analytical deep dive into the Olist Brazilian E-Commerce dataset (99,441 real orders, 2016–2018), examining how delivery speed, geography, payment behavior, and product category shape order value and customer satisfaction.

---

## 📊 Project Overview

This project explores how logistics and customer behavior interact across Brazil's largest e-commerce marketplace dataset:

1. **Does delivery reliability drive customer satisfaction?** Yes — buffer time matters more than raw speed
2. **Is cross-state shipping a structural cost problem?** Nearly 2x the delivery time, 76% higher freight cost
3. **Are negative reviews a trend or a symptom?** Isolated quarterly spikes, not steady decline

### Deliverables

- ✅ **Analysis Notebook** (`analysis.ipynb`) — 10 analytical questions, each with a publication-ready Plotly visualization
- ✅ **PDF Presentation** — key insights, real charts, and dashboard snapshots
- ✅ **Interactive Dashboard** (`app.py`) — [live on Streamlit Community Cloud](https://olist-ecommerce-dashboard-dv.streamlit.app/)
- ✅ **GitHub Repository** — full source code and data

---

## 🗂️ Project Structure

```
olist-ecommerce-project/
│
├── data/
│   ├── olist_orders_dataset.csv
│   ├── olist_customers_dataset.csv
│   ├── olist_order_items_dataset.csv
│   ├── olist_order_payments_dataset.csv
│   ├── olist_order_reviews_dataset.csv
│   ├── olist_products_dataset.csv
│   ├── olist_sellers_dataset.csv
│   ├── olist_geolocation_dataset.csv
│   └── product_category_name_translation.csv
│
├── analysis.ipynb              # Main analysis notebook (10 questions, Plotly visuals)
├── analysis.html               # Static HTML export of the notebook
│
├── app.py                      # Streamlit interactive dashboard
├── requirements.txt            # Pinned Python dependencies
│
├── .gitignore
└── README.md                   # This file
```

---

## 📈 Analysis Questions & Key Findings

### Q1: Delivery Delay vs. Review Score by State
**Visualization:** Scatter plot, bubble size = order volume
**Finding:** States with less delivery buffer score lower — AP (18.7 days early) averages 4.28★, while MA (only 10 days early) averages 3.74★. Arriving *comfortably* early matters more than simply being on time.

### Q2: Revenue per R$1 of Freight Cost, by Category
**Visualization:** Horizontal bar chart, top 15 categories
**Finding:** Computers (`pcs`) generate ~R$22–23 in revenue per R$1 of shipping cost — more than double most other categories.

### Q3: Order Value Trend — Top- vs. Bottom-Selling Categories
**Visualization:** Multi-line time series, solid vs. dashed
**Finding:** Top-selling categories (health & beauty, bed & bath, sports) hold a stable average order value month to month. Low-volume categories swing wildly, reflecting thin, unpredictable demand.

### Q4: Installment Payments vs. Order Value
**Visualization:** Box plot by payment type
**Finding:** Installment purchases on credit cards have a median order value of R$134, vs. R$77 for one-time payments — customers financing a purchase buy meaningfully bigger-ticket items.

### Q5: Review Score by Category, Conditioned on Delivery Delay
**Visualization:** Grouped bar chart, early/on-time vs. late
**Finding:** Late deliveries cut the average review score roughly in half — consistently, across every one of the top 10 categories. Delivery reliability outweighs product category as a satisfaction driver.

### Q6: Freight Cost as a Share of Product Price, by State
**Visualization:** Horizontal bar chart, color-scaled
**Finding:** Roraima (RR) and Maranhão (MA) see freight run 26–28% of product price; Alagoas (AL) sits closest to 19%.

### Q7: Weight vs. Freight Cost, by Shipping Distance
**Visualization:** Binned line chart, cross-state vs. in-state
**Finding:** Cross-state shipments cost more at every weight tier, and the gap widens further for heavier items.

### Q8: Cross-State vs. In-State Orders
**Visualization:** Dual-axis grouped bar chart
**Finding:** Cross-state orders average 14.6 days to deliver (vs. 7.5 in-state) and cost R$23.68 in freight (vs. R$13.47) — nearly double the time, 76% more cost.

### Q9: Negative Review Rate by Category, Over Time
**Visualization:** Bar chart + quarterly heatmap
**Finding:** `fashion_roupa_masculina` has the highest negative review rate (31.2%), but no category shows a steady worsening trend — negative rates spike in isolated single quarters rather than declining steadily, pointing to one-off disruptions rather than systemic quality issues.

### Q10: Order Volume & Delivery Buffer by Day of Week
**Visualization:** Combo bar + line chart, dual axis
**Finding:** Weekend orders run ~26% below weekday volume, but Saturday orders that do come in tend to arrive with slightly more delivery buffer.

---

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Clone the repo
git clone https://github.com/Hency-Babariya/olist-ecommerce-project.git
cd olist-ecommerce-project

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the Jupyter Notebook

```bash
jupyter notebook analysis.ipynb
```

Run cells sequentially to load and merge all 9 tables, explore the data, and reproduce all 10 visualizations.

### 3. Run the Streamlit Dashboard (Local)

```bash
streamlit run app.py
```

Opens the interactive dashboard at `http://localhost:8501`.

### 4. Or Just Use the Live Version

No setup needed: **[olist-ecommerce-dashboard-dv.streamlit.app](https://olist-ecommerce-dashboard-dv.streamlit.app/)**

---

## 📊 Dataset Used

| Dataset | Source | Coverage |
|---|---|---|
| **Olist Brazilian E-Commerce** | [Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) | 99,441 orders, 9 linked tables, 2016–2018 |

Real-world, rich, and varied — numerical (price, freight, review score, weight), categorical (70+ product categories, payment type), spatial (customer & seller state/city), and temporal (purchase, delivery, and estimated-delivery timestamps).

---

## 🎨 Design Principles Applied

✅ **CVD-Safe Colors** — no red-green comparisons; blue/amber/red used deliberately
✅ **Clear Titles** — state the takeaway, not just the variables plotted
✅ **Decluttered** — gridlines and chart-junk removed where they don't add information
✅ **Direct Annotation** — labels placed on the chart itself where it aids reading
✅ **Visual Hierarchy** — muted grey for context, one highlight color for the story
✅ **Clean White Background** — consistent across notebook and dashboard

---

## 🔧 Technologies Used

| Tool | Purpose |
|---|---|
| **Python** | Data processing & analysis |
| **Pandas** | Data merging & transformation |
| **Plotly** | Interactive, publication-ready visualizations |
| **Jupyter** | Analysis notebook |
| **Streamlit** | Interactive dashboard |
| **GitHub + Streamlit Community Cloud** | Version control & live deployment |

---

## 📋 Submission Checklist

- [x] All 9 CSV files in `/data`
- [x] `analysis.ipynb` runs without errors, HTML export included
- [x] 10 analytical questions, each with its own visualization
- [x] Dashboard runs locally with `streamlit run app.py`
- [x] GitHub repo is public with working code
- [x] Dashboard deployed live on Streamlit Community Cloud
- [x] PDF presentation with insights, real charts, and dashboard snapshots
- [x] README complete with setup instructions
- [ ] Submitted via Microsoft Teams — **Deadline: Friday, 31.07.2026**

---

## 📚 Data Source & Citation

**Olist Brazilian E-Commerce Public Dataset**
Source: [Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
Provided by Olist, a Brazilian e-commerce marketplace connecting small businesses to major online channels.

---

**Project Status:** ✅ Complete
**Last Updated:** July 2026
**Deadline:** 31.07.2026
