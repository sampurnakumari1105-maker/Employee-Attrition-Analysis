import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load Dataset
df = pd.read_csv("HR_Analytics.csv.csv")

print("Employee Dataset Loaded Successfully!")
print(df.head())

# Basic Information
print("\nDataset Information:")
print(df.info())

# Total Employees
print("\nTotal Employees:", len(df))

# Leavers and Stayers
print("\nEmployee Attrition Count:")
print(df["Attrition"].value_counts())

# Department Analysis
department = df.groupby("Department").agg(
    Total_Employees=("Attrition", "count"),
    Employees_Left=("Attrition", lambda x: (x == "Yes").sum())
)

department["Attrition_Rate"] = (
    department["Employees_Left"] /
    department["Total_Employees"] * 100
)

print("\nDepartment Analysis:")
print(department)

# Salary Analysis
df["Salary_Band"] = pd.cut(
    df["MonthlyIncome"],
    bins=[0, 3000, 6000, 10000, float("inf")],
    labels=["Low", "Medium", "High", "Very High"]
)

salary = df.groupby("Salary_Band", observed=True).agg(
    Total_Employees=("Attrition", "count"),
    Employees_Left=("Attrition", lambda x: (x == "Yes").sum())
)

salary["Attrition_Rate"] = (
    salary["Employees_Left"] /
    salary["Total_Employees"] * 100
)

print("\nSalary Analysis:")
print(salary)

# Tenure Analysis
df["Tenure_Group"] = pd.cut(
    df["YearsAtCompany"],
    bins=[-1, 2, 5, 10, float("inf")],
    labels=["0-2 Years", "3-5 Years", "6-10 Years", "10+ Years"]
)

tenure = df.groupby("Tenure_Group", observed=True).agg(
    Total_Employees=("Attrition", "count"),
    Employees_Left=("Attrition", lambda x: (x == "Yes").sum())
)

tenure["Attrition_Rate"] = (
    tenure["Employees_Left"] /
    tenure["Total_Employees"] * 100
)

print("\nTenure Analysis:")
print(tenure)

# Save Analysis Reports
os.makedirs("output", exist_ok=True)

department.to_csv("output/department_analysis.csv")
salary.to_csv("output/salary_analysis.csv")
tenure.to_csv("output/tenure_analysis.csv")

# 1. Employee Attrition Distribution

plt.figure(figsize=(7, 5))

sns.countplot(data=df, x="Attrition")

plt.title("Employee Attrition Distribution")
plt.xlabel("Attrition")
plt.ylabel("Number of Employees")

plt.savefig("output/attrition_distribution.png")
plt.show()


# 2. Department-wise Attrition

plt.figure(figsize=(8, 5))

sns.barplot(
    data=department.reset_index(),
    x="Department",
    y="Attrition_Rate"
)

plt.title("Department-wise Attrition Rate")
plt.xlabel("Department")
plt.ylabel("Attrition Rate (%)")

plt.savefig("output/department_attrition.png")
plt.show()


# 3. Salary-wise Attrition

plt.figure(figsize=(8, 5))

sns.barplot(
    data=salary.reset_index(),
    x="Salary_Band",
    y="Attrition_Rate"
)

plt.title("Salary-wise Attrition Rate")
plt.xlabel("Salary Band")
plt.ylabel("Attrition Rate (%)")

plt.savefig("output/salary_attrition.png")
plt.show()


# 4. Experience-wise Attrition

plt.figure(figsize=(8, 5))

sns.barplot(
    data=tenure.reset_index(),
    x="Tenure_Group",
    y="Attrition_Rate"
)

plt.title("Experience-wise Attrition Rate")
plt.xlabel("Years at Company")
plt.ylabel("Attrition Rate (%)")

plt.savefig("output/experience_attrition.png")
plt.show()

print("All Graphs Generated Successfully!")

# FINAL PROJECT REPORT

total = len(df)

leavers = (df["Attrition"] == "Yes").sum()
stayers = (df["Attrition"] == "No").sum()

attrition_rate = (leavers / total) * 100

highest_department = department["Attrition_Rate"].idxmax()
highest_salary_band = salary["Attrition_Rate"].idxmax()
highest_tenure_group = tenure["Attrition_Rate"].idxmax()

report = f"""
====================================
     EMPLOYEE ATTRITION REPORT
====================================

Total Employees: {total}

Employees Who Left: {leavers}

Employees Who Stayed: {stayers}

Overall Attrition Rate: {attrition_rate:.2f}%

----------- KEY FINDINGS -----------

Department with Highest Attrition:
{highest_department}

Salary Band with Highest Attrition:
{highest_salary_band}

Tenure Group with Highest Attrition:
{highest_tenure_group}

----------- CONCLUSION -----------

Employee attrition analysis helps
organizations understand employee
turnover patterns.

Department, salary and years at
company are useful factors for
understanding employee attrition.

====================================
"""

with open("output/final_report.txt", "w") as file:
    file.write(report)

print(report)
print("Final Report Generated Successfully!")