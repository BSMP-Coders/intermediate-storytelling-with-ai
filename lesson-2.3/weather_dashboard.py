import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="Washington DC Weather Analysis Dashboard",
    page_icon="🌤️",
    layout="wide"
)

@st.cache_data
def load_weather_data(filename):
    """Load and clean the weather data from CSV file."""
    try:
        # Read the CSV file, skipping the first row (unit headers) and using the second row as column names
        df = pd.read_csv(filename, skiprows=1)
        
        # Convert the Date column to datetime
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Clean column names (remove units and spaces)
        df.columns = df.columns.str.strip()
        
        # Add month information
        df['Month'] = df['Date'].dt.month
        df['Month_Name'] = df['Date'].dt.strftime('%B')
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

def display_dataset_overview(df):
    """Display basic dataset information."""
    st.header("📊 Dataset Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Records", len(df))
    
    with col2:
        st.metric("Date Range", f"{df['Date'].min().strftime('%Y-%m-%d')} to {df['Date'].max().strftime('%Y-%m-%d')}")
    
    with col3:
        st.metric("Number of Columns", len(df.columns))
    
    with col4:
        rainy_days = len(df[df['precipitationTotal'] > 0])
        st.metric("Rainy Days", f"{rainy_days} ({rainy_days/len(df)*100:.1f}%)")
    
    # Show raw data with pagination
    st.subheader("📋 Raw Data")
    
    # Add filters for the data
    col1, col2 = st.columns(2)
    
    with col1:
        month_filter = st.multiselect(
            "Filter by Month:",
            options=df['Month_Name'].unique(),
            default=df['Month_Name'].unique()
        )
    
    with col2:
        temp_range = st.slider(
            "Temperature Range (°F):",
            min_value=int(df['tMin'].min()),
            max_value=int(df['tMax'].max()),
            value=(int(df['tMin'].min()), int(df['tMax'].max()))
        )
    
    # Filter the data
    filtered_df = df[
        (df['Month_Name'].isin(month_filter)) &
        (df['tAvg'] >= temp_range[0]) &
        (df['tAvg'] <= temp_range[1])
    ]
    
    st.dataframe(
        filtered_df[['Date', 'tMax', 'tAvg', 'tMin', 'hAvg', 'wAvg', 'precipitationTotal']],
        use_container_width=True,
        height=400
    )

def display_summary_statistics(df):
    """Display comprehensive summary statistics."""
    st.header("📈 Summary Statistics")
    
    # Temperature Statistics
    st.subheader("🌡️ Temperature Statistics")
    temp_col1, temp_col2, temp_col3 = st.columns(3)
    
    with temp_col1:
        st.metric(
            "Average Temperature",
            f"{df['tAvg'].mean():.1f}°F",
            f"Range: {df['tAvg'].min():.1f}°F - {df['tAvg'].max():.1f}°F"
        )
    
    with temp_col2:
        hottest_day = df.loc[df['tMax'].idxmax()]
        st.metric(
            "Highest Temperature",
            f"{df['tMax'].max():.1f}°F",
            f"on {hottest_day['Date'].strftime('%B %d, %Y')}"
        )
    
    with temp_col3:
        coldest_day = df.loc[df['tMin'].idxmin()]
        st.metric(
            "Lowest Temperature",
            f"{df['tMin'].min():.1f}°F",
            f"on {coldest_day['Date'].strftime('%B %d, %Y')}"
        )
    
    # Humidity Statistics
    st.subheader("💧 Humidity Statistics")
    humidity_col1, humidity_col2, humidity_col3 = st.columns(3)
    
    with humidity_col1:
        st.metric(
            "Average Humidity",
            f"{df['hAvg'].mean():.1f}%",
            f"Std: {df['hAvg'].std():.1f}%"
        )
    
    with humidity_col2:
        st.metric(
            "Highest Humidity",
            f"{df['hMax'].max():.1f}%"
        )
    
    with humidity_col3:
        st.metric(
            "Lowest Humidity",
            f"{df['hMin'].min():.1f}%"
        )
    
    # Wind Statistics
    st.subheader("💨 Wind Statistics")
    wind_col1, wind_col2, wind_col3 = st.columns(3)
    
    with wind_col1:
        st.metric(
            "Average Wind Speed",
            f"{df['wAvg'].mean():.1f} mph",
            f"Std: {df['wAvg'].std():.1f} mph"
        )
    
    with wind_col2:
        st.metric(
            "Maximum Wind Speed",
            f"{df['wMax'].max():.1f} mph"
        )
    
    with wind_col3:
        st.metric(
            "Minimum Wind Speed",
            f"{df['wMin'].min():.1f} mph"
        )
    
    # Precipitation Statistics
    st.subheader("🌧️ Precipitation Statistics")
    precip_col1, precip_col2, precip_col3 = st.columns(3)
    
    with precip_col1:
        total_precipitation = df['precipitationTotal'].sum()
        st.metric(
            "Total Precipitation",
            f"{total_precipitation:.2f} inches"
        )
    
    with precip_col2:
        rainy_days = len(df[df['precipitationTotal'] > 0])
        st.metric(
            "Rainy Days",
            f"{rainy_days} days",
            f"{rainy_days/len(df)*100:.1f}% of total days"
        )
    
    with precip_col3:
        if rainy_days > 0:
            avg_rain = df[df['precipitationTotal'] > 0]['precipitationTotal'].mean()
            st.metric(
                "Avg Rain per Rainy Day",
                f"{avg_rain:.2f} inches"
            )

def display_monthly_analysis(df):
    """Display monthly weather analysis."""
    st.header("📅 Monthly Analysis")
    
    # Monthly statistics table
    monthly_stats = df.groupby('Month_Name').agg({
        'tAvg': ['mean', 'min', 'max'],
        'hAvg': 'mean',
        'wAvg': 'mean',
        'precipitationTotal': 'sum'
    }).round(1)
    
    # Flatten column names
    monthly_stats.columns = ['_'.join(col).strip() for col in monthly_stats.columns.values]
    monthly_stats = monthly_stats.rename(columns={
        'tAvg_mean': 'Avg Temp (°F)',
        'tAvg_min': 'Min Temp (°F)',
        'tAvg_max': 'Max Temp (°F)',
        'hAvg_mean': 'Avg Humidity (%)',
        'wAvg_mean': 'Avg Wind Speed (mph)',
        'precipitationTotal_sum': 'Total Precipitation (in)'
    })
    
    st.subheader("📊 Monthly Summary Table")
    st.dataframe(monthly_stats, use_container_width=True)
    
    # Monthly charts
    st.subheader("📈 Monthly Trends")
    
    # Create tabs for different charts
    tab1, tab2, tab3, tab4 = st.tabs(["Temperature", "Humidity", "Wind Speed", "Precipitation"])
    
    with tab1:
        monthly_temp = df.groupby('Month_Name')['tAvg'].mean().reset_index()
        fig = px.bar(monthly_temp, x='Month_Name', y='tAvg', 
                     title='Average Monthly Temperature',
                     labels={'tAvg': 'Temperature (°F)', 'Month_Name': 'Month'})
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        monthly_humidity = df.groupby('Month_Name')['hAvg'].mean().reset_index()
        fig = px.bar(monthly_humidity, x='Month_Name', y='hAvg', 
                     title='Average Monthly Humidity',
                     labels={'hAvg': 'Humidity (%)', 'Month_Name': 'Month'})
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        monthly_wind = df.groupby('Month_Name')['wAvg'].mean().reset_index()
        fig = px.bar(monthly_wind, x='Month_Name', y='wAvg', 
                     title='Average Monthly Wind Speed',
                     labels={'wAvg': 'Wind Speed (mph)', 'Month_Name': 'Month'})
        st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        monthly_precipitation = df.groupby('Month_Name')['precipitationTotal'].sum().reset_index()
        fig = px.bar(monthly_precipitation, x='Month_Name', y='precipitationTotal', 
                     title='Total Monthly Precipitation',
                     labels={'precipitationTotal': 'Precipitation (inches)', 'Month_Name': 'Month'})
        st.plotly_chart(fig, use_container_width=True)

def display_interactive_charts(df):
    """Display interactive charts and visualizations."""
    st.header("📊 Interactive Visualizations")
    
    # Temperature trends over time
    st.subheader("🌡️ Temperature Trends Over Time")
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(x=df['Date'], y=df['tMax'], mode='lines', name='Max Temperature', line=dict(color='red')))
    fig.add_trace(go.Scatter(x=df['Date'], y=df['tAvg'], mode='lines', name='Avg Temperature', line=dict(color='orange')))
    fig.add_trace(go.Scatter(x=df['Date'], y=df['tMin'], mode='lines', name='Min Temperature', line=dict(color='blue')))
    
    fig.update_layout(
        title='Temperature Trends Over Time',
        xaxis_title='Date',
        yaxis_title='Temperature (°F)',
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Humidity vs Temperature scatter plot
    st.subheader("💧 Humidity vs Temperature Relationship")
    fig = px.scatter(df, x='tAvg', y='hAvg', color='precipitationTotal',
                     title='Humidity vs Temperature (colored by precipitation)',
                     labels={'tAvg': 'Average Temperature (°F)', 'hAvg': 'Average Humidity (%)', 'precipitationTotal': 'Precipitation (in)'})
    st.plotly_chart(fig, use_container_width=True)
    
    # Wind speed distribution
    st.subheader("💨 Wind Speed Distribution")
    fig = px.histogram(df, x='wAvg', nbins=20, title='Wind Speed Distribution',
                       labels={'wAvg': 'Average Wind Speed (mph)'})
    st.plotly_chart(fig, use_container_width=True)
    
    # Daily precipitation
    st.subheader("🌧️ Daily Precipitation")
    fig = px.bar(df, x='Date', y='precipitationTotal', title='Daily Precipitation',
                 labels={'precipitationTotal': 'Precipitation (inches)'})
    st.plotly_chart(fig, use_container_width=True)

def display_extreme_weather_events(df):
    """Display extreme weather events and patterns."""
    st.header("⚡ Extreme Weather Events")
    
    # Create columns for different extreme events
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔥 Hottest Days")
        hottest_days = df.nlargest(5, 'tMax')[['Date', 'tMax', 'hAvg', 'precipitationTotal']]
        hottest_days['Date'] = hottest_days['Date'].dt.strftime('%Y-%m-%d')
        st.dataframe(hottest_days, use_container_width=True, hide_index=True)
        
        st.subheader("💨 Windiest Days")
        windiest_days = df.nlargest(5, 'wMax')[['Date', 'wMax', 'tAvg', 'precipitationTotal']]
        windiest_days['Date'] = windiest_days['Date'].dt.strftime('%Y-%m-%d')
        st.dataframe(windiest_days, use_container_width=True, hide_index=True)
    
    with col2:
        st.subheader("🥶 Coldest Days")
        coldest_days = df.nsmallest(5, 'tMin')[['Date', 'tMin', 'hAvg', 'precipitationTotal']]
        coldest_days['Date'] = coldest_days['Date'].dt.strftime('%Y-%m-%d')
        st.dataframe(coldest_days, use_container_width=True, hide_index=True)
        
        st.subheader("🌧️ Rainiest Days")
        rainiest_days = df.nlargest(5, 'precipitationTotal')[['Date', 'precipitationTotal', 'tAvg', 'hAvg']]
        rainiest_days['Date'] = rainiest_days['Date'].dt.strftime('%Y-%m-%d')
        st.dataframe(rainiest_days, use_container_width=True, hide_index=True)

def display_correlations(df):
    """Display weather correlations and patterns."""
    st.header("🔗 Weather Correlations")
    
    # Calculate correlations
    temp_humidity_corr = df['tAvg'].corr(df['hAvg'])
    wind_precip_corr = df['wAvg'].corr(df['precipitationTotal'])
    temp_precip_corr = df['tAvg'].corr(df['precipitationTotal'])
    
    # Display correlation metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Temperature-Humidity Correlation", f"{temp_humidity_corr:.3f}")
    
    with col2:
        st.metric("Wind-Precipitation Correlation", f"{wind_precip_corr:.3f}")
    
    with col3:
        st.metric("Temperature-Precipitation Correlation", f"{temp_precip_corr:.3f}")
    
    # Correlation heatmap
    st.subheader("📊 Correlation Heatmap")
    correlation_data = df[['tAvg', 'hAvg', 'wAvg', 'precipitationTotal']].corr()
    
    fig = px.imshow(correlation_data, 
                    labels=dict(x="Variables", y="Variables", color="Correlation"),
                    title="Weather Variables Correlation Matrix")
    st.plotly_chart(fig, use_container_width=True)

def main():
    """Main Streamlit application."""
    st.title("🌤️ Washington DC Weather Analysis Dashboard")
    st.markdown("### Interactive Weather Data Analysis for 2025")
    
    # Load data
    df = load_weather_data('washington_dc_weather_sample_2025.csv')
    
    if df is not None:
        # Sidebar for navigation
        st.sidebar.title("Navigation")
        page = st.sidebar.selectbox(
            "Choose a section:",
            ["Dataset Overview", "Summary Statistics", "Monthly Analysis", 
             "Interactive Charts", "Extreme Weather", "Correlations"]
        )
        
        # Display selected page
        if page == "Dataset Overview":
            display_dataset_overview(df)
        elif page == "Summary Statistics":
            display_summary_statistics(df)
        elif page == "Monthly Analysis":
            display_monthly_analysis(df)
        elif page == "Interactive Charts":
            display_interactive_charts(df)
        elif page == "Extreme Weather":
            display_extreme_weather_events(df)
        elif page == "Correlations":
            display_correlations(df)
        
        # Add some additional info in the sidebar
        st.sidebar.markdown("---")
        st.sidebar.markdown("### Data Information")
        st.sidebar.info(f"📅 **Date Range:** {df['Date'].min().strftime('%B %d, %Y')} to {df['Date'].max().strftime('%B %d, %Y')}")
        st.sidebar.info(f"📊 **Total Records:** {len(df)}")
        st.sidebar.info(f"🌧️ **Rainy Days:** {len(df[df['precipitationTotal'] > 0])}")
        
    else:
        st.error("Failed to load weather data. Please check the file path and format.")

if __name__ == "__main__":
    main()
