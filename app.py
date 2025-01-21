import pandas as pd
import streamlit as st
import plotly.express as px

# App title
st.title("DHL SEA Campaign Analysis Dashboard")
st.markdown("**Confidential SEA Campaign Data Analysis**")

# File upload section
uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file:
    # Load data
    data = pd.read_csv(uploaded_file)
    st.write("### Uploaded Data Preview:")
    st.dataframe(data.head())

    # Ensure required columns exist
    required_columns = ['Market', 'Clicks', 'Impressions', 'Cost', 'Leads_Number', 'CTR']
    if all(col in data.columns for col in required_columns):
        # Calculate key metrics
        data['CTR'] = data['CTR'] * 100  # Convert CTR to percentage
        data['CPC'] = data['Cost'] / data['Clicks']
        data['Conversion_Rate'] = (data['Leads_Number'] / data['Clicks']) * 100
        data['CPL'] = data['Cost'] / data['Leads_Number']  # Cost Per Lead

        # Display calculated metrics
        st.write("#### Metrics Summary")
        metrics_summary = data.groupby('Market')[['CTR', 'CPC', 'Conversion_Rate', 'CPL']].mean().reset_index()
        st.dataframe(metrics_summary)

        # Visualizations with Plotly
        st.write("### Visualizations")

        # CTR Visualization
        st.write("#### Click-Through Rate (CTR) by Market")
        fig_ctr = px.bar(metrics_summary, x='Market', y='CTR', 
                         title="CTR by Market", 
                         labels={'CTR': 'CTR (%)', 'Market': 'Market'},
                         color='CTR', color_continuous_scale='Viridis')
        st.plotly_chart(fig_ctr, use_container_width=True)

        # CPC Visualization
        st.write("#### Cost Per Click (CPC) by Market")
        fig_cpc = px.bar(metrics_summary, x='Market', y='CPC', 
                         title="CPC by Market", 
                         labels={'CPC': 'CPC (Cost per Click)', 'Market': 'Market'},
                         color='CPC', color_continuous_scale='Magma')
        st.plotly_chart(fig_cpc, use_container_width=True)

        # CPL Visualization
        st.write("#### Cost Per Lead (CPL) by Market")
        fig_cpl = px.bar(metrics_summary, x='Market', y='CPL', 
                         title="CPL by Market", 
                         labels={'CPL': 'CPL (Cost per Lead)', 'Market': 'Market'},
                         color='CPL', color_continuous_scale='Plasma')
        st.plotly_chart(fig_cpl, use_container_width=True)

        # Budget Re-Allocation Suggestions
        st.write("### Budget Re-Allocation Suggestions")

        # Identify top and bottom performers
        top_performers = metrics_summary.sort_values(by='Conversion_Rate', ascending=False).head(3)
        bottom_performers = metrics_summary.sort_values(by='Conversion_Rate').head(3)

        # Display top performers
        st.write("#### Top Performing Markets Based on Conversion Rate")
        st.dataframe(top_performers)

        # Display bottom performers
        st.write("#### Underperforming Markets Based on Conversion Rate")
        st.dataframe(bottom_performers)

        # Budget recommendations
        st.markdown("**Budget Reallocation Proposal:**")
        st.markdown(
            """
            1. **Increase Budget For:**
               - Markets with **low CPL** and **high Conversion Rate** (e.g., {}).
               - Markets with **high CTR** and **low CPC** (e.g., {}).
            
            2. **Decrease Budget For:**
               - Markets with **high CPL** and **low Conversion Rate** (e.g., {}).
               - Markets with **low CTR** and **high CPC** (e.g., {}).
            
            3. **Monitor Continuously:**
               - Track performance monthly and adjust budgets dynamically.
            """.format(
                ', '.join(top_performers['Market'].tolist()),
                ', '.join(metrics_summary.sort_values(by='CTR', ascending=False).head(3)['Market'].tolist()),
                ', '.join(bottom_performers['Market'].tolist()),
                ', '.join(metrics_summary.sort_values(by='CTR').head(3)['Market'].tolist())
            )
        )

    else:
        st.error(f"Missing required columns in the uploaded file. Ensure the file contains: {', '.join(required_columns)}")
