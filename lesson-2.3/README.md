# DC Weather Analysis (Jan–Mar 2025)

This project guides students through analyzing real-world weather data from Washington, DC using Python and GitHub Copilot.

## 📁 Files Included

- `washington_dc_weather_sample_2025.csv`: Raw CSV/Excel file for optional data cleaning activity
- `README.md`: This guide
- `activities.md`: Instructions and exercises
- `app.py`: Empty program template to start with
- `app_final.py`: Final program sample

## 🧠 Learning Objectives

Students will:
- Learn data analysis fundamentals
- Load and explore weather data
- Clean and structure datasets
- Perform statistical analysis
- Visualize trends using seaborn and matplotlib Python libraries
- Use GitHub Copilot to assist with coding

## 📊 Data Source

Data was sourced/scraped from: https://www.wunderground.com/history/monthly/KJPN/date/2025-1

## 🚀 Getting Started

When diving into data analysis, there's a mental checklist seasoned analysts instinctively run through—like muscle memory. Here's a refined list of pro tips to sharpen your analysis and spot insights that others might miss:

### 🧹 1. Start with a Clean Sweep

**Understand the data values**: Is it Qualitative or Quantitative? 
- **Qualitative data**: Descriptive and often expressed in words
- **Quantitative data**: Numerical and can be divided into discrete and continuous subcategories

**Check for missing values**: Look for patterns—missing completely at random (MCAR) vs. not at random (MNAR) matters.

**Identify outliers**: Useful for deeper insight or flagging data quality issues.

**Verify data types**: Numeric stored as text? Dates misformatted? Catch these early.

**Deduplicate**: Remove or investigate duplicates that might skew results.


### 🧭 2. Understand the Data Context

- What was the original purpose of this data?
- How was it collected (survey, sensor, scraped, manual input)?
- Are there any known biases (sampling, confirmation, survivorship)?
- **Talk to stakeholders**: A 10-minute chat often unlocks insights buried in metadata


### 📈 3. Always Explore Before Modeling

- **Summary stats**: Mean, median, mode, std dev, ranges—start simple with basic statistics
- **Distributions**: Visualize histograms to see shape and skew
- **Correlations**: Use heatmaps, scatterplots—but watch for odd relationships


### 🎯 4. Focus on Relevance, Not Just Significance

- **Statistically significant vs. practically meaningful**: Avoid p-value obsession
- **Look for business impact**: Would this insight change a decision?


### 🧠 5. Don't Trust, Verify

- **Cross-validate results**: Sanity-check trends across different slices of data or sources
- **Baseline comparisons**: Use control groups or past periods to frame findings
- **Version control**: Track transformations to preserve reproducibility. Can anyone replicate your results?


### 🧩 6. Think in Stories, Not Just Stats

- **What's the narrative?** Why does this matter? So what?
- **Use visuals to support a point**—not just to decorate a dashboard
- **Research counterarguments** in your storytelling, pre-emptively to build credibility

## 🎯 Ready to Practice?

Let's do some activities to practice these skills with weather data exercises in [`activities.md`](./activities.md)

## 📊 Pro Tip for Analysts

When choosing a visualization chart, always start with the question you're answering:

- Are you comparing values?
- Showing change over time?
- Revealing relationships?
- Displaying distribution?
- Highlighting composition?

## 📓 Learn Modules 

Microsoft Learn has excellent resources for data analysis with Python:
- [Explore and analyze data with Python](https://learn.microsoft.com/en-us/training/modules/explore-analyze-data-with-python)

Jupyter Notebooks are a great way to learn Python and data analysis interactively. You can run code cells, visualize data, and document your analysis all in one place. Here is a video to get you started with Jupyter Notebooks in Visual Studio Code:
- [Getting started with Jupyter Notebooks in VS Code](https://learn.microsoft.com/en-us/shows/visual-studio-code/getting-started-with-jupyter-notebooks-in-vs-code)

## 📊 Other Data Sources

There is data galore to research and practice with. Here are a few great sources to explore or find others through Copilot:

- **[Data.gov](https://resources.data.gov)**: Directory of federal agency data hubs (e.g., NASA, CDC, DOJ) for deep dives into specific domains like health, energy, and justice
- **[Kaggle Datasets](https://www.kaggle.com/datasets)**: Thousands of datasets across domains like health, finance, sports, and more


## 📌 Other References
| Description | Link |
|-------------|------|
| Data literacy in 10 minutes | https://www.linkedin.com/pulse/data-literacy-10-minutes-buck-woody/ |
| Data visualization chart usages | https://ft-interactive.github.io/visual-vocabulary/ |
| Statistics Cheatsheet | https://web.mit.edu/~csvoss/Public/usabo/stats_handout.pdf |
| Pandas | https://pandas.pydata.org/docs/ |
| Seaborn | https://seaborn.pydata.org/ |
| Matplotlib | https://matplotlib.org/stable/contents.html |
| Streamlit | https://docs.streamlit.io/ |
| NumPy | https://numpy.org/doc/ |

