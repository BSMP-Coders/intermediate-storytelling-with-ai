# 🧪 Activity 1: Let's start to read the data

1. Open `app.py` and use GitHub Copilot to generate initial code by entering (try with Ctrl-I to open chat pallete vs. chat): 

```
i have weather data in a csv, can you load it for me and help me analyze
```

2. Review the generated code, review the output, notice the first two rows are header data, skip the first row by updating the read as needed, note the column names.  

# 🧪 Activity 2: Review/Clean the Raw Data

Before using the CSV, students can practice:
1. Inspecting the raw file, Notice the Date is not of type date, it looks like a generic number

```
Date column should be converted to datetime
Date column should be converted to datetime careful with the format
```

2. Any missing or malformed data
```
check for missing values
```

3. Renaming columns for clarity
```
rename the tMax column to Temperature Max
do the same for tMin, tAvg, tMax, pressureAvg, pressureMin, precipitationTotal
```

4. Drop data that is not needed for analysis
```
delete dewMax, dewMin, dewAvg columns
```

5. Saving the cleaned version as a CSV
```
Save the cleaned DataFrame to a new CSV file
```

# 🧪 Activity 3: Visualize the updated data
1. Display raw data
```
display raw data using streamlit library, allowing users to scroll through the data 
```

2. What are temperature highs and lows by month
```
how would i show the hottest and coldest days by month
```

3. Draw a line chart comparing the 3 temperatures
```
generate a line chart with a line for Min Temperature, Max Temperature, and Avg Temperature
```

4. Draw a line chart comparing the wind

```
generate a line chart with a line for Min Wind, Max Wind, and Avg Wind
```

5. Any other graphs? 

```
what graphs do you suggest for this data to show trends or make predications
```

6. Select and implement one of the methods suggested, will the graph make sense to your users?discuss usefulness (e.g. correlation one)

# 🧪 Activity 4: Reflect - Are there other data sets or domains you'd be interested in to analyze?

# 🧪 Activity 5: Review learn module homework (uses jupyter notebooks)
