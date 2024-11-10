# 📊 EDA on Body Composition and Workout Routines for Gym Members

## 📝 Project Overview
This project conducts an **Exploratory Data Analysis (EDA)** on gym members' body composition metrics and workout routines to gain insights on optimizing fitness. The goal is to understand the relationships between body composition (BMI, fat percentage) and workout factors (frequency, session duration, calories burned) to provide actionable recommendations for improving physical fitness.

## 📁 Datasets Used
1. **Gym Members Exercise Dataset**:
   - Source: [Kaggle Gym Dataset](https://www.kaggle.com/datasets/valakhorasani/gym-members-exercise-dataset)
   - Total Records: 973
   - Features: Age, Gender, Weight, Height, BMI, Fat Percentage, Workout Frequency, Session Duration, Calories Burned, Workout Type, and Experience Level.

2. **Personal Body Composition Data**:
   - Source: [Garmin Index S2 Scale](https://connect.garmin.com/modern/weight)
   - Total Records: 278
   - Features: Time, Weight, BMI, Fat Percentage, Muscle Mass, Bone Mass, and Body Water.

## 🛠️ EDA Process
### 1. **Data Cleaning**
- Removed unrealistic records based on:
  - **Fat Percentage**: Removed entries below 3% or above 50%.
  - **Weight**: Removed entries below 30 kg or above 200 kg.
  - **Height**: Removed entries below 1.2 m or above 2.5 m.
- Detected and eliminated incongruent records:
  - **Underweight** with **High Fat Percentage**.
  - **Obesity** with **Low Fat Percentage**.

### 2. **Feature Engineering**
- Created new columns for **BMI Status** and **Fat Status** based on standard health guidelines.
- Estimated **Muscle Mass Percentage** using lean body mass and adjusted for gender, age, and experience level.
- Calculated **Basal Metabolic Rate (BMR)** using the Harris-Benedict equation.

### 3. **Data Analysis**
- Conducted descriptive statistics to understand distributions and averages of key metrics.
- Performed **correlation analysis** to find relationships between session duration, calories burned, BMI, and fat percentage.
- Created visualizations:
  - **Histograms**: Showed distributions of Age, BMI, and Fat Percentage.
  - **Bar Charts**: Displayed counts of different BMI and Fat Status categories.
  - **Scatter Plots**: Analyzed session duration vs. calories burned.
  - **Heatmap**: Visualized correlations between features.

### 4. **Interpretation and Insights**
- Added an **Interpretation** column to classify body composition:
  - High BMI with low fat percentage labeled as **High Muscle Mass**.
  - Normal weight with high fat percentage labeled as **Consider Reducing Fat**.
  - Underweight with low fat percentage labeled as **Gain Muscle Mass**.
- Created a **Workout Advisor** column:
  - Suggested increasing workout frequency for members with high fat percentage and less than 4 workouts per week.
  - Recommended higher intensity workouts for members burning fewer than 915 calories per session.

### 5. **Key Findings**
- High BMI is often associated with lower workout frequency.
- Members with higher fat percentages tend to work out fewer days per week.
- A positive correlation exists between session duration and calories burned.

## 📈 Visualizations
1. **Distribution of BMI and Fat Percentage**: Shows the spread of body composition metrics.
2. **Bar Plot of Interpretations**: Displays the count of each body composition interpretation category.
3. **Correlation Heatmap**: Highlights the relationships between features like session duration, calories burned, and body composition metrics.

## 🚧 Limitations
- The analysis may be limited by the relatively small sample size.
- The absence of key health metrics like muscle mass, blood pressure, and waist measurements may impact the conclusions.
- The dataset could be biased towards more advanced gym members who track their workouts diligently.

## 💡 Recommendations
- Increase workout frequency for members with high body fat percentages.
- Recommend higher intensity workouts for members with lower calorie expenditure per session.
- Collect more comprehensive health data (e.g., waist measurements, blood pressure) for future analysis.

## 📋 Tools Used
- **Python** for data analysis and cleaning.
- **Pandas** for data manipulation.
- **Matplotlib** and **Seaborn** for visualizations.
- **Jupyter Notebook** for documenting the EDA process.

## 📜 How to Use
1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd eda-gym-analysis



