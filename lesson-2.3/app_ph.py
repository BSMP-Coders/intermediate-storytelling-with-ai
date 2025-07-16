import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime

# Set up matplotlib for better plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def load_weather_data(filename):
    """Load and clean the weather data from CSV file."""
    try:
        # Read the CSV file, skipping the first row (unit headers) and using the second row as column names
        df = pd.read_csv(filename, skiprows=1)
        
        # Convert the Date column to datetime
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Clean column names (remove units and spaces)
        df.columns = df.columns.str.strip()
        
        print(f"Successfully loaded {len(df)} records from {filename}")
        print(f"Columns: {list(df.columns)}")
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def analyze_weather_data(df):
    """Perform basic analysis on the weather data."""
    print("\n=== WEATHER DATA ANALYSIS ===")
    print(f"Data range: {df['Date'].min()} to {df['Date'].max()}")
    print(f"Total days: {len(df)}")
    
    # Basic statistics for key metrics
    print("\n=== TEMPERATURE STATISTICS ===")
    print(f"Average temperature: {df['tAvg'].mean():.1f}°F")
    print(f"Highest temperature: {df['tMax'].max():.1f}°F on {df.loc[df['tMax'].idxmax(), 'Date'].strftime('%B %d, %Y')}")
    print(f"Lowest temperature: {df['tMin'].min():.1f}°F on {df.loc[df['tMin'].idxmin(), 'Date'].strftime('%B %d, %Y')}")
    
    print("\n=== HUMIDITY STATISTICS ===")
    print(f"Average humidity: {df['hAvg'].mean():.1f}%")
    print(f"Highest humidity: {df['hMax'].max():.1f}%")
    print(f"Lowest humidity: {df['hMin'].min():.1f}%")
    
    print("\n=== WIND STATISTICS ===")
    print(f"Average wind speed: {df['wAvg'].mean():.1f} mph")
    print(f"Maximum wind speed: {df['wMax'].max():.1f} mph")
    
    print("\n=== PRECIPITATION STATISTICS ===")
    total_precipitation = df['precipitationTotal'].sum()
    rainy_days = len(df[df['precipitationTotal'] > 0])
    print(f"Total precipitation: {total_precipitation:.2f} inches")
    print(f"Rainy days: {rainy_days} out of {len(df)} days ({rainy_days/len(df)*100:.1f}%)")
    
    if rainy_days > 0:
        avg_rain_per_rainy_day = df[df['precipitationTotal'] > 0]['precipitationTotal'].mean()
        print(f"Average rainfall on rainy days: {avg_rain_per_rainy_day:.2f} inches")

def create_visualizations(df):
    """Create visualizations for the weather data."""
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Washington DC Weather Analysis 2025', fontsize=16, fontweight='bold')
    
    # 1. Temperature trends over time
    axes[0, 0].plot(df['Date'], df['tMax'], label='Max Temp', alpha=0.7, color='red')
    axes[0, 0].plot(df['Date'], df['tAvg'], label='Avg Temp', alpha=0.7, color='orange')
    axes[0, 0].plot(df['Date'], df['tMin'], label='Min Temp', alpha=0.7, color='blue')
    axes[0, 0].set_title('Temperature Trends Over Time')
    axes[0, 0].set_ylabel('Temperature (°F)')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # 2. Humidity vs Temperature scatter plot
    scatter = axes[0, 1].scatter(df['tAvg'], df['hAvg'], c=df['precipitationTotal'], 
                                cmap='Blues', alpha=0.6, s=50)
    axes[0, 1].set_title('Humidity vs Temperature')
    axes[0, 1].set_xlabel('Average Temperature (°F)')
    axes[0, 1].set_ylabel('Average Humidity (%)')
    plt.colorbar(scatter, ax=axes[0, 1], label='Precipitation (in)')
    
    # 3. Wind speed distribution
    axes[1, 0].hist(df['wAvg'], bins=20, alpha=0.7, color='green', edgecolor='black')
    axes[1, 0].set_title('Wind Speed Distribution')
    axes[1, 0].set_xlabel('Average Wind Speed (mph)')
    axes[1, 0].set_ylabel('Frequency')
    axes[1, 0].grid(True, alpha=0.3)
    
    # 4. Precipitation over time
    axes[1, 1].bar(df['Date'], df['precipitationTotal'], alpha=0.7, color='blue')
    axes[1, 1].set_title('Daily Precipitation')
    axes[1, 1].set_ylabel('Precipitation (inches)')
    axes[1, 1].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.show()

def monthly_analysis(df):
    """Analyze weather patterns by month."""
    df['Month'] = df['Date'].dt.month
    df['Month_Name'] = df['Date'].dt.strftime('%B')
    
    monthly_stats = df.groupby('Month_Name').agg({
        'tAvg': ['mean', 'min', 'max'],
        'hAvg': 'mean',
        'wAvg': 'mean',
        'precipitationTotal': 'sum'
    }).round(1)
    
    print("\n=== MONTHLY WEATHER SUMMARY ===")
    print(monthly_stats)
    
    # Monthly temperature comparison
    plt.figure(figsize=(12, 8))
    
    plt.subplot(2, 2, 1)
    monthly_temp = df.groupby('Month_Name')['tAvg'].mean()
    plt.bar(monthly_temp.index, monthly_temp.values, color='orange', alpha=0.7)
    plt.title('Average Monthly Temperature')
    plt.ylabel('Temperature (°F)')
    plt.xticks(rotation=45)
    
    plt.subplot(2, 2, 2)
    monthly_humidity = df.groupby('Month_Name')['hAvg'].mean()
    plt.bar(monthly_humidity.index, monthly_humidity.values, color='blue', alpha=0.7)
    plt.title('Average Monthly Humidity')
    plt.ylabel('Humidity (%)')
    plt.xticks(rotation=45)
    
    plt.subplot(2, 2, 3)
    monthly_wind = df.groupby('Month_Name')['wAvg'].mean()
    plt.bar(monthly_wind.index, monthly_wind.values, color='green', alpha=0.7)
    plt.title('Average Monthly Wind Speed')
    plt.ylabel('Wind Speed (mph)')
    plt.xticks(rotation=45)
    
    plt.subplot(2, 2, 4)
    monthly_precipitation = df.groupby('Month_Name')['precipitationTotal'].sum()
    plt.bar(monthly_precipitation.index, monthly_precipitation.values, color='purple', alpha=0.7)
    plt.title('Total Monthly Precipitation')
    plt.ylabel('Precipitation (inches)')
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.show()

def find_weather_patterns(df):
    """Find interesting weather patterns and correlations."""
    print("\n=== WEATHER PATTERNS & CORRELATIONS ===")
    
    # Temperature-humidity correlation
    temp_humidity_corr = df['tAvg'].corr(df['hAvg'])
    print(f"Temperature-Humidity correlation: {temp_humidity_corr:.3f}")
    
    # Wind speed and precipitation correlation
    wind_precip_corr = df['wAvg'].corr(df['precipitationTotal'])
    print(f"Wind Speed-Precipitation correlation: {wind_precip_corr:.3f}")
    
    # Find extreme weather days
    print("\n=== EXTREME WEATHER DAYS ===")
    
    # Hottest days
    hottest_days = df.nlargest(5, 'tMax')[['Date', 'tMax', 'hAvg', 'precipitationTotal']]
    print("Hottest 5 days:")
    print(hottest_days.to_string(index=False))
    
    # Coldest days
    coldest_days = df.nsmallest(5, 'tMin')[['Date', 'tMin', 'hAvg', 'precipitationTotal']]
    print("\nColdest 5 days:")
    print(coldest_days.to_string(index=False))
    
    # Windiest days
    windiest_days = df.nlargest(5, 'wMax')[['Date', 'wMax', 'tAvg', 'precipitationTotal']]
    print("\nWindiest 5 days:")
    print(windiest_days.to_string(index=False))
    
    # Rainiest days
    rainiest_days = df.nlargest(5, 'precipitationTotal')[['Date', 'precipitationTotal', 'tAvg', 'hAvg']]
    print("\nRainiest 5 days:")
    print(rainiest_days.to_string(index=False))

def main():
    """Main function to run the weather analysis."""
    # Load the weather data
    df = load_weather_data('washington_dc_weather_sample_2025.csv')
    
    if df is not None:
        # Display basic info about the dataset
        print("\n=== DATASET OVERVIEW ===")
        print(f"Columns: {list(df.columns)}")
        print(f"Shape: {df.shape}")
        print(f"Data types:")
        print(df.dtypes)
        
        # Perform analysis
        analyze_weather_data(df)
        
        # Create visualizations
        create_visualizations(df)
        
        # Monthly analysis
        monthly_analysis(df)
        
        # Find patterns
        find_weather_patterns(df)
        
        print("\n=== ANALYSIS COMPLETE ===")
        print("Weather data has been successfully loaded and analyzed!")
        print("Check the generated plots for visual insights.")
    else:
        print("Failed to load weather data. Please check the file path and format.")

if __name__ == "__main__":
    main()

