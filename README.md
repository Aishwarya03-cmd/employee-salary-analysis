# Employee Salary Analysis

A data cleaning and exploratory data analysis (EDA) project built with Python during my Data Analytics using Python course.

## Objective
Clean an employee dataset, analyze salary patterns across departments, gender and experience, and present the findings with visualizations.

## Tools Used
- Python
- Pandas, NumPy
- Matplotlib, Seaborn

## Dataset
`EmployeeData.xlsx` contains employee details: department, gender, experience and annual salary.

> Note: the file in this repository is a sample dataset created for demonstration. Replace it with your own data if needed. The column names used are `DEPARTMENT`, `GENDER`, `EXPERIENCE` and `ANNUAL_SALARY`.

## What the Project Does
1. **Data cleaning**
   - Removes duplicate records
   - Converts salary to numeric and handles invalid values
   - Fills missing salaries with the median (salary data is usually right-skewed)
   - Drops rows with other missing values
   - Saves the result to `EmployeeData_cleaned.xlsx`
2. **Exploratory data analysis**
   - Statistical summary of salary (mean, median, min, max, standard deviation)
   - Average salary by department and by gender
   - Outlier detection using the IQR method
3. **Visualizations**
   - Salary distribution
   - Average salary by department
   - Salary by experience
   - Gender distribution
   - Employee count per department
   - Correlation heatmap
4. **Key insights** generated automatically from the data

## How to Run
1. Open the project in Google Colab or Jupyter Notebook.
2. Upload `EmployeeData.xlsx`.
3. Run `employee_salary_analysis.py`.

Install the libraries if needed:

```
pip install pandas numpy matplotlib seaborn openpyxl
```

## Screenshots
Add your chart screenshots here.

## Key Learnings
- Handling missing values, duplicates and invalid data types
- Choosing median over mean for skewed data
- Detecting outliers with the IQR method
- Turning raw data into insights with visualizations

## Author
**Aishwarya Gudi**
BCA student | Aspiring software developer and data analyst
[LinkedIn](https://www.linkedin.com/in/aishwarya-gudi-2b60a9354)
