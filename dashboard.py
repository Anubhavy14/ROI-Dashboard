import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from faker import Faker
import datetime

# --- Page Configuration ---
st.set_page_config(
    page_title="HealthKart Influencer ROI Dashboard",
    page_icon=":)",
    layout="wide"
)

# --- Data Simulation ---
# In a real application, this data would be loaded from a database or CSV files.
@st.cache_data
def generate_fake_data():
    """Generates realistic-looking datasets for the dashboard."""
    fake = Faker()
    
    # 1. Influencers
    influencers_data = [
        {'id': 'INF001', 'name': 'Aarav Sharma', 'category': 'Fitness', 'gender': 'Male', 'follower_count': 250000, 'platform': 'Instagram'},
        {'id': 'INF002', 'name': 'Priya Patel', 'category': 'Nutrition', 'gender': 'Female', 'follower_count': 150000, 'platform': 'YouTube'},
        {'id': 'INF003', 'name': 'Rohan Mehta', 'category': 'Lifestyle', 'gender': 'Male', 'follower_count': 80000, 'platform': 'Twitter'},
        {'id': 'INF004', 'name': 'Sneha Verma', 'category': 'Fitness', 'gender': 'Female', 'follower_count': 500000, 'platform': 'YouTube'},
        {'id': 'INF005', 'name': 'Vikram Singh', 'category': 'Grit', 'gender': 'Male', 'follower_count': 120000, 'platform': 'Instagram'},
        {'id': 'INF006', 'name': 'Ananya Reddy', 'category': 'Nutrition', 'gender': 'Female', 'follower_count': 300000, 'platform': 'Instagram'},
    ]
    influencers_df = pd.DataFrame(influencers_data)

    brands = ['MuscleBlaze', 'HKVitals', 'Gritzo']
    products = {
        'MuscleBlaze': ['MB Biozyme Whey', 'MB Fuel One BCAA', 'MB Pre-Workout 200'],
        'HKVitals': ['HK Vitals Multivitamin', 'HK Vitals Fish Oil', 'HK Vitals Biotin'],
        'Gritzo': ['Gritzo SuperMilk', 'Gritzo Gummy Stars', 'Gritzo Protein Oats'],
    }

    start_date = datetime.date(2024, 1, 1)
    end_date = datetime.date(2024, 6, 30)

    # 2. Posts
    posts_list = []
    for _, inf in influencers_df.iterrows():
        for _ in range(np.random.randint(3, 8)):
            post_date = fake.date_between(start_date=start_date, end_date=end_date)
            posts_list.append({
                'post_id': f'POST{np.random.randint(1000, 9999)}',
                'influencer_id': inf['id'],
                'platform': inf['platform'],
                'date': post_date,
                'url': f'https://fakeplatform.com/post/{fake.uuid4()}',
                'caption': fake.sentence(nb_words=15),
                'reach': int(inf['follower_count'] * np.random.uniform(0.3, 0.8)),
                'likes': int(inf['follower_count'] * np.random.uniform(0.01, 0.1)),
                'comments': int(inf['follower_count'] * np.random.uniform(0.001, 0.01)),
            })
    posts_df = pd.DataFrame(posts_list)
    posts_df['date'] = pd.to_datetime(posts_df['date'])

    # 3. Tracking Data & Payouts
    tracking_list = []
    payouts_list = []
    for _, inf in influencers_df.iterrows():
        basis = np.random.choice(['per_post', 'per_order'])
        total_revenue_inf = 0
        total_orders_inf = 0
        
        campaign_brand = np.random.choice(brands)
        campaign_products = products[campaign_brand]

        for _ in range(np.random.randint(50, 200)):
            order_date = fake.date_between(start_date=start_date, end_date=end_date)
            revenue = np.random.randint(500, 3000)
            total_revenue_inf += revenue
            total_orders_inf += 1
            tracking_list.append({
                'source': f"{inf['name'].split(' ')[0].lower()}_{inf['platform'][:2].lower()}",
                'campaign': f"{campaign_brand}_Q1Q2_2024",
                'brand': campaign_brand,
                'influencer_id': inf['id'],
                'user_id': f'USR{np.random.randint(1000, 9999)}',
                'product': np.random.choice(campaign_products),
                'date': order_date,
                'orders': 1,
                'revenue': revenue,
            })
        
        rate = 0
        payout_amount = 0
        if basis == 'per_post':
            rate = int(inf['follower_count'] * np.random.uniform(0.05, 0.15))
            payout_amount = rate * len(posts_df[posts_df['influencer_id'] == inf['id']])
        else: # per_order
            rate = np.random.uniform(0.10, 0.20) # 10-20% commission
            payout_amount = total_revenue_inf * rate

        payouts_list.append({
            'influencer_id': inf['id'],
            'basis': basis,
            'rate': round(rate, 2),
            'orders': total_orders_inf,
            'total_payout': round(payout_amount, 2),
        })

    tracking_df = pd.DataFrame(tracking_list)
    tracking_df['date'] = pd.to_datetime(tracking_df['date'])
    payouts_df = pd.DataFrame(payouts_list)

    return influencers_df, posts_df, tracking_df, payouts_df

# --- Helper Functions ---
def to_csv(df):
    """Converts a DataFrame to a CSV string for downloading."""
    return df.to_csv(index=False).encode('utf-8')

# --- Load Data ---
influencers_df, posts_df, tracking_df, payouts_df = generate_fake_data()

# --- Main Dashboard UI ---
st.title("HealthKart Influencer ROI Dashboard")
st.markdown("Analyze campaign performance and maximize your return on investment.")

# --- Sidebar Filters ---
st.sidebar.header("Filters")

# Date Range Filter
min_date = tracking_df['date'].min().date()
max_date = tracking_df['date'].max().date()
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

start_date, end_date = date_range
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Other Filters
brand_filter = st.sidebar.selectbox("Brand", options=['All'] + list(tracking_df['brand'].unique()))
platform_filter = st.sidebar.selectbox("Platform", options=['All'] + list(influencers_df['platform'].unique()))
influencer_type_filter = st.sidebar.selectbox("Influencer Category", options=['All'] + list(influencers_df['category'].unique()))

# --- Filtering Logic ---
# Apply date filter first
filtered_tracking_df = tracking_df[(tracking_df['date'] >= start_date) & (tracking_df['date'] <= end_date)]
filtered_posts_df = posts_df[(posts_df['date'] >= start_date) & (posts_df['date'] <= end_date)]

# Apply other filters
filtered_influencers_df = influencers_df.copy()
if platform_filter != 'All':
    filtered_influencers_df = filtered_influencers_df[filtered_influencers_df['platform'] == platform_filter]
if influencer_type_filter != 'All':
    filtered_influencers_df = filtered_influencers_df[filtered_influencers_df['category'] == influencer_type_filter]

# Filter tracking data based on selected influencers and brand
filtered_influencer_ids = filtered_influencers_df['id'].unique()
filtered_tracking_df = filtered_tracking_df[filtered_tracking_df['influencer_id'].isin(filtered_influencer_ids)]
if brand_filter != 'All':
    filtered_tracking_df = filtered_tracking_df[filtered_tracking_df['brand'] == brand_filter]

# Final list of influencers who have tracking data in the filtered set
final_influencer_ids = filtered_tracking_df['influencer_id'].unique()
final_influencers_df = influencers_df[influencers_df['id'].isin(final_influencer_ids)]
final_payouts_df = payouts_df[payouts_df['influencer_id'].isin(final_influencer_ids)]
final_posts_df = filtered_posts_df[filtered_posts_df['influencer_id'].isin(final_influencer_ids)]


# --- Analytics Calculation ---
if not filtered_tracking_df.empty:
    total_revenue = filtered_tracking_df['revenue'].sum()
    total_payout = final_payouts_df['total_payout'].sum()
    total_orders = filtered_tracking_df['orders'].sum()
    roas = total_revenue / total_payout if total_payout > 0 else 0

    # Assumption: Baseline revenue is 35% of the attributed revenue.
    baseline_multiplier = 0.35
    incremental_revenue = total_revenue * (1 - baseline_multiplier)
    incremental_roas = incremental_revenue / total_payout if total_payout > 0 else 0
else:
    total_revenue, total_payout, total_orders, roas, incremental_roas = 0, 0, 0, 0, 0


# --- UI Tabs ---
tab1, tab2, tab3 = st.tabs([" Campaign Overview", " Influencer Deep Dive", " Payouts Tracker"])

with tab1:
    st.header("Campaign Performance Overview")

    if filtered_tracking_df.empty:
        st.warning("No data available for the selected filters. Please adjust your selection.")
    else:
        # KPIs
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Revenue", f"₹{total_revenue:,.0f}")
        col2.metric("Total Payout", f"₹{total_payout:,.0f}")
        col3.metric("Overall ROAS", f"{roas:.2f}")
        col4.metric("Incremental ROAS", f"{incremental_roas:.2f}")
        st.caption("Note: Incremental ROAS assumes a 35% baseline revenue that would have occurred without the campaign.")
        
        st.markdown("---")

        # Charts
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Revenue by Platform")
            platform_revenue = filtered_tracking_df.merge(influencers_df[['id', 'platform']], left_on='influencer_id', right_on='id')
            platform_revenue = platform_revenue.groupby('platform')['revenue'].sum().reset_index()
            fig = px.bar(platform_revenue, x='platform', y='revenue', title="Total Revenue per Platform", text_auto='.2s', color='platform')
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("Revenue by Influencer Category")
            category_revenue = filtered_tracking_df.merge(influencers_df[['id', 'category']], left_on='influencer_id', right_on='id')
            category_revenue = category_revenue.groupby('category')['revenue'].sum().reset_index()
            fig = px.pie(category_revenue, names='category', values='revenue', title="Revenue Share by Influencer Category", hole=0.3)
            st.plotly_chart(fig, use_container_width=True)

        st.subheader("Top 5 Influencers by ROAS")
        # Corrected the merge operation here
        influencer_performance = final_influencers_df.merge(final_payouts_df, left_on='id', right_on='influencer_id')
        inf_revenue = filtered_tracking_df.groupby('influencer_id')['revenue'].sum().reset_index()
        influencer_performance = influencer_performance.merge(inf_revenue, on='influencer_id')
        
        # Ensure total_payout is not zero to avoid division by zero errors
        influencer_performance = influencer_performance[influencer_performance['total_payout'] > 0]
        influencer_performance['roas'] = influencer_performance['revenue'] / influencer_performance['total_payout']
        
        top_5_roas = influencer_performance.sort_values('roas', ascending=False).head(5)

        fig = px.bar(top_5_roas, x='roas', y='name', orientation='h', title="Top 5 Influencers by ROAS", text_auto='.2f', color='name')
        fig.update_layout(yaxis_title="Influencer", xaxis_title="ROAS", showlegend=False)
        st.plotly_chart(fig, use_container_width=True)


with tab2:
    st.header("Influencer Deep Dive")
    if final_influencers_df.empty:
        st.warning("No influencers match the current filter criteria.")
    else:
        influencer_list = final_influencers_df['name'].tolist()
        selected_influencer_name = st.selectbox("Select an Influencer", options=influencer_list)
        
        influencer_id = final_influencers_df[final_influencers_df['name'] == selected_influencer_name]['id'].iloc[0]
        
        # Get influencer details
        inf_details = influencers_df[influencers_df['id'] == influencer_id].iloc[0]
        inf_posts = final_posts_df[final_posts_df['influencer_id'] == influencer_id]
        inf_tracking = filtered_tracking_df[filtered_tracking_df['influencer_id'] == influencer_id]
        inf_payout = final_payouts_df[final_payouts_df['influencer_id'] == influencer_id].iloc[0]

        inf_revenue = inf_tracking['revenue'].sum()
        inf_roas = inf_revenue / inf_payout['total_payout'] if inf_payout['total_payout'] > 0 else 0
        
        # Display KPIs for the selected influencer
        st.subheader(f"Performance for {selected_influencer_name}")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Followers", f"{inf_details['follower_count']:,}")
        col2.metric("Total Revenue Generated", f"₹{inf_revenue:,.0f}")
        col3.metric("Total Payout", f"₹{inf_payout['total_payout']:,.0f}")
        col4.metric("ROAS", f"{inf_roas:.2f}")

        # Display posts and tracking data in tables
        st.subheader("Attributed Orders")
        st.dataframe(inf_tracking[['date', 'campaign', 'product', 'revenue']].sort_values('date', ascending=False))
        st.download_button(
            label="📥 Download Orders as CSV",
            data=to_csv(inf_tracking),
            file_name=f"{selected_influencer_name}_orders.csv",
            mime='text/csv',
        )

        st.subheader("Campaign Posts")
        st.dataframe(inf_posts[['date', 'platform', 'reach', 'likes', 'comments', 'url']].sort_values('date', ascending=False))


with tab3:
    st.header("Payouts Tracker")
    st.markdown("This table shows the payout details for all influencers matching the current filters.")
    
    if final_payouts_df.empty:
        st.warning("No payout data available for the selected filters.")
    else:
        payouts_display_df = final_payouts_df.merge(final_influencers_df[['id', 'name', 'platform']], left_on='influencer_id', right_on='id')
        payouts_display_df = payouts_display_df[['name', 'platform', 'basis', 'rate', 'orders', 'total_payout']]
        st.dataframe(payouts_display_df)

        st.download_button(
            label="Download Payouts as CSV",
            data=to_csv(payouts_display_df),
            file_name="payout_data.csv",
            mime='text/csv',
        )
 