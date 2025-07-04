import pandas as pd

# Replace 'weather.csv' with your actual file path
df = pd.read_csv('./washington_dc_weather_sample_2025.csv',skiprows=1)

# Show the first few rows to inspect the data
print(df.head())

# Show basic info and statistics
print(df.info())
print(df.describe())

# Date column should be converted to datetime careful with the format
# Assuming the date format is MM/DD/YYYY
df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
print(df.head())
 
#check for missing values
print(df.isnull().sum())

#rename the tMax column yp Temperature Max
df.rename(columns={'tMax': 'Temperature Max'}, inplace=True)
df.rename(columns={'tMin': 'Temperature Min'}, inplace=True)
df.rename(columns={'tAvg': 'Temperature Avg'}, inplace=True)

df.rename(columns={'wMax': 'Wind Max'}, inplace=True)
df.rename(columns={'wMin': 'Wind Min'}, inplace=True)
df.rename(columns={'wAvg': 'Wind Avg'}, inplace=True)

df.rename(columns={'hMax': 'Humidity Max'}, inplace=True)
df.rename(columns={'hMin': 'Humidity Min'}, inplace=True)
df.rename(columns={'hAvg': 'Humidity Avg'}, inplace=True)

df.rename(columns={'pressureAvg': 'Pressure Max'}, inplace=True)
df.rename(columns={'pressureMin': 'Pressure Min'}, inplace=True)
df.rename(columns={'precipitationTotal': 'Total Precipitation'}, inplace=True)

#delete dewMax, dewMin, dewAvg columns
df.drop(columns=['dewMax', 'dewMin', 'dewAvg'], inplace=True)
print(df.head())

# Save the cleaned DataFrame to a new CSV file
df.to_csv('./cleaned_washington_dc_weather_sample_2025.csv', index=False)

# Visualize Min Temperature and Max Temperature and Max Temperature as a line chart
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# First plot - Temperature Trends
fig1, ax1 = plt.subplots(figsize=(14, 7))
sns.lineplot(data=df, x='Date', y='Temperature Min', label='Min Temperature', color='blue', ax=ax1)
sns.lineplot(data=df, x='Date', y='Temperature Max', label='Max Temperature', color='red', ax=ax1)
sns.lineplot(data=df, x='Date', y='Temperature Avg', label='Avg Temperature', color='green', ax=ax1)
ax1.set_title('Temperature Trends in Washington DC (2025)')
ax1.set_xlabel('Date')
ax1.set_ylabel('Temperature (°F)')
ax1.legend()
ax1.tick_params(axis='x', rotation=45)
plt.tight_layout()

# Second plot - Wind Speed Trends
fig2, ax2 = plt.subplots(figsize=(14, 7))
sns.lineplot(data=df, x='Date', y='Wind Min', label='Min Wind Speed', color='blue', ax=ax2)
sns.lineplot(data=df, x='Date', y='Wind Max', label='Max Wind Speed', color='red', ax=ax2)
sns.lineplot(data=df, x='Date', y='Wind Avg', label='Avg Wind Speed', color='green', ax=ax2)
ax2.set_title('Wind Speed Trends in Washington DC (2025)')
ax2.set_xlabel('Date')
ax2.set_ylabel('Wind Speed (mph)')
ax2.legend()
ax2.tick_params(axis='x', rotation=45)
plt.tight_layout()

st.title("Washington DC Weather Data Analysis (2025)")
st.write("### Raw Data Sample")
#st.dataframe(df, height=600, use_container_width=True)
st.write("Showing 25 records per page. Use the table controls below to page through the data.")
#st.dataframe(df, height=600, use_container_width=True, hide_index=True)
# For paging, use Streamlit's built-in pagination with st.dataframe, or implement custom paging:
page_size = 25
total_rows = len(df)
page_num = st.number_input("Page", min_value=1, max_value=(total_rows - 1) // page_size + 1, value=1)
start_idx = (page_num - 1) * page_size
end_idx = start_idx + page_size
st.dataframe(df.iloc[start_idx:end_idx], height=600, use_container_width=True)

st.write("### Temperature Trends")
st.pyplot(fig1)

st.write("### Wind Speed Trends")
st.pyplot(fig2) 

# 1. Correlation Heatmap - Shows relationships between all variables
st.write("### Correlation Heatmap")
fig5, ax5 = plt.subplots(figsize=(12, 8))
# Select only numeric columns for correlation
numeric_cols = ['Temperature Max', 'Temperature Min', 'Temperature Avg', 
                'Wind Max', 'Wind Min', 'Wind Avg', 
                'Humidity Max', 'Humidity Min', 'Humidity Avg',
                'Pressure Max', 'Pressure Min', 'Total Precipitation']
correlation_matrix = df[numeric_cols].corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, ax=ax5)
ax5.set_title('Weather Variables Correlation Matrix')
plt.tight_layout()
st.pyplot(fig5)

# Extract month from date for grouping
df['Month'] = df['Date'].dt.month
df['Month_Name'] = df['Date'].dt.strftime('%B')

# Find hottest and coldest days by month
st.write("### Hottest and Coldest Days by Month")

# Method 1: Summary table
monthly_extremes = df.groupby(['Month', 'Month_Name']).agg({
    'Temperature Max': ['max', 'idxmax'],
    'Temperature Min': ['min', 'idxmin'],
    'Date': 'first'  # Just to get month info
}).round(1)

# Flatten column names
monthly_extremes.columns = ['Max_Temp', 'Max_Temp_Idx', 'Min_Temp', 'Min_Temp_Idx', 'Month_Date']

# Create a clean summary table by month
summary_data = []
for month, month_name in monthly_extremes.index:
    row = monthly_extremes.loc[(month, month_name)]
    
    # Get the actual dates for hottest and coldest days
    hottest_date = df.loc[row['Max_Temp_Idx'], 'Date'].strftime('%B %d, %Y')
    coldest_date = df.loc[row['Min_Temp_Idx'], 'Date'].strftime('%B %d, %Y')
    
    summary_data.append({
        'Month': month_name,
        'Hottest Day': hottest_date,
        'Max Temperature (°F)': row['Max_Temp'],
        'Coldest Day': coldest_date,
        'Min Temperature (°F)': row['Min_Temp'],
        'Temperature Range (°F)': row['Max_Temp'] - row['Min_Temp']
    })

summary_df = pd.DataFrame(summary_data)
st.dataframe(summary_df, use_container_width=True)

st.write("### Scatterplot: Max Humidity vs Total Precipitation")
fig6, ax6 = plt.subplots(figsize=(10, 6))
sns.scatterplot(
    data=df,
    x='Humidity Max',
    y='Total Precipitation',
    ax=ax6,
    color='purple'
)
ax6.set_title('Max Humidity vs Total Precipitation')
ax6.set_xlabel('Max Humidity (%)')
ax6.set_ylabel('Total Precipitation (inches)')
plt.tight_layout()
st.pyplot(fig6)