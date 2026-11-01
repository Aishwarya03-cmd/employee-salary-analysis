# ============================================================
# EMPLOYEE SALARY ANALYSIS
# Data cleaning, EDA and visualization using Python
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")


def section(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


# ------------------------------------------------------------
# 1. LOAD DATA
# ------------------------------------------------------------
df = pd.read_excel("EmployeeData.xlsx")

section("FIRST FIVE RECORDS")
print(df.head())

section("SHAPE OF THE DATASET")
print(df.shape)

section("DATASET INFO")
df.info()  # info() prints by itself, so no print() needed

section("MISSING VALUES (BEFORE CLEANING)")
print(df.isnull().sum())

# ------------------------------------------------------------
# 2. DATA CLEANING
# ------------------------------------------------------------
rows_start = df.shape[0]

# Step 1: remove duplicates FIRST so they don't skew the fill value
df = df.drop_duplicates()
print(f"\nDuplicates removed: {rows_start - df.shape[0]}")

# Step 2: make sure salary is numeric
# errors='coerce' turns non-numeric values (like 'N/A') into NaN
section("SALARY DATA TYPE (BEFORE)")
print(df["ANNUAL_SALARY"].dtype)
df["ANNUAL_SALARY"] = pd.to_numeric(df["ANNUAL_SALARY"], errors="coerce")

# Step 3: fill missing salaries with the MEDIAN
# Median is used instead of mean because salary data is usually
# right-skewed and a few high salaries would pull the mean up.
missing_salary = df["ANNUAL_SALARY"].isnull().sum()
df["ANNUAL_SALARY"] = df["ANNUAL_SALARY"].fillna(df["ANNUAL_SALARY"].median())
print(f"Missing salaries filled with median: {missing_salary}")

# Step 4: drop rows that still have missing values in other columns
rows_before_dropna = df.shape[0]
df = df.dropna()
print(f"Rows dropped for other missing values: {rows_before_dropna - df.shape[0]}")

section("SHAPE AFTER CLEANING")
print(df.shape)
print(f"Total rows removed: {rows_start - df.shape[0]}")

# Step 5: save to a NEW file so the original data stays safe
df.to_excel("EmployeeData_cleaned.xlsx", index=False)
print("\nCleaned data saved to EmployeeData_cleaned.xlsx")

# ------------------------------------------------------------
# 3. EXPLORATORY DATA ANALYSIS
# ------------------------------------------------------------
section("STATISTICAL SUMMARY OF SALARY")
print(df["ANNUAL_SALARY"].describe())

print("\nMean   :", round(df["ANNUAL_SALARY"].mean(), 2))
print("Median :", round(df["ANNUAL_SALARY"].median(), 2))
print("Min    :", df["ANNUAL_SALARY"].min())
print("Max    :", df["ANNUAL_SALARY"].max())
print("Std Dev:", round(df["ANNUAL_SALARY"].std(), 2))

section("DEPARTMENT-WISE AVERAGE SALARY")
dept_avg = df.groupby("DEPARTMENT")["ANNUAL_SALARY"].mean().sort_values(ascending=False)
print(dept_avg.round(2))

section("GENDER-WISE AVERAGE SALARY")
gender_avg = df.groupby("GENDER")["ANNUAL_SALARY"].mean()
print(gender_avg.round(2))

section("AVERAGE SALARY BY DEPARTMENT AND GENDER")
dept_gender = df.pivot_table(
    values="ANNUAL_SALARY", index="DEPARTMENT", columns="GENDER", aggfunc="mean"
)
print(dept_gender.round(2))

# ------------------------------------------------------------
# 4. OUTLIER DETECTION (IQR METHOD)
# ------------------------------------------------------------
section("OUTLIER DETECTION IN SALARY (IQR METHOD)")
q1 = df["ANNUAL_SALARY"].quantile(0.25)
q3 = df["ANNUAL_SALARY"].quantile(0.75)
iqr = q3 - q1
lower = q1 - 1.5 * iqr
upper = q3 + 1.5 * iqr

outliers = df[(df["ANNUAL_SALARY"] < lower) | (df["ANNUAL_SALARY"] > upper)]
print(f"Q1: {q1:.2f} | Q3: {q3:.2f} | IQR: {iqr:.2f}")
print(f"Valid range: {lower:.2f} to {upper:.2f}")
print(f"Number of outliers: {len(outliers)}")

# ------------------------------------------------------------
# 5. VISUALIZATIONS
# ------------------------------------------------------------

# 5.1 Salary distribution
plt.figure(figsize=(8, 5))
sns.histplot(df["ANNUAL_SALARY"], kde=True)  # kde draws a smooth curve
plt.title("Salary Distribution")
plt.xlabel("Annual Salary")
plt.tight_layout()
plt.show()

# 5.2 Average salary by department (sorted)
plt.figure(figsize=(9, 5))
dept_avg.plot(kind="bar", color="steelblue")
plt.title("Average Salary by Department")
plt.ylabel("Average Salary")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()

# 5.3 Salary by experience
# If EXPERIENCE is continuous, group it into ranges so the chart is readable
plt.figure(figsize=(9, 5))
if df["EXPERIENCE"].nunique() > 10:
    exp_group = pd.cut(
        df["EXPERIENCE"],
        bins=[-1, 2, 5, 10, 20, 100],
        labels=["0-2", "3-5", "6-10", "11-20", "20+"],
    )
    sns.boxplot(x=exp_group, y=df["ANNUAL_SALARY"])
    plt.xlabel("Experience (years)")
else:
    sns.boxplot(x="EXPERIENCE", y="ANNUAL_SALARY", data=df)
plt.title("Salary by Experience")
plt.tight_layout()
plt.show()

# 5.4 Gender distribution
plt.figure(figsize=(6, 6))
df["GENDER"].value_counts().plot(kind="pie", autopct="%1.1f%%")
plt.title("Gender Distribution")
plt.ylabel("")
plt.tight_layout()
plt.show()

# 5.5 Employee count per department
plt.figure(figsize=(9, 5))
sns.countplot(
    x="DEPARTMENT", data=df, order=df["DEPARTMENT"].value_counts().index
)
plt.title("Employee Count per Department")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()

# 5.6 Correlation heatmap (numeric columns only)
plt.figure(figsize=(7, 5))
sns.heatmap(df.corr(numeric_only=True), annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Heatmap")
plt.tight_layout()
plt.show()

# ------------------------------------------------------------
# 6. KEY INSIGHTS (generated from the data)
# ------------------------------------------------------------
section("KEY INSIGHTS")

print(f"1. Highest paying department: {dept_avg.index[0]} "
      f"(avg {dept_avg.iloc[0]:,.0f}); lowest: {dept_avg.index[-1]} "
      f"(avg {dept_avg.iloc[-1]:,.0f}).")

print(f"2. Average salary is {df['ANNUAL_SALARY'].mean():,.0f} and the median is "
      f"{df['ANNUAL_SALARY'].median():,.0f}, so salaries are "
      f"{'right-skewed (a few high earners)' if df['ANNUAL_SALARY'].mean() > df['ANNUAL_SALARY'].median() else 'fairly balanced'}.")

if pd.api.types.is_numeric_dtype(df["EXPERIENCE"]):
    corr = df["EXPERIENCE"].corr(df["ANNUAL_SALARY"])
    print(f"3. Correlation between experience and salary is {corr:.2f}, "
          f"showing a {'strong' if abs(corr) > 0.6 else 'moderate' if abs(corr) > 0.3 else 'weak'} relationship.")

print(f"4. {len(outliers)} salary outlier(s) found using the IQR method.")

top_gender = gender_avg.idxmax()
print(f"5. Highest average salary by gender group: {top_gender} "
      f"({gender_avg.max():,.0f}) vs {gender_avg.min():,.0f}.")
