import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.data_processor import DataProcessor
from utils.visualization import Visualizer
from datetime import datetime, timedelta
import json

# Page config
st.set_page_config(
    page_title="FSN KPI Dashboard",
    page_icon="📊",
    layout="wide"
)

# Load custom CSS
with open('assets/styles.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Attempt to get the device width in the main area
try:
    from streamlit_javascript import st_javascript
    # Run in main area with a unique key to avoid caching issues
    raw_width = st_javascript("window.innerWidth", key="device_width")
    device_width = int(raw_width)
except Exception:
    # Fallback (assume desktop)
    device_width = 1024

st.write("Device width:", device_width)  # Debug output
# Add version parameter to force cache invalidation
@st.cache_data(ttl=60)  # Cache expires after 60 seconds
def load_data(version=1):
    """Load and process the JSON data"""
    with open('attached_assets/bfarm_entries.json') as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    # Convert date and clean data
    df['date'] = pd.to_datetime(df['date'])
    # Remove rows with missing or empty company/product
    df = df.dropna(subset=['company', 'product'])
    df = df[df['company'].str.strip() != '']
    df = df[df['product'].str.strip() != '']
    return df

# Initialize
df = load_data(version=datetime.now().timestamp())  # Force cache refresh
data_processor = DataProcessor(df)
visualizer = Visualizer()

# Sidebar filters
st.sidebar.title("Filters")

# Determine placement of date filters based on screen width
if device_width < 650:
    # Mobile: date filters in main section later below
    start_date_main = True
else:
    # Desktop: put them in the sidebar
    start_date_main = False

# If on desktop, render date filters in sidebar
if not start_date_main:
    min_date = df['date'].min().date()
    max_date = df['date'].max().date()
    start_date = st.sidebar.date_input(
        "Start Date",
        value=min_date,
        min_value=min_date,
        max_value=max_date
    )
    end_date = st.sidebar.date_input(
        "End Date",
        value=max_date,
        min_value=min_date,
        max_value=max_date
    )
else:
    # Just define min and max dates for later (in case filters are later in
    # the main section)
    min_date = df['date'].min().date()
    max_date = df['date'].max().date()

# Company multiselect filter - exclude empty values
companies = sorted(df['company'].unique().tolist())
selected_companies = st.sidebar.multiselect(
    "Select Companies",
    options=companies,
    default=None,
    help="Select one or more companies to compare"
)

# Category filter
categories = ['All'] + sorted(df['category'].unique().tolist())
selected_category = st.sidebar.selectbox("Select Category", categories)

# Main dashboard title
st.title("Field Safety Notice (FSN) KPI Dashboard")

# If mobile, display date filters in main section now
if start_date_main:
    col_date1, col_date2 = st.columns(2)
    with col_date1:
        start_date = st.date_input(
            "Start Date",
            value=min_date,
            min_value=min_date,
            max_value=max_date
        )
    with col_date2:
        end_date = st.date_input(
            "End Date",
            value=max_date,
            min_value=min_date,
            max_value=max_date
        )

# Filter data based on selections
filtered_df = data_processor.filter_data(
    start_date,
    end_date,
    selected_companies,  # Will pass None if empty list
    selected_category if selected_category != 'All' else None
)

if filtered_df.empty:
    st.warning("No data available for the selected filters")
else:
    # KPI metrics row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total FSNs", len(filtered_df))
    with col2:
        st.metric("Companies", filtered_df['company'].nunique())
    with col3:
        st.metric("Products", filtered_df['product'].nunique())
    with col4:
        st.metric("Categories", filtered_df['category'].nunique())

    # Charts section
    st.subheader("Analysis Charts")
    tab1, tab2, tab3 = st.tabs(["Time Analysis", "Company Analysis", "Product Analysis"])

    with tab1:
        if selected_companies:
            fig_timeline = visualizer.create_timeline_chart(filtered_df, group_by='company')
        else:
            fig_timeline = visualizer.create_timeline_chart(filtered_df)
        st.plotly_chart(fig_timeline, use_container_width=True)

    with tab2:
        fig_companies = visualizer.create_company_chart(filtered_df)
        st.plotly_chart(fig_companies, use_container_width=True)

    with tab3:
        fig_products = visualizer.create_product_chart(filtered_df)
        st.plotly_chart(fig_products, use_container_width=True)

    # Data table section
    st.subheader("FSN Details")
    sorted_df = filtered_df.sort_values('date', ascending=False)
    st.dataframe(
        sorted_df[['date', 'company', 'product', 'title', 'category', 'reference_number', 'link']],
        use_container_width=True,
        column_config={
            "link": st.column_config.LinkColumn("PDF Link"),
            "date": st.column_config.DateColumn("Date"),
        },
        hide_index=True
    )