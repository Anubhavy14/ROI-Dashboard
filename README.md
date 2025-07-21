# Healthkart 
HealthKart Influencer ROI Dashboard
<img width="1911" height="918" alt="Screenshot 2025-07-21 111409" src="https://github.com/user-attachments/assets/1395dca5-4677-4629-8e64-49db53daacba" />


An interactive web application built with Python and Streamlit to track, analyze, and visualize the performance and ROI of HealthKart's influencer marketing campaigns.

Overview
This dashboard provides a centralized platform to measure the effectiveness of influencer collaborations across various brands (MuscleBlaze, HKVitals, Gritzo) and social media platforms. It allows marketing teams to move beyond simple engagement metrics and focus on tangible business outcomes like revenue and Return on Ad Spend (ROAS).

The application uses simulated data to demonstrate its full functionality out-of-the-box.

Features
Campaign Performance KPIs: At-a-glance metrics for Total Revenue, Total Payouts, Overall ROAS, and Incremental ROAS.

Interactive Visualizations: Bar charts, pie charts, and tables to visualize revenue by platform, influencer category, and top performers.

Influencer Deep Dive: Select individual influencers to analyze their specific performance, attributed orders, and campaign posts.

Payouts Tracker: A clear, filterable table showing payout details for each influencer, including their payment basis (per-post or per-order).

Advanced Filtering: Dynamically filter the entire dashboard by date range, brand, platform, and influencer category.

Data Export: Download filtered datasets for orders and payouts as CSV files for offline analysis.

Tech Stack
Language: Python

Framework: Streamlit (for the web app interface)

Data Manipulation: Pandas

Data Visualization: Plotly Express

Data Simulation: Faker

Setup and Installation
To run this dashboard on your local machine, follow these steps:

1. Clone the Repository

git clone [https://github.com/your-username/healthkart-dashboard.git](https://github.com/your-username/healthkart-dashboard.git)
cd healthkart-dashboard

2. Create and Activate a Virtual Environment (Recommended)

macOS/Linux:

python3 -m venv venv
source venv/bin/activate

Windows:

python -m venv venv
.\venv\Scripts\activate

3. Install Dependencies
Create a file named requirements.txt and add the following lines:

streamlit
pandas
numpy
plotly
Faker

Then, install the libraries from this file:

pip install -r requirements.txt

4. Run the Streamlit App
Once the dependencies are installed, run the following command in your terminal:

streamlit run app.py

The application should automatically open in a new tab in your web browser.

Data Model
The dashboard simulates four core datasets to function:

influencers: Contains details about each influencer (ID, name, category, followers, platform).

posts: Logs every post made by an influencer (ID, platform, date, engagement metrics).

tracking_data: Records every order attributed to an influencer via tracking links (campaign, brand, product, revenue).

payouts: Details the payment structure and total payout for each influencer (basis, rate, total amount).

Key Assumptions
Incremental ROAS Calculation: The dashboard calculates Incremental ROAS based on a key assumption:

A baseline of 35% of the revenue attributed to an influencer would have been generated organically without the campaign.

Incremental Revenue = Total Revenue * (1 - 0.35)

This multiplier is a placeholder and should be adjusted based on historical data or marketing mix models for a more accurate calculation.

Contributing
Contributions are welcome! If you have ideas for new features or improvements, feel free to fork the repository, make your changes, and submit a pull request.
